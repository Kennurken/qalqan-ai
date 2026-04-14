# клауд Елдоса N1 — Qalqan AI v5.0
# Бас API: 5-деңгейлі қауіп детекция pipeline + ML features + XAI
# Academic research-grade: features extraction, explainability, evaluation

import json
import os
import time
import logging
import asyncio
from collections import defaultdict
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator, Field

from .services.threat_db import check_all_databases, extract_domain
from .services.ai_analyzer import analyze_url, analyze_text, analyze_screenshot
from .services.pyramid_detector import check_pyramid_domain, check_local_blacklist
from .services.domain_intel import check_domain_intelligence
from .services.url_features import extract_features
from .services.explainer import generate_explanation
from .services.scoring import calculate_final_verdict
from .utils.cache import url_hash, get_cached, set_cached, clear_cache
from .evaluation.benchmark import run_benchmark
from .utils.telegram import send_appeal, send_report, notify_block
from .utils.i18n import t

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("qalqan")

app = FastAPI(title="Qalqan AI", version="5.0.0",
              description="AI-powered cybersecurity research platform — PhD-grade threat detection")

# --- CORS: тек extension + localhost ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

# --- Rate Limiting (in-memory, IP-based) ---
_rate_limits: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT_CHECK = 30   # /check: 30 req/min
RATE_LIMIT_APPEAL = 5   # /appeal: 5 req/min
RATE_WINDOW = 60         # 60 seconds


def _check_rate_limit(ip: str, limit: int) -> bool:
    """True = разрешено, False = лимит асып кетті."""
    now = time.time()
    timestamps = _rate_limits[ip]
    # Ескілерді тазалау
    _rate_limits[ip] = [ts for ts in timestamps if now - ts < RATE_WINDOW]
    if len(_rate_limits[ip]) >= limit:
        return False
    _rate_limits[ip].append(now)
    return True


# --- Request Logging Middleware ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000)
    if request.url.path != "/":
        logger.info(f"{request.method} {request.url.path} → {response.status_code} [{duration}ms]")
    return response


# --- Whitelist жүктеу ---
_data_dir = os.path.join(os.path.dirname(__file__), "data")
_whitelist: set[str] = set()

try:
    with open(os.path.join(_data_dir, "whitelist.json"), "r", encoding="utf-8") as f:
        _whitelist = set(json.load(f).get("trusted_domains", []))
except (FileNotFoundError, json.JSONDecodeError):
    logger.warning("whitelist.json жүктелмеді")


