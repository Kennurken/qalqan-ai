# Qalqan AI v5.1
# Бас API: 6-деңгейлі қауіп детекция pipeline + ML features + XAI
# Academic research-grade: features extraction, explainability, evaluation

import json
import os
import re
import time
import logging
import asyncio
import traceback
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from .templates import LANDING_HTML, DASHBOARD_HTML, INSTALL_HTML, MINIAPP_HTML, GRAPH_HTML, MOBILE_HTML, SW_JS
from .utils.api_auth import verify_api_key, key_id, is_demo, usage_for, partner_count, DEMO_KEY
from .demo import _DEMO_RESULTS
from pydantic import BaseModel, field_validator, Field

from .services.threat_db import check_all_databases, extract_domain, feed_stats
from .services.ai_analyzer import analyze_url, analyze_text, analyze_screenshot, analyze_situation
from .services.pyramid_detector import check_pyramid_domain, check_local_blacklist, detect_pyramid_patterns
from .services.pyramid_registry import check_pyramid_name, registry_size
from .services.kz_intel import check_kz_social_engineering, check_kz_impersonation_url, check_gambling_domain
from .services.domain_intel import check_domain_intelligence
from .services.goszakup import check_goszakup_url, analyse_procurement_data, is_goszakup_url
from .services.url_features import extract_features
from .services.explainer import generate_explanation
from .services.scoring import calculate_final_verdict
from .utils.cache import url_hash, get_cached, set_cached, clear_cache, check_rate_limit, check_health as redis_health
from .evaluation.benchmark import run_benchmark
from .utils.telegram import send_appeal, send_report, notify_block
from .utils.i18n import t
from .utils.supabase import log_report, log_appeal, log_check, get_trends as supabase_trends, check_health as supabase_health, get_admin_data, get_dashboard_data, get_community_stats, record_vote

_PRIVATE_IP_RE = re.compile(
    r"^(localhost|127\.|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|169\.254\.|"
    r"100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.|0\.0\.0\.0|::1|::ffff:|"
    r"fc[0-9a-f]{2}:|fd[0-9a-f]{2}:|fe80:)",
    re.IGNORECASE
)

_VALID_IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$|^[0-9a-fA-F:]+$")


def _get_client_ip(req: Request) -> str:
    """Real client IP — prefers X-Forwarded-For (Vercel proxies real IP there)."""
    xff = req.headers.get("x-forwarded-for", "")
    if xff:
        ip = xff.split(",")[0].strip()
        if _VALID_IP_RE.match(ip):
            return ip
    return req.client.host if req.client else "unknown"


def _get_geo(req: Request) -> tuple[str | None, str | None]:
    """(country, region) from Vercel edge geo headers. None when not behind Vercel."""
    h = req.headers
    country = h.get("x-vercel-ip-country")
    region = h.get("x-vercel-ip-country-region")
    return (country or None, region or None)

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


app = FastAPI(title="Qalqan AI", version="5.1.0",
              description="AI-powered cybersecurity research platform — PhD-grade threat detection",
              lifespan=lifespan)

# --- CORS: extension + localhost only (not wildcard) ---
_ALLOWED_ORIGINS = [
    "chrome-extension://",          # any Chrome extension (prefix match done below)
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1",
    "https://qalqan-ai-nu.vercel.app",
]

def _allowed_extension_ids() -> set[str]:
    """Pinned extension IDs from env (comma-separated). Empty = dev mode (allow any)."""
    raw = os.getenv("QALQAN_EXTENSION_IDS", "")
    return {x.strip() for x in raw.split(",") if x.strip()}


def _cors_origin_allowed(origin: str) -> bool:
    if not origin:
        return False
    if origin.startswith("chrome-extension://"):
        pinned = _allowed_extension_ids()
        if not pinned:
            return True  # dev: no IDs pinned yet → allow any extension
        ext_id = origin[len("chrome-extension://"):].strip("/")
        return ext_id in pinned  # prod: only our published extension(s)
    return origin in _ALLOWED_ORIGINS

_CORS_ALLOW_HEADERS = {"Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                       "Access-Control-Allow-Headers": "Content-Type",
                       "Access-Control-Max-Age": "86400"}

# --- Rate Limits (per IP, per endpoint, 60s window via Redis) ---
RATE_LIMIT_CHECK = 30    # /check: 30 req/min
RATE_LIMIT_SCREEN = 5    # /analyze-screen: 5 req/min (AI vision — expensive)
RATE_LIMIT_APPEAL = 5    # /appeal: 5 req/min
RATE_LIMIT_REPORT = 3    # /report: 3 req/min


# --- CORS + origin enforcement (replaces CORSMiddleware — handles chrome-extension:// prefix) ---
@app.middleware("http")
async def enforce_origin(request: Request, call_next):
    """Full CORS handler + origin gate. No CORSMiddleware needed."""
    origin = request.headers.get("origin", "")
    allowed = not origin or _cors_origin_allowed(origin)

    # OPTIONS preflight — block disallowed origins before they probe the API
    if request.method == "OPTIONS":
        if allowed and origin:
            return JSONResponse(status_code=200, content={},
                                headers={**_CORS_ALLOW_HEADERS, "Access-Control-Allow-Origin": origin})
        return JSONResponse(status_code=403, content={"error": "Origin not allowed"})

    if not allowed:
        logger.warning(f"Blocked request from disallowed origin: {origin}")
        return JSONResponse(status_code=403, content={"error": "Origin not allowed"})

    response = await call_next(request)
    if origin:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


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
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    logger.error(f"UNHANDLED {type(exc).__name__} on {request.url.path}: {str(exc)[:300]}\nTRACEBACK:\n{tb[-800:]}")
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

# (_DEMO_RESULTS moved to demo.py)


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
    image_base64: str = Field(..., max_length=4_000_000)  # ~3MB image; body must stay under Vercel 4.5MB limit
    lang: str = Field(default="kk", max_length=5)

    @field_validator("image_base64")
    @classmethod
    def validate_base64(cls, v):
        import base64
        # Must be valid base64, must start with image magic after decode
        try:
            decoded = base64.b64decode(v[:64], validate=True)  # check header only (fast)
        except Exception:
            raise ValueError("image_base64 must be valid base64")
        # Check image magic bytes (JPEG: FF D8, PNG: 89 50, GIF: 47 49, WEBP: 52 49)
        if not (decoded[:2] in (b'\xff\xd8', b'\x89P') or
                decoded[:4] in (b'GIF8', b'RIFF') or
                decoded[:6] == b'GIF89a'):
            raise ValueError("image_base64 must be a valid image (JPEG/PNG/GIF/WEBP)")
        return v

class AppealRequest(BaseModel):
    url: str = Field(..., max_length=2048)
    reason: str = Field(..., max_length=500)   # tightened from 1000

class ReportRequest(BaseModel):
    url: str = Field(..., max_length=2048)
    threat_type: str = Field(default="scam", pattern=r"^(phishing|pyramid|gambling|scam|malware|fake_shop|social_engineering|other)$")
    note: str = Field(default="", max_length=500)

class BatchRequest(BaseModel):
    urls: list[str] = Field(..., min_length=1, max_length=15)  # enforced at model level (was 50)
    lang: str = Field(default="kk", max_length=5)

    @field_validator("urls")
    @classmethod
    def validate_urls(cls, v):
        from urllib.parse import urlparse
        cleaned = []
        for url in v:
            url = url.strip()
            if not url:
                continue
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            if len(url) > 2048:
                raise ValueError(f"URL too long: {url[:50]}...")
            host = urlparse(url).hostname or ""
            if _PRIVATE_IP_RE.match(host):
                raise ValueError(f"Private/internal address not allowed: {host}")
            cleaned.append(url)
        return cleaned

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


# --- Health check ---
@app.get("/")
async def root(request: Request):
    accept = request.headers.get("accept", "")
    # API clients get JSON
    if "text/html" not in accept:
        return {
            "status": "online", "name": "Qalqan AI", "version": "5.1.0",
            "pipeline": "6-tier threat detection",
            "ai_providers": {
                "groq": "configured" if os.getenv("GROQ_API_KEY") else "missing",
                "gemini": "configured" if os.getenv("GEMINI_API_KEY") else "missing"
            }
        }
    return HTMLResponse(content=LANDING_HTML)


# (LANDING_HTML moved to templates.py)


def _to_domain(s: str) -> str:
    """Normalize a URL or bare hostname to a domain (extract_domain needs a scheme)."""
    s = (s or "").strip()
    if s and "://" not in s:
        s = "https://" + s
    return extract_domain(s)


async def community_verdict(domain: str) -> dict | None:
    """Crowd-block tier: if a domain is community-confirmed scam, return a DANGEROUS hit.
    Returns None (and never raises) when not blocked or storage unavailable."""
    try:
        stats = await get_community_stats(domain)
    except Exception:
        return None
    if not stats.get("auto_blocked"):
        return None
    return {
        "verdict": "DANGEROUS", "threat_score": 88, "threat_type": "community_blocked",
        "source": "community",
        "reason_kk": f"Қоғамдастық бұғаттаған: {stats['confirms']} растау, {stats['reports']} шағым",
        "reason_ru": f"Заблокировано сообществом: {stats['confirms']} подтверждений, {stats['reports']} жалоб",
        "reason_en": f"Community-blocked: {stats['confirms']} confirmations, {stats['reports']} reports",
        "indicators": ["community_blocked"], "community": stats,
    }


