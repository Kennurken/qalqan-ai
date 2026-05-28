# Qalqan AI v5.1
# Telegram Bot webhook handler — serverless, no python-telegram-bot dependency
# Supports: /start /help /check /report /stats /lang + inline mode

import os
import re
import logging
import asyncio
import httpx
from datetime import datetime, timezone

logger = logging.getLogger("qalqan")

# ── Telegram API helpers ─────────────────────────────────────────────────────

def _token() -> str:
    return os.getenv("TELEGRAM_BOT_TOKEN", "")

TG_API = "https://api.telegram.org/bot"

# URL regex — matches http(s) and bare domain.tld patterns
_URL_RE = re.compile(
    r"(https?://[^\s]+|(?:www\.)[^\s]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)",
    re.IGNORECASE
)


async def _tg(method: str, payload: dict) -> dict:
    """Call Telegram Bot API method."""
    token = _token()
    if not token:
        logger.warning("TELEGRAM_BOT_TOKEN not set")
        return {}
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            res = await client.post(f"{TG_API}{token}/{method}", json=payload)
            return res.json()
    except Exception as e:
        logger.error(f"Telegram API error ({method}): {e}")
        return {}


async def send_message(chat_id: int | str, text: str, parse_mode="HTML",
                       reply_to: int | None = None, disable_preview=True) -> dict:
    payload: dict = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": disable_preview,
    }
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    return await _tg("sendMessage", payload)


async def answer_inline(inline_query_id: str, results: list) -> dict:
    return await _tg("answerInlineQuery", {
        "inline_query_id": inline_query_id,
        "results": results,
        "cache_time": 30,
    })


def _esc(text: str) -> str:
    """Escape HTML special chars."""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── Verdict formatting ────────────────────────────────────────────────────────

_VERDICT_EMOJI = {
    "DANGEROUS": "🛑",
    "SUSPICIOUS": "⚠️",
    "SAFE": "✅",
}

_THREAT_LABELS = {
    "phishing":               "Фишинг",
    "gambling":               "Gambling / Ойын автоматтары",
    "pyramid":                "Қаржылық пирамида",
    "malware":                "Зиянды бағдарлама",
    "suspicious_infrastructure": "Күдікті инфрақұрылым",
    "kz_impersonation":       "KZ бренд қолдан жасау",
    "fraud":                  "Алаяқтық",
    "social_engineering":     "Әлеуметтік инженерия",
}


def format_result(url: str, result: dict, lang: str = "kk") -> str:
    verdict = result.get("verdict", "UNKNOWN")
    score   = result.get("threat_score", 0)
    emoji   = _VERDICT_EMOJI.get(verdict, "❓")
    source  = result.get("source", "qalqan")
    ttype   = result.get("threat_type", "")
    threat_label = _THREAT_LABELS.get(ttype, ttype.replace("_", " ").title())

    # Pick reason by lang
    reason_key = f"reason_{lang}" if lang in ("kk", "ru", "en") else "reason_kk"
    reason = (result.get(reason_key)
              or result.get("reason_kk")
              or result.get("detail_kk")
              or result.get("detail")
              or "")

    score_bar = _score_bar(score)

    if verdict == "SAFE":
        lines = [
            f"{emoji} <b>ҚАУІПСІЗ</b>",
            f"",
            f"🌐 <code>{_esc(url[:80])}</code>",
            f"📊 Қауіп деңгейі: {score}/100 {score_bar}",
            f"🔍 Тексерді: <i>{_esc(source)}</i>",
        ]
    else:
        lines = [
            f"{emoji} <b>{'ҚАУІПТІ' if verdict == 'DANGEROUS' else 'КҮДІКТІ'}</b>",
            f"",
            f"🌐 <code>{_esc(url[:80])}</code>",
            f"📊 Қауіп деңгейі: <b>{score}/100</b> {score_bar}",
        ]
        if threat_label:
            lines.append(f"⚠️ Қауіп түрі: <b>{_esc(threat_label)}</b>")
        if reason:
            lines.append(f"")
            lines.append(f"📋 <i>{_esc(reason[:300])}</i>")
        lines += [
            f"",
            f"🔍 Дерек көзі: <i>{_esc(source)}</i>",
            f"",
            f"🛡️ <b>Бұл сайтқа кіруді ұсынбаймыз!</b>",
        ]

    lines.append(f"\n<i>Qalqan AI · qalqan.kz</i>")
    return "\n".join(lines)


