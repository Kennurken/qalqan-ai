# Qalqan AI v5.1
# Бас API: 6-деңгейлі қауіп детекция pipeline + ML features + XAI
# Academic research-grade: features extraction, explainability, evaluation

import json
import os
import re
import time
import hmac
import logging
import asyncio
import traceback
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from .templates import LANDING_HTML, DASHBOARD_HTML, INSTALL_HTML, MINIAPP_HTML, GRAPH_HTML, MOBILE_HTML, SW_JS, PARTNERS_HTML, NOTFOUND_HTML, LEAK_HTML, HELP_HTML, BRAND_HTML, SCAN_HTML, IMPACT_HTML, BATCH_HTML, SCREEN_HTML
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
from .utils.telegram import send_appeal, send_report, notify_block, health_alert
from .utils.i18n import t
from .utils.supabase import log_report, log_appeal, log_check, get_trends as supabase_trends, check_health as supabase_health, get_admin_data, get_dashboard_data, get_community_stats, record_vote, get_federated_feed, add_brand_watch as supabase_add_brand_watch, list_brand_watches as supabase_list_brand_watches, update_brand_watch_snapshot as supabase_update_brand_watch, list_digest_subs as supabase_list_digest_subs

_PRIVATE_IP_RE = re.compile(
    r"^(localhost|127\.|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|169\.254\.|"
    r"100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.|0\.0\.0\.0|::1|::ffff:|"
    r"fc[0-9a-f]{2}:|fd[0-9a-f]{2}:|fe80:)",
    re.IGNORECASE
)

_VALID_IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$|^[0-9a-fA-F:]+$")


def _get_client_ip(req: Request) -> str:
    """Real client IP — prefers X-Forwarded-For (Vercel proxies real IP there).
    SECURITY: trusting the FIRST XFF value is only safe behind a proxy that
    overwrites it (Vercel does). On a self-hosted VPS behind Caddy/nginx a client
    can spoof XFF to evade per-IP rate limits — there, terminate at a proxy that
    sets a trusted header and read the rightmost hop instead."""
    xff = req.headers.get("x-forwarded-for", "")
    if xff:
        ip = xff.split(",")[0].strip()
        if _VALID_IP_RE.match(ip):
            return ip
    return req.client.host if req.client else "unknown"


