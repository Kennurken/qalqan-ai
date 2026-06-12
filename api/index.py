# Qalqan AI v5.1
# Бас API: 6-деңгейлі қауіп детекция pipeline + ML features + XAI
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
from .services.kz_intel import check_kz_social_engineering, check_kz_impersonation_url, check_gambling_domain
from .services.domain_intel import check_domain_intelligence
from .services.goszakup import check_goszakup_url, analyse_procurement_data, is_goszakup_url
from .services.url_features import extract_features
from .services.explainer import generate_explanation
from .services.scoring import calculate_final_verdict
from .utils.cache import url_hash, get_cached, set_cached, clear_cache
from .evaluation.benchmark import run_benchmark
from .utils.telegram import send_appeal, send_report, notify_block
from .utils.i18n import t
from .utils.supabase import log_report, log_appeal, log_check, check_health as supabase_health

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

def _cors_origin_allowed(origin: str) -> bool:
    if not origin:
        return False
    # Allow all chrome-extension:// origins (user's own extension)
    if origin.startswith("chrome-extension://"):
        return True
    return origin in _ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # FastAPI CORS doesn't support prefix match —
    allow_methods=["GET", "POST", "OPTIONS"],   # we enforce origin in middleware below
    allow_headers=["Content-Type"],
)

# --- Rate Limiting (in-memory, IP-based) ---
_rate_limits: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT_CHECK = 30    # /check: 30 req/min
RATE_LIMIT_SCREEN = 5    # /analyze-screen: 5 req/min (AI vision — expensive)
RATE_LIMIT_APPEAL = 5    # /appeal: 5 req/min
RATE_LIMIT_REPORT = 3    # /report: 3 req/min (separate from appeal — fix #4)
RATE_WINDOW = 60         # 60 seconds


# --- Origin enforcement middleware (CORS fix #1) ---
@app.middleware("http")
async def enforce_origin(request: Request, call_next):
    """Block browser requests from non-extension origins. CLI/curl (no Origin) always allowed."""
    origin = request.headers.get("origin", "")
    if origin and not _cors_origin_allowed(origin):
        logger.warning(f"Blocked request from disallowed origin: {origin}")
        return JSONResponse(status_code=403, content={"error": "Origin not allowed"})
    return await call_next(request)


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
    image_base64: str = Field(..., max_length=5_500_000)  # ~4MB base64 (was 7MB — tightened)
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
async def root():
    return {
        "status": "online",
        "name": "Qalqan AI",
        "version": "5.1.0",
        "pipeline": "6-tier: cache → ML_features → pyramid/kz/gambling → databases → domain_intel → AI + XAI",
        "databases": ["PhishTank", "SafeBrowsing", "URLhaus", "OpenPhish", "RDAP", "SSL", "KZ_Gambling"],
        "ml_features": "30+ URL lexical features, homoglyph detection, brand similarity",
        "ai_providers": {
            "groq": "configured" if os.getenv("GROQ_API_KEY") else "missing",
            "gemini": "configured" if os.getenv("GEMINI_API_KEY") else "missing"
        }
    }


# --- НЕГІЗГІ ТЕКСЕРУ: 6-деңгейлі pipeline ---
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

    # --- Tier 1.7: KZ Brand Impersonation (fast, offline, very high precision) ---
    kz_impersonation_hit = check_kz_impersonation_url(domain)
    if kz_impersonation_hit:
        result = calculate_final_verdict([], kz_impersonation_hit, None, url_features=url_feats, lang=lang)
        result["explanation"] = generate_explanation(url_feats, None, [], None, None, result["threat_score"])
        result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": "kz_impersonation"}
        set_cached(key, result)
        return result

    # --- Tier 1.8: Gambling / unlicensed bookmaker (KZ banned sites) ---
    gambling_hit = check_gambling_domain(domain)
    if gambling_hit:
        result = calculate_final_verdict([], gambling_hit, None, url_features=url_feats, lang=lang)
        result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": "gambling_list"}
        set_cached(key, result)
        return result

    # --- Tier 1.9: Госзакупки fraud detection (goszakup.gov.kz URLs) ---
    if is_goszakup_url(url):
        goszakup_hit = await check_goszakup_url(url)
        if goszakup_hit and goszakup_hit.get("verdict") in ("DANGEROUS", "SUSPICIOUS"):
            result = calculate_final_verdict([goszakup_hit], None, None, url_features=url_feats, lang=lang)
            result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": "goszakup_fraud"}
            result["red_flags"] = goszakup_hit.get("red_flags", [])
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
        if domain_info and domain_info.get("domain_details"):
            result["domain_details"] = domain_info["domain_details"]
        set_cached(key, result)
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
                                                  None if ai_failed else ai_result, None, result["threat_score"])
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
    set_cached(key, result)
    logger.info(f"CHECK {domain} → {result['verdict']} ({result['threat_score']}) via {result['source']} [{result['metadata']['processing_time_ms']}ms]")

    # Telegram notification for dangerous sites
    if result.get("verdict") == "DANGEROUS":
        asyncio.create_task(notify_block(url, result["verdict"], result["threat_score"], result.get("source", "")))

    # Supabase: async log (fire-and-forget, never blocks response)
    asyncio.create_task(log_check(
        domain=domain,
        verdict=result["verdict"],
        score=result["threat_score"],
        top_source=result.get("source", "unknown"),
        ai_used=not ai_failed,
        ai_skipped=ai_failed,
        latency_ms=result["metadata"]["processing_time_ms"],
    ))

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