def _score_bar(score: int) -> str:
    filled = round(score / 10)
    empty  = 10 - filled
    color  = "🟥" if score >= 70 else "🟨" if score >= 30 else "🟩"
    return color * filled + "⬜" * empty


# ── Command handlers ──────────────────────────────────────────────────────────

async def handle_start(chat_id: int, first_name: str = ""):
    text = (
        f"🛡️ <b>Qalqan AI-ға қош келдіңіз, {_esc(first_name)}!</b>\n\n"
        f"Мен — Қазақстанның бірінші AI киберқауіпсіздік боты.\n"
        f"Фишинг, пирамида, gambling сайттарын анықтаймын.\n\n"
        f"<b>Командалар:</b>\n"
        f"  /check &lt;url&gt; — URL тексеру\n"
        f"  /tender &lt;нөмір&gt; — тендер алаяқтығын тексеру\n"
        f"  /report &lt;url&gt; — алаяқтықты хабарлау\n"
        f"  /stats — бүгінгі статистика\n"
        f"  /help — толық нұсқаулық\n\n"
        f"💡 Немесе жай URL жазыңыз — автоматты тексереді!\n\n"
        f"<i>🇰🇿 Қазақстанды онлайн алаяқтықтан қорғаймыз</i>"
    )
    await send_message(chat_id, text)


async def handle_help(chat_id: int):
    text = (
        f"🛡️ <b>Qalqan AI — Нұсқаулық</b>\n\n"
        f"<b>Командалар:</b>\n"
        f"  /check kaspi-support.kz — URL тексеру\n"
        f"  /tender 12345678 — тендер алаяқтығын тексеру 🏛️\n"
        f"  /report scam-site.kz — алаяқтықты хабарлау\n"
        f"  /stats — бүгінгі қорғаныс статистикасы\n\n"
        f"<b>Автоматты тексеру:</b>\n"
        f"  Кез-келген URL жіберіңіз — бот автоматты тексереді\n\n"
        f"<b>Inline режим:</b>\n"
        f"  @QalqanAI_bot URL — кез-келген чатта тексеріңіз\n\n"
        f"<b>Анықталатын қауіптер:</b>\n"
        f"  🔴 Фишинг — Kaspi/eGov/Halyk жалған сайттар\n"
        f"  🔴 Қаржылық пирамидалар\n"
        f"  🟡 Gambling / ойын автоматтары\n"
        f"  🟡 Күдікті домендер\n\n"
        f"<i>Деректер: 6-деңгейлі AI pipeline · Верификацияланған KZ дерекқор</i>"
    )
    await send_message(chat_id, text)


async def handle_check(chat_id: int, url: str, message_id: int | None = None):
    """Run full Qalqan pipeline on URL and reply with result."""
    # Normalise URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    await send_message(chat_id, f"🔍 Тексерілуде: <code>{_esc(url[:80])}</code>...",
                       reply_to=message_id)

    try:
        result = await _run_pipeline(url)
        text = format_result(url, result)
        await send_message(chat_id, text, reply_to=message_id)
    except Exception as e:
        logger.error(f"Bot check error for {url}: {e}")
        await send_message(chat_id,
            f"❌ Тексеру қатесі: <code>{_esc(str(e)[:100])}</code>",
            reply_to=message_id)


async def handle_report(chat_id: int, url: str, message_id: int | None = None):
    """Forward user-submitted scam report to admin Telegram chat."""
    from ..utils.telegram import send_report
    if not url:
        await send_message(chat_id,
            "ℹ️ Пайдаланылуы: /report &lt;url&gt;\n"
            "Мысал: /report kaspi-bonus123.kz")
        return

    result = await send_report(url, "user_report", f"Telegram bot report from user")
    if result.get("status") == "success":
        await send_message(chat_id,
            f"✅ Шағымыңыз қабылданды!\n"
            f"🌐 URL: <code>{_esc(url[:80])}</code>\n\n"
            f"<i>Модераторлар тексереді. Рахмет!</i>",
            reply_to=message_id)
    else:
        await send_message(chat_id, "❌ Жіберу қатесі. Кейінірек қайталаңыз.",
                           reply_to=message_id)