# --- НЕГІЗГІ ТЕКСЕРУ: 6-деңгейлі pipeline ---
@app.post("/check")
async def check_site(request: CheckRequest, req: Request, background_tasks: BackgroundTasks):
    # Rate limit (consumer tier — per IP)
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="check"):
        return JSONResponse(status_code=429, content={
            "error": "Rate limit exceeded", "detail": "Max 30 requests per minute"
        })
    return await _run_url_check(request, req, background_tasks)


async def _run_url_check(request: CheckRequest, req: Request, background_tasks: BackgroundTasks):
    """Core URL-check pipeline (no rate limit) — shared by /check and the partner API."""
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
    cached = await get_cached(key)
    if cached:
        return cached

    # --- Tier 1.5: URL Feature Extraction (ML) — needed for explanation even on early hits ---
    start_time = time.time()
    url_feats = extract_features(url)

    # --- Tier 1: Pyramid list + Local blacklist ---
    pyramid_hit = check_pyramid_domain(url)
    if pyramid_hit:
        result = calculate_final_verdict([], None, pyramid_hit, lang=lang)
        result["explanation"] = generate_explanation(url_feats, None, [], None, pyramid_hit, result["threat_score"], lang=lang)
        result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": "pyramid_list"}
        await set_cached(key, result)
        return result

    blacklist_hit = check_local_blacklist(url)
    if blacklist_hit:
        result = calculate_final_verdict([blacklist_hit], None, None, lang=lang)
        result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": "blacklist"}
        await set_cached(key, result)
        return result

    # --- Tier 1.7: KZ Brand Impersonation (fast, offline, very high precision) ---
    kz_impersonation_hit = check_kz_impersonation_url(domain)
    if kz_impersonation_hit:
        result = calculate_final_verdict([], None, None, url_features=url_feats, lang=lang, deterministic_hit=kz_impersonation_hit)
        result["explanation"] = generate_explanation(url_feats, None, [], None, None, result["threat_score"], lang=lang)
        result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": "kz_impersonation"}
        await set_cached(key, result)
        return result

    # --- Tier 1.8: Gambling / unlicensed bookmaker (KZ banned sites) ---
    gambling_hit = check_gambling_domain(domain)
    if gambling_hit:
        result = calculate_final_verdict([], None, None, url_features=url_feats, lang=lang, deterministic_hit=gambling_hit)
        result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": "gambling_list"}
        await set_cached(key, result)
        return result

    # --- Tier 1.9: Госзакупки fraud detection (goszakup.gov.kz URLs) ---
    if is_goszakup_url(url):
        goszakup_hit = await check_goszakup_url(url)
        if goszakup_hit and goszakup_hit.get("verdict") in ("DANGEROUS", "SUSPICIOUS"):
            result = calculate_final_verdict([goszakup_hit], None, None, url_features=url_feats, lang=lang)
            result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": "goszakup_fraud"}
            result["red_flags"] = goszakup_hit.get("red_flags", [])
            await set_cached(key, result)
            return result

    # --- Tier 2 + 2.5 + 2.7: Databases, domain intel AND community in parallel ---
    community_hit = None
    try:
        _t2 = await asyncio.gather(
            check_all_databases(url),
            check_domain_intelligence(domain, url),
            community_verdict(domain),
            return_exceptions=True,
        )
        db_results = _t2[0] if isinstance(_t2[0], list) else []
        domain_info = _t2[1] if isinstance(_t2[1], dict) else None
        community_hit = _t2[2] if isinstance(_t2[2], dict) else None
        if isinstance(_t2[0], BaseException):
            logger.error(f"check_all_databases raised: {type(_t2[0]).__name__}: {_t2[0]}")
        if isinstance(_t2[1], BaseException):
            logger.error(f"check_domain_intelligence raised: {type(_t2[1]).__name__}: {_t2[1]}")
    except BaseException as e:
        logger.error(f"Tier2 gather failed: {type(e).__name__}: {e}")
        db_results, domain_info = [], None

    # Combine DB results (+ community crowd-block as a DANGEROUS source)
    all_db = db_results + ([domain_info] if domain_info else []) + ([community_hit] if community_hit else [])

    if any(r.get("verdict") == "DANGEROUS" for r in all_db):
        result = calculate_final_verdict(all_db, None, None,
                                         domain_info=domain_info, url_features=url_feats, lang=lang)
        result["explanation"] = generate_explanation(url_feats, domain_info, db_results, None, None, result["threat_score"], lang=lang)
        result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": "databases"}
        if domain_info and domain_info.get("domain_details"):
            result["domain_details"] = domain_info["domain_details"]
        await set_cached(key, result)
        return result

    # --- Tier 3: AI analysis (with URL feature context for better accuracy) ---
    ai_result = await analyze_url(url, context=url_feats)
    ai_failed = ai_result.get("source") == "ai_error"

    result = calculate_final_verdict(
        db_results,
        None if ai_failed else ai_result,
        None, domain_info=domain_info, url_features=url_feats, lang=lang
    )
    result["explanation"] = generate_explanation(url_feats, domain_info, db_results,
                                                  None if ai_failed else ai_result, None, result["threat_score"], lang=lang)
    result["metadata"] = {
        "processing_time_ms": int((time.time() - start_time) * 1000),
        "tier_hit": "heuristics_only" if ai_failed else "ai",
        "ai_provider": ai_result.get("source", "unknown") if not ai_failed else "none"
    }
    if ai_failed:
        result["ai_skipped"] = True
        result["ai_skip_reason"] = "all_providers_failed"
        logger.warning(f"AI_SKIPPED for {domain} — scoring by heuristics only")
    if domain_info and domain_info.get("domain_details"):
        result["domain_details"] = domain_info["domain_details"]
    await set_cached(key, result)
    logger.info(f"CHECK {domain} → {result['verdict']} ({result['threat_score']}) via {result['source']} [{result['metadata']['processing_time_ms']}ms]")

    # Telegram notification for dangerous sites
    if result.get("verdict") == "DANGEROUS":
        background_tasks.add_task(notify_block, url, result["verdict"], result["threat_score"], result.get("source", ""))

    # Supabase: async log (fire-and-forget, never blocks response)
    _country, _region = _get_geo(req)
    background_tasks.add_task(
        log_check,
        domain=domain,
        verdict=result["verdict"],
        score=result["threat_score"],
        top_source=result.get("source", "unknown"),
        ai_used=not ai_failed,
        ai_skipped=ai_failed,
        latency_ms=result["metadata"]["processing_time_ms"],
        country=_country,
        region=_region,
    )

    return result


# --- МӘТІН ТЕКСЕРУ ---
@app.post("/check-text")
async def check_text(request: TextCheckRequest, req: Request):
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="check_text"):
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


# --- AI СКАМ-СОВЕТНИК: опиши ситуацию словами → вердикт + совет ---
class AdvisorRequest(BaseModel):
    text: str = Field(..., max_length=2000)
    lang: str = Field(default="ru", max_length=5)


@app.post("/advisor")
async def advisor(request: AdvisorRequest, req: Request):
    """AI scam-advisor. User describes a situation (call/SMS/offer) in free text →
    verdict + reasoning + red_flags + advice, KZ-aware, in the user's language."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="advisor"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    return await analyze_situation(request.text, request.lang)


# --- АФМ/АРРФР ПИРАМИДА ТІЗІМІ: атау бойынша тексеру ---
class PyramidNameRequest(BaseModel):
    name: str = Field(..., max_length=200)
    lang: str = Field(default="ru", max_length=5)


@app.post("/pyramid/check")
async def pyramid_name_check(request: PyramidNameRequest, req: Request):
    """Check a company/brand NAME against the AFM/ARDFM pyramid registry.
    POST {"name": "Финико", "lang": "ru"} → verdict (DANGEROUS if listed) or clean."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="pyramid_name"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    hit = check_pyramid_name(request.name, lang=request.lang)
    if hit:
        result = calculate_final_verdict([], None, None, lang=request.lang, deterministic_hit=hit)
        result["match"] = hit.get("match")
        result["confidence"] = hit.get("confidence")
        result["status"] = hit.get("status")
        result["official_link"] = hit.get("official_link")
        result["registry_size"] = registry_size()
        return result

    # No match → not a guarantee; advise verifying with the official registry
    not_found = {
        "kk": "Реестрде табылмады. Бұл 100% кепілдік емес — АРРФР ресми тізімін тексеріңіз.",
        "ru": "В реестре не найдено. Это не 100% гарантия — сверьтесь с офиц. списком АРРФР.",
        "en": "Not found in the registry. Not a guarantee — verify with the official ARDFM list.",
    }
    return {
        "verdict": "SAFE", "threat_score": 0, "risk_level": "low",
        "threat_type": "not_listed", "source": "pyramid_registry",
        "match": None, "registry_size": registry_size(),
        "official_link": "https://www.gov.kz/memleket/entities/ardfm",
        "detail": not_found.get(request.lang, not_found["ru"]),
        "detail_kk": not_found["kk"], "detail_ru": not_found["ru"], "detail_en": not_found["en"],
        "indicators": [],
    }


