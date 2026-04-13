# клауд Елдоса N1 — Qalqan AI v3.0
# Telegram бот: апелляциялар мен хабарламалар жіберу

import os
import httpx

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


async def send_appeal(url: str, reason: str) -> dict:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return {"status": "error", "message": "Telegram баптаулары жоқ!"}

    message = (
        f"🛡️ *QALQAN AI: ЖАҢА АПЕЛЛЯЦИЯ*\n\n"
        f"🌐 *Сайт:* {url}\n"
        f"📝 *Себебі:* {reason}\n"
        f"⏰ *Уақыт:* автоматты"
    )

    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.post(api_url, json=payload)
            if res.status_code == 200:
                return {"status": "success", "message": "Апелляция Телеграмға жіберілді!"}
            return {"status": "error", "message": f"Telegram қатесі: {res.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)[:100]}


async def send_report(url: str, threat_type: str, reporter_note: str = "") -> dict:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return {"status": "error", "message": "Telegram баптаулары жоқ!"}

    message = (
        f"🚨 *QALQAN AI: ЖАҢА ШАҒЫМ*\n\n"
        f"🌐 *Сайт:* {url}\n"
        f"⚠️ *Қауіп түрі:* {threat_type}\n"
        f"📝 *Ескерту:* {reporter_note or 'жоқ'}"
    )

    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.post(api_url, json=payload)
            if res.status_code == 200:
                return {"status": "success", "message": "Шағым жіберілді!"}
            return {"status": "error", "message": f"Telegram қатесі: {res.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)[:100]}