def _get_geo(req: Request) -> tuple[str | None, str | None]:
    """(country, region) from edge geo headers — Vercel, or Cloudflare when the
    backend runs on a VPS behind CF. None when no edge geo is available."""
    h = req.headers
    country = h.get("x-vercel-ip-country") or h.get("cf-ipcountry")
    region = h.get("x-vercel-ip-country-region") or h.get("cf-region-code")
    return (country or None, region or None)

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("qalqan")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: kick off feed loading in the background so cold start isn't blocked
    by the multi-second URLhaus/OpenPhish fetch (check_openphish lazy-loads on first
    use too). Shutdown: close the shared pooled HTTP client."""
    from .services.threat_db import load_openphish_feed
    try:
        asyncio.create_task(load_openphish_feed())
    except Exception as e:
        logger.warning(f"feed preload kickoff failed (lazy-loads on first check): {e}")
    # Register the Telegram / command menu + Menu button (idempotent, no-op
    # without a bot token) so it applies automatically on deploy.
    try:
        from .services.bot_handler import register_bot_ui
        asyncio.create_task(register_bot_ui())
    except Exception as e:
        logger.warning(f"bot UI registration kickoff failed: {e}")
    yield
    from .utils.http import aclose
    await aclose()


app = FastAPI(title="Qalqan AI", version="5.1.0",
              description="AI-powered cybersecurity research platform — PhD-grade threat detection",
              lifespan=lifespan)

# gzip large HTML/JSON responses (landing, dashboard, graph are 30KB+ each)
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1024)

# Static HTML shells — let the CDN serve them (data loads via AJAX, not cached)
_HTML_CACHE = {"Cache-Control": "public, max-age=300, s-maxage=600"}

# Inline SVG favicon — kills the /favicon.ico 404 (browser auto-requests it)
_FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#00d4ff">'
            '<path d="M12 2 4 5v6c0 5 3.4 8.6 8 10 4.6-1.4 8-5 8-10V5z"/></svg>')


@app.get("/favicon.ico")
@app.get("/favicon.svg")
async def favicon():
    from fastapi.responses import Response as _Resp
    return _Resp(content=_FAVICON, media_type="image/svg+xml",
                 headers={"Cache-Control": "public, max-age=604800"})

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
    # Local dev on any port (http://localhost:8899 etc.)
    if origin.startswith(("http://localhost:", "http://127.0.0.1:")):
        return True
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


# --- Security headers (the Vercel deploy is primary; only the VPS Caddyfile set
#     these before, so every Vercel-served page — landing, admin, stats — shipped
#     bare). Applied to all responses; frame-blocking is scoped so it doesn't break
#     the Telegram Mini App (/app, /m) which legitimately loads inside an iframe. ---
_NO_FRAME_PATHS = ("/admin",)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Strict-Transport-Security",
                                "max-age=31536000; includeSubDomains")
    if request.url.path in _NO_FRAME_PATHS:
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "frame-ancestors 'none'"
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
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    if "text/html" in request.headers.get("accept", ""):
        return HTMLResponse(NOTFOUND_HTML, status_code=404,
                            headers={"Cache-Control": "public, max-age=300"})
    return JSONResponse(status_code=404, content={"error": "not_found", "path": request.url.path})


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


def _is_encoded_internal_ip(host: str) -> bool:
    """Catch decimal/hex-encoded IPs the string regex misses (e.g. http://2130706433/
    = 127.0.0.1). No DNS — pure int decode, safe in a sync validator."""
    import ipaddress
    h = (host or "").strip().lower()
    ip = None
    try:
        if h.isdigit():
            ip = ipaddress.ip_address(int(h))
        elif h.startswith("0x"):
            ip = ipaddress.ip_address(int(h, 16))
    except (ValueError, OverflowError):
        return False
    if ip is None:
        return False
    return (ip.is_private or ip.is_loopback or ip.is_link_local
            or ip.is_reserved or ip.is_multicast or ip.is_unspecified)


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
        if _PRIVATE_IP_RE.match(host) or _is_encoded_internal_ip(host):
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
            "pipeline": "7-tier threat detection",
            "ai_providers": {
                "groq": "configured" if os.getenv("GROQ_API_KEY") else "missing",
                "gemini": "configured" if os.getenv("GEMINI_API_KEY") else "missing"
            }
        }
    return HTMLResponse(content=LANDING_HTML, headers=_HTML_CACHE)


# (LANDING_HTML moved to templates.py)


# urlparse().hostname passes through HTML metacharacters (e.g. "abc<script>.kz"),
# so a crafted URL could store an XSS payload as a "domain". Keep only chars that
# can legitimately appear in a hostname — belt-and-suspenders alongside HTML-escaping.
_DOMAIN_SANITIZE_RE = re.compile(r"[^a-z0-9.\-:_]")


def _to_domain(s: str) -> str:
    """Normalize a URL or bare hostname to a domain (extract_domain needs a scheme)."""
    s = (s or "").strip()
    if s and "://" not in s:
        s = "https://" + s
    dom = extract_domain(s)
    return _DOMAIN_SANITIZE_RE.sub("", dom.lower())


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


async def run_pipeline_internal(url: str, lang: str = "kk") -> dict:
    """In-process pipeline entry for same-process callers (Telegram bot handler).
    Skips the HTTP self-loop the bot used to make (extra serverless invocation +
    ~200-400ms). Validation still runs via CheckRequest (private-IP guard etc.)."""
    return await _run_url_check(CheckRequest(url=url, lang=lang), None, None)


async def _run_url_check(request: CheckRequest, req: Request | None,
                         background_tasks: BackgroundTasks | None):
    """Core URL-check pipeline (no rate limit) — shared by /check, the partner API
    and the in-process bot entry (req/background_tasks are None there: no edge geo,
    side-effects scheduled via asyncio.create_task instead)."""
    url = request.url
    lang = request.lang
    domain = extract_domain(url)
    # lang in the cache key — AI explanations are generated per-language, so a
    # ru-cached verdict must not be served to an en request (and vice versa).
    key = url_hash(url + "|" + lang)

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

    # --- Tier 2 + 2.5 + 2.7 + 2.8: Databases, domain intel, community AND the
    #     fine-tuned ML model (external service, skipped when unconfigured) — all in parallel ---
    from .services.ml_model import ml_predict
    community_hit = None
    ml_hit = None
    try:
        _t2 = await asyncio.gather(
            check_all_databases(url),
            check_domain_intelligence(domain, url),
            community_verdict(domain),
            ml_predict(url),
            return_exceptions=True,
        )
        db_results = _t2[0] if isinstance(_t2[0], list) else []
        domain_info = _t2[1] if isinstance(_t2[1], dict) else None
        community_hit = _t2[2] if isinstance(_t2[2], dict) else None
        ml_hit = _t2[3] if isinstance(_t2[3], dict) else None
        if isinstance(_t2[0], BaseException):
            logger.error(f"check_all_databases raised: {type(_t2[0]).__name__}: {_t2[0]}")
        if isinstance(_t2[1], BaseException):
            logger.error(f"check_domain_intelligence raised: {type(_t2[1]).__name__}: {_t2[1]}")
    except BaseException as e:
        logger.error(f"Tier2 gather failed: {type(e).__name__}: {e}")
        db_results, domain_info = [], None

    # Combine DB results (+ community crowd-block + confident ML verdict as DANGEROUS sources)
    all_db = (db_results + ([domain_info] if domain_info else [])
              + ([community_hit] if community_hit else [])
              + ([ml_hit] if ml_hit else []))

    if any(r.get("verdict") == "DANGEROUS" for r in all_db):
        result = calculate_final_verdict(all_db, None, None,
                                         domain_info=domain_info, url_features=url_feats, lang=lang)
        result["explanation"] = generate_explanation(url_feats, domain_info, db_results, None, None, result["threat_score"], lang=lang)
        _tier = "ml_model" if result.get("source") == "ml_model" else "databases"
        result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": _tier}
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

    # Fire-and-forget side effects. BackgroundTasks when called from an HTTP route;
    # asyncio.create_task for in-process callers (bot) that have no Response cycle.
    def _defer(fn, *args, **kwargs):
        if background_tasks is not None:
            background_tasks.add_task(fn, *args, **kwargs)
        else:
            asyncio.create_task(fn(*args, **kwargs))

    # Telegram notification for dangerous sites
    if result.get("verdict") == "DANGEROUS":
        _defer(notify_block, url, result["verdict"], result["threat_score"], result.get("source", ""))

    # Supabase: async log (never blocks response)
    _country, _region = _get_geo(req) if req is not None else (None, None)
    _defer(
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
class PhoneRequest(BaseModel):
    phone: str = Field(..., max_length=32)
    lang: str = Field(default="kk", max_length=5)


@app.post("/phone")
async def check_phone(request: PhoneRequest, req: Request):
    """Heuristic scam check for a KZ phone number (first-class: API + mobile + bot)."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="phone"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    from .services.phone_sms import analyze_phone
    result = analyze_phone(request.phone, request.lang)
    if not result.get("error") and result.get("formatted"):
        key = "phone:" + result["formatted"].replace(" ", "")
        crowd = await get_community_stats(key)
        result["crowd_reports"] = crowd.get("reports", 0) + crowd.get("confirms", 0)
    return result


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


