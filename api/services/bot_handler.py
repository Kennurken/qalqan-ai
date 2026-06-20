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
                       reply_to: int | None = None, disable_preview=True,
                       reply_markup: dict | None = None) -> dict:
    payload: dict = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": disable_preview,
    }
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return await _tg("sendMessage", payload)


async def answer_callback(callback_id: str, text: str = "", alert: bool = False) -> dict:
    return await _tg("answerCallbackQuery", {
        "callback_query_id": callback_id, "text": text[:200], "show_alert": alert,
    })


# KZ-CERT incident reporting (official national CERT)
_KZCERT_URL = "https://www.cert.gov.kz/"


def _result_keyboard(domain: str) -> dict | None:
    """Inline keyboard for a check result: community vote + report to KZ-CERT.
    callback_data must stay <=64 bytes, so skip vote buttons for very long domains."""
    rows = []
    if domain and len(domain) <= 48:
        rows.append([
            {"text": "🚨 Растау (скам)", "callback_data": f"v:c:{domain}"},
            {"text": "🙅 Жалған дабыл", "callback_data": f"v:d:{domain}"},
        ])
    rows.append([{"text": "📢 KZ-CERT-ке хабарлау", "url": _KZCERT_URL}])
    return {"inline_keyboard": rows} if rows else None


async def _resolve_redirects(url: str, max_hops: int = 5) -> list[str]:
    """Follow redirects (short-link unmasking). Returns the hop chain incl. final URL."""
    chain: list[str] = []
    try:
        async with httpx.AsyncClient(timeout=6, follow_redirects=False) as client:
            cur = url
            for _ in range(max_hops):
                r = await client.get(cur, headers={"User-Agent": "QalqanAI/1.0"})
                if r.status_code in (301, 302, 303, 307, 308) and "location" in r.headers:
                    nxt = str(httpx.URL(cur).join(r.headers["location"]))
                    chain.append(nxt)
                    cur = nxt
                else:
                    break
    except Exception as e:
        logger.debug(f"redirect resolve failed for {url}: {e}")
    return chain


async def send_photo(chat_id: int | str, photo_url: str, caption: str = "",
                     reply_to: int | None = None) -> dict:
    payload: dict = {"chat_id": chat_id, "photo": photo_url, "parse_mode": "HTML"}
    if caption:
        payload["caption"] = caption[:1000]
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    return await _tg("sendPhoto", payload)


def _screenshot_url(url: str) -> str:
    """Third-party renderer (WordPress mShots) — they render the page, we never
    touch the malicious site ourselves. Safe preview for the user."""
    from urllib.parse import quote
    return f"https://s.wordpress.com/mshots/v1/{quote(url, safe='')}?w=720"


# ── Deepfake / AI voice-scam awareness (2025 жаһандық тренд) ──────────────────
_DEEPFAKE_FLAGS = [
    # ru
    "голосов", "видеозвон", "видео-звон", "подтвердите голос", "ваш голос",
    "синтез голос", "дипфейк", "deepfake", "голосовое подтверждение",
    "руководитель просит", "директор просит перевести", "ии-голос", "ai голос",
    # kk
    "дауыспен раста", "бейнеқоңырау", "дауысыңызды", "басшы сұрап",
    # en
    "voice verification", "video call verify", "voice of your", "ai voice", "voice clone",
]


def _deepfake_flag(text: str) -> bool:
    t = (text or "").lower()
    return any(k in t for k in _DEEPFAKE_FLAGS)


async def handle_deepfake(chat_id: int, message_id: int | None = None):
    """Advisory on AI voice/video (deepfake) scams — a fast-growing 2025 threat."""
    text = (
        "🎭 <b>Deepfake / AI-дауыс алаяқтығы</b>\n"
        "<i>2025 жылы дүниежүзінде ~$1.1 млрд зиян, импер. алаяқтық +1400%</i>\n\n"
        "<b>Қалай танимыз:</b>\n"
        "• Туыс/басшы кенет ақша/құпиясөз сұрайды — асығыс\n"
        "• Дауыс «бір қалыпты», тыныс алу/эмоция табиғи емес\n"
        "• Видеода ауыз/көз синхрон емес, жарық/көлеңке оғаш\n"
        "• «Қазір растау керек», қысым жасайды\n\n"
        "<b>Не істеу керек:</b>\n"
        "• Қоңырауды доғарып, <b>таныс нөмірге өзің қайта қоңырау шал</b>\n"
        "• Отбасылық «құпия сөз» келісіп қой\n"
        "• Ешқашан дауыс/видео арқылы ақша аударма\n\n"
        "Күдікті сілтеме/нөмір болса: /check, /phone, /sms"
    )
    await send_message(chat_id, text, reply_to=message_id)


