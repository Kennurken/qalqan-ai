# Qalqan AI v3.0
# Telegram бот: апелляциялар мен хабарламалар жіберу

import os
import re

from .http import get_client

def _bot_token() -> str | None:
    return os.getenv("TELEGRAM_BOT_TOKEN")

def _chat_id() -> str | None:
    return os.getenv("TELEGRAM_CHAT_ID")

def _channel_id() -> str | None:
    """Public threat-broadcast channel (bot must be admin). Optional."""
    return os.getenv("TELEGRAM_CHANNEL_ID")


async def _send(chat_id: str, text: str, parse_mode: str = "Markdown") -> bool:
    token = _bot_token()
    if not token or not chat_id:
        return False
    try:
        client = get_client()
        r = await client.post(f"https://api.telegram.org/bot{token}/sendMessage",
                              json={"chat_id": chat_id, "text": text,
                                    "parse_mode": parse_mode, "disable_web_page_preview": True})
        return r.status_code == 200
    except Exception:
        return False


async def notify_channel(url: str, verdict: str, score: int):
    """Broadcast a newly-detected dangerous site to the public channel (if set).
    Deduped per domain per 24h so repeat checks don't spam the channel."""
    ch = _channel_id()
    if not ch:
        return
    from .cache import once_per
    from ..services.threat_db import extract_domain
    dom = extract_domain(url) or url
    if not await once_per(f"chan:{dom}", ttl=86400):
        return
    text = (
        f"🛑 *Жаңа қауіпті сайт анықталды*\n\n"
        f"🌐 `{_escape_md(dom)}`\n"
        f"⚠️ {verdict} ({score}/100)\n\n"
        f"_Qalqan AI сізді қорғайды_ · @QalqanAI\\_bot"
    )
    await _send(ch, text)


async def health_alert(text: str) -> bool:
    """Send an ops/health alert to the admin chat."""
    return await _send(_chat_id() or "", f"🚨 *Qalqan AI · мониторинг*\n\n{text}")


def _escape_md(text: str) -> str:
    """Fix #2: Escape Telegram MarkdownV1 special chars in user-supplied text.
    Prevents Markdown injection via crafted URL/reason fields."""
    # In Markdown mode, these chars can break formatting or inject links
    return re.sub(r"([_*`\[\]()])", r"\\\1", str(text)[:500])


async def send_appeal(url: str, reason: str) -> dict:
    if not _bot_token() or not _chat_id():
        return {"status": "error", "message": "Telegram баптаулары жоқ!"}

    safe_url = _escape_md(url)
    safe_reason = _escape_md(reason)
    message = (
        f"🛡️ *QALQAN AI: ЖАҢА АПЕЛЛЯЦИЯ*\n\n"
        f"🌐 *Сайт:* `{safe_url}`\n"
        f"📝 *Себебі:* {safe_reason}\n"
        f"⏰ *Уақыт:* автоматты"
    )

    api_url = f"https://api.telegram.org/bot{_bot_token()}/sendMessage"
    payload = {
        "chat_id": _chat_id(),
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        client = get_client()
        res = await client.post(api_url, json=payload)
        if res.status_code == 200:
            return {"status": "success", "message": "Апелляция Телеграмға жіберілді!"}
        return {"status": "error", "message": f"Telegram қатесі: {res.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)[:100]}


async def notify_block(url: str, verdict: str, score: int, source: str):
    """Send Telegram notification when a dangerous site is blocked."""
    if not _bot_token() or not _chat_id():
        return
    message = (
        f"🛑 *QALQAN AI: БЛОКИРОВКА*\n\n"
        f"🌐 *Сайт:* `{_escape_md(url)}`\n"
        f"⚠️ *Вердикт:* {verdict} ({score}/100)\n"
        f"🔍 *Источник:* {_escape_md(source)}"
    )
    api_url = f"https://api.telegram.org/bot{_bot_token()}/sendMessage"
    try:
        client = get_client()
        await client.post(api_url, json={"chat_id": _chat_id(), "text": message, "parse_mode": "Markdown"})
    except Exception:
        pass
    # Also broadcast to the public threat channel (best-effort, only if configured)
    await notify_channel(url, verdict, score)


async def send_report(url: str, threat_type: str, reporter_note: str = "") -> dict:
    if not _bot_token() or not _chat_id():
        return {"status": "error", "message": "Telegram баптаулары жоқ!"}

    message = (
        f"🚨 *QALQAN AI: ЖАҢА ШАҒЫМ*\n\n"
        f"🌐 *Сайт:* `{_escape_md(url)}`\n"
        f"⚠️ *Қауіп түрі:* {_escape_md(threat_type)}\n"
        f"📝 *Ескерту:* {_escape_md(reporter_note) or 'жоқ'}"
    )

    api_url = f"https://api.telegram.org/bot{_bot_token()}/sendMessage"
    payload = {
        "chat_id": _chat_id(),
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        client = get_client()
        res = await client.post(api_url, json=payload)
        if res.status_code == 200:
            return {"status": "success", "message": "Шағым жіберілді!"}
        return {"status": "error", "message": f"Telegram қатесі: {res.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)[:100]}


async def brand_alert(brand: str, new_domains: list[dict]) -> bool:
    """Alert the admin chat when NEW look-alike registrations appear for a
    watched brand (daily brand-watch cron)."""
    if not new_domains:
        return False
    lines = "\n".join(
        f"• `{_escape_md(d['domain'])}`"
        + (f" — {d['age_days']} дн." if d.get("age_days") is not None else "")
        for d in new_domains[:10])
    text = (
        f"⚠️ *Brand-watch: новые клоны для* `{_escape_md(brand)}`\n\n"
        f"{lines}\n\n"
        f"_Проверить: qalqan-ai-nu.vercel.app/brand_"
    )
    return await _send(_chat_id() or "", text)
