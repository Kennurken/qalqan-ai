# клауд Елдоса N1 — Qalqan AI v3.0
# Бас API: 3-деңгейлі қауіп детекция pipeline
# Tier 0: Whitelist + Cache → Tier 1: Pyramid + Blacklist → Tier 2: External DBs → Tier 3: Gemini AI

import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .services.threat_db import check_all_databases, extract_domain
from .services.ai_analyzer import analyze_url, analyze_text, analyze_screenshot
from .services.pyramid_detector import check_pyramid_domain, check_local_blacklist
from .services.scoring import calculate_final_verdict
from .utils.cache import url_hash, get_cached, set_cached
from .utils.telegram import send_appeal, send_report
from .utils.i18n import t

app = FastAPI(title="Qalqan AI", version="3.0.0",
              description="AI-powered cybersecurity platform — қазақстандық киберқорғаныс")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Whitelist жүктеу ---
_data_dir = os.path.join(os.path.dirname(__file__), "data")
_whitelist: set[str] = set()

try:
    with open(os.path.join(_data_dir, "whitelist.json"), "r", encoding="utf-8") as f:
        _whitelist = set(json.load(f).get("trusted_domains", []))
except FileNotFoundError:
    pass


# --- Деректер модельдері ---
class CheckRequest(BaseModel):
    url: str
    lang: str = "kk"

class TextCheckRequest(BaseModel):
    text: str
    lang: str = "kk"

class ScreenRequest(BaseModel):
    image_base64: str
    lang: str = "kk"

class AppealRequest(BaseModel):
    url: str
    reason: str

class ReportRequest(BaseModel):
    url: str
    threat_type: str = "scam"
    note: str = ""


# --- Health check ---
@app.get("/")
async def root():
    return {
        "status": "online",
        "name": "Qalqan AI",
        "version": "3.0.0",
        "pipeline": "3-tier: cache → databases → AI",
        "databases": ["PhishTank", "Google Safe Browsing", "URLhaus", "OpenPhish", "Pyramid List"]
    }


# --- НЕГІЗГІ ТЕКСЕРУ: 3-деңгейлі pipeline ---
@app.post("/check")
async def check_site(request: CheckRequest):
    """
    3-Tier Threat Detection Pipeline:
    Tier 0: Whitelist + Cache (< 5ms)
    Tier 1: Pyramid list + Local blacklist (< 10ms)
    Tier 2: PhishTank + SafeBrowsing + URLhaus + OpenPhish (< 500ms)
    Tier 3: Gemini AI deep analysis (< 3s)
    """
    url = request.url.strip()
    lang = request.lang or "kk"
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

    # --- Tier 2: External databases (параллель) ---
    db_results = await check_all_databases(url)
    if db_results:
        result = calculate_final_verdict(db_results, None, None, lang=lang)
        set_cached(key, result)
        return result

    # --- Tier 3: Gemini AI ---
    ai_result = await analyze_url(url)
    result = calculate_final_verdict([], ai_result, None, lang=lang)
    set_cached(key, result)
    return result


# --- МӘТІН ТЕКСЕРУ ---
@app.post("/check-text")
async def check_text(request: TextCheckRequest):
    """Мәтінді AI арқылы тексеру (хабарлама, email, мәтін)."""
    ai_result = await analyze_text(request.text)
    return calculate_final_verdict([], ai_result, None, lang=request.lang)


# --- СКРИНШОТ ТЕКСЕРУ ---
@app.post("/analyze-screen")
async def check_screen(request: ScreenRequest):
    """Экран скриншотын Gemini Vision арқылы тексеру."""
    result = await analyze_screenshot(request.image_base64)
    return calculate_final_verdict([], result, None, lang=request.lang)


# --- АПЕЛЛЯЦИЯ ---
@app.post("/appeal")
async def appeal(request: AppealRequest):
    """Қате блоктау туралы апелляция жіберу (Telegram)."""
    return await send_appeal(request.url, request.reason)


# --- ШАҒЫМ ---
@app.post("/report")
async def report_site(request: ReportRequest):
    """Қауіпті сайт туралы шағым жіберу."""
    return await send_report(request.url, request.threat_type, request.note)


# --- СТАТИСТИКА ---
_stats = {"checked": 0, "dangerous": 0, "suspicious": 0, "safe": 0}

@app.get("/stats")
async def get_stats():
    """API қолдану статистикасы."""
    return _stats