# --- BATCH ТЕКСЕРУ (max 15 URL) ---
@app.post("/batch")
async def check_batch(request: BatchRequest, req: Request):
    """Check up to 15 URLs in parallel. Returns list of verdicts."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="check"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    urls = request.urls[:15]  # hard cap
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
            cached = await get_cached(key)
            if cached:
                return {**cached, "url": url}

            url_feats = extract_features(url)  # sync — fast, no I/O

            pyramid_hit = check_pyramid_domain(url)
            if pyramid_hit:
                r = calculate_final_verdict([], None, pyramid_hit, lang=lang)
                r["explanation"] = generate_explanation(url_feats, None, [], None, pyramid_hit, r["threat_score"], lang=lang)
                await set_cached(key, r)
                return {**r, "url": url}

            blacklist_hit = check_local_blacklist(url)
            if blacklist_hit:
                r = calculate_final_verdict([blacklist_hit], None, None, lang=lang)
                await set_cached(key, r)
                return {**r, "url": url}

            kz_impersonation_hit = check_kz_impersonation_url(domain)
            if kz_impersonation_hit:
                r = calculate_final_verdict([], kz_impersonation_hit, None, url_features=url_feats, lang=lang)
                await set_cached(key, r)
                return {**r, "url": url}

            gambling_hit = check_gambling_domain(domain)
            if gambling_hit:
                r = calculate_final_verdict([], gambling_hit, None, url_features=url_feats, lang=lang)
                await set_cached(key, r)
                return {**r, "url": url}

            _t2b = await asyncio.gather(
                check_all_databases(url),
                check_domain_intelligence(domain, url),
                return_exceptions=True,
            )
            db_results = _t2b[0] if isinstance(_t2b[0], list) else []
            domain_info = _t2b[1] if isinstance(_t2b[1], dict) else None
            ai_result = await analyze_url(url, context=url_feats)
            r = calculate_final_verdict(db_results, ai_result, None,
                                        domain_info=domain_info, url_features=url_feats, lang=lang)
            r["explanation"] = generate_explanation(url_feats, domain_info, db_results, ai_result, None, r["threat_score"], lang=lang)
            await set_cached(key, r)
            return {**r, "url": url}
        except Exception as e:
            logger.error(f"Batch check error for {url}: {e}")
            return {"url": url, "verdict": "SUSPICIOUS", "threat_score": 50, "error": str(e)[:100]}

    results = await asyncio.gather(*[_check_one(u) for u in urls])
    return {"results": list(results), "checked": len(results)}


# --- СКРИНШОТ ТЕКСЕРУ ---
@app.post("/analyze-screen")
async def check_screen(request: ScreenRequest, req: Request):
    client_ip = _get_client_ip(req)
    # Fix #3: separate rate limit key + lower limit (5/min, not shared with /check)
    if not await check_rate_limit(client_ip, RATE_LIMIT_SCREEN, endpoint="screen"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded. Max 5 screenshot analyses per minute."})

    result = await analyze_screenshot(request.image_base64)
    return calculate_final_verdict([], result, None, lang=request.lang)


# --- VOICE / CALL-SCAM (audio → transcript → fraud verdict) ---
@app.post("/voice")
async def check_voice(req: Request, file: UploadFile = File(...), lang: str = "kk"):
    """Upload a voice/call recording → transcribe (Groq Whisper) → call-scam verdict."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_SCREEN, endpoint="voice"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded. Max 5/min."})
    from .services.voice_scam import analyze_voice, MAX_AUDIO_BYTES
    audio = await file.read()
    if not audio:
        return JSONResponse(status_code=422, content={"error": "Empty audio"})
    if len(audio) > MAX_AUDIO_BYTES:
        return JSONResponse(status_code=413, content={"error": "Audio too large (max 20MB)"})
    return await analyze_voice(audio, file.filename or "audio.ogg", lang)