async def handle_stats(chat_id: int):
    """Fetch /stats from Qalqan API and format for Telegram."""
    base_url = os.getenv("QALQAN_API_URL", "https://qalqan-ai.vercel.app")
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            res = await client.get(f"{base_url}/stats")
            data = res.json()

        total    = data.get("total_checks", 0)
        blocked  = data.get("blocked", 0)
        phishing = data.get("by_type", {}).get("phishing", 0)
        pyramid  = data.get("by_type", {}).get("pyramid", 0)
        gambling = data.get("by_type", {}).get("gambling", 0)
        today    = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        text = (
            f"📊 <b>Qalqan AI — Статистика</b>\n"
            f"<i>{today}</i>\n\n"
            f"🔍 Жалпы тексеру: <b>{total:,}</b>\n"
            f"🛑 Блокталған: <b>{blocked:,}</b>\n\n"
            f"<b>Қауіп түрлері:</b>\n"
            f"  🎣 Фишинг: {phishing:,}\n"
            f"  💰 Пирамида: {pyramid:,}\n"
            f"  🎰 Gambling: {gambling:,}\n\n"
            f"<i>🛡️ Qalqan AI қорғап тұр!</i>"
        )
    except Exception as e:
        logger.error(f"Stats fetch error: {e}")
        text = "❌ Статистика алу қатесі. API қолжетімсіз."

    await send_message(chat_id, text)


async def handle_tender_check(chat_id: int, tender_number: str, message_id: int | None = None):
    """Check a госзакупки tender for fraud red-flags."""
    await send_message(chat_id,
        f"🏛️ Тендер тексерілуде: <code>{_esc(tender_number)}</code>...",
        reply_to=message_id)
    try:
        from .goszakup import check_tender_by_number
        result = await check_tender_by_number(tender_number)
        verdict = result.get("verdict", "UNKNOWN")
        score   = result.get("threat_score", 0)
        emoji   = _VERDICT_EMOJI.get(verdict, "❓")
        red_flags = result.get("red_flags", [])

        lines = [
            f"{emoji} <b>ТЕНДЕР #{_esc(tender_number)}</b>",
            f"",
            f"📊 Алаяқтық деңгейі: <b>{score}/100</b> {_score_bar(score)}",
            f"⚖️ Вердикт: <b>{'АЛАЯҚТЫҚ' if verdict == 'DANGEROUS' else 'КҮДІКТІ' if verdict == 'SUSPICIOUS' else 'ҚАЛЫПТЫ'}</b>",
        ]
        if red_flags:
            lines += ["", "🚩 <b>Анықталған red-flag ережелері:</b>"]
            for rf in red_flags[:5]:
                lines.append(f"  • [{rf['score']}] {_esc(rf.get('kk', rf.get('en', '')))}")
        elif verdict == "SAFE":
            lines.append("")
            lines.append("✅ Алаяқтық белгілері анықталмады")

        lines.append(f"\n<i>Qalqan AI · Госзакупки Fraud Detector</i>")
        await send_message(chat_id, "\n".join(lines), reply_to=message_id)
    except Exception as e:
        logger.error(f"Tender check error {tender_number}: {e}")
        await send_message(chat_id, "❌ Тендер тексеру қатесі.", reply_to=message_id)