@app.post("/sms")
async def check_sms(request: TextCheckRequest, req: Request):
    """SMS scam check — same analysis as /check-text plus any extracted links."""
    result = await check_text(request, req)
    if isinstance(result, dict):
        from .services.phone_sms import extract_urls
        result["urls_found"] = extract_urls(request.text)[:5]
    return result


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
async def check_batch(request: BatchRequest, req: Request, background_tasks: BackgroundTasks):
    """Check up to 15 URLs in parallel. Reuses the single tested pipeline
    (_run_url_check) so every tier — whitelist, cache, KZ intel, databases,
    community crowd-block, goszakup, AI — runs identically to /check."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="check"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    urls = request.urls[:15]  # hard cap (model already validated + normalized)
    lang = request.lang

    async def _one(url: str) -> dict:
        try:
            r = await _run_url_check(CheckRequest(url=url, lang=lang), req, background_tasks)
            return {**r, "url": url}
        except Exception as e:
            logger.error(f"Batch check error for {extract_domain(url)}: {e}")
            return {"url": url, "verdict": "SUSPICIOUS", "threat_score": 50, "error": str(e)[:100]}

    results = await asyncio.gather(*[_one(u) for u in urls])
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
    domain = _to_domain(request.url)
    background_tasks.add_task(
        log_appeal,
        domain=domain,
        verdict_received=getattr(request, "verdict", None),
        reason=request.reason,
    )

    return result


# --- ШАҒЫМ (crowd-sourced; backed by Supabase — serverless-safe, no in-memory store) ---
@app.post("/report")
async def report_site(request: ReportRequest, req: Request, background_tasks: BackgroundTasks):
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_REPORT, endpoint="report"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded. Max 3 reports per minute."})

    domain = _to_domain(request.url)
    # Persist to Supabase, awaited so the crowd count below reflects this report
    await log_report(domain=domain, url=request.url, category=request.threat_type,
                     comment=request.note, lang=getattr(request, "lang", "ru"),
                     reporter_ip=client_ip)

    result = await send_report(request.url, request.threat_type, request.note)

    # Authoritative crowd status from Supabase (no ephemeral in-memory counter)
    stats = await get_community_stats(domain)
    result["reports_count"] = stats.get("reports", 0)
    result["auto_blocked"] = bool(stats.get("auto_blocked"))
    if result["auto_blocked"]:
        logger.warning(f"AUTO-BLOCKED (crowd): {domain}")
        # Broadcast crowd-blocks to the public threat channel (deduped inside)
        _defer(notify_channel, domain, "CROWD-BLOCKED", 100)
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
    trends = await supabase_trends() or {}
    top_rep = trends.get("top_reported_domains", [])
    json_data = {
        "total_reports": trends.get("total_reports", 0),
        "total_reported_domains": len(top_rep),
        "auto_blocked": sum(1 for d in top_rep if d.get("auto_blocked")),
        "whitelist_size": len(_whitelist),
        "cache_entries": len(_mem),
        "demo_mode": DEMO_MODE,
        "version": "5.1.0",
        "features": ["goszakup_fraud_detection", "telegram_bot", "kz_threat_report", "7tier_pipeline", "xai_explainer"],
        "report_url": "/report/generate",
    }
    if "text/html" not in request.headers.get("accept", ""):
        return json_data

    # HTML page reuses the trends fetched above (renderer in pages.py)
    from .pages import render_stats_page
    return HTMLResponse(content=render_stats_page(trends, len(_whitelist)))


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
    return HTMLResponse(DASHBOARD_HTML, headers=_HTML_CACHE)


@app.get("/app")
async def mini_app():
    """Telegram Mini App (Web App): URL checker + AI advisor + KZ threat map."""
    return HTMLResponse(MINIAPP_HTML, headers=_HTML_CACHE)


# --- Weekly Telegram report (cron: every Sunday 09:00 UTC) ---
def _authorize_cron(req: Request) -> bool:
    """Allow only Vercel cron (Authorization: Bearer CRON_SECRET) or explicit ?secret=.
    Fail-closed: if CRON_SECRET is unset these endpoints are DENIED (they broadcast to
    Telegram, so must not be open). Set ALLOW_UNAUTHENTICATED_CRON=true to opt out."""
    secret = os.getenv("CRON_SECRET", "")
    if not secret:
        return os.getenv("ALLOW_UNAUTHENTICATED_CRON", "").lower() in ("1", "true", "yes")
    if hmac.compare_digest(req.headers.get("authorization", ""), f"Bearer {secret}"):
        return True
    return hmac.compare_digest(req.query_params.get("secret", ""), secret)


@app.get("/telegram/weekly-report")
async def telegram_weekly_report(req: Request):
    """Send weekly threat summary to Telegram admin channel. Called by Vercel cron.
    Protected by CRON_SECRET so outsiders can't trigger broadcasts."""
    if not _authorize_cron(req):
        return JSONResponse(status_code=403, content={"error": "Forbidden"})
    # send_message lives in bot_handler (utils.telegram has no such symbol —
    # the old import made this cron 500 every Sunday)
    from .services.bot_handler import send_message as _tg_send
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
        # Personal digest fan-out (/subscribe in the bot)
        subs = await supabase_list_digest_subs()
        sent = 0
        for s_id in subs[:100]:
            try:
                await _tg_send(int(s_id), text)
                sent += 1
                await asyncio.sleep(0.05)   # stay under Telegram's ~30 msg/s
            except Exception:
                continue
        logger.info(f"Weekly Telegram report sent (+{sent} subscribers)")
        return {"ok": True, "sent_to": chat_id, "subscribers": sent, "total_checks": total}
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
                 headers={"Cache-Control": "public, max-age=300"})