# --- BATCH ТЕКСЕРУ (max 15 URL) ---
@app.post("/batch")
async def check_batch(request: BatchRequest, req: Request):
    """Check up to 15 URLs in parallel. Returns list of verdicts."""
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"check:{client_ip}", RATE_LIMIT_CHECK):
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

            kz_impersonation_hit = check_kz_impersonation_url(domain)
            if kz_impersonation_hit:
                r = calculate_final_verdict([], kz_impersonation_hit, None, url_features=url_feats, lang=lang)
                set_cached(key, r)
                return {**r, "url": url}

            gambling_hit = check_gambling_domain(domain)
            if gambling_hit:
                r = calculate_final_verdict([], gambling_hit, None, url_features=url_feats, lang=lang)
                set_cached(key, r)
                return {**r, "url": url}

            db_results, domain_info = await asyncio.gather(
                check_all_databases(url),
                check_domain_intelligence(domain, url)
            )
            ai_result = await analyze_url(url, context=url_feats)
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
    # Fix #3: separate rate limit key + lower limit (5/min, not shared with /check)
    if not _check_rate_limit(f"screen:{client_ip}", RATE_LIMIT_SCREEN):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded. Max 5 screenshot analyses per minute."})

    result = await analyze_screenshot(request.image_base64)
    return calculate_final_verdict([], result, None, lang=request.lang)


# --- АПЕЛЛЯЦИЯ ---
@app.post("/appeal")
async def appeal(request: AppealRequest, req: Request):
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"appeal:{client_ip}", RATE_LIMIT_APPEAL):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    result = await send_appeal(request.url, request.reason)

    # Supabase: persist appeal (fire-and-forget)
    domain = extract_domain(request.url)
    asyncio.create_task(log_appeal(
        domain=domain,
        verdict_received=getattr(request, "verdict", None),
        reason=request.reason,
    ))

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
async def report_site(request: ReportRequest, req: Request):
    client_ip = req.client.host if req.client else "unknown"
    # Fix #4: separate rate limit key (was "appeal:", now "report:")
    if not _check_rate_limit(f"report:{client_ip}", RATE_LIMIT_REPORT):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded. Max 3 reports per minute."})

    domain = extract_domain(request.url)
    reports = _load_reports()
    if domain not in reports:
        reports[domain] = {"count": 0, "types": [], "unique_ips": [], "first_report": time.time()}

    reports[domain]["count"] += 1
    reports[domain]["types"].append(request.threat_type)
    # Fix #9: track unique IPs — require reports from 10 unique IPs before auto-block
    # This prevents a single attacker from mass-reporting a legitimate domain
    unique_ips: list = reports[domain].setdefault("unique_ips", [])
    if client_ip not in unique_ips:
        unique_ips.append(client_ip)

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
    asyncio.create_task(log_report(
        domain=domain,
        url=request.url,
        category=request.threat_type,
        comment=request.note,
        lang=getattr(request, "lang", "ru"),
        reporter_ip=client_ip,
    ))

    return result