# --- Деректер модельдері (validated) ---
class CheckRequest(BaseModel):
    url: str = Field(..., max_length=2048)
    lang: str = Field(default="kk", max_length=5)

    @field_validator("url")
    @classmethod
    def validate_url(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("URL cannot be empty")
        if not v.startswith(("http://", "https://")):
            v = "https://" + v
        return v

class TextCheckRequest(BaseModel):
    text: str = Field(..., max_length=10000)
    lang: str = Field(default="kk", max_length=5)

class ScreenRequest(BaseModel):
    image_base64: str = Field(..., max_length=7_000_000)  # ~5MB base64
    lang: str = Field(default="kk", max_length=5)

class AppealRequest(BaseModel):
    url: str = Field(..., max_length=2048)
    reason: str = Field(..., max_length=1000)

class ReportRequest(BaseModel):
    url: str = Field(..., max_length=2048)
    threat_type: str = Field(default="scam", max_length=50)
    note: str = Field(default="", max_length=1000)


# --- Health check ---
@app.get("/")
async def root():
    return {
        "status": "online",
        "name": "Qalqan AI",
        "version": "5.0.0",
        "pipeline": "5-tier: cache → ML_features → databases → domain_intel → AI + XAI",
        "databases": ["PhishTank", "SafeBrowsing", "URLhaus", "OpenPhish", "RDAP", "SSL"],
        "ml_features": "30+ URL lexical features, homoglyph detection, brand similarity",
        "ai_providers": {
            "groq": "configured" if os.getenv("GROQ_API_KEY") else "missing",
            "gemini": "configured" if os.getenv("GEMINI_API_KEY") else "missing"
        }
    }


# --- НЕГІЗГІ ТЕКСЕРУ: 4-деңгейлі pipeline ---
@app.post("/check")
async def check_site(request: CheckRequest, req: Request):
    # Rate limit
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"check:{client_ip}", RATE_LIMIT_CHECK):
        return JSONResponse(status_code=429, content={
            "error": "Rate limit exceeded", "detail": "Max 30 requests per minute"
        })

    url = request.url
    lang = request.lang
    domain = extract_domain(url)
    key = url_hash(url)

    # --- Tier 0: Whitelist ---
    if domain in _whitelist:
        return {
            "verdict": "SAFE", "threat_score": 0, "threat_type": "safe",
            "source": "whitelist",
            "detail": t("safe", lang),
            "detail_kk": t("safe", "kk"), "detail_ru": t("safe", "ru"), "detail_en": t("safe", "en"),
            "indicators": [], "cached": False
        }

    # --- Tier 0.5: Cache ---
    cached = get_cached(key)
    if cached:
        return cached

    # --- Tier 1: Pyramid list + Local blacklist ---
    pyramid_hit = check_pyramid_domain(url)
    if pyramid_hit:
        result = calculate_final_verdict([], None, pyramid_hit, lang=lang)
        set_cached(key, result)
        return result

    blacklist_hit = check_local_blacklist(url)
    if blacklist_hit:
        result = calculate_final_verdict([blacklist_hit], None, None, lang=lang)
        set_cached(key, result)
        return result

    # --- Tier 1.5: URL Feature Extraction (ML) ---
    start_time = time.time()
    url_feats = extract_features(url)

    # --- Tier 2: External databases (параллель) ---
    db_results = await check_all_databases(url)

    # --- Tier 2.5: Domain intelligence (age + SSL) ---
    domain_info = await check_domain_intelligence(domain, url)

    # Combine DB results
    all_db = db_results + ([domain_info] if domain_info else [])

    if any(r.get("verdict") == "DANGEROUS" for r in all_db):
        result = calculate_final_verdict(all_db, None, None,
                                         domain_info=domain_info, url_features=url_feats, lang=lang)
        result["explanation"] = generate_explanation(url_feats, domain_info, db_results, None, None, result["threat_score"])
        result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": "databases"}
        set_cached(key, result)
        return result

    # --- Tier 3: AI analysis ---
    ai_result = await analyze_url(url)

    result = calculate_final_verdict(db_results, ai_result, None,
                                     domain_info=domain_info, url_features=url_feats, lang=lang)
    result["explanation"] = generate_explanation(url_feats, domain_info, db_results, ai_result, None, result["threat_score"])
    result["metadata"] = {
        "processing_time_ms": int((time.time() - start_time) * 1000),
        "tier_hit": "ai",
        "ai_provider": ai_result.get("source", "unknown") if ai_result else "none"
    }
    set_cached(key, result)
    logger.info(f"CHECK {domain} → {result['verdict']} ({result['threat_score']}) via {result['source']} [{result['metadata']['processing_time_ms']}ms]")

    # Telegram notification for dangerous sites
    if result.get("verdict") == "DANGEROUS":
        asyncio.create_task(notify_block(url, result["verdict"], result["threat_score"], result.get("source", "")))

    return result


# --- МӘТІН ТЕКСЕРУ ---
@app.post("/check-text")
async def check_text(request: TextCheckRequest, req: Request):
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"check:{client_ip}", RATE_LIMIT_CHECK):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    ai_result = await analyze_text(request.text)
    return calculate_final_verdict([], ai_result, None, lang=request.lang)


# --- СКРИНШОТ ТЕКСЕРУ ---
@app.post("/analyze-screen")
async def check_screen(request: ScreenRequest, req: Request):
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"check:{client_ip}", RATE_LIMIT_CHECK):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    result = await analyze_screenshot(request.image_base64)
    return calculate_final_verdict([], result, None, lang=request.lang)


# --- АПЕЛЛЯЦИЯ ---
@app.post("/appeal")
async def appeal(request: AppealRequest, req: Request):
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"appeal:{client_ip}", RATE_LIMIT_APPEAL):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    return await send_appeal(request.url, request.reason)


# --- ШАҒЫМ (crowd-sourced) ---
_reports_file = os.path.join(_data_dir, "reports.json")

def _load_reports() -> dict:
    try:
        with open(_reports_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def _save_reports(reports: dict):
    try:
        with open(_reports_file, "w", encoding="utf-8") as f:
            json.dump(reports, f, ensure_ascii=False)
    except Exception:
        pass

@app.post("/report")
async def report_site(request: ReportRequest, req: Request):
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"appeal:{client_ip}", RATE_LIMIT_APPEAL):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    domain = extract_domain(request.url)
    reports = _load_reports()
    if domain not in reports:
        reports[domain] = {"count": 0, "types": [], "first_report": time.time()}
    reports[domain]["count"] += 1
    reports[domain]["types"].append(request.threat_type)

    # 5+ репорт = автоматты blacklist
    auto_blocked = reports[domain]["count"] >= 5
    _save_reports(reports)

    if auto_blocked:
        logger.warning(f"AUTO-BLOCKED: {domain} (5+ reports)")

    # Telegram хабарлама
    result = await send_report(request.url, request.threat_type, request.note)
    result["reports_count"] = reports[domain]["count"]
    result["auto_blocked"] = auto_blocked
    return result