# --- Installation guide page ---
@app.get("/install")
async def install_page():
    return HTMLResponse(content=INSTALL_HTML, headers=_HTML_CACHE)


# --- Mobile PWA (installable, offline-capable app shell) ---
@app.get("/m")
async def mobile_app():
    return HTMLResponse(content=MOBILE_HTML, headers=_HTML_CACHE)


@app.get("/leak")
async def leak_check():
    """Password-leak checker (HIBP k-anonymity; hash prefix only, client-side)."""
    return HTMLResponse(LEAK_HTML, headers=_HTML_CACHE)


@app.get("/help")
async def help_resources():
    """«Обманули — куда обращаться»: official KZ fraud/cyber helplines + action plan."""
    return HTMLResponse(HELP_HTML, headers=_HTML_CACHE)


class BrandRequest(BaseModel):
    domain: str = Field(..., max_length=253)


@app.post("/brand/scan")
async def brand_scan(request: BrandRequest, req: Request):
    """Brand-protection radar: generate the phishing look-alikes of a brand domain
    and classify them by risk (homoglyph / free-TLD / affix / typo). Deterministic,
    no network — the B2G economic-security tool for banks & agencies."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="brand"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    from .services.brand_protect import generate_typosquats
    return generate_typosquats(request.domain)


@app.post("/brand/live-scan")
async def brand_live_scan(request: BrandRequest, req: Request):
    """Live RDAP scan: which of the highest-risk look-alikes are ACTUALLY registered
    right now. Heavier than /brand/scan (network) → tighter rate limit."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_SCREEN, endpoint="brandlive"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    from .services.brand_watch import scan_brand
    return await scan_brand(request.domain)