async def handle_ask(chat_id: int, situation: str, message_id: int | None = None):
    """AI scam-advisor: user describes a situation in words → AI verdict + advice."""
    await send_message(chat_id, "🤔 Жағдайды талдап жатырмын...", reply_to=message_id)
    try:
        base_url = os.getenv("QALQAN_API_URL", "https://qalqan-ai-nu.vercel.app")
        async with httpx.AsyncClient(timeout=25) as client:
            res = await client.post(f"{base_url}/advisor",
                                    json={"text": situation[:2000], "lang": "ru"})
        d = res.json()
        verdict = d.get("verdict", "SUSPICIOUS")
        score = d.get("threat_score", 50)
        icon = "🔴" if verdict == "DANGEROUS" else "🟡" if verdict == "SUSPICIOUS" else "🟢"
        parts = [f"{icon} <b>AI-кеңесші</b> · {verdict} ({score}/100)\n"]
        if d.get("reasoning"):
            parts.append(_esc(str(d["reasoning"])[:500]))
        if d.get("red_flags"):
            parts.append("\n⚠️ <b>Қауіп белгілері:</b>")
            parts += [f"  • {_esc(str(f))}" for f in d["red_flags"][:5]]
        if d.get("advice"):
            parts.append("\n✅ <b>Не істеу керек:</b>")
            parts += [f"  • {_esc(str(a))}" for a in d["advice"][:5]]
        await send_message(chat_id, "\n".join(parts), reply_to=message_id)
    except Exception as e:
        logger.error(f"ask error: {e}")
        await send_message(chat_id, "❌ Талдау қатесі. Кейінірек қайталаңыз.", reply_to=message_id)


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
        f"  /phone &lt;номер&gt; — телефон нөмірін тексеру\n"
        f"  /sms &lt;мәтін&gt; — SMS алаяқтығын тексеру\n"
        f"  /pyramid &lt;атау&gt; — қаржы пирамидасын тексеру (АФМ)\n"
        f"  /ask &lt;жағдай&gt; — AI-кеңесшіге жағдайды сипаттаңыз\n"
        f"  /deepfake — AI-дауыс/видео алаяқтығынан қорғану\n"
        f"  /tender &lt;нөмір&gt; — тендер алаяқтығын тексеру\n"
        f"  /report &lt;url&gt; — алаяқтықты хабарлау\n"
        f"  /stats — бүгінгі статистика\n"
        f"  /help — толық нұсқаулық\n\n"
        f"💡 Немесе жай URL жіберіңіз — автоматты тексереді!\n\n"
        f"<i>🇰🇿 Қазақстанды онлайн алаяқтықтан қорғаймыз</i>"
    )
    await send_message(chat_id, text)


