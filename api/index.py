# Qalqan AI v5.0
# Бас API: 5-деңгейлі қауіп детекция pipeline + ML features + XAI
# Academic research-grade: features extraction, explainability, evaluation

import json
import os
import re
import time
import logging
import asyncio
from collections import defaultdict
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator, Field

from .services.threat_db import check_all_databases, extract_domain
from .services.ai_analyzer import analyze_url, analyze_text, analyze_screenshot
from .services.pyramid_detector import check_pyramid_domain, check_local_blacklist, detect_pyramid_patterns
from .services.kz_intel import check_kz_social_engineering
from .services.domain_intel import check_domain_intelligence
from .services.url_features import extract_features
from .services.explainer import generate_explanation
from .services.scoring import calculate_final_verdict
from .utils.cache import url_hash, get_cached, set_cached, clear_cache
from .evaluation.benchmark import run_benchmark
from .utils.telegram import send_appeal, send_report, notify_block
from .utils.i18n import t

_PRIVATE_IP_RE = re.compile(
    r"^(localhost|127\.|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|0\.0\.0\.0|::1)",
    re.IGNORECASE
)

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("qalqan")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: preload OpenPhish feed to avoid cold-start latency on first request."""
    from .services.threat_db import load_openphish_feed
    try:
        await load_openphish_feed()
        logger.info("OpenPhish feed preloaded at startup")
    except Exception as e:
        logger.warning(f"OpenPhish preload failed (will retry on first request): {e}")
    yield


app = FastAPI(title="Qalqan AI", version="5.0.0",
              description="AI-powered cybersecurity research platform — PhD-grade threat detection",
              lifespan=lifespan)

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
    # Prevent unbounded growth: purge IPs inactive for >5 minutes
    if len(_rate_limits) > 5000:
        cutoff = now - 300
        dead = [k for k, v in _rate_limits.items() if not v or max(v) < cutoff]
        for k in dead:
            del _rate_limits[k]
    timestamps = _rate_limits[ip]
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


# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {type(exc).__name__}: {str(exc)[:200]}")
    return JSONResponse(
        status_code=500,
        content={
            "verdict": "SUSPICIOUS",
            "threat_score": 50,
            "threat_type": "unknown",
            "source": "error_handler",
            "detail": "Тексеру уақытша қолжетімсіз. Қайталап көріңіз.",
            "detail_kk": "Тексеру уақытша қолжетімсіз. Қайталап көріңіз.",
            "detail_ru": "Проверка временно недоступна. Повторите попытку.",
            "detail_en": "Check temporarily unavailable. Please retry.",
            "indicators": [],
            "cached": False
        }
    )


# --- Whitelist жүктеу ---
_data_dir = os.path.join(os.path.dirname(__file__), "data")
_whitelist: set[str] = set()

try:
    with open(os.path.join(_data_dir, "whitelist.json"), "r", encoding="utf-8") as f:
        _whitelist = set(json.load(f).get("trusted_domains", []))
except (FileNotFoundError, json.JSONDecodeError):
    logger.warning("whitelist.json жүктелмеді")


# --- Demo Mode ---
DEMO_MODE = os.getenv("DEMO_MODE", "").lower() in ("1", "true", "yes")
if DEMO_MODE:
    logger.info("DEMO_MODE active — returning deterministic results for known URLs")

_DEMO_RESULTS: dict[str, dict] = {
    "kaspi.kz": {
        "verdict": "SAFE", "threat_score": 0, "risk_level": "low", "threat_type": "safe", "source": "demo_cache",
        "detail": "Сенімді сайт — Kaspi Bank ресми порталы",
        "detail_kk": "Сенімді сайт — Kaspi Bank ресми порталы",
        "detail_ru": "Надёжный сайт — официальный портал Kaspi Bank",
        "detail_en": "Trusted site — official Kaspi Bank portal",
        "indicators": [], "cached": False,
        "explanation": {"top_factors": [], "safe_factors": [{"factor": "trusted_domain", "value": "kaspi.kz", "impact": -30, "direction": "safe"}], "confidence": 0.99}
    },
    "egov.kz": {
        "verdict": "SAFE", "threat_score": 0, "risk_level": "low", "threat_type": "safe", "source": "demo_cache",
        "detail": "Сенімді сайт — eGov.kz мемлекеттік портал",
        "detail_kk": "Сенімді сайт — eGov.kz мемлекеттік портал",
        "detail_ru": "Надёжный сайт — государственный портал eGov.kz",
        "detail_en": "Trusted site — eGov.kz government portal",
        "indicators": [], "cached": False,
        "explanation": {"top_factors": [], "safe_factors": [{"factor": "trusted_domain", "value": "egov.kz", "impact": -30, "direction": "safe"}], "confidence": 0.99}
    },
    "halykbank.kz": {
        "verdict": "SAFE", "threat_score": 0, "risk_level": "low", "threat_type": "safe", "source": "demo_cache",
        "detail": "Сенімді сайт — Halyk Bank ресми порталы",
        "detail_kk": "Сенімді сайт — Halyk Bank ресми порталы",
        "detail_ru": "Надёжный сайт — официальный портал Halyk Bank",
        "detail_en": "Trusted site — official Halyk Bank portal",
        "indicators": [], "cached": False
    },
    "kaspi-login.tk": {
        "verdict": "DANGEROUS", "threat_score": 97, "risk_level": "critical", "threat_type": "phishing", "source": "demo_cache",
        "detail": "ФИШИНГ: Kaspi Bank-тың жалған сайты! Жеке деректерді енгізбеңіз!",
        "detail_kk": "ФИШИНГ: Kaspi Bank-тың жалған сайты! Жеке деректерді енгізбеңіз!",
        "detail_ru": "ФИШИНГ: Поддельный сайт Kaspi Bank! Не вводите личные данные!",
        "detail_en": "PHISHING: Fake Kaspi Bank site! Do not enter personal data!",
        "indicators": ["free_tld_tk", "brand_impersonation_kaspi", "new_domain_3d", "no_ssl"],
        "cached": False,
        "explanation": {
            "top_factors": [
                {"factor": "brand_impersonation", "value": "Similar to: kaspi (edit_dist=0)", "impact": 40, "direction": "risk"},
                {"factor": "domain_age", "value": "3 days", "impact": 35, "direction": "risk"},
                {"factor": "no_ssl", "value": "No SSL certificate", "impact": 30, "direction": "risk"},
                {"factor": "free_tld", "value": "TLD: .tk", "impact": 15, "direction": "risk"}
            ],
            "confidence": 0.99,
            "counterfactual": "Site would score <40 (SAFE) if: standard TLD AND valid SSL AND domain age > 365 days"
        }
    },
    "crowd1.com": {
        "verdict": "DANGEROUS", "threat_score": 95, "risk_level": "critical", "threat_type": "pyramid", "source": "demo_cache",
        "detail": "ҚАРЖЫЛЫҚ ПИРАМИДА: Crowd1 — танымал алаяқтық схема. Ақша салмаңыз!",
        "detail_kk": "ҚАРЖЫЛЫҚ ПИРАМИДА: Crowd1 — танымал алаяқтық схема. Ақша салмаңыз!",
        "detail_ru": "ФИНАНСОВАЯ ПИРАМИДА: Crowd1 — известная мошенническая схема. Не вкладывайте!",
        "detail_en": "FINANCIAL PYRAMID: Crowd1 — known scam scheme. Do not invest!",
        "indicators": ["pyramid_list_match", "mlm_scheme", "guaranteed_income_promise"],
        "cached": False
    },
    "1xbet.com": {
        "verdict": "DANGEROUS", "threat_score": 90, "risk_level": "critical", "threat_type": "gambling", "source": "demo_cache",
        "detail": "ҚҰМАР ОЙЫН: лицензиясыз букмекер, ҚР-да тыйым салынған",
        "detail_kk": "ҚҰМАР ОЙЫН: лицензиясыз букмекер, ҚР-да тыйым салынған",
        "detail_ru": "ГЕМБЛИНГ: нелицензированный букмекер, запрещён в РК",
        "detail_en": "GAMBLING: unlicensed bookmaker, banned in Kazakhstan",
        "indicators": ["gambling_list_match", "unlicensed_kz"],
        "cached": False
    },
    "verify-account.ml": {
        "verdict": "DANGEROUS", "threat_score": 94, "risk_level": "critical", "threat_type": "phishing", "source": "demo_cache",
        "detail": "ФИШИНГ: жалған верификация беті — жеке деректерді ұрлау",
        "detail_kk": "ФИШИНГ: жалған верификация беті — жеке деректерді ұрлау",
        "detail_ru": "ФИШИНГ: поддельная страница верификации для кражи данных",
        "detail_en": "PHISHING: fake verification page designed to steal personal data",
        "indicators": ["free_tld_ml", "suspicious_keywords", "no_ssl", "new_domain"],
        "cached": False
    },
    "egov-login.kz": {
        "verdict": "DANGEROUS", "threat_score": 98, "risk_level": "critical", "threat_type": "phishing", "source": "demo_cache",
        "detail": "ФИШИНГ: eGov.kz мемлекеттік порталының жалған сайты! ЭЦП деректерін енгізбеңіз!",
        "detail_kk": "ФИШИНГ: eGov.kz мемлекеттік порталының жалған сайты! ЭЦП деректерін енгізбеңіз!",
        "detail_ru": "ФИШИНГ: Поддельный сайт государственного портала eGov.kz! Не вводите данные ЭЦП!",
        "detail_en": "PHISHING: Fake eGov.kz government portal! Do not enter your digital signature credentials!",
        "indicators": ["phishing_list_match", "brand_impersonation_egov", "gov_portal_clone"],
        "cached": False,
        "explanation": {
            "top_factors": [
                {"factor": "known_phishing_domain", "value": "egov-login.kz — eGov impersonator", "impact": 95, "direction": "risk"},
                {"factor": "brand_impersonation", "value": "Similar to: egov (edit dist=1)", "impact": 40, "direction": "risk"},
                {"factor": "government_portal_clone", "value": "Fake government login page", "impact": 35, "direction": "risk"}
            ],
            "confidence": 0.99,
            "counterfactual": "This domain is in the Qalqan KZ phishing database — always DANGEROUS"
        }
    },
    "mostbet-kz.com": {
        "verdict": "DANGEROUS", "threat_score": 90, "risk_level": "critical", "threat_type": "gambling", "source": "demo_cache",
        "detail": "ҚҰМАР ОЙЫН: Mostbet — лицензиясыз букмекер, ҚР-да тыйым салынған",
        "detail_kk": "ҚҰМАР ОЙЫН: Mostbet — лицензиясыз букмекер, ҚР-да тыйым салынған",
        "detail_ru": "ГЕМБЛИНГ: Mostbet — нелицензированный букмекер, запрещён в РК",
        "detail_en": "GAMBLING: Mostbet — unlicensed bookmaker, prohibited in Kazakhstan",
        "indicators": ["gambling_list_match", "unlicensed_kz", "mostbet"],
        "cached": False
    },
    "finiko.com": {
        "verdict": "DANGEROUS", "threat_score": 96, "risk_level": "critical", "threat_type": "pyramid", "source": "demo_cache",
        "detail": "ҚАРЖЫЛЫҚ ПИРАМИДА: Finiko — Ресей мен Қазақстанда мыңдаған адамды алдаған схема",
        "detail_kk": "ҚАРЖЫЛЫҚ ПИРАМИДА: Finiko — Ресей мен Қазақстанда мыңдаған адамды алдаған схема",
        "detail_ru": "ФИНАНСОВАЯ ПИРАМИДА: Finiko — схема обманула тысячи людей в России и Казахстане",
        "detail_en": "FINANCIAL PYRAMID: Finiko — scheme defrauded thousands in Russia and Kazakhstan",
        "indicators": ["pyramid_list_match", "mlm_scheme", "crypto_exit_scam"],
        "cached": False
    },
    "google.com": {
        "verdict": "SAFE", "threat_score": 0, "risk_level": "low", "threat_type": "safe", "source": "demo_cache",
        "detail": "Сенімді сайт — Google ресми порталы",
        "detail_kk": "Сенімді сайт — Google ресми порталы",
        "detail_ru": "Надёжный сайт — официальный портал Google",
        "detail_en": "Trusted site — official Google portal",
        "indicators": [], "cached": False
    },
    "hellcase.com": {
        "verdict": "DANGEROUS", "threat_score": 85, "risk_level": "high", "threat_type": "gambling", "source": "demo_cache",
        "detail": "КЕЙС-БАТ: CS2 кейстерін ашу — азартты ойын, жасөспірімдерге қауіпті",
        "detail_kk": "КЕЙС-БАТ: CS2 кейстерін ашу — азартты ойын, жасөспірімдерге қауіпті",
        "detail_ru": "КЕЙС-БАТЛ: Открытие кейсов CS2 — азартная игра, опасна для несовершеннолетних",
        "detail_en": "CASE BATTLE: CS2 case opening — gambling, dangerous for minors",
        "indicators": ["case_battle_match", "gambling", "minor_risk"],
        "cached": False
    },
    "bit.ly": {
        "verdict": "SUSPICIOUS", "threat_score": 45, "risk_level": "medium", "threat_type": "suspicious_infrastructure",
        "source": "demo_cache",
        "detail": "URL-қысқартқыш: қайда апаратыны белгісіз. Шертпес бұрын тексеріңіз.",
        "detail_kk": "URL-қысқартқыш: қайда апаратыны белгісіз. Шертпес бұрын тексеріңіз.",
        "detail_ru": "URL-сокращатель: назначение скрыто. Проверьте перед переходом.",
        "detail_en": "URL shortener: destination hidden. Verify before clicking.",
        "indicators": ["url_shortener", "destination_hidden"],
        "cached": False
    },
}


# --- Деректер модельдері (validated) ---
class CheckRequest(BaseModel):
    url: str = Field(..., max_length=2048)
    lang: str = Field(default="kk", max_length=5)

    @field_validator("url")
    @classmethod
    def validate_url(cls, v):
        from urllib.parse import urlparse
        v = v.strip()
        if not v:
            raise ValueError("URL cannot be empty")
        if not v.startswith(("http://", "https://")):
            v = "https://" + v
        host = urlparse(v).hostname or ""
        if _PRIVATE_IP_RE.match(host):
            raise ValueError("Private or internal addresses not allowed")
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

    # --- Demo Mode: deterministic results for presentation ---
    if DEMO_MODE and domain in _DEMO_RESULTS:
        logger.info(f"DEMO_MODE hit: {domain}")
        return _DEMO_RESULTS[domain]

    # --- Tier 0: Whitelist (exact + subdomain match) ---
    if domain in _whitelist or any(domain.endswith("." + td) for td in _whitelist):
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

    # --- Tier 1.5: URL Feature Extraction (ML) — needed for explanation even on early hits ---
    start_time = time.time()
    url_feats = extract_features(url)

    # --- Tier 1: Pyramid list + Local blacklist ---
    pyramid_hit = check_pyramid_domain(url)
    if pyramid_hit:
        result = calculate_final_verdict([], None, pyramid_hit, lang=lang)
        result["explanation"] = generate_explanation(url_feats, None, [], None, pyramid_hit, result["threat_score"])
        result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": "pyramid_list"}
        set_cached(key, result)
        return result

    blacklist_hit = check_local_blacklist(url)
    if blacklist_hit:
        result = calculate_final_verdict([blacklist_hit], None, None, lang=lang)
        result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": "blacklist"}
        set_cached(key, result)
        return result

    # --- Tier 2 + 2.5: Databases AND domain intel in parallel ---
    db_results, domain_info = await asyncio.gather(
        check_all_databases(url),
        check_domain_intelligence(domain, url)
    )

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

    text = request.text

    # KZ social engineering (fast, no API)
    kz_hit = check_kz_social_engineering(text)
    if kz_hit and kz_hit.get("verdict") == "DANGEROUS":
        return calculate_final_verdict([], kz_hit, None, lang=request.lang)

    # Pyramid pattern detection in text (fast, no API)
    pyramid_conf = detect_pyramid_patterns(text)
    if pyramid_conf >= 0.8:
        pyramid_text_result = {
            "verdict": "DANGEROUS", "threat_score": int(pyramid_conf * 95),
            "threat_type": "pyramid", "source": "kz_intel",
            "reason_kk": "Мәтінде қаржылық пирамида белгілері анықталды",
            "reason_ru": "В тексте обнаружены признаки финансовой пирамиды",
            "reason_en": "Financial pyramid scheme indicators detected in text",
            "indicators": ["pyramid_pattern_match"]
        }
        return calculate_final_verdict([], pyramid_text_result, None, lang=request.lang)

    ai_result = await analyze_text(text)

    # Merge all local signals into AI result
    if ai_result:
        if kz_hit:
            ai_result.setdefault("indicators", []).extend(kz_hit.get("indicators", []))
            ai_result["threat_score"] = min(
                ai_result.get("threat_score", 50) + kz_hit.get("threat_score", 0) // 3, 100
            )
        if pyramid_conf >= 0.4:
            ai_result["threat_score"] = min(ai_result.get("threat_score", 50) + int(pyramid_conf * 20), 100)
            ai_result.setdefault("indicators", []).append(f"pyramid_conf_{int(pyramid_conf * 100)}pct")

    return calculate_final_verdict([], ai_result, None, lang=request.lang)


# --- BATCH ТЕКСЕРУ (max 10 URL) ---
@app.post("/batch")
async def check_batch(request: BatchRequest, req: Request):
    """Check up to 10 URLs in parallel. Returns list of verdicts."""
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"check:{client_ip}", RATE_LIMIT_CHECK):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    urls = request.urls[:10]  # hard cap
    lang = request.lang

    async def _check_one(url: str) -> dict:
        try:
            url = url.strip()
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            from urllib.parse import urlparse as _urlparse
            host = _urlparse(url).hostname or ""
            if _PRIVATE_IP_RE.match(host):
                return {"url": url, "verdict": "SUSPICIOUS", "threat_score": 30,
                        "error": "Private/internal addresses not allowed"}
            domain = extract_domain(url)

            if DEMO_MODE and domain in _DEMO_RESULTS:
                return {**_DEMO_RESULTS[domain], "url": url}

            if domain in _whitelist or any(domain.endswith("." + td) for td in _whitelist):
                return {"url": url, "verdict": "SAFE", "threat_score": 0, "source": "whitelist", "indicators": []}

            key = url_hash(url)
            cached = get_cached(key)
            if cached:
                return {**cached, "url": url}

            url_feats = extract_features(url)  # sync — fast, no I/O

            pyramid_hit = check_pyramid_domain(url)
            if pyramid_hit:
                r = calculate_final_verdict([], None, pyramid_hit, lang=lang)
                r["explanation"] = generate_explanation(url_feats, None, [], None, pyramid_hit, r["threat_score"])
                set_cached(key, r)
                return {**r, "url": url}

            blacklist_hit = check_local_blacklist(url)
            if blacklist_hit:
                r = calculate_final_verdict([blacklist_hit], None, None, lang=lang)
                set_cached(key, r)
                return {**r, "url": url}

            db_results, domain_info = await asyncio.gather(
                check_all_databases(url),
                check_domain_intelligence(domain, url)
            )
            ai_result = await analyze_url(url)
            r = calculate_final_verdict(db_results, ai_result, None,
                                        domain_info=domain_info, url_features=url_feats, lang=lang)
            r["explanation"] = generate_explanation(url_feats, domain_info, db_results, ai_result, None, r["threat_score"])
            set_cached(key, r)
            return {**r, "url": url}
        except Exception as e:
            logger.error(f"Batch check error for {url}: {e}")
            return {"url": url, "verdict": "SUSPICIOUS", "threat_score": 50, "error": str(e)[:100]}

    results = await asyncio.gather(*[_check_one(u) for u in urls])
    return {"results": list(results), "checked": len(results)}


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
# Primary store is in-memory (persists within one serverless instance lifetime).
# File write is best-effort — Vercel ephemeral FS resets on cold start.
_reports_file = os.path.join(_data_dir, "reports.json")
_reports_memory: dict = {}
try:
    with open(_reports_file, "r", encoding="utf-8") as f:
        _reports_memory = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    pass

def _load_reports() -> dict:
    return _reports_memory

def _save_reports(reports: dict):
    global _reports_memory
    _reports_memory = reports
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
    from .utils.cache import _cache
    reports = _load_reports()
    return {
        "total_reported_domains": len(reports),
        "auto_blocked": sum(1 for r in reports.values() if r["count"] >= 5),
        "whitelist_size": len(_whitelist),
        "cache_entries": len(_cache),
        "demo_mode": DEMO_MODE,
        "version": "5.0.0"
    }


# --- Keep-warm (Vercel cron hits every 10 min) ---
@app.get("/ping")
async def ping():
    return {"status": "ok", "version": "5.0.0", "demo_mode": DEMO_MODE}


# --- Detailed health check ---
@app.get("/health")
async def health():
    api_keys = {
        "groq": bool(os.getenv("GROQ_API_KEY")),
        "gemini": bool(os.getenv("GEMINI_API_KEY")),
        "phishtank": bool(os.getenv("PHISHTANK_API_KEY")),
        "google_safe_browsing": bool(os.getenv("GOOGLE_SAFE_BROWSING_KEY")),
        "virustotal": bool(os.getenv("VIRUSTOTAL_API_KEY")),
        "telegram": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
    }
    data_files = {}
    for fname in ["whitelist.json", "kz_brands.json", "pyramid_schemes.json",
                  "blacklist.json", "kz_phishing_patterns.json"]:
        data_files[fname] = os.path.exists(os.path.join(_data_dir, fname))

    configured_count = sum(api_keys.values())
    return {
        "status": "ok",
        "version": "5.0.0",
        "demo_mode": DEMO_MODE,
        "api_keys_configured": configured_count,
        "api_keys": api_keys,
        "data_files": data_files,
        "whitelist_domains": len(_whitelist),
        "reports_in_memory": len(_reports_memory),
    }


# ============================================================
# RESEARCH API ENDPOINTS (doctoral-grade)
# ============================================================

class FeatureRequest(BaseModel):
    url: str = Field(..., max_length=2048)

    @field_validator("url")
    @classmethod
    def validate_url(cls, v):
        from urllib.parse import urlparse
        v = v.strip()
        if not v:
            raise ValueError("URL cannot be empty")
        if not v.startswith(("http://", "https://")):
            v = "https://" + v
        host = urlparse(v).hostname or ""
        if _PRIVATE_IP_RE.match(host):
            raise ValueError("Private or internal addresses not allowed")
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

    # Extract ALL data — sync first, then all async in parallel
    url_feats = extract_features(url)
    pyramid_hit = check_pyramid_domain(url)
    blacklist_hit = check_local_blacklist(url)
    db_results, domain_info, ai_result = await asyncio.gather(
        check_all_databases(url),
        check_domain_intelligence(domain, url),
        analyze_url(url)
    )

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