# --- АПЕЛЛЯЦИЯ ---
@app.post("/appeal")
async def appeal(request: AppealRequest, req: Request, background_tasks: BackgroundTasks):
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_APPEAL, endpoint="appeal"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    result = await send_appeal(request.url, request.reason)

    # Supabase: persist appeal (fire-and-forget)
    domain = extract_domain(request.url)
    background_tasks.add_task(
        log_appeal,
        domain=domain,
        verdict_received=getattr(request, "verdict", None),
        reason=request.reason,
    )

    return result


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
async def report_site(request: ReportRequest, req: Request, background_tasks: BackgroundTasks):
    client_ip = _get_client_ip(req)
    # Fix #4: separate rate limit key (was "appeal:", now "report:")
    if not await check_rate_limit(client_ip, RATE_LIMIT_REPORT, endpoint="report"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded. Max 3 reports per minute."})

    domain = extract_domain(request.url)
    reports = _load_reports()
    if domain not in reports:
        reports[domain] = {"count": 0, "types": [], "unique_ips": [], "first_report": time.time()}

    reports[domain]["count"] += 1
    reports[domain]["types"].append(request.threat_type)
    # Hash IP before storing (privacy — GDPR / KZ ЗоПД compliance)
    from hashlib import md5 as _md5
    ip_hash = _md5(client_ip.encode()).hexdigest()[:16]
    unique_ips: list = reports[domain].setdefault("unique_ips", [])
    if ip_hash not in unique_ips:
        unique_ips.append(ip_hash)

    # Fix #9: threshold raised to 10 AND requires 3+ unique IPs
    auto_blocked = reports[domain]["count"] >= 10 and len(unique_ips) >= 3
    _save_reports(reports)

    if auto_blocked:
        logger.warning(f"AUTO-BLOCKED: {domain} ({reports[domain]['count']} reports, {len(unique_ips)} unique IPs)")

    # Telegram хабарлама
    result = await send_report(request.url, request.threat_type, request.note)
    result["reports_count"] = reports[domain]["count"]
    result["auto_blocked"] = auto_blocked

    # Supabase: persist report (fire-and-forget)
    background_tasks.add_task(
        log_report,
        domain=domain,
        url=request.url,
        category=request.threat_type,
        comment=request.note,
        lang=getattr(request, "lang", "ru"),
        reporter_ip=client_ip,
    )

    return result


# --- ҚОҒАМДАСТЫҚ ДАУЫСЫ (community voting) ---
class VoteRequest(BaseModel):
    target: str = Field(..., max_length=2048)   # url or bare domain
    vote: str = Field(..., max_length=10)        # "confirm" | "dispute"


@app.post("/vote")
async def community_vote(request: VoteRequest, req: Request):
    """Community confirm/dispute vote on a domain. One vote per IP per domain.
    confirm = «это действительно скам», dispute = «ложное срабатывание»."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_REPORT, endpoint="vote"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    vote = request.vote.strip().lower()
    if vote not in ("confirm", "dispute"):
        return JSONResponse(status_code=400, content={"error": "vote must be 'confirm' or 'dispute'"})
    domain = _to_domain(request.target)
    if not domain or "." not in domain:
        return JSONResponse(status_code=400, content={"error": "invalid domain"})
    return await record_vote(domain, vote, client_ip)


@app.get("/community/{domain}")
async def community_info(domain: str):
    """Public crowd-intelligence for a domain: reports, confirm/dispute votes, auto-block."""
    return await get_community_stats(_to_domain(domain))


# --- СТАТИСТИКА ---
@app.get("/stats")
async def get_stats(request: Request):
    from .utils.cache import _mem
    reports = _load_reports()
    json_data = {
        "total_reported_domains": len(reports),
        "auto_blocked": sum(1 for r in reports.values() if r["count"] >= 10 and len(r.get("unique_ips", [])) >= 3),
        "whitelist_size": len(_whitelist),
        "cache_entries": len(_mem),
        "demo_mode": DEMO_MODE,
        "version": "5.1.0",
        "features": ["goszakup_fraud_detection", "telegram_bot", "kz_threat_report", "6tier_pipeline", "xai_explainer"],
        "report_url": "/report/generate",
    }
    if "text/html" not in request.headers.get("accept", ""):
        return json_data

    # Fetch live trends from Supabase for HTML page
    trends = await supabase_trends() or {}
    total = trends.get("total_checks", 0)
    dist = trends.get("verdict_distribution", {})
    dangerous = dist.get("DANGEROUS", 0)
    suspicious = dist.get("SUSPICIOUS", 0)
    safe_cnt = dist.get("SAFE", 0)
    top_domains = trends.get("top_domains_checked", [])[:5]
    top_reported = trends.get("top_reported_domains", [])[:5]

    top_dom_html = "".join(
        f'<div class="row-item"><span class="ri-name">{d["domain"]}</span><span class="ri-count">{d["checks"]}</span></div>'
        for d in top_domains
    ) or '<div class="row-item muted">Нет данных</div>'
    top_rep_html = "".join(
        f'<div class="row-item"><span class="ri-name">{d["domain"]}</span><span class="ri-count ri-danger">{d["reports"]}</span></div>'
        for d in top_reported
    ) or '<div class="row-item muted">Нет данных</div>'

    danger_pct = round(dangerous / total * 100) if total else 0

    html = f"""<!DOCTYPE html>
<html lang="kk"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Qalqan AI — Статистика</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0a0e1a;color:#e2e8f0;font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;padding:0}}
.navbar{{background:rgba(10,14,26,.95);border-bottom:1px solid #1e2d4a;padding:16px 24px;display:flex;align-items:center;justify-content:space-between}}
.logo{{color:#00d4ff;font-weight:700;font-size:18px;text-decoration:none}}
.nav-back{{color:#64748b;font-size:14px;text-decoration:none}}
.nav-back:hover{{color:#00d4ff}}
.page{{max-width:1000px;margin:0 auto;padding:40px 24px}}
h1{{font-size:28px;font-weight:700;margin-bottom:6px}}
.subtitle{{color:#64748b;font-size:14px;margin-bottom:40px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:40px}}
.card{{background:#131d35;border:1px solid #1e2d4a;border-radius:14px;padding:24px}}
.card-num{{font-size:36px;font-weight:800;color:#00d4ff;font-variant-numeric:tabular-nums}}
.card-num.danger{{color:#ef4444}}
.card-num.warn{{color:#f59e0b}}
.card-num.safe{{color:#22c55e}}
.card-label{{font-size:12px;color:#64748b;margin-top:4px;text-transform:uppercase;letter-spacing:.5px}}
.section{{margin-bottom:32px}}
.section-title{{font-size:16px;font-weight:600;margin-bottom:16px;color:#94a3b8}}
.row-item{{display:flex;justify-content:space-between;align-items:center;padding:10px 16px;background:#0f1629;border-radius:8px;margin-bottom:6px;font-size:13px}}
.ri-name{{color:#e2e8f0;font-family:monospace}}
.ri-count{{color:#00d4ff;font-weight:600}}
.ri-danger{{color:#ef4444}}
.muted{{color:#64748b}}
.bar-wrap{{background:#0f1629;border-radius:8px;height:28px;margin-bottom:10px;overflow:hidden;position:relative}}
.bar-fill{{height:100%;display:flex;align-items:center;padding-left:10px;font-size:12px;font-weight:600;color:#0a0e1a;transition:width .5s ease}}
.bar-label{{position:absolute;right:10px;top:50%;transform:translateY(-50%);font-size:12px;color:#64748b}}
.report-btn{{display:inline-flex;align-items:center;gap:8px;background:#00d4ff;color:#0a0e1a;padding:12px 24px;border-radius:10px;font-weight:700;font-size:14px;text-decoration:none;margin-top:24px}}
.report-btn:hover{{opacity:.85}}
footer{{text-align:center;padding:32px;color:#334155;font-size:12px;border-top:1px solid #1e2d4a;margin-top:40px}}
</style></head><body>
<div class="navbar">
  <a class="logo" href="/">🛡 Qalqan AI</a>
  <a class="nav-back" href="/">← Басты бет</a>
</div>
<div class="page">
  <h1>Статистика</h1>
  <p class="subtitle">Нақты уақыт деректері · Real-time from Supabase</p>

  <div class="grid">
    <div class="card"><div class="card-num">{total}</div><div class="card-label">Барлығы тексерілді</div></div>
    <div class="card"><div class="card-num danger">{dangerous}</div><div class="card-label">Қауіпті анықталды</div></div>
    <div class="card"><div class="card-num warn">{suspicious}</div><div class="card-label">Күдікті</div></div>
    <div class="card"><div class="card-num safe">{safe_cnt}</div><div class="card-label">Қауіпсіз</div></div>
    <div class="card"><div class="card-num">{danger_pct}%</div><div class="card-label">Қауіп үлесі</div></div>
    <div class="card"><div class="card-num">{json_data["whitelist_size"]}</div><div class="card-label">Ақ тізім</div></div>
  </div>

  <div class="section">
    <div class="section-title">Вердикт бойынша бөлініс</div>
    <div class="bar-wrap"><div class="bar-fill" style="width:{danger_pct}%;background:#ef4444">{danger_pct}% ОПАСНО</div><div class="bar-label">{dangerous} сайт</div></div>
    <div class="bar-wrap"><div class="bar-fill" style="width:{round(suspicious/total*100) if total else 0}%;background:#f59e0b">{round(suspicious/total*100) if total else 0}% ПОДОЗРИТЕЛЬНО</div><div class="bar-label">{suspicious} сайт</div></div>
    <div class="bar-wrap"><div class="bar-fill" style="width:{round(safe_cnt/total*100) if total else 0}%;background:#22c55e">{round(safe_cnt/total*100) if total else 0}% БЕЗОПАСНО</div><div class="bar-label">{safe_cnt} сайт</div></div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">
    <div class="section">
      <div class="section-title">Жиі тексерілген домендер</div>
      {top_dom_html}
    </div>
    <div class="section">
      <div class="section-title">Жиі хабарланған домендер</div>
      {top_rep_html}
    </div>
  </div>

  <a class="report-btn" href="/report/generate">PDF есеп жүктеу</a>
</div>
<footer>Qalqan AI v5.1.0 · Деректер: Supabase PostgreSQL · © 2026 Қыдырбек Елдос</footer>
</body></html>"""
    return HTMLResponse(content=html)


# --- ТРЕНДЫ (crowd-sourced) ---
@app.get("/trends")
async def get_trends():
    """Threat trends from Supabase check_logs + reports — real crowd intelligence."""
    data = await supabase_trends()
    if data is None:
        # Supabase not configured — return empty structure (not an error)
        return {
            "total_checks": 0,
            "top_domains_checked": [],
            "verdict_distribution": {},
            "top_detection_sources": [],
            "ai_stats": {"ai_used": 0, "ai_skipped": 0, "heuristics_only": 0},
            "avg_latency_ms": None,
            "total_reports": 0,
            "top_reported_domains": [],
            "report_categories": {},
            "note": "Supabase not configured",
        }
    return data


# ── Regulator Dashboard ───────────────────────────────────────────────────────
# (DASHBOARD_HTML moved to templates.py)


def _dashboard_demo() -> dict:
    """Deterministic, realistic demo dataset so the dashboard always renders
    populated for a judge demo even when Supabase is empty."""
    import datetime
    base = datetime.date(2026, 6, 19)
    series = []
    for i in range(29, -1, -1):
        day = base - datetime.timedelta(days=i)
        n = 29 - i
        total = 180 + n * 9 + (40 if day.weekday() < 5 else -30)
        threats = int(total * (0.20 + 0.004 * n))
        series.append({"date": day.isoformat(), "total": total, "threats": threats})
    total_checks = sum(s["total"] for s in series)
    blocked = sum(s["threats"] for s in series)
    suspicious = int(blocked * 0.6)
    return {
        "kpis": {
            "total_checks": total_checks, "threats_blocked": blocked, "suspicious": suspicious,
            "block_rate_pct": round(100 * blocked / total_checks, 1),
            "total_reports": 342, "avg_score": 38.4,
        },
        "time_series": series,
        "verdict_distribution": {
            "SAFE": total_checks - blocked - suspicious, "SUSPICIOUS": suspicious, "DANGEROUS": blocked,
        },
        "threat_types": {
            "Фишинг": 1240, "Гемблинг": 880, "Финпирамиды": 560, "KZ-угрозы": 430,
            "Подозр. инфраструктура": 390, "Госзакуп-фрод": 210,
        },
        "tier_effectiveness": {
            "groq_ai": 1450, "gambling_list": 880, "local_blacklist": 620, "pyramid_list": 560,
            "domain_intel": 390, "kz_impersonation": 300, "url_features": 260, "goszakup": 210,
        },
        "top_dangerous_domains": [
            {"domain": "kaspi-bonus123.kz", "count": 47}, {"domain": "halyk-verify.com", "count": 39},
            {"domain": "egov-kz.support", "count": 33}, {"domain": "1xbet-kz.top", "count": 28},
            {"domain": "finiko-invest.kz", "count": 24}, {"domain": "mostbet-kz.bet", "count": 21},
            {"domain": "kaspi-gold.site", "count": 18}, {"domain": "qazaqstan-lottery.com", "count": 15},
        ],
        "report_categories": {"phishing": 156, "pyramid": 89, "gambling": 61, "other": 36},
        "regions": {
            "Алматы қ.": {"total": 1840, "threats": 612}, "Астана": {"total": 1320, "threats": 430},
            "Шымкент": {"total": 760, "threats": 295}, "Қарағанды": {"total": 540, "threats": 178},
            "Алматы обл.": {"total": 510, "threats": 165}, "Түркістан": {"total": 470, "threats": 188},
            "Атырау": {"total": 360, "threats": 121}, "Маңғыстау": {"total": 330, "threats": 110},
            "Ақтөбе": {"total": 310, "threats": 96}, "Павлодар": {"total": 280, "threats": 84},
            "Қостанай": {"total": 260, "threats": 72}, "ШҚО": {"total": 250, "threats": 79},
            "Қызылорда": {"total": 230, "threats": 88}, "Жамбыл": {"total": 220, "threats": 81},
            "БҚО": {"total": 190, "threats": 55}, "Ақмола": {"total": 180, "threats": 49},
            "СҚО": {"total": 150, "threats": 41}, "Абай": {"total": 130, "threats": 44},
            "Жетісу": {"total": 120, "threats": 38}, "Ұлытау": {"total": 90, "threats": 27},
        },
    }


@app.get("/dashboard/data")
async def dashboard_data(req: Request):
    """JSON feed for the regulator dashboard. Falls back to demo data when
    Supabase is empty/unavailable so the page never looks broken.
    ?demo=1 forces the full demo dataset (for presentations/screenshots)."""
    force_demo = req.query_params.get("demo", "").lower() in ("1", "true", "yes")
    if not force_demo:
        data = await get_dashboard_data()
        if data and data.get("kpis", {}).get("total_checks", 0) >= 10:
            data["_source"] = "live"
            return data
    demo = _dashboard_demo()
    demo["_source"] = "demo"
    return demo


@app.get("/dashboard")
async def dashboard_page():
    """Regulator-facing threat-landscape dashboard (KZ economic-cyber threats)."""
    from fastapi.responses import HTMLResponse
    return HTMLResponse(DASHBOARD_HTML)


@app.get("/app")
async def mini_app():
    """Telegram Mini App (Web App): URL checker + AI advisor + KZ threat map."""
    return HTMLResponse(MINIAPP_HTML)


# --- Weekly Telegram report (cron: every Sunday 09:00 UTC) ---
def _authorize_cron(req: Request) -> bool:
    """Allow only Vercel cron (Authorization: Bearer CRON_SECRET) or explicit ?secret=.
    If CRON_SECRET is unset, allow (set CRON_SECRET in env to lock cron-only endpoints down)."""
    secret = os.getenv("CRON_SECRET", "")
    if not secret:
        return True
    if req.headers.get("authorization", "") == f"Bearer {secret}":
        return True
    return req.query_params.get("secret", "") == secret


@app.get("/telegram/weekly-report")
async def telegram_weekly_report(req: Request):
    """Send weekly threat summary to Telegram admin channel. Called by Vercel cron.
    Protected by CRON_SECRET so outsiders can't trigger broadcasts."""
    if not _authorize_cron(req):
        return JSONResponse(status_code=403, content={"error": "Forbidden"})
    from .utils.telegram import send_message as _tg_send
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    if not chat_id:
        return {"error": "TELEGRAM_CHAT_ID not set"}
    try:
        trends = await supabase_trends() or {}
        total = trends.get("total_checks", 0)
        dist = trends.get("verdict_distribution", {})
        dangerous = dist.get("DANGEROUS", 0)
        suspicious = dist.get("SUSPICIOUS", 0)
        safe_cnt = dist.get("SAFE", 0)
        top_rep = trends.get("top_reported_domains", [])[:3]
        rep_lines = "\n".join(f"  • <code>{d['domain']}</code> ({d['reports']} хабарлама)" for d in top_rep) or "  —"

        from datetime import datetime, timezone
        week = datetime.now(timezone.utc).strftime("%d.%m.%Y")
        text = (
            f"📊 <b>Qalqan AI — Апталық есеп</b>\n"
            f"<i>{week} ұяты</i>\n\n"
            f"🔍 Тексерілді: <b>{total}</b>\n"
            f"🔴 Қауіпті: <b>{dangerous}</b>\n"
            f"🟡 Күдікті: <b>{suspicious}</b>\n"
            f"🟢 Қауіпсіз: <b>{safe_cnt}</b>\n\n"
            f"📌 Жиі хабарланған:\n{rep_lines}\n\n"
            f"🌐 <a href='https://qalqan-ai-nu.vercel.app/stats'>Толық статистика</a>"
        )
        await _tg_send(int(chat_id), text)
        logger.info("Weekly Telegram report sent")
        return {"ok": True, "sent_to": chat_id, "total_checks": total}
    except Exception as e:
        logger.error(f"Weekly report failed: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)[:100]})


# --- PWA Web App Manifest ---
@app.get("/manifest.webmanifest")
async def pwa_manifest():
    from fastapi.responses import Response as _Resp
    import json as _json
    manifest = {
        "name": "Qalqan AI — Cyber Shield",
        "short_name": "Qalqan AI",
        "description": "AI-powered cybersecurity for Kazakhstan. Blocks phishing, scams, gambling.",
        "id": "/m",
        "start_url": "/m",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#0a0e1a",
        "theme_color": "#0a0e1a",
        "lang": "kk",
        "icons": [
            {"src": "https://raw.githubusercontent.com/Kennurken/qalqan-ai/master/extension/public/icons/icon48.png",
             "sizes": "48x48", "type": "image/png"},
            {"src": "https://raw.githubusercontent.com/Kennurken/qalqan-ai/master/extension/public/icons/icon128.png",
             "sizes": "128x128", "type": "image/png"}
        ],
        "categories": ["security", "utilities"],
        "shortcuts": [
            {"name": "URL тексеру", "url": "/", "description": "Check a URL for threats"},
            {"name": "Статистика", "url": "/stats", "description": "View threat statistics"},
            {"name": "Орнату", "url": "/install", "description": "Install the extension"}
        ]
    }
    return _Resp(content=_json.dumps(manifest), media_type="application/manifest+json",
                 headers={"Cache-Control": "public, max-age=86400"})


# --- Installation guide page ---
@app.get("/install")
async def install_page():
    return HTMLResponse(content=INSTALL_HTML)


# --- Mobile PWA (installable, offline-capable app shell) ---
@app.get("/m")
async def mobile_app():
    return HTMLResponse(content=MOBILE_HTML)


@app.get("/sw.js")
async def service_worker():
    from fastapi.responses import Response as _Resp
    return _Resp(content=SW_JS, media_type="application/javascript",
                 headers={"Cache-Control": "no-cache", "Service-Worker-Allowed": "/"})


# --- Keep-warm (Vercel cron hits every 10 min) ---
@app.get("/ping")
async def ping():
    return {"status": "ok", "version": "5.1.0", "demo_mode": DEMO_MODE}


# --- Detailed health check (Fix #5: no longer reveals which keys are configured) ---
@app.get("/health")
async def health():
    # Count configured keys without revealing WHICH ones (prevents targeted key-fishing)
    key_names = ["GROQ_API_KEY", "GEMINI_API_KEY", "PHISHTANK_API_KEY",
                 "GOOGLE_SAFE_BROWSING_KEY", "VIRUSTOTAL_API_KEY", "TELEGRAM_BOT_TOKEN"]
    configured_count = sum(1 for k in key_names if os.getenv(k))
    data_files_ok = sum(
        1 for fname in ["whitelist.json", "kz_brands.json", "pyramid_schemes.json",
                        "blacklist.json", "kz_phishing_patterns.json"]
        if os.path.exists(os.path.join(_data_dir, fname))
    )
    sb_health, rd_health = await asyncio.gather(supabase_health(), redis_health())
    return {
        "status": "ok",
        "version": "5.1.0",
        "demo_mode": DEMO_MODE,
        "api_keys_configured": f"{configured_count}/{len(key_names)}",
        "data_files_ok": f"{data_files_ok}/5",
        "whitelist_domains": len(_whitelist),
        "supabase": sb_health,
        "redis": rd_health,
    }


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.get("/admin")
async def admin_dashboard(req: Request, key: str | None = None):
    admin_secret = os.getenv("ADMIN_SECRET", "")
    header_key = req.headers.get("x-admin-key", "")
    cookie_key = req.cookies.get("qadmin", "")
    provided = header_key or cookie_key or (key or "")
    if not admin_secret or provided != admin_secret:
        return HTMLResponse(
            '<html><body style="background:#0f172a;color:#ef4444;font-family:monospace;'
            'display:flex;align-items:center;justify-content:center;height:100vh;margin:0;">'
            '<div style="text-align:center"><div style="font-size:48px">🛡️</div>'
            '<h1>401 — Unauthorized</h1>'
            '<p>Use <code>X-Admin-Key</code> header (preferred) or <code>?key=</code> once</p></div></body></html>',
            status_code=401,
        )

    # If authenticated via the URL query, move the secret into an httponly cookie and
    # redirect to a clean URL so it never lingers in browser history / bookmarks (P0-4).
    if key and key == admin_secret and not (header_key or cookie_key):
        from fastapi.responses import RedirectResponse
        resp = RedirectResponse(url="/admin", status_code=303)
        resp.set_cookie("qadmin", admin_secret, httponly=True, secure=True,
                        samesite="lax", max_age=86400)
        return resp

    import json as _json
    data = await get_admin_data(limit=100)
    if not data:
        data = {"reports": [], "appeals": [], "check_logs": []}

    reports = data["reports"]
    appeals = data["appeals"]
    logs = data["check_logs"]

    total_checks = len(logs)
    total_reports = len(reports)
    total_appeals = len(appeals)
    dangerous = sum(1 for r in logs if r.get("verdict") == "DANGEROUS")
    pct_dangerous = round(dangerous / total_checks * 100) if total_checks else 0

    def _row_color(verdict):
        return {"DANGEROUS": "#ef4444", "SUSPICIOUS": "#f59e0b", "SAFE": "#10b981"}.get(verdict, "#94a3b8")

    def _fmt_time(ts):
        return (ts or "")[:19].replace("T", " ")

    def _build_rows_logs():
        rows = ""
        for r in logs[:50]:
            c = _row_color(r.get("verdict", ""))
            rows += (
                f"<tr>"
                f"<td>{_fmt_time(r.get('created_at'))}</td>"
                f"<td style='max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{r.get('domain','')}</td>"
                f"<td><span style='color:{c};font-weight:bold'>{r.get('verdict','')}</span></td>"
                f"<td>{r.get('score','')}</td>"
                f"<td>{r.get('top_source','')}</td>"
                f"<td>{'✓' if r.get('ai_used') else '—'}</td>"
                f"<td>{r.get('latency_ms','')}</td>"
                f"</tr>"
            )
        return rows

    def _build_rows_reports():
        rows = ""
        for r in reports[:50]:
            rows += (
                f"<tr>"
                f"<td>{_fmt_time(r.get('created_at'))}</td>"
                f"<td style='max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{r.get('domain','')}</td>"
                f"<td><span style='background:#7c3aed;padding:2px 6px;border-radius:4px;font-size:11px'>{r.get('category','')}</span></td>"
                f"<td>{r.get('lang','')}</td>"
                f"<td style='max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{r.get('comment','') or '—'}</td>"
                f"</tr>"
            )
        return rows

    def _build_rows_appeals():
        rows = ""
        for r in appeals[:50]:
            rows += (
                f"<tr>"
                f"<td>{_fmt_time(r.get('created_at'))}</td>"
                f"<td style='max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{r.get('domain','')}</td>"
                f"<td><span style='color:#ef4444'>{r.get('verdict_received','')}</span></td>"
                f"<td style='max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{r.get('reason','') or '—'}</td>"
                f"</tr>"
            )
        return rows

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Qalqan AI — Admin</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:#0a0f1e;color:#e2e8f0;font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh}}
  .topbar{{background:linear-gradient(135deg,#1e3a5f,#1e1b4b);padding:16px 32px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #334155}}
  .topbar h1{{font-size:20px;font-weight:700;background:linear-gradient(135deg,#3b82f6,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
  .topbar span{{font-size:12px;color:#64748b;margin-left:auto}}
  .stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:24px 32px}}
  .stat-card{{background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:20px;text-align:center}}
  .stat-card .num{{font-size:36px;font-weight:800;margin-bottom:4px}}
  .stat-card .label{{font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:.5px}}
  .tabs{{display:flex;gap:0;padding:0 32px;border-bottom:1px solid #1e293b}}
  .tab{{padding:12px 20px;font-size:13px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;color:#64748b;transition:all .2s;background:none;border-left:none;border-right:none;border-top:none}}
  .tab.active{{color:#3b82f6;border-bottom-color:#3b82f6}}
  .tab:hover{{color:#93c5fd}}
  .panel{{display:none;padding:24px 32px}}
  .panel.active{{display:block}}
  .table-wrap{{overflow-x:auto;border-radius:8px;border:1px solid #1e293b}}
  table{{width:100%;border-collapse:collapse;font-size:13px}}
  th{{background:#0f172a;padding:10px 12px;text-align:left;font-weight:600;color:#64748b;font-size:11px;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid #1e293b}}
  td{{padding:10px 12px;border-bottom:1px solid #0f172a;vertical-align:top}}
  tr:hover td{{background:rgba(59,130,246,.06)}}
  tr:last-child td{{border-bottom:none}}
  .badge{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600}}
  .refresh-btn{{float:right;background:#1e40af;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-size:13px}}
  .refresh-btn:hover{{background:#2563eb}}
  .section-title{{font-size:15px;font-weight:700;margin-bottom:16px;color:#94a3b8;display:flex;align-items:center;gap:8px}}
  .count{{font-size:12px;background:#1e293b;padding:2px 8px;border-radius:20px;color:#64748b}}
  @media(max-width:768px){{.stats{{grid-template-columns:repeat(2,1fr)}}.topbar{{padding:12px 16px}}.panel,.tabs{{padding-left:16px;padding-right:16px}}}}
</style>
</head>
<body>
<div class="topbar">
  <div style="font-size:24px">🛡️</div>
  <h1>Qalqan AI — Admin Dashboard</h1>
  <span id="clock"></span>
</div>

<div class="stats">
  <div class="stat-card">
    <div class="num" style="color:#3b82f6">{total_checks}</div>
    <div class="label">Тексерулер / Checks</div>
  </div>
  <div class="stat-card">
    <div class="num" style="color:#ef4444">{pct_dangerous}%</div>
    <div class="label">Қауіпті / Dangerous</div>
  </div>
  <div class="stat-card">
    <div class="num" style="color:#f59e0b">{total_reports}</div>
    <div class="label">Шағымдар / Reports</div>
  </div>
  <div class="stat-card">
    <div class="num" style="color:#8b5cf6">{total_appeals}</div>
    <div class="label">Апелляциялар / Appeals</div>
  </div>
</div>

<div class="tabs">
  <button class="tab active" onclick="showTab('logs')">Check Logs ({total_checks})</button>
  <button class="tab" onclick="showTab('reports')">Reports ({total_reports})</button>
  <button class="tab" onclick="showTab('appeals')">Appeals ({total_appeals})</button>
  <button class="refresh-btn" onclick="location.reload()">↻ Refresh</button>
</div>

<div id="logs" class="panel active">
  <div class="section-title">Recent Check Logs <span class="count">last 50</span></div>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Time</th><th>Domain</th><th>Verdict</th><th>Score</th><th>Source</th><th>AI</th><th>ms</th></tr></thead>
      <tbody>{_build_rows_logs()}</tbody>
    </table>
  </div>
</div>

<div id="reports" class="panel">
  <div class="section-title">User Reports <span class="count">last 50</span></div>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Time</th><th>Domain</th><th>Category</th><th>Lang</th><th>Comment</th></tr></thead>
      <tbody>{_build_rows_reports()}</tbody>
    </table>
  </div>
</div>

<div id="appeals" class="panel">
  <div class="section-title">User Appeals <span class="count">last 50</span></div>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Time</th><th>Domain</th><th>Verdict was</th><th>Reason</th></tr></thead>
      <tbody>{_build_rows_appeals()}</tbody>
    </table>
  </div>
</div>

<script>
function showTab(id) {{
  document.querySelectorAll('.tab').forEach((t,i) => t.classList.toggle('active', ['logs','reports','appeals'][i]===id));
  document.querySelectorAll('.panel').forEach(p => p.classList.toggle('active', p.id===id));
}}
function tick() {{
  document.getElementById('clock').textContent = new Date().toLocaleString('ru-KZ');
}}
tick(); setInterval(tick, 1000);
// Auto-refresh every 60s
setTimeout(() => location.reload(), 60000);
</script>
</body>
</html>"""

    return HTMLResponse(html)


# ============================================================
# RESEARCH API ENDPOINTS (doctoral-grade)
# ============================================================

@app.post("/features")
async def get_features(request: FeatureRequest, req: Request):
    """Extract 30+ ML features from URL (no HTTP request, pure lexical analysis).
    Use for: ML model training, feature importance analysis, dataset building."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="check"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    return extract_features(request.url)


@app.post("/check-research")
async def check_research(request: CheckRequest, req: Request):
    """Full research output: all features, all scores, explanation, metadata.
    Use for: paper benchmarks, ablation studies, system evaluation."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="check"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    url = request.url
    lang = request.lang
    domain = extract_domain(url)
    start_time = time.time()

    # Extract ALL data — sync first, then all async in parallel
    url_feats = extract_features(url)
    pyramid_hit = check_pyramid_domain(url)
    blacklist_hit = check_local_blacklist(url)
    kz_hit = check_kz_impersonation_url(domain)
    gambling_hit = check_gambling_domain(domain)
    # Fix #8: pass url_feats context to AI for better accuracy (same as /check endpoint)
    _t2r = await asyncio.gather(
        check_all_databases(url),
        check_domain_intelligence(domain, url),
        analyze_url(url, context=url_feats),
        return_exceptions=True,
    )
    db_results = _t2r[0] if isinstance(_t2r[0], list) else []
    domain_info = _t2r[1] if isinstance(_t2r[1], dict) else None
    ai_result = _t2r[2] if isinstance(_t2r[2], dict) else {"source": "ai_error"}

    # Calculate final verdict (pyramid > kz_impersonation > gambling > blacklist > DB > AI)
    effective_hit = pyramid_hit or kz_hit or gambling_hit
    result = calculate_final_verdict(
        db_results, ai_result if not effective_hit else None, effective_hit or None,
        domain_info=domain_info, url_features=url_feats, lang=lang
    )
    if not effective_hit and blacklist_hit and not db_results:
        result = calculate_final_verdict([blacklist_hit], None, None, url_features=url_feats, lang=lang)

    # Generate explanation
    explanation = generate_explanation(
        url_feats, domain_info, db_results, ai_result, pyramid_hit, result["threat_score"], lang=lang
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
            "kz_impersonation": kz_hit,
            "gambling": gambling_hit,
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
            "version": "5.1.0"
        }
    }


# ============================================================
# EVALUATION ENDPOINT
# ============================================================

@app.post("/evaluate")
async def evaluate(req: Request):
    """Run benchmark on built-in test dataset. Returns accuracy, F1, MCC, per-URL results."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, 5, endpoint="eval"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    results = await run_benchmark()
    return results


# ── Telegram Bot Webhook ──────────────────────────────────────────────────────

@app.post("/telegram/webhook")
async def telegram_webhook(req: Request, background_tasks: BackgroundTasks):
    """Receive Telegram Bot API updates via webhook.
    Security: verified by TELEGRAM_WEBHOOK_SECRET header token.
    """
    # Verify secret token (set when registering webhook via setWebhook)
    secret = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
    if not secret:
        logger.warning("Telegram webhook called but TELEGRAM_WEBHOOK_SECRET not configured")
        return JSONResponse(status_code=403, content={"error": "Webhook not configured"})
    incoming = req.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if incoming != secret:
        logger.warning("Telegram webhook: invalid secret token")
        return JSONResponse(status_code=403, content={"error": "Forbidden"})

    try:
        update = await req.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON"})

    # Fire-and-forget dispatch (don't await — respond 200 to Telegram immediately)
    background_tasks.add_task(_dispatch_update, update)
    return JSONResponse(status_code=200, content={"ok": True})


async def _dispatch_update(update: dict):
    try:
        from .services.bot_handler import dispatch
        await dispatch(update)
    except Exception as e:
        logger.error(f"Bot dispatch error: {e}")


@app.get("/telegram/set-webhook")
async def set_telegram_webhook(req: Request):
    """Register Telegram webhook. Call once after deployment.
    Protected: requires TELEGRAM_WEBHOOK_SECRET env var to be set.
    GET /telegram/set-webhook?secret=<TELEGRAM_WEBHOOK_SECRET>
    """
    secret = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
    token  = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not token:
        return JSONResponse(status_code=500, content={"error": "TELEGRAM_BOT_TOKEN not set"})

    # Auth: caller must supply the secret in query param
    caller_secret = req.query_params.get("secret", "")
    if secret and caller_secret != secret:
        return JSONResponse(status_code=403, content={"error": "Forbidden"})

    base = os.getenv("QALQAN_API_URL", str(req.base_url).rstrip("/"))
    webhook_url = f"{base}/telegram/webhook"

    payload: dict = {"url": webhook_url, "allowed_updates": ["message", "inline_query", "callback_query"]}
    if secret:
        payload["secret_token"] = secret

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.post(
                f"https://api.telegram.org/bot{token}/setWebhook",
                json=payload
            )
            data = res.json()
        logger.info(f"Telegram setWebhook: {data}")
        return {"ok": data.get("ok"), "webhook_url": webhook_url, "telegram_response": data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ── Госзакупки Fraud Detection API ───────────────────────────────────────────

class GoszakupRequest(BaseModel):
    """Raw procurement data for fraud analysis (when caller scrapes it themselves)."""
    tender_number:      str | None = None
    supplier_bin:       str | None = None
    purchase_method_code: str | None = None
    participants_count: int | None = None
    lot_amount:         float | None = None
    ref_price:          float | None = None
    created_date:       str | None = None
    end_date:           str | None = None
    name_ru:            str | None = None
    name_kz:            str | None = None
    supplier:           dict | None = None   # nested supplier object
    region_stats:       dict | None = None   # {total_tenders, won_tenders}


@app.post("/goszakup/analyse")
async def goszakup_analyse(request: GoszakupRequest, req: Request):
    """Analyse government procurement data for fraud red-flags.
    Accepts raw tender/supplier data JSON and returns fraud verdict + red flags.
    10 detection rules: monopoly, inflated pricing, shell company, tailored specs, etc.
    """
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="check"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    data = request.model_dump(exclude_none=True)
    result = await analyse_procurement_data(data)
    logger.info(f"GOSZAKUP {data.get('tender_number','?')} → {result['verdict']} ({result['threat_score']})")
    return result


@app.get("/goszakup/check/{tender_number}")
async def goszakup_check_tender(tender_number: str, req: Request):
    """Fetch tender from goszakup.gov.kz by number and run fraud analysis."""
    if not re.match(r"^\d{6,20}$", tender_number):
        return JSONResponse(status_code=422, content={"error": "Invalid tender number — digits only, 6-20 chars"})
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="check"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    from .services.goszakup import check_tender_by_number
    result = await check_tender_by_number(tender_number)
    return result


# ── Goszakup Fraud Graph (affiliation / collusion / cartel) ──────────────────


class GraphRequest(BaseModel):
    companies: list[dict] = Field(default_factory=list)
    tenders: list[dict] = Field(default_factory=list)


@app.post("/goszakup/graph")
async def goszakup_graph_analyse(request: GraphRequest, req: Request):
    """Build a procurement relationship graph and detect affiliation, collusion,
    conflict-of-interest and cartel-bidding patterns."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="check"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    from .services.goszakup_graph import build_fraud_graph
    return build_fraud_graph({"companies": request.companies, "tenders": request.tenders})


@app.get("/goszakup/graph/demo")
async def goszakup_graph_demo():
    from .services.goszakup_graph import build_fraud_graph, demo_graph_data
    g = build_fraud_graph(demo_graph_data())
    g["_source"] = "demo"
    return g


@app.get("/goszakup/graph")
async def goszakup_graph_page():
    from fastapi.responses import HTMLResponse
    return HTMLResponse(GRAPH_HTML)


# ── KZ Threat Report ──────────────────────────────────────────────────────────

@app.get("/report/generate")
async def generate_threat_report(req: Request, month: str | None = None):
    """
    Generate 'KZ Cyber Threat Landscape 2026' PDF report.
    GET /report/generate              → PDF with default (demo) stats
    GET /report/generate?month=Jun    → same, custom month label
    Returns: application/pdf
    """
    from fastapi.responses import Response
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, 3, endpoint="report"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    try:
        from .services.threat_report import generate_report, DEFAULT_STATS
        import copy
        stats = copy.deepcopy(DEFAULT_STATS)
        if month:
            stats["report_month"] = month

        pdf_bytes = generate_report(stats)
        logger.info(f"Threat report generated: {len(pdf_bytes):,} bytes for {client_ip}")
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="KZ_Threat_Report_{stats["report_month"].replace(" ", "_")}.pdf"',
                "Content-Length": str(len(pdf_bytes)),
            },
        )
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        return JSONResponse(status_code=500, content={"error": f"Report generation failed: {str(e)[:100]}"})


# ── Offline DB update feed ────────────────────────────────────────────────────

# ── Published KZ Threat Feed (open data moat, CC-BY) ──────────────────────────
_kz_feed_cache: dict | None = None


def _build_kz_feed() -> dict:
    """Assemble the Kazakhstan threat feed from bundled KZ-curated data."""
    global _kz_feed_cache
    if _kz_feed_cache is not None:
        return _kz_feed_cache
    entries: list[dict] = []
    seen: set[str] = set()
    try:
        with open(os.path.join(_data_dir, "pyramid_schemes.json"), encoding="utf-8") as f:
            schemes = json.load(f).get("known_schemes", [])
        for s in schemes:
            for d in s.get("domains", []):
                d = (d or "").lower().strip()
                if d and d not in seen:
                    seen.add(d)
                    entries.append({"domain": d, "type": s.get("type", "pyramid"),
                                    "name": s.get("name", "")})
    except Exception as e:
        logger.warning(f"KZ feed build failed: {e}")
    entries.sort(key=lambda e: e["domain"])
    _kz_feed_cache = {
        "name": "Qalqan AI — Kazakhstan Threat Feed",
        "description": "Curated Kazakhstan-specific scam / phishing / pyramid / gambling domains",
        "license": "CC-BY-4.0",
        "attribution": "Qalqan AI — github.com/Kennurken/qalqan-ai",
        "homepage": "https://qalqan-ai-nu.vercel.app",
        "count": len(entries),
        "entries": entries,
    }
    return _kz_feed_cache


@app.get("/feed")
async def feed_index():
    """Feed index — published KZ feed + live ingested threat-feed stats."""
    kz = _build_kz_feed()
    return {
        "kz_feed": {"count": kz["count"], "url": "/feed/kz", "txt": "/feed/kz?format=txt",
                    "license": kz["license"]},
        "live_threat_feeds": feed_stats(),
    }


@app.get("/feed/kz")
async def kz_threat_feed(format: str | None = None):
    """Published Kazakhstan threat feed (CC-BY-4.0) — the open data-moat artifact.
    ?format=txt → newline-separated domains for feed consumers."""
    feed = _build_kz_feed()
    if format == "txt":
        from fastapi.responses import PlainTextResponse
        body = ("# Qalqan AI — Kazakhstan Threat Feed (CC-BY-4.0)\n"
                "# github.com/Kennurken/qalqan-ai\n")
        body += "\n".join(e["domain"] for e in feed["entries"])
        return PlainTextResponse(body)
    from datetime import datetime, timezone
    return {**feed, "generated_at": datetime.now(timezone.utc).isoformat()}


# ── Partner (B2G) API — banks / regulators via X-API-Key ─────────────────────
_PARTNERS_HTML = """<!DOCTYPE html>
<html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Qalqan AI — Партнёрский API (B2G)</title>
<style>
:root{--bg:#0a0e1a;--panel:#111827;--bd:#1e293b;--tx:#e6edf6;--mut:#8194ad;--cyan:#00d4ff;--green:#22c55e}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:24px;max-width:860px;margin:0 auto;line-height:1.6}
a{color:var(--cyan);text-decoration:none}
h1{font-size:26px;font-weight:800;margin-bottom:4px}
.sub{color:var(--mut);margin-bottom:24px}
h2{font-size:17px;margin:26px 0 10px;border-left:3px solid var(--cyan);padding-left:10px}
.card{background:var(--panel);border:1px solid var(--bd);border-radius:12px;padding:16px;margin-bottom:14px}
table{width:100%;border-collapse:collapse;font-size:14px}
th,td{text-align:left;padding:9px 8px;border-bottom:1px solid var(--bd)}
th{color:var(--mut);font-size:12px;text-transform:uppercase}
code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
code{background:#0d1424;padding:2px 6px;border-radius:5px;color:var(--cyan);font-size:13px}
pre{background:#0d1424;border:1px solid var(--bd);border-radius:10px;padding:14px;overflow-x:auto;font-size:13px;color:#cbd5e1;margin:8px 0}
.method{color:var(--green);font-weight:700}
.tag{display:inline-block;font-size:11px;font-weight:700;color:#06121a;background:var(--cyan);padding:3px 9px;border-radius:999px}
.foot{color:var(--mut);font-size:12px;margin-top:30px;text-align:center}
</style></head><body>
<h1>🛡 Qalqan AI — Партнёрский API <span class="tag">B2G</span></h1>
<div class="sub">Для банков, Антифрод-центра Нацбанка, KZ-CERT, АФМ. Проверка угроз в реальном времени.</div>

<h2>Авторизация</h2>
<div class="card">Все запросы — с заголовком <code>X-API-Key: &lt;ваш ключ&gt;</code>.<br>
Демо-ключ (ограниченный): <code>qalqan-demo-2026</code>. Боевой ключ — по запросу.</div>

<h2>Эндпоинты</h2>
<div class="card"><table>
<tr><th>Метод</th><th>Путь</th><th>Назначение</th></tr>
<tr><td><span class="method">POST</span></td><td><code>/v1/check</code></td><td>Проверка одного URL</td></tr>
<tr><td><span class="method">POST</span></td><td><code>/v1/batch</code></td><td>Пакетная проверка URL</td></tr>
<tr><td><span class="method">GET</span></td><td><code>/v1/feed</code></td><td>Полный KZ threat-feed</td></tr>
<tr><td><span class="method">GET</span></td><td><code>/v1/usage</code></td><td>Счётчик запросов вашего ключа</td></tr>
</table></div>

<h2>Пример — проверка URL</h2>
<pre>curl -X POST https://qalqan-ai-nu.vercel.app/v1/check \\
  -H "X-API-Key: qalqan-demo-2026" \\
  -H "Content-Type: application/json" \\
  -d '{"url":"kaspi-bonus123.kz","lang":"ru"}'</pre>
<pre>{
  "partner": "Demo (rate-limited)",
  "request_id": "a1b2c3d4e5f6...",
  "result": { "verdict": "DANGEROUS", "threat_score": 95, ... }
}</pre>

<h2>Лимиты</h2>
<div class="card">Демо-ключ: <b>30 запросов/мин</b>. Партнёрский ключ: <b>600/мин</b> (настраивается).<br>
Ответ <code>429</code> при превышении.</div>

<h2>Получить боевой ключ</h2>
<div class="card">Напишите на <a href="mailto:kmarukob76@gmail.com">kmarukob76@gmail.com</a> с указанием организации.
Ключ выдаётся под конкретного партнёра, лимиты и логирование — индивидуально.</div>

<div class="foot">Qalqan AI · Республиканский конкурс ДЭР 2026 · <a href="/">главная</a> · <a href="/dashboard">панель</a></div>
</body></html>"""


def _partner_auth(req: Request) -> tuple[str, str | None]:
    key = req.headers.get("x-api-key", "") or req.query_params.get("api_key", "")
    return key, verify_api_key(key)


def _partner_limit(key: str) -> int:
    return 30 if is_demo(key) else 600   # demo tier vs partner tier (per min)


@app.post("/v1/check")
async def api_v1_check(request: CheckRequest, req: Request, background_tasks: BackgroundTasks):
    """Partner URL check. Auth: X-API-Key header. Higher rate tier than public /check."""
    key, partner = _partner_auth(req)
    if not partner:
        return JSONResponse(status_code=401, content={"error": "Invalid or missing X-API-Key"})
    limit = _partner_limit(key)
    if not await check_rate_limit(key_id(key), limit, endpoint="apiv1"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded", "limit_per_min": limit})
    import uuid
    result = await _run_url_check(request, req, background_tasks)
    return {"partner": partner, "request_id": uuid.uuid4().hex[:16], "result": result}


@app.post("/v1/batch")
async def api_v1_batch(request: BatchRequest, req: Request, background_tasks: BackgroundTasks):
    """Partner bulk URL check (up to model limit)."""
    key, partner = _partner_auth(req)
    if not partner:
        return JSONResponse(status_code=401, content={"error": "Invalid or missing X-API-Key"})
    limit = _partner_limit(key)
    if not await check_rate_limit(key_id(key), limit, endpoint="apiv1b"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded", "limit_per_min": limit})
    results = await asyncio.gather(
        *[_run_url_check(CheckRequest(url=u, lang=request.lang), req, background_tasks)
          for u in request.urls],
        return_exceptions=True,
    )
    out = [r if isinstance(r, dict) else {"error": str(r)[:80]} for r in results]
    return {"partner": partner, "count": len(out), "results": out}


@app.get("/v1/feed")
async def api_v1_feed(req: Request):
    """Partner access to the full Kazakhstan threat feed."""
    key, partner = _partner_auth(req)
    if not partner:
        return JSONResponse(status_code=401, content={"error": "Invalid or missing X-API-Key"})
    return _build_kz_feed()


@app.get("/v1/usage")
async def api_v1_usage(req: Request):
    """Partner's own usage counter (this process)."""
    key, partner = _partner_auth(req)
    if not partner:
        return JSONResponse(status_code=401, content={"error": "Invalid or missing X-API-Key"})
    return {"partner": partner, "requests": usage_for(key), "rate_limit_per_min": _partner_limit(key)}


@app.get("/partners")
async def partners_docs():
    from fastapi.responses import HTMLResponse
    return HTMLResponse(_PARTNERS_HTML)


@app.get("/offline-db")
async def offline_db_feed():
    """
    Returns flat domain lists for extension offline DB auto-update.
    Extension fetches this daily, merges into in-memory Sets.
    """
    import hashlib as _hl
    data_dir = os.path.join(os.path.dirname(__file__), "data")

    def _load(filename: str, key: str) -> list[str]:
        try:
            with open(os.path.join(data_dir, filename)) as f:
                obj = json.load(f)
            return obj.get(key, [])
        except Exception:
            return []

    # Pyramid domains: flatten list-of-{domains:[...]} entries
    try:
        with open(os.path.join(data_dir, "pyramid_schemes.json")) as f:
            schemes = json.load(f).get("known_schemes", [])
        pyramids = [d for s in schemes for d in s.get("domains", [])]
    except Exception:
        pyramids = []

    whitelist = _load("whitelist.json", "trusted_domains")
    blacklist = _load("blacklist.json", "domains")

    payload = {"pyramids": pyramids, "whitelist": whitelist, "blacklist": blacklist}

    # ETag: fingerprint for cache — extension skips update if unchanged
    raw = json.dumps(payload, sort_keys=True)
    etag = _hl.md5(raw.encode()).hexdigest()[:12]

    from fastapi.responses import Response as _Resp
    return _Resp(
        content=raw,
        media_type="application/json",
        headers={
            "ETag": etag,
            "Cache-Control": "public, max-age=43200",  # 12h CDN cache
        },
    )