async def handle_inline(inline_query_id: str, query: str):
    """Inline query: @QalqanAI_bot <url>"""
    query = query.strip()
    if not query:
        await answer_inline(inline_query_id, [_inline_tip()])
        return

    # Extract URL
    m = _URL_RE.search(query)
    url = m.group(0) if m else query
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        result = await _run_pipeline(url)
        verdict = result.get("verdict", "UNKNOWN")
        score   = result.get("threat_score", 0)
        emoji   = _VERDICT_EMOJI.get(verdict, "❓")
        body    = format_result(url, result)

        results = [{
            "type": "article",
            "id": "1",
            "title": f"{emoji} {verdict} — {score}/100",
            "description": url[:80],
            "input_message_content": {
                "message_text": body,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
        }]
    except Exception:
        results = [{
            "type": "article",
            "id": "1",
            "title": "❌ Тексеру қатесі",
            "description": "API қолжетімсіз",
            "input_message_content": {
                "message_text": "❌ Тексеру қатесі. Кейінірек қайталаңыз.",
                "parse_mode": "HTML",
            },
        }]

    await answer_inline(inline_query_id, results)


def _inline_tip() -> dict:
    return {
        "type": "article",
        "id": "tip",
        "title": "🛡️ Qalqan AI — URL тексеру",
        "description": "@QalqanAI_bot <url> деп жазыңыз",
        "input_message_content": {
            "message_text": (
                "🛡️ <b>Qalqan AI</b>\n"
                "URL тексеру үшін: <code>/check &lt;url&gt;</code>\n"
                "немесе inline: <code>@QalqanAI_bot kaspi-bonus.kz</code>"
            ),
            "parse_mode": "HTML",
        },
    }


# ── Internal pipeline call ────────────────────────────────────────────────────

async def _run_pipeline(url: str) -> dict:
    """Call Qalqan detection pipeline directly (same process)."""
    from ..services.threat_db import check_all_databases, extract_domain
    from ..services.kz_intel import check_kz_impersonation_url, check_gambling_domain
    from ..services.pyramid_detector import check_pyramid_domain
    from ..services.domain_intel import check_domain_intelligence
    from ..services.scoring import calculate_final_verdict
    from ..utils.cache import url_hash, get_cached, set_cached

    # Cache check
    h = url_hash(url)
    cached = get_cached(h)
    if cached:
        return cached

    domain = extract_domain(url)
    results = []

    # Run checks concurrently
    tasks = [
        check_all_databases(url),
        check_kz_impersonation_url(url),
        check_gambling_domain(domain),
        check_pyramid_domain(domain),
        check_domain_intelligence(domain, url),
    ]
    checks = await asyncio.gather(*tasks, return_exceptions=True)

    for c in checks:
        if c and not isinstance(c, Exception):
            if isinstance(c, list):
                results.extend(c)
            else:
                results.append(c)

    verdict_data = calculate_final_verdict(results, url)
    set_cached(h, verdict_data)
    return verdict_data


# ── Main dispatcher ───────────────────────────────────────────────────────────

async def dispatch(update: dict) -> None:
    """Route incoming Telegram update to correct handler."""

    # ── Inline query ──
    if "inline_query" in update:
        iq = update["inline_query"]
        await handle_inline(iq["id"], iq.get("query", ""))
        return

    # ── Regular message ──
    msg = update.get("message") or update.get("edited_message")
    if not msg:
        return

    chat_id    = msg["chat"]["id"]
    message_id = msg.get("message_id")
    text       = (msg.get("text") or "").strip()
    first_name = msg.get("from", {}).get("first_name", "")

    if not text:
        return

    # ── Command routing ──
    if text.startswith("/start"):
        await handle_start(chat_id, first_name)

    elif text.startswith("/help"):
        await handle_help(chat_id)

    elif text.startswith("/stats"):
        await handle_stats(chat_id)

    elif text.startswith("/check"):
        parts = text.split(maxsplit=1)
        url = parts[1].strip() if len(parts) > 1 else ""
        if not url:
            await send_message(chat_id,
                "ℹ️ Пайдаланылуы: /check &lt;url&gt;\n"
                "Мысал: /check kaspi-bonus123.kz",
                reply_to=message_id)
        else:
            await handle_check(chat_id, url, message_id)

    elif text.startswith("/report"):
        parts = text.split(maxsplit=1)
        url = parts[1].strip() if len(parts) > 1 else ""
        await handle_report(chat_id, url, message_id)

    elif text.startswith("/tender"):
        parts = text.split(maxsplit=1)
        number = parts[1].strip() if len(parts) > 1 else ""
        if not number:
            await send_message(chat_id,
                "ℹ️ Пайдаланылуы: /tender &lt;нөмір&gt;\n"
                "Мысал: /tender 12345678",
                reply_to=message_id)
        else:
            await handle_tender_check(chat_id, number, message_id)

    # ── Auto-check: plain URL ──
    elif _URL_RE.search(text) and not text.startswith("/"):
        m = _URL_RE.search(text)
        if m:
            await handle_check(chat_id, m.group(0), message_id)