@app.post("/brand/watch")
async def brand_watch_subscribe(request: BrandRequest, req: Request):
    """Subscribe a brand domain to daily look-alike monitoring. New registrations
    are detected by the daily cron and alerted to the Qalqan admin channel (pilot);
    partner-facing alert routing comes with the B2G API keys."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_REPORT, endpoint="brandwatch"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    from .services.brand_protect import _split_domain
    name, tld = _split_domain(request.domain)
    if not name or not re.match(r"^[a-z0-9-]+$", name):
        return JSONResponse(status_code=422, content={"error": "invalid domain"})
    domain = f"{name}.{tld}"
    ok = await supabase_add_brand_watch(domain, client_ip)
    return {"ok": ok, "domain": domain,
            "note": "Мониторинг активен — ежедневная проверка RDAP" if ok
            else "Хранилище недоступно — попробуйте позже"}


@app.get("/cron/brand-watch")
async def cron_brand_watch(req: Request):
    """Daily brand-watch scan (Vercel cron, CRON_SECRET-gated): re-scan every watched
    brand, diff against the stored snapshot, alert admin on NEW registrations."""
    if not _authorize_cron(req):
        return JSONResponse(status_code=403, content={"error": "forbidden"})
    from .services.brand_watch import scan_brand, registered_set
    from .utils.telegram import brand_alert
    watches = await supabase_list_brand_watches()
    alerted = []
    for w in watches:
        try:
            scan = await scan_brand(w["domain"])
            if scan.get("error"):
                continue
            current = registered_set(scan)
            previous = set(filter(None, (w.get("snapshot") or "").split(",")))
            new = current - previous
            if new and previous:   # skip alert on the very first scan (baseline)
                new_details = [r for r in scan["registered"] if r["domain"] in new]
                await brand_alert(w["domain"], new_details)
                alerted.append({"brand": w["domain"], "new": sorted(new)})
            await supabase_update_brand_watch(w["id"], ",".join(sorted(current)))
        except Exception as e:
            logger.warning(f"brand-watch scan failed for {w.get('domain')}: {e}")
    return {"watched": len(watches), "alerts": alerted}


@app.get("/brand")
async def brand_page():
    """Brand-protection radar page."""
    return HTMLResponse(BRAND_HTML, headers=_HTML_CACHE)


@app.get("/scan/{domain}")
async def security_scan(domain: str, req: Request):
    """Website security grade (A–F): runs the verdict pipeline + domain intel and
    composes an SSL-Labs-style report card (TLS, domain age, TLD, homoglyph, infra)."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="scan"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    try:
        creq = CheckRequest(url=domain, lang="ru")
    except Exception:
        return JSONResponse(status_code=422, content={"error": "invalid domain"})
    url = creq.url
    dom = extract_domain(url)
    url_feats = extract_features(url)
    verdict_result, domain_info = await asyncio.gather(
        run_pipeline_internal(url, "ru"),
        check_domain_intelligence(dom, url),
    )
    from .services.security_scan import build_grade
    grade = build_grade(verdict_result, domain_info if isinstance(domain_info, dict) else None, url_feats)
    grade["domain"] = dom
    grade["checked_url"] = url
    return grade


@app.get("/scan")
async def scan_page():
    """Security-grade scanner page."""
    return HTMLResponse(SCAN_HTML, headers=_HTML_CACHE)


@app.get("/impact")
async def impact_page():
    """Economic-effect calculator — prevented fraud loss in ₸ (ДЭР economic framing)."""
    return HTMLResponse(IMPACT_HTML, headers=_HTML_CACHE)


@app.get("/screen")
async def screen_page():
    """Screenshot analysis page — Groq/Gemini Vision reads the image and verdicts it."""
    return HTMLResponse(SCREEN_HTML, headers=_HTML_CACHE)


_BADGE_MEM: dict[str, tuple[str, float]] = {}   # domain → (svg, expires)