async def handle_help(chat_id: int):
    text = (
        f"🛡️ <b>Qalqan AI — Нұсқаулық</b>\n\n"
        f"<b>Командалар:</b>\n"
        f"  /check kaspi-support.kz — URL тексеру\n"
        f"  /phone +77771234567 — телефон нөмірін тексеру\n"
        f"  /sms Сіздің шотыңыз бұғатталды... — SMS тексеру\n"
        f"  /pyramid Финико — қаржы пирамидасын атау бойынша тексеру (АФМ/АРРФР)\n"
        f"  /ask Каспиден қоңырау, кодты сұрап жатыр — жағдайды сөзбен сипаттап, AI-кеңес ал\n"
        f"  /deepfake — AI-дауыс/видео (deepfake) алаяқтығынан қорғану кеңесі\n"
        f"  /tender 12345678 — тендер алаяқтығын тексеру\n"
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
        f"  🟡 Күдікті SMS хабарламалар\n"
        f"  🟡 Алаяқтық телефон нөмірлері\n\n"
        f"<i>6-деңгейлі AI pipeline · Верификацияланған KZ дерекқор</i>"
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
        # Pipeline + redirect-chain unmasking in parallel (no extra latency)
        result, chain = await asyncio.gather(_run_pipeline(url), _resolve_redirects(url))
        text = format_result(url, result)
        if chain:
            hops = " →\n     ".join(f"<code>{_esc(h[:70])}</code>" for h in chain[:4])
            text += (f"\n\n🔗 <b>Бағыттау тізбегі</b> (қысқа сілтеме ашылды):\n"
                     f"     <code>{_esc(url[:70])}</code> →\n     {hops}")
        from .threat_db import extract_domain
        await send_message(chat_id, text, reply_to=message_id,
                           reply_markup=_result_keyboard(extract_domain(url)))
        # Screenshot preview (rendered by a third-party service — we never load the site)
        if (os.getenv("BOT_SCREENSHOTS", "1") != "0"
                and result.get("verdict") in ("DANGEROUS", "SUSPICIOUS")):
            try:
                await send_photo(chat_id, _screenshot_url(url),
                                 caption="📸 Сайттың алдын ала көрінісі (ашпаңыз!)")
            except Exception as e:
                logger.debug(f"screenshot send failed: {e}")
    except Exception as e:
        logger.error(f"Bot check error for {url}: {e}")
        await send_message(chat_id,
            f"❌ Тексеру қатесі: <code>{_esc(str(e)[:100])}</code>",
            reply_to=message_id)


async def handle_phone_check(chat_id: int, phone: str, message_id: int | None = None):
    """Check Kazakhstan phone number for scam/fraud patterns."""
    # Normalize: strip spaces, dashes, parens
    raw = re.sub(r"[\s\-\(\)\+]", "", phone)
    if raw.startswith("8") and len(raw) == 11:
        raw = "7" + raw[1:]
    if not re.match(r"^7[0-9]{10}$", raw):
        await send_message(chat_id,
            "⚠️ Телефон нөмірі дұрыс емес. ҚР форматы: +7 7XX XXX XX XX",
            reply_to=message_id)
        return

    prefix3 = raw[1:4]
    prefix4 = raw[1:5]

    # KZ scam call center prefixes (documented by KNB/ДКНБ)
    SCAM_PREFIXES = {
        "700", "701", "702", "705", "706", "707", "708", "709",
        "747", "771", "775", "776", "777", "778",
    }
    # Highly suspicious patterns
    suspicious_patterns = [
        raw == raw[0] * len(raw),                   # all same digit
        raw[1:5] in ("7000", "7777", "0000"),        # common scam vanity
        len(set(raw[1:])) <= 3,                      # very few unique digits
    ]
    is_valid_kz_mobile = prefix3 in SCAM_PREFIXES

    if any(suspicious_patterns) and is_valid_kz_mobile:
        verdict = "SUSPICIOUS"
        score = 55
        icon = "⚠️"
        detail = "Қайталанатын цифрлар немесе алаяқтыққа тән үлгі"
        detail_ru = "Повторяющиеся цифры или подозрительный паттерн"
    elif not is_valid_kz_mobile:
        verdict = "SUSPICIOUS"
        score = 40
        icon = "⚠️"
        detail = "Белгісіз ҚР мобилдік префикс"
        detail_ru = "Неизвестный мобильный префикс РК"
    else:
        verdict = "SAFE"
        score = 10
        icon = "✅"
        detail = "Стандартты ҚР мобилдік нөмір"
        detail_ru = "Стандартный мобильный номер РК"

    formatted = f"+7 {raw[1:4]} {raw[4:7]} {raw[7:9]} {raw[9:11]}"
    text = (
        f"{icon} <b>Телефон тексеру: {formatted}</b>\n\n"
        f"Вердикт: <b>{verdict}</b> ({score}/100)\n"
        f"RU: {detail_ru}\n"
        f"KK: {detail}\n\n"
        f"ℹ️ Толық тексеру үшін: <a href='https://qalqan-ai-nu.vercel.app'>qalqan-ai-nu.vercel.app</a>"
    )
    await send_message(chat_id, text, reply_to=message_id)


async def handle_sms_check(chat_id: int, sms_text: str, message_id: int | None = None):
    """Analyze SMS/message text for scam patterns using the AI pipeline."""
    if len(sms_text) > 1000:
        sms_text = sms_text[:1000]

    await send_message(chat_id, "🔍 SMS тексерілуде...", reply_to=message_id)

    try:
        base_url = os.getenv("QALQAN_API_URL", "https://qalqan-ai-nu.vercel.app")
        async with httpx.AsyncClient(timeout=20) as client:
            res = await client.post(f"{base_url}/check-text",
                json={"text": sms_text, "lang": "ru"})
        data = res.json()

        verdict = data.get("verdict", "UNKNOWN")
        score = data.get("threat_score", 0)
        detail = data.get("detail_ru") or data.get("detail") or ""

        if verdict == "DANGEROUS":
            icon = "🔴"
        elif verdict == "SUSPICIOUS":
            icon = "🟡"
        else:
            icon = "🟢"

        # Extract URLs found in SMS
        urls_found = re.findall(
            r"(?:https?://[^\s]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)",
            sms_text
        )
        url_lines = ""
        if urls_found:
            url_lines = "\n🔗 Табылған сілтемелер:\n" + "\n".join(
                f"  • <code>{u[:60]}</code>" for u in urls_found[:3]
            )

        df_line = ""
        if _deepfake_flag(sms_text):
            df_line = ("\n\n🎭 <b>Deepfake/AI-дауыс белгісі!</b> Дауыс/видео арқылы "
                       "растау сұраса — таныс нөмірге өзің қайта қоңырау шал. /deepfake")
        text = (
            f"{icon} <b>SMS талдауы</b>\n\n"
            f"Вердикт: <b>{verdict}</b> ({score}/100)\n"
            f"{detail}"
            f"{url_lines}"
            f"{df_line}\n\n"
            f"💡 Егер алаяқтық деп ойласаңыз — ешкімге жіберме, блоктаңыз"
        )
        await send_message(chat_id, text, reply_to=message_id)
    except Exception as e:
        logger.error(f"SMS check error: {e}")
        await send_message(chat_id, "❌ Тексеру қатесі. Кейінірек қайталаңыз.", reply_to=message_id)


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


async def handle_pyramid_check(chat_id: int, name: str, message_id: int | None = None):
    """Check a company/brand name against the AFM/ARDFM pyramid registry."""
    await send_message(chat_id,
        f"🔺 Пирамида тізімінен тексерілуде: <b>{_esc(name)}</b>...",
        reply_to=message_id)
    try:
        import os
        base_url = os.getenv("QALQAN_API_URL", "https://qalqan-ai-nu.vercel.app")
        async with httpx.AsyncClient(timeout=15) as client:
            res = await client.post(f"{base_url}/pyramid/check", json={"name": name, "lang": "kk"})
            result = res.json()
        verdict = result.get("verdict", "UNKNOWN")
        score   = result.get("threat_score", 0)
        emoji   = _VERDICT_EMOJI.get(verdict, "❓")
        match   = result.get("match")
        if match:
            lines = [
                f"{emoji} <b>«{_esc(str(match))}»</b>",
                "",
                f"📊 Қауіп деңгейі: <b>{score}/100</b> {_score_bar(score)}",
                f"🎯 Сәйкестік: {int(float(result.get('confidence', 0)) * 100)}%",
                "",
                _esc(result.get("detail") or result.get("detail_kk", "")),
            ]
            link = result.get("official_link")
            if link:
                lines.append(f"\n🔗 <a href='{link}'>АРРФР ресми тізімі</a>")
        else:
            lines = [
                f"✅ <b>«{_esc(name)}»</b> реестрде табылмады.",
                "",
                _esc(result.get("detail") or result.get("detail_kk", "")),
            ]
        lines.append("\n<i>Qalqan AI · АФМ/АРРФР пирамида тізімі</i>")
        await send_message(chat_id, "\n".join(lines), reply_to=message_id)
    except Exception as e:
        logger.error(f"Pyramid check error {name}: {e}")
        await send_message(chat_id, "❌ Пирамида тексеру қатесі.", reply_to=message_id)


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

async def handle_callback(cb: dict) -> None:
    """Handle inline-button presses (community confirm/dispute votes)."""
    cb_id = cb.get("id", "")
    data = cb.get("data", "")
    user_id = cb.get("from", {}).get("id", "anon")

    if data.startswith(("v:c:", "v:d:")):
        vote = "confirm" if data[2] == "c" else "dispute"
        domain = data[4:]
        from ..utils.supabase import record_vote
        res = await record_vote(domain, vote, f"tg:{user_id}")
        if res.get("already_voted"):
            await answer_callback(cb_id, "Сіз бұл домен бойынша дауыс бергенсіз ✓")
        elif res.get("ok"):
            st = res.get("stats", {})
            label = "Растадыңыз 🚨" if vote == "confirm" else "Жалған дабыл деп белгіледіңіз 🙅"
            blocked = " · ҚОҒАМ БҰҒАТТАДЫ 🛑" if st.get("auto_blocked") else ""
            await answer_callback(
                cb_id,
                f"{label} (растау: {st.get('confirms', 0)}, шағым: {st.get('reports', 0)}){blocked}",
            )
        else:
            await answer_callback(cb_id, "Дауыс сақталмады, кейінірек қайталаңыз")
        return
    await answer_callback(cb_id, "")


async def dispatch(update: dict) -> None:
    """Route incoming Telegram update to correct handler."""

    # ── Callback query (inline buttons: votes) ──
    if "callback_query" in update:
        await handle_callback(update["callback_query"])
        return

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

    elif text.startswith("/phone"):
        parts = text.split(maxsplit=1)
        phone = parts[1].strip() if len(parts) > 1 else ""
        if not phone:
            await send_message(chat_id,
                "ℹ️ Пайдаланылуы: /phone &lt;номер&gt;\n"
                "Мысал: /phone +77771234567",
                reply_to=message_id)
        else:
            await handle_phone_check(chat_id, phone, message_id)

    elif text.startswith("/sms"):
        parts = text.split(maxsplit=1)
        sms_text = parts[1].strip() if len(parts) > 1 else ""
        if not sms_text:
            await send_message(chat_id,
                "ℹ️ Пайдаланылуы: /sms &lt;хабарлама мәтіні&gt;\n"
                "Мысал: /sms Сіздің шотыңыздан ақша алынды касп1.kz/verify",
                reply_to=message_id)
        else:
            await handle_sms_check(chat_id, sms_text, message_id)

    elif text.startswith("/pyramid"):
        parts = text.split(maxsplit=1)
        name = parts[1].strip() if len(parts) > 1 else ""
        if not name:
            await send_message(chat_id,
                "ℹ️ Пайдаланылуы: /pyramid &lt;компания атауы&gt;\n"
                "Мысал: /pyramid Финико",
                reply_to=message_id)
        else:
            await handle_pyramid_check(chat_id, name, message_id)

    elif text.startswith("/deepfake") or text.startswith("/voice"):
        await handle_deepfake(chat_id, message_id)

    elif text.startswith("/ask"):
        parts = text.split(maxsplit=1)
        q = parts[1].strip() if len(parts) > 1 else ""
        if not q:
            await send_message(chat_id,
                "ℹ️ /ask &lt;жағдайды сипаттаңыз&gt;\n"
                "Мысал: /ask Каспи қауіпсіздік қызметінен қоңырау шалып, SMS-кодты сұрап жатыр",
                reply_to=message_id)
        else:
            await handle_ask(chat_id, q, message_id)

    # ── Auto: plain URL → check ──
    elif _URL_RE.search(text) and not text.startswith("/"):
        m = _URL_RE.search(text)
        if m:
            await handle_check(chat_id, m.group(0), message_id)

    # ── Auto: free-text situation (40+ chars, no URL) → AI advisor ──
    elif not text.startswith("/") and len(text) >= 40:
        await handle_ask(chat_id, text, message_id)
