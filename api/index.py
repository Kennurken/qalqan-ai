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
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse
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
from .utils.cache import url_hash, get_cached, set_cached, clear_cache, check_rate_limit, check_health as redis_health
from .evaluation.benchmark import run_benchmark
from .utils.telegram import send_appeal, send_report, notify_block
from .utils.i18n import t
from .utils.supabase import log_report, log_appeal, log_check, get_trends as supabase_trends, check_health as supabase_health, get_admin_data

_PRIVATE_IP_RE = re.compile(
    r"^(localhost|127\.|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|0\.0\.0\.0|::1)",
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
    return HTMLResponse(content=_LANDING_HTML)


_LANDING_HTML = """<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Qalqan AI — Қазақстандық киберқауіпсіздік</title>
<meta name="description" content="Qalqan AI — AI-powered cybersecurity extension protecting Kazakhstani users from phishing, scams, gambling and pyramid schemes.">
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--cyan:#00d4ff;--cyan2:#00b8d9;--green:#22c55e;--red:#ef4444;--amber:#f59e0b;--bg:#0a0e1a;--bg2:#0f1629;--card:#131d35;--border:#1e2d4a;--text:#e2e8f0;--muted:#64748b}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;overflow-x:hidden}
a{color:var(--cyan);text-decoration:none}
/* SCANLINE */
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,212,255,.015) 2px,rgba(0,212,255,.015) 4px);pointer-events:none;z-index:0}
/* NAV */
nav{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(10,14,26,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:0 24px;height:56px;display:flex;align-items:center;justify-content:space-between}
.nav-logo{display:flex;align-items:center;gap:10px;font-weight:700;font-size:18px;color:var(--cyan)}
.nav-logo svg{width:28px;height:28px}
.nav-links{display:flex;gap:20px;font-size:14px}
.nav-links a{color:var(--muted);transition:color .2s}
.nav-links a:hover{color:var(--cyan)}
.nav-cta{background:var(--cyan);color:#0a0e1a;padding:7px 16px;border-radius:6px;font-weight:600;font-size:13px;transition:opacity .2s}
.nav-cta:hover{opacity:.85}
/* HERO */
.hero{position:relative;min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:100px 24px 60px}
.hero-glow{position:absolute;top:20%;left:50%;transform:translateX(-50%);width:600px;height:600px;background:radial-gradient(ellipse,rgba(0,212,255,.12) 0%,transparent 70%);pointer-events:none}
.hero-badge{display:inline-flex;align-items:center;gap:6px;background:rgba(0,212,255,.1);border:1px solid rgba(0,212,255,.25);border-radius:20px;padding:5px 14px;font-size:12px;color:var(--cyan);margin-bottom:24px;letter-spacing:.5px}
.hero-badge span{width:6px;height:6px;border-radius:50%;background:var(--cyan);animation:pulse 2s infinite}
h1{font-size:clamp(36px,6vw,72px);font-weight:800;line-height:1.1;margin-bottom:20px;background:linear-gradient(135deg,#fff 30%,var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-sub{font-size:clamp(16px,2vw,20px);color:var(--muted);max-width:600px;margin:0 auto 40px;line-height:1.6}
/* CHECKER */
.checker{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:28px;max-width:600px;margin:0 auto;position:relative}
.checker-title{font-size:13px;color:var(--muted);margin-bottom:14px;text-align:left;text-transform:uppercase;letter-spacing:1px}
.checker-row{display:flex;gap:10px}
.checker-input{flex:1;background:#0a0e1a;border:1px solid var(--border);border-radius:8px;padding:12px 16px;color:var(--text);font-size:15px;outline:none;transition:border-color .2s}
.checker-input:focus{border-color:var(--cyan)}
.checker-input::placeholder{color:var(--muted)}
.checker-btn{background:var(--cyan);color:#0a0e1a;border:none;border-radius:8px;padding:12px 22px;font-weight:700;font-size:14px;cursor:pointer;transition:opacity .2s;white-space:nowrap}
.checker-btn:hover{opacity:.85}
.checker-btn:disabled{opacity:.5;cursor:not-allowed}
.result-box{margin-top:16px;padding:16px;border-radius:10px;border:1px solid;display:none;text-align:left;animation:fadeUp .2s ease}
.result-box.safe{border-color:rgba(34,197,94,.3);background:rgba(34,197,94,.06)}
.result-box.danger{border-color:rgba(239,68,68,.3);background:rgba(239,68,68,.06)}
.result-box.suspicious{border-color:rgba(245,158,11,.3);background:rgba(245,158,11,.06)}
.result-verdict{font-size:18px;font-weight:700;margin-bottom:4px}
.result-detail{font-size:13px;color:var(--muted);line-height:1.5}
/* STATS */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;max-width:900px;margin:60px auto 0;padding:0 24px}
.stat-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px;text-align:center}
.stat-num{font-size:32px;font-weight:800;color:var(--cyan);font-variant-numeric:tabular-nums}
.stat-label{font-size:12px;color:var(--muted);margin-top:4px;text-transform:uppercase;letter-spacing:.5px}
/* FEATURES */
.section{padding:80px 24px;max-width:1100px;margin:0 auto}
.section-label{font-size:12px;color:var(--cyan);text-transform:uppercase;letter-spacing:2px;margin-bottom:12px}
.section-title{font-size:clamp(24px,4vw,40px);font-weight:700;margin-bottom:16px}
.section-sub{color:var(--muted);font-size:16px;max-width:500px;line-height:1.6}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:48px}
.feat-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:24px;transition:border-color .2s,transform .2s}
.feat-card:hover{border-color:rgba(0,212,255,.35);transform:translateY(-2px)}
.feat-icon{width:40px;height:40px;border-radius:10px;background:rgba(0,212,255,.1);display:flex;align-items:center;justify-content:center;margin-bottom:16px}
.feat-icon svg{width:20px;height:20px;stroke:var(--cyan);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.feat-title{font-size:15px;font-weight:600;margin-bottom:8px}
.feat-desc{font-size:13px;color:var(--muted);line-height:1.6}
/* PIPELINE */
.pipeline{background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:60px 24px}
.pipeline-inner{max-width:900px;margin:0 auto}
.pipeline-steps{display:flex;flex-wrap:wrap;gap:0;margin-top:40px}
.pipe-step{flex:1;min-width:120px;position:relative;padding:20px 16px;text-align:center}
.pipe-step:not(:last-child)::after{content:'→';position:absolute;right:-8px;top:50%;transform:translateY(-50%);color:var(--cyan);font-size:18px}
.pipe-num{width:32px;height:32px;border-radius:50%;border:2px solid var(--cyan);color:var(--cyan);font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center;margin:0 auto 10px}
.pipe-name{font-size:12px;color:var(--muted);font-weight:500}
/* TELEGRAM */
.tg-section{padding:80px 24px;text-align:center}
.tg-card{max-width:500px;margin:0 auto;background:var(--card);border:1px solid var(--border);border-radius:20px;padding:40px}
.tg-icon{width:60px;height:60px;background:rgba(0,212,255,.1);border-radius:16px;display:flex;align-items:center;justify-content:center;margin:0 auto 20px}
.tg-icon svg{width:30px;height:30px;fill:var(--cyan)}
.tg-title{font-size:22px;font-weight:700;margin-bottom:10px}
.tg-sub{color:var(--muted);font-size:14px;line-height:1.6;margin-bottom:24px}
.tg-btn{display:inline-flex;align-items:center;gap:8px;background:var(--cyan);color:#0a0e1a;padding:13px 28px;border-radius:10px;font-weight:700;font-size:15px;transition:opacity .2s}
.tg-btn:hover{opacity:.85;color:#0a0e1a}
/* TECH STACK */
.stack-grid{display:flex;flex-wrap:wrap;gap:10px;margin-top:32px}
.stack-tag{background:var(--card);border:1px solid var(--border);border-radius:6px;padding:6px 14px;font-size:13px;color:var(--muted);font-family:monospace}
/* FOOTER */
footer{background:var(--bg2);border-top:1px solid var(--border);padding:40px 24px;text-align:center}
.footer-logo{font-size:20px;font-weight:700;color:var(--cyan);margin-bottom:8px}
.footer-sub{font-size:13px;color:var(--muted);margin-bottom:16px}
.footer-links{display:flex;justify-content:center;gap:20px;font-size:13px;flex-wrap:wrap}
/* ANIMATIONS */
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
@keyframes fadeUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
/* RESPONSIVE */
@media(max-width:600px){
  .nav-links{display:none}
  .checker-row{flex-direction:column}
  .pipe-step:not(:last-child)::after{display:none}
}
</style>
</head>
<body>

<!-- NAV -->
<nav>
  <div class="nav-logo">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      <polyline points="9 12 11 14 15 10"/>
    </svg>
    Qalqan AI
  </div>
  <div class="nav-links">
    <a href="#features">Функции</a>
    <a href="#pipeline">Pipeline</a>
    <a href="#telegram">Telegram</a>
    <a href="#tech">Технологии</a>
  </div>
  <a class="nav-cta" href="https://github.com/Kennurken/qalqan-ai" target="_blank">GitHub</a>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-glow"></div>
  <div style="position:relative;z-index:1">
    <div class="hero-badge"><span></span>v5.1.0 · Қазақстан үшін</div>
    <h1>Фишингтен<br>AI Қорғанысы</h1>
    <p class="hero-sub">Qalqan AI — Chrome кеңейтімі, ол барған сайын автоматты тексереді. Фишинг, пирамидалар, гемблинг — бет жүктелмей бұрын бұғаттайды.</p>

    <!-- LIVE CHECKER -->
    <div class="checker">
      <div class="checker-title">Сайтты тексеру / Проверить сайт</div>
      <div class="checker-row">
        <input class="checker-input" id="urlInput" type="text" placeholder="kaspi-bonus123.kz немесе https://..." autocomplete="off">
        <button class="checker-btn" id="checkBtn" onclick="checkUrl()">Тексеру</button>
      </div>
      <div class="result-box" id="resultBox">
        <div class="result-verdict" id="resultVerdict"></div>
        <div class="result-detail" id="resultDetail"></div>
      </div>
    </div>

    <!-- STATS -->
    <div class="stats" id="statsRow">
      <div class="stat-card"><div class="stat-num" id="statChecked">—</div><div class="stat-label">Тексерілді</div></div>
      <div class="stat-card"><div class="stat-num" id="statBlocked">—</div><div class="stat-label">Бұғатталды</div></div>
      <div class="stat-card"><div class="stat-num" id="statDomains">390+</div><div class="stat-label">Офлайн база</div></div>
      <div class="stat-card"><div class="stat-num">7</div><div class="stat-label">Анықтау деңгейі</div></div>
    </div>
  </div>
</section>

<!-- FEATURES -->
<section class="section" id="features">
  <div class="section-label">Функционал</div>
  <div class="section-title">Не қорғайды?</div>
  <p class="section-sub">7 деңгейлі pipeline — 1 мс кеш-тексеруден AI анализіне дейін</p>

  <div class="features-grid">
    <div class="feat-card">
      <div class="feat-icon"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg></div>
      <div class="feat-title">Фишинг сайттары</div>
      <div class="feat-desc">Kaspi, eGov, Halyk Bank клондарын анықтайды. Беттің жүктелуіне дейін бұғаттайды.</div>
    </div>
    <div class="feat-card">
      <div class="feat-icon"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>
      <div class="feat-title">Қаржылық пирамидалар</div>
      <div class="feat-desc">166+ белгілі пирамида схемасы базасы. Finiko, МММ, HYIP сайттарын автоматты анықтайды.</div>
    </div>
    <div class="feat-card">
      <div class="feat-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg></div>
      <div class="feat-title">Нелегал гемблинг</div>
      <div class="feat-desc">80+ ҚР-да тыйым салынған сайт. 1xbet, Mostbet, Pin-Up — браузерде ашылмайды.</div>
    </div>
    <div class="feat-card">
      <div class="feat-icon"><svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div>
      <div class="feat-title">Скриншот анализі</div>
      <div class="feat-desc">Vision AI арқылы бет скриншотын тексереді. Жасырын алаяқтық элементтерін анықтайды.</div>
    </div>
    <div class="feat-card">
      <div class="feat-icon"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div>
      <div class="feat-title">SMS / Хабарлама тексеру</div>
      <div class="feat-desc">Алынған SMS немесе хабарламадағы алаяқтық сілтемелерді AI арқылы анализдейді.</div>
    </div>
    <div class="feat-card">
      <div class="feat-icon"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
      <div class="feat-title">Goszakup тендер тексеру</div>
      <div class="feat-desc">goszakup.gov.kz тендерлерінде алаяқтық белгілерін 10 ереже бойынша анықтайды.</div>
    </div>
  </div>
</section>

<!-- PIPELINE -->
<section class="pipeline" id="pipeline">
  <div class="pipeline-inner">
    <div class="section-label">Архитектура</div>
    <div class="section-title">7-деңгейлі анықтау</div>
    <div class="pipeline-steps">
      <div class="pipe-step"><div class="pipe-num">1</div><div class="pipe-name">Ақ тізім</div></div>
      <div class="pipe-step"><div class="pipe-num">2</div><div class="pipe-name">Redis кэш</div></div>
      <div class="pipe-step"><div class="pipe-num">3</div><div class="pipe-name">Офлайн DB</div></div>
      <div class="pipe-step"><div class="pipe-num">4</div><div class="pipe-name">KZ Intel</div></div>
      <div class="pipe-step"><div class="pipe-num">5</div><div class="pipe-name">Сыртқы DB</div></div>
      <div class="pipe-step"><div class="pipe-num">6</div><div class="pipe-name">ML модель</div></div>
      <div class="pipe-step"><div class="pipe-num">7</div><div class="pipe-name">Groq / Gemini AI</div></div>
    </div>
  </div>
</section>

<!-- TELEGRAM -->
<section class="tg-section" id="telegram">
  <div class="tg-card">
    <div class="tg-icon">
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12L7.26 13.561l-2.94-.916c-.64-.203-.654-.64.135-.954l11.566-4.461c.537-.194 1.006.131.873.991z"/>
      </svg>
    </div>
    <div class="tg-title">Telegram Bot</div>
    <div class="tg-sub">Telegram арқылы кез-келген сілтемені тексер. Пәрмендер: /check, /report, /stats</div>
    <a class="tg-btn" href="https://t.me/QalqanAI_bot" target="_blank">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="#0a0e1a"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12L7.26 13.561l-2.94-.916c-.64-.203-.654-.64.135-.954l11.566-4.461c.537-.194 1.006.131.873.991z"/></svg>
      @QalqanAI_bot ашу
    </a>
  </div>
</section>

<!-- TECH STACK -->
<section class="section" id="tech">
  <div class="section-label">Технологиялар</div>
  <div class="section-title">Технологиялық стек</div>
  <div class="stack-grid">
    <span class="stack-tag">Python 3.11</span>
    <span class="stack-tag">FastAPI</span>
    <span class="stack-tag">React 19</span>
    <span class="stack-tag">Chrome MV3</span>
    <span class="stack-tag">Groq llama-3.3-70b</span>
    <span class="stack-tag">Gemini 2.5-flash</span>
    <span class="stack-tag">XLM-RoBERTa</span>
    <span class="stack-tag">Upstash Redis</span>
    <span class="stack-tag">Supabase / PostgreSQL</span>
    <span class="stack-tag">Vercel Serverless</span>
    <span class="stack-tag">PhishTank API</span>
    <span class="stack-tag">Google Safe Browsing</span>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-logo">🛡 Qalqan AI</div>
  <div class="footer-sub">Қазақстандық пайдаланушыларды цифрлық қауіптерден қорғау · v5.1.0</div>
  <div class="footer-links">
    <a href="https://github.com/Kennurken/qalqan-ai" target="_blank">GitHub</a>
    <a href="/docs">API Docs</a>
    <a href="/stats">Statistics</a>
    <a href="/health">Health</a>
  </div>
  <div style="margin-top:16px;font-size:12px;color:var(--muted)">
    Разработчик: Қыдырбек Елдос Нүркенұлы · Кызылординский университет имени Коркыт ата<br>
    ДЭР по Кызылординской области · 2026
  </div>
</footer>

<script>
async function checkUrl() {
  const input = document.getElementById('urlInput');
  const btn = document.getElementById('checkBtn');
  const box = document.getElementById('resultBox');
  const verdict = document.getElementById('resultVerdict');
  const detail = document.getElementById('resultDetail');

  let url = input.value.trim();
  if (!url) return;
  if (!url.startsWith('http')) url = 'https://' + url;

  btn.disabled = true;
  btn.textContent = '...';
  box.style.display = 'none';

  try {
    const res = await fetch('/check', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({url, lang:'ru'})
    });
    const data = await res.json();

    box.className = 'result-box';
    const v = data.verdict || 'UNKNOWN';
    const score = data.threat_score || 0;

    if (v === 'SAFE') {
      box.classList.add('safe');
      verdict.textContent = '✓ БЕЗОПАСНО (' + score + '/100)';
      verdict.style.color = '#22c55e';
    } else if (v === 'DANGEROUS') {
      box.classList.add('danger');
      verdict.textContent = '✗ ОПАСНО (' + score + '/100)';
      verdict.style.color = '#ef4444';
    } else {
      box.classList.add('suspicious');
      verdict.textContent = '⚠ ПОДОЗРИТЕЛЬНО (' + score + '/100)';
      verdict.style.color = '#f59e0b';
    }

    detail.textContent = data.detail_ru || data.detail || data.detail_kk || '';
    box.style.display = 'block';
  } catch(e) {
    box.className = 'result-box suspicious';
    box.style.display = 'block';
    verdict.textContent = 'Ошибка соединения';
    verdict.style.color = '#f59e0b';
    detail.textContent = e.message;
  }

  btn.disabled = false;
  btn.textContent = 'Тексеру';
}

document.getElementById('urlInput').addEventListener('keydown', e => {
  if (e.key === 'Enter') checkUrl();
});

// Load stats
async function loadStats() {
  try {
    const res = await fetch('/stats');
    const data = await res.json();
    const t = data.today || {};
    const el = id => document.getElementById(id);
    if (t.total_checks) el('statChecked').textContent = t.total_checks.toLocaleString();
    if (t.dangerous_blocked) el('statBlocked').textContent = t.dangerous_blocked.toLocaleString();
  } catch {}
}
loadStats();
</script>
</body>
</html>"""


# --- НЕГІЗГІ ТЕКСЕРУ: 6-деңгейлі pipeline ---
@app.post("/check")
async def check_site(request: CheckRequest, req: Request, background_tasks: BackgroundTasks):
    # Rate limit
    client_ip = _get_client_ip(req)
    if not await check_rate_limit(client_ip, RATE_LIMIT_CHECK, endpoint="check"):
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
        result = calculate_final_verdict([], kz_impersonation_hit, None, url_features=url_feats, lang=lang)
        result["explanation"] = generate_explanation(url_feats, None, [], None, None, result["threat_score"], lang=lang)
        result["metadata"] = {"processing_time_ms": int((time.time() - start_time) * 1000), "tier_hit": "kz_impersonation"}
        await set_cached(key, result)
        return result

    # --- Tier 1.8: Gambling / unlicensed bookmaker (KZ banned sites) ---
    gambling_hit = check_gambling_domain(domain)
    if gambling_hit:
        result = calculate_final_verdict([], gambling_hit, None, url_features=url_feats, lang=lang)
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

    # --- Tier 2 + 2.5: Databases AND domain intel in parallel ---
    try:
        _t2 = await asyncio.gather(
            check_all_databases(url),
            check_domain_intelligence(domain, url),
            return_exceptions=True,
        )
        db_results = _t2[0] if isinstance(_t2[0], list) else []
        domain_info = _t2[1] if isinstance(_t2[1], dict) else None
        if isinstance(_t2[0], BaseException):
            logger.error(f"check_all_databases raised: {type(_t2[0]).__name__}: {_t2[0]}")
        if isinstance(_t2[1], BaseException):
            logger.error(f"check_domain_intelligence raised: {type(_t2[1]).__name__}: {_t2[1]}")
    except BaseException as e:
        logger.error(f"Tier2 gather failed: {type(e).__name__}: {e}")
        db_results, domain_info = [], None

    # Combine DB results
    all_db = db_results + ([domain_info] if domain_info else [])

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
    background_tasks.add_task(
        log_check,
        domain=domain,
        verdict=result["verdict"],
        score=result["threat_score"],
        top_source=result.get("source", "unknown"),
        ai_used=not ai_failed,
        ai_skipped=ai_failed,
        latency_ms=result["metadata"]["processing_time_ms"],
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


# --- СТАТИСТИКА ---
@app.get("/stats")
async def get_stats():
    from .utils.cache import _mem
    reports = _load_reports()
    return {
        "total_reported_domains": len(reports),
        "auto_blocked": sum(1 for r in reports.values() if r["count"] >= 10 and len(r.get("unique_ips", [])) >= 3),
        "whitelist_size": len(_whitelist),
        "cache_entries": len(_mem),
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
async def admin_dashboard(key: str | None = None):
    admin_secret = os.getenv("ADMIN_SECRET", "")
    if not admin_secret or key != admin_secret:
        return HTMLResponse(
            '<html><body style="background:#0f172a;color:#ef4444;font-family:monospace;'
            'display:flex;align-items:center;justify-content:center;height:100vh;margin:0;">'
            '<div style="text-align:center"><div style="font-size:48px">🛡️</div>'
            '<h1>401 — Unauthorized</h1>'
            '<p>Provide ?key=ADMIN_SECRET</p></div></body></html>',
            status_code=401,
        )

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