# --- СТАТИСТИКА ---
@app.get("/stats")
async def get_stats():
    from .utils.cache import _cache
    reports = _load_reports()
    return {
        "total_reported_domains": len(reports),
        "auto_blocked": sum(1 for r in reports.values() if r["count"] >= 10 and len(r.get("unique_ips", [])) >= 3),
        "whitelist_size": len(_whitelist),
        "cache_entries": len(_cache),
        "demo_mode": DEMO_MODE,
        "version": "5.1.0",
        "features": [
            "goszakup_fraud_detection",
            "telegram_bot",
            "kz_threat_report",
            "6tier_pipeline",
            "xai_explainer",
        ],
        "report_url": "/report/generate",
    }


# --- ТРЕНДЫ (crowd-sourced) ---
@app.get("/trends")
async def get_trends():
    """Top reported threat domains and types — crowd intelligence."""
    reports = _load_reports()
    if not reports:
        return {"top_domains": [], "threat_type_counts": {}, "total_reports": 0}

    # Top 10 most reported domains
    sorted_domains = sorted(reports.items(), key=lambda x: x[1]["count"], reverse=True)
    top_domains = [
        {
            "domain": domain,
            "reports": data["count"],
            "types": list(set(data.get("types", []))),
            "auto_blocked": data["count"] >= 5
        }
        for domain, data in sorted_domains[:10]
    ]

    # Threat type distribution
    type_counts: dict[str, int] = {}
    for data in reports.values():
        for t_type in data.get("types", []):
            type_counts[t_type] = type_counts.get(t_type, 0) + 1

    total_reports = sum(d["count"] for d in reports.values())

    return {
        "top_domains": top_domains,
        "threat_type_counts": dict(sorted(type_counts.items(), key=lambda x: x[1], reverse=True)),
        "total_reports": total_reports,
        "unique_domains_reported": len(reports)
    }


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
    sb_health = await supabase_health()
    return {
        "status": "ok",
        "version": "5.1.0",
        "demo_mode": DEMO_MODE,
        "api_keys_configured": f"{configured_count}/{len(key_names)}",
        "data_files_ok": f"{data_files_ok}/5",
        "whitelist_domains": len(_whitelist),
        "supabase": sb_health,
    }


# ============================================================
# RESEARCH API ENDPOINTS (doctoral-grade)
# ============================================================

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
    kz_hit = check_kz_impersonation_url(domain)
    gambling_hit = check_gambling_domain(domain)
    # Fix #8: pass url_feats context to AI for better accuracy (same as /check endpoint)
    db_results, domain_info, ai_result = await asyncio.gather(
        check_all_databases(url),
        check_domain_intelligence(domain, url),
        analyze_url(url, context=url_feats)
    )

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
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"check:{client_ip}", 5):  # max 5 evals/min
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    results = await run_benchmark()
    return results


# ── Telegram Bot Webhook ──────────────────────────────────────────────────────

@app.post("/telegram/webhook")
async def telegram_webhook(req: Request):
    """Receive Telegram Bot API updates via webhook.
    Security: verified by TELEGRAM_WEBHOOK_SECRET header token.
    """
    # Verify secret token (set when registering webhook via setWebhook)
    secret = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
    if secret:
        incoming = req.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if incoming != secret:
            logger.warning("Telegram webhook: invalid secret token")
            return JSONResponse(status_code=403, content={"error": "Forbidden"})

    try:
        update = await req.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON"})

    # Fire-and-forget dispatch (don't await — respond 200 to Telegram immediately)
    asyncio.create_task(_dispatch_update(update))
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

    payload: dict = {"url": webhook_url, "allowed_updates": ["message", "inline_query"]}
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
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"check:{client_ip}", RATE_LIMIT_CHECK):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    data = request.model_dump(exclude_none=True)
    result = await analyse_procurement_data(data)
    logger.info(f"GOSZAKUP {data.get('tender_number','?')} → {result['verdict']} ({result['threat_score']})")
    return result


@app.get("/goszakup/check/{tender_number}")
async def goszakup_check_tender(tender_number: str, req: Request):
    """Fetch tender from goszakup.gov.kz by number and run fraud analysis."""
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"check:{client_ip}", RATE_LIMIT_CHECK):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

    from .services.goszakup import check_tender_by_number
    result = await check_tender_by_number(tender_number)
    return result


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
    client_ip = req.client.host if req.client else "unknown"
    if not _check_rate_limit(f"report:{client_ip}", 3):   # max 3/min
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