def _badge_svg(label: str, grade: str, color: str) -> str:
    left_w, right_w = 88, 42
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{left_w+right_w}" height="24" role="img" aria-label="{label}: {grade}">'
        f'<rect rx="4" width="{left_w+right_w}" height="24" fill="#1e293b"/>'
        f'<rect rx="4" x="{left_w}" width="{right_w}" height="24" fill="{color}"/>'
        f'<rect x="{left_w}" width="4" height="24" fill="{color}"/>'
        f'<path transform="translate(6,4) scale(0.67)" d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z" fill="none" stroke="#e7ebf3" stroke-width="2"/>'
        f'<text x="{left_w//2+14}" y="16" text-anchor="middle" fill="#e7ebf3" font-family="Verdana,sans-serif" font-size="11">{label}</text>'
        f'<text x="{left_w+right_w//2}" y="16" text-anchor="middle" fill="#04121a" font-family="Verdana,sans-serif" font-size="12" font-weight="bold">{grade}</text>'
        f'</svg>'
    )


@app.get("/badge/{domain}")
async def qalqan_badge(domain: str, req: Request):
    """Embeddable SVG badge: <img src="https://.../badge/example.kz">.
    Shows the site's Qalqan security grade; cached 24h per domain."""
    from fastapi.responses import Response as _R
    dom = _to_domain(domain.removesuffix(".svg"))
    if not dom or "." not in dom or len(dom) > 100:
        return _R(_badge_svg("Qalqan", "?", "#7d8aa0"), media_type="image/svg+xml")
    hit = _BADGE_MEM.get(dom)
    if hit and hit[1] > time.time():
        return _R(hit[0], media_type="image/svg+xml",
                  headers={"Cache-Control": "public, max-age=86400"})
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="badge"):
        return _R(_badge_svg("Qalqan", "…", "#7d8aa0"), media_type="image/svg+xml")
    try:
        creq = CheckRequest(url=dom, lang="ru")
        url_feats = extract_features(creq.url)
        verdict_result, domain_info = await asyncio.gather(
            run_pipeline_internal(creq.url, "ru"),
            check_domain_intelligence(extract_domain(creq.url), creq.url),
        )
        from .services.security_scan import build_grade
        grade = build_grade(verdict_result, domain_info if isinstance(domain_info, dict) else None, url_feats)
        g = grade.get("grade", "?")
        color = {"A+": "#9ece6a", "A": "#9ece6a", "B": "#b8d68c", "C": "#e0af68",
                 "D": "#e08f68", "E": "#f7768e", "F": "#f7768e"}.get(g, "#7d8aa0")
        svg = _badge_svg("Qalqan", g, color)
        _BADGE_MEM[dom] = (svg, time.time() + 86400)
        if len(_BADGE_MEM) > 500:
            _BADGE_MEM.pop(next(iter(_BADGE_MEM)))
        return _R(svg, media_type="image/svg+xml",
                  headers={"Cache-Control": "public, max-age=86400"})
    except Exception as e:
        logger.warning(f"badge failed for {dom}: {e}")
        return _R(_badge_svg("Qalqan", "?", "#7d8aa0"), media_type="image/svg+xml")


@app.get("/batch-check")
async def batch_check_page():
    """Bulk URL screening page (banks / regulators / corporate security)."""
    return HTMLResponse(BATCH_HTML, headers=_HTML_CACHE)


_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9.-]{1,255}\.[A-Za-z]{2,24}$")


@app.get("/leak/email")
async def leak_email(email: str, req: Request):
    """Email breach lookup via XposedOrNot (free, no key). Privacy: the email is
    forwarded to the breach API only, never logged or stored by Qalqan."""
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_SCREEN, endpoint="leakemail"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    email = (email or "").strip()
    if not _EMAIL_RE.match(email):
        return JSONResponse(status_code=422, content={"error": "invalid_email"})
    try:
        from .utils.http import get_client
        r = await get_client().get(
            f"https://api.xposedornot.com/v1/check-email/{email}", timeout=8)
        if r.status_code == 404:
            return {"breached": False, "count": 0, "breaches": []}
        if r.status_code != 200:
            return JSONResponse(status_code=502, content={"error": "breach_api_unavailable"})
        data = r.json()
        raw = data.get("breaches") or []
        names = raw[0] if raw and isinstance(raw[0], list) else raw
        names = [str(b) for b in names][:20]
        return {"breached": bool(names), "count": len(names), "breaches": names}
    except Exception as e:
        logger.warning(f"leak_email lookup failed: {e}")
        return JSONResponse(status_code=502, content={"error": "breach_api_unavailable"})


