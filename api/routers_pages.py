# Static page routes — every endpoint here just serves a prebuilt template.
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from .templates import BATCH_HTML, BRAND_HTML, HELP_HTML, IMPACT_HTML, LEAK_HTML, MINIAPP_HTML, SCAN_HTML, SCREEN_HTML

router = APIRouter()
_HTML_CACHE = {"Cache-Control": "public, max-age=300, s-maxage=600"}


@router.get("/app")
async def mini_app():
    """Telegram Mini App (Web App): URL checker + AI advisor + KZ threat map."""
    return HTMLResponse(MINIAPP_HTML, headers=_HTML_CACHE)


@router.get("/leak")
async def leak_check():
    """Password-leak checker (HIBP k-anonymity; hash prefix only, client-side)."""
    return HTMLResponse(LEAK_HTML, headers=_HTML_CACHE)


@router.get("/help")
async def help_resources():
    """«Обманули — куда обращаться»: official KZ fraud/cyber helplines + action plan."""
    return HTMLResponse(HELP_HTML, headers=_HTML_CACHE)


@router.get("/brand")
async def brand_page():
    """Brand-protection radar page."""
    return HTMLResponse(BRAND_HTML, headers=_HTML_CACHE)


@router.get("/scan")
async def scan_page():
    """Security-grade scanner page."""
    return HTMLResponse(SCAN_HTML, headers=_HTML_CACHE)


@router.get("/impact")
async def impact_page():
    """Economic-effect calculator — prevented fraud loss in ₸ (ДЭР economic framing)."""
    return HTMLResponse(IMPACT_HTML, headers=_HTML_CACHE)


@router.get("/screen")
async def screen_page():
    """Screenshot analysis page — Groq/Gemini Vision reads the image and verdicts it."""
    return HTMLResponse(SCREEN_HTML, headers=_HTML_CACHE)


@router.get("/batch-check")
async def batch_check_page():
    """Bulk URL screening page (banks / regulators / corporate security)."""
    return HTMLResponse(BATCH_HTML, headers=_HTML_CACHE)