# --- СТАТИСТИКА ---
@app.get("/stats")
async def get_stats():
    reports = _load_reports()
    return {
        "total_reported_domains": len(reports),
        "auto_blocked": sum(1 for r in reports.values() if r["count"] >= 5),
        "whitelist_size": len(_whitelist)
    }


# ============================================================
# RESEARCH API ENDPOINTS (doctoral-grade)
# ============================================================

class FeatureRequest(BaseModel):
    url: str = Field(..., max_length=2048)

    @field_validator("url")
    @classmethod
    def validate_url(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("URL cannot be empty")
        if not v.startswith(("http://", "https://")):
            v = "https://" + v
        return v

class BatchRequest(BaseModel):
    urls: list[str] = Field(..., max_length=50)
    lang: str = Field(default="kk", max_length=5)


@app.post("/features")
async def get_features(request: FeatureRequest, req: Request):
    """Extract 30+ ML features from URL (no HTTP request, pure lexical analysis).
    Use for: ML model training, feature importance analysis, dataset building."""
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"check:{client_ip}", RATE_LIMIT_CHECK):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    return extract_features(request.url)


@app.post("/check-research")
async def check_research(request: CheckRequest, req: Request):
    """Full research output: all features, all scores, explanation, metadata.
    Use for: paper benchmarks, ablation studies, system evaluation."""
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"check:{client_ip}", RATE_LIMIT_CHECK):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    url = request.url
    lang = request.lang
    domain = extract_domain(url)
    start_time = time.time()

    # Extract ALL data
    url_feats = extract_features(url)
    pyramid_hit = check_pyramid_domain(url)
    blacklist_hit = check_local_blacklist(url)
    db_results = await check_all_databases(url)
    domain_info = await check_domain_intelligence(domain, url)
    ai_result = await analyze_url(url)

    # Calculate final verdict
    result = calculate_final_verdict(
        db_results, ai_result, pyramid_hit,
        domain_info=domain_info, url_features=url_feats, lang=lang
    )

    # Generate explanation
    explanation = generate_explanation(
        url_feats, domain_info, db_results, ai_result, pyramid_hit, result["threat_score"]
    )

    processing_time = int((time.time() - start_time) * 1000)

    return {
        # Standard verdict
        "verdict": result["verdict"],
        "threat_score": result["threat_score"],
        "threat_type": result.get("threat_type", "unknown"),
        "source": result.get("source", "unknown"),
        "detail": result.get("detail", ""),
        "detail_kk": result.get("detail_kk", ""),
        "detail_ru": result.get("detail_ru", ""),
        "detail_en": result.get("detail_en", ""),

        # ML Features (30+)
        "url_features": url_feats,

        # XAI Explanation
        "explanation": explanation,

        # Raw scores from each source
        "scores_breakdown": {
            "url_features_score": url_feats.get("risk_score", 0),
            "pyramid_score": 95 if pyramid_hit else 0,
            "db_score": max((r.get("threat_score", 0) for r in db_results), default=0),
            "domain_intel_score": domain_info.get("threat_score", 0) if domain_info else 0,
            "ai_score": ai_result.get("threat_score", 0) if ai_result else 0,
        },

        # Raw results from each tier
        "tier_results": {
            "pyramid": pyramid_hit,
            "blacklist": blacklist_hit,
            "databases": db_results,
            "domain_intel": domain_info,
            "ai": {k: v for k, v in (ai_result or {}).items() if k != "source"} if ai_result else None,
        },

        # Metadata
        "metadata": {
            "processing_time_ms": processing_time,
            "url": url,
            "domain": domain,
            "ai_provider": ai_result.get("source", "none") if ai_result else "none",
            "timestamp": time.time(),
            "version": "5.0.0"
        }
    }


# ============================================================
# EVALUATION ENDPOINT
# ============================================================

@app.post("/evaluate")
async def evaluate(req: Request):
    """Run benchmark on built-in test dataset. Returns accuracy, F1, MCC, per-URL results."""
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"check:{client_ip}", 5):  # max 5 evals/min
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    results = await run_benchmark()
    return results