@app.get("/cron/refresh-feeds")
async def cron_refresh_feeds(req: Request):
    """Force-reload OpenPhish/URLhaus feeds (daily Vercel cron — Hobby plan allows
    daily precision only; the lazy 12h-TTL reload still applies per instance,
    CRON_SECRET-gated)."""
    if not _authorize_cron(req):
        return JSONResponse(status_code=403, content={"error": "forbidden"})
    from .services.threat_db import load_threat_feeds, feed_stats
    await load_threat_feeds()
    return {"ok": True, "feeds": feed_stats()}


_PUBLIC_PAGES = ["/", "/install", "/stats", "/dashboard", "/leak", "/help",
                 "/brand", "/scan", "/impact", "/screen", "/batch-check", "/m", "/partners",
                 "/goszakup/graph"]


@app.get("/robots.txt")
async def robots():
    from fastapi.responses import PlainTextResponse
    base = os.getenv("QALQAN_API_URL", "https://qalqan-ai-nu.vercel.app")
    return PlainTextResponse(
        "User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /telegram/\n"
        f"Sitemap: {base}/sitemap.xml\n",
        headers={"Cache-Control": "public, max-age=86400"})


@app.get("/sitemap.xml")
async def sitemap():
    from fastapi.responses import Response as _Resp
    base = os.getenv("QALQAN_API_URL", "https://qalqan-ai-nu.vercel.app")
    urls = "".join(f"<url><loc>{base}{p}</loc></url>" for p in _PUBLIC_PAGES)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    return _Resp(content=xml, media_type="application/xml",
                 headers={"Cache-Control": "public, max-age=86400"})


@app.get("/kz-regions.js")
async def kz_regions_js():
    """Kazakhstan ADM1 geometry (20 regions, 2023 COD-AB) for the threat map."""
    from fastapi.responses import Response as _Resp
    from .kz_geo import KZ_GEO_JS
    return _Resp(content=KZ_GEO_JS, media_type="application/javascript",
                 headers={"Cache-Control": "public, max-age=86400, s-maxage=604800"})


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
    from .services.ml_model import ml_health
    sb_health, rd_health, ml_h = await asyncio.gather(
        supabase_health(), redis_health(), ml_health())
    return {
        "status": "ok",
        "version": "5.1.0",
        "demo_mode": DEMO_MODE,
        "api_keys_configured": f"{configured_count}/{len(key_names)}",
        "data_files_ok": f"{data_files_ok}/5",
        "whitelist_domains": len(_whitelist),
        "supabase": sb_health,
        "redis": rd_health,
        "ml_model": ml_h,
    }


@app.get("/health/check")
async def health_check_alert(req: Request):
    """Monitoring probe (cron/secret-gated): checks deps, alerts admin Telegram
    on degradation. Wire to Vercel cron or UptimeRobot."""
    if not _authorize_cron(req):
        return JSONResponse(status_code=403, content={"error": "Forbidden"})
    sb, rd = await asyncio.gather(supabase_health(), redis_health())
    problems = []
    if sb.get("status") not in ("ok", "disabled"):
        problems.append(f"Supabase: {sb.get('status')}")
    if rd.get("status") not in ("ok", "disabled"):
        problems.append(f"Redis: {rd.get('status')}")
    if not os.getenv("GROQ_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        problems.append("AI: ешқандай кілт жоқ (no AI key)")
    if problems:
        await health_alert("Деградация:\n• " + "\n• ".join(problems))
    return {"status": "degraded" if problems else "ok", "problems": problems}


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.get("/admin")
async def admin_dashboard(req: Request, key: str | None = None):
    # Rate-limit to blunt brute-force of ADMIN_SECRET (10/min per IP).
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, 10, endpoint="admin"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    admin_secret = os.getenv("ADMIN_SECRET", "")
    header_key = req.headers.get("x-admin-key", "")
    cookie_key = req.cookies.get("qadmin", "")
    provided = header_key or cookie_key or (key or "")
    # Constant-time comparison (avoids timing side-channel on the secret).
    authed = bool(admin_secret) and hmac.compare_digest(provided, admin_secret)
    if not authed:
        return HTMLResponse(
            '<html><body style="background:#0f172a;color:#ef4444;font-family:monospace;'
            'display:flex;align-items:center;justify-content:center;height:100vh;margin:0;">'
            '<div style="text-align:center"><div><svg viewBox="0 0 24 24" fill="none" stroke="#7aa2f7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:48px;height:48px"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg></div>'
            '<h1>401 — Unauthorized</h1>'
            '<p>Use <code>X-Admin-Key</code> header (preferred) or <code>?key=</code> once</p></div></body></html>',
            status_code=401,
        )

    # If authenticated via the URL query, move the secret into an httponly cookie and
    # redirect to a clean URL so it never lingers in browser history / bookmarks (P0-4).
    if key and hmac.compare_digest(key, admin_secret) and not (header_key or cookie_key):
        from fastapi.responses import RedirectResponse
        resp = RedirectResponse(url="/admin", status_code=303)
        resp.set_cookie("qadmin", admin_secret, httponly=True, secure=True,
                        samesite="lax", max_age=86400)
        return resp

    data = await get_admin_data(limit=100)
    if not data:
        data = {"reports": [], "appeals": [], "check_logs": []}

    from .pages import render_admin_page
    return HTMLResponse(render_admin_page(data))


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
    if not hmac.compare_digest(incoming, secret):
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

    # Auth is mandatory: without a configured secret this endpoint could be used to
    # re-point the bot's webhook, so refuse to run until TELEGRAM_WEBHOOK_SECRET is set.
    if not secret:
        return JSONResponse(status_code=403,
                            content={"error": "TELEGRAM_WEBHOOK_SECRET not configured"})
    caller_secret = req.query_params.get("secret", "")
    if not hmac.compare_digest(caller_secret, secret):
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
        # Also register the / command menu + Menu button (Mini App)
        from .services.bot_handler import register_bot_ui
        await register_bot_ui()
        return {"ok": data.get("ok"), "webhook_url": webhook_url,
                "ui_registered": True, "telegram_response": data}
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
    # Bounded — build_fraud_graph has O(n²) pair/cartel loops; cap inputs to
    # prevent a single huge request from pinning a worker.
    companies: list[dict] = Field(default_factory=list, max_length=300)
    tenders: list[dict] = Field(default_factory=list, max_length=1000)


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
    return HTMLResponse(GRAPH_HTML, headers=_HTML_CACHE)


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
        "federated_feed": {"url": "/feed/federated",
                           "contribute": "POST /v1/contribute (X-API-Key)"},
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


@app.get("/feed/federated")
async def federated_feed():
    """Federated KZ threat feed: Qalqan-curated + live partner/CERT contributions.
    The data-network-effect artifact — grows as institutions contribute."""
    contributed = await get_federated_feed() or []
    base = _build_kz_feed()
    return {
        "name": "Qalqan AI — Federated Kazakhstan Threat Feed",
        "license": "CC-BY-4.0",
        "sources": ["qalqan_curated", "partner_contributions", "openphish/urlhaus (live ingest)"],
        "curated_count": base["count"],
        "contributed_count": len(contributed),
        "contributed": contributed[:200],
        "curated": base["entries"][:200],
    }


# ── Partner (B2G) API — banks / regulators via X-API-Key ─────────────────────


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


class ContributeRequest(BaseModel):
    indicator: str = Field(..., max_length=2048)     # domain / URL
    type: str = Field(default="phishing", max_length=32)
    evidence: str = Field(default="", max_length=500)


@app.post("/v1/contribute")
async def api_v1_contribute(request: ContributeRequest, req: Request, background_tasks: BackgroundTasks):
    """Federated threat-sharing: a partner/CERT contributes a threat indicator.
    Feeds the crowd-intelligence store and the federated feed."""
    key, partner = _partner_auth(req)
    if not partner:
        return JSONResponse(status_code=401, content={"error": "Invalid or missing X-API-Key"})
    if not await check_rate_limit(key_id(key), _partner_limit(key), endpoint="apicontrib"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    domain = extract_domain(request.indicator) or request.indicator.strip().lower()
    background_tasks.add_task(
        log_report, domain=domain, url=request.indicator,
        category=f"federated:{request.type}",
        comment=f"[{partner}] {request.evidence}"[:500], lang="en",
        reporter_ip=f"partner:{partner}")
    community = await get_community_stats(domain)
    return {"accepted": True, "partner": partner, "indicator": domain,
            "type": request.type, "community": community}


@app.post("/v1/phone")
async def api_v1_phone(request: PhoneRequest, req: Request):
    """Partner KZ phone-scam check (partner rate tier)."""
    key, partner = _partner_auth(req)
    if not partner:
        return JSONResponse(status_code=401, content={"error": "Invalid or missing X-API-Key"})
    if not await check_rate_limit(key_id(key), _partner_limit(key), endpoint="apiphone"):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    from .services.phone_sms import analyze_phone
    return {"partner": partner, "result": analyze_phone(request.phone, request.lang)}


@app.get("/partners")
async def partners_docs():
    from fastapi.responses import HTMLResponse
    return HTMLResponse(PARTNERS_HTML, headers=_HTML_CACHE)


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
