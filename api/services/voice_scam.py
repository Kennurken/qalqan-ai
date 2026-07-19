# Qalqan AI — Voice / call-scam detector
# Telephone fraud is the #1 economic threat in KZ. Flow: audio → Groq Whisper
# transcription → call-scam pattern analysis (+ AI situation layer) → verdict.

import os
import re
import logging

from ..utils.http import get_client

logger = logging.getLogger("qalqan")

_GROQ_TRANSCRIBE = "https://api.groq.com/openai/v1/audio/transcriptions"
_WHISPER_MODEL = "whisper-large-v3-turbo"
MAX_AUDIO_BYTES = 20 * 1024 * 1024  # 20 MB

# ── Call-scam patterns (weighted). KZ telephone-fraud playbook, kk + ru ──────
# Each: (regex, score, label_kk, label_ru)
_PATTERNS: list[tuple[str, int, str, str]] = [
    (r"\b(sms|см[еэ]с|код|kod|бір реттік|одноразов\w+ пароль|құпия код)\b.{0,30}\b(айт|скаж|введ|назов|сообщ|жібер)",
     35, "SMS/құпия кодты сұрау", "Запрос SMS/одноразового кода"),
    (r"(қауіпсіздік қызмет|служб[аы] безопасности|банк.{0,12}(қызмет|отдел|служба))",
     30, "«Банк қауіпсіздік қызметі»", "«Служба безопасности банка»"),
    (r"(карт\w*.{0,15}(бұғатта|блокир|заблокир)|шот\w*.{0,15}(бұғатта|блокир))",
     30, "«Картаңыз бұғатталды»", "«Карта заблокирована»"),
    (r"(қауіпсіз шот|безопасн\w+ счет|резервн\w+ счет|аудар\w+.{0,20}шот)",
     35, "«Қауіпсіз шотқа аударыңыз»", "«Переведите на безопасный счёт»"),
    (r"(несие|кредит|займ).{0,25}(рәсімде|оформ|взят|на ваше имя|сіздің атың)",
     30, "Сіздің атыңызға несие", "Кредит на ваше имя"),
    (r"(полиц|прокурор|прокуратур|кнб|следовател|финпол)",
     25, "Полиция/прокуратура атынан", "От имени полиции/прокуратуры"),
    (r"(жеңіп ал|ұтып ал|выигр\w+|приз|сыйлық|бонус).{0,25}(акци|тег[іи]н|алу үшін|получ)",
     20, "«Жеңіп алдыңыз / сыйлық»", "«Вы выиграли / приз»"),
    (r"(инвестиц|крипт|биткоин|bitcoin|forex|кіріс|доход|табыс).{0,25}(кепілд|гаранти|100%|еселе|пайыз)",
     25, "Кепілді инвестиция/крипто", "Гарантированный доход / крипто"),
    (r"(жедел|тез|дереу|срочно|немедленно|сейчас же|прямо сейчас|2 минут|уақыт жоқ)",
     15, "Жасанды жеделдік", "Искусственная срочность"),
    (r"(ешкімге айтпа|никому не говор|не сообщ\w+ никому|құпия сақта)",
     20, "«Ешкімге айтпаңыз»", "«Никому не говорите»"),
    (r"(анедеск|anydesk|teamviewer|қашықтан|удал[её]нн\w+ доступ|telegram.{0,8}код)",
     30, "Қашықтан қол жеткізу сұрау", "Запрос удалённого доступа"),
]


async def transcribe_audio(audio: bytes, filename: str = "audio.ogg") -> str | None:
    """Transcribe audio via Groq Whisper. Returns text or None."""
    key = os.getenv("GROQ_API_KEY", "")
    if not key:
        logger.warning("GROQ_API_KEY not set — cannot transcribe")
        return None
    if not audio or len(audio) > MAX_AUDIO_BYTES:
        return None
    try:
        res = await get_client().post(
            _GROQ_TRANSCRIBE,
            headers={"Authorization": f"Bearer {key}"},
            files={"file": (filename, audio, "application/octet-stream")},
            data={"model": _WHISPER_MODEL, "temperature": "0",
                  "response_format": "json"},
            timeout=40,
        )
        if res.status_code != 200:
            logger.warning(f"Groq transcription failed: {res.status_code} {res.text[:120]}")
            return None
        return (res.json().get("text") or "").strip()
    except Exception as e:
        logger.error(f"transcribe_audio error: {e}")
        return None


def analyze_transcript(text: str, lang: str = "kk") -> dict:
    """Score a call/voice transcript against KZ call-scam patterns."""
    t = (text or "").lower()
    matched: list[dict] = []
    score = 0
    for rx, sc, kk, ru in _PATTERNS:
        if re.search(rx, t, re.IGNORECASE):
            score += sc
            matched.append({"score": sc, "kk": kk, "ru": ru})
    score = min(score, 100)
    verdict = "DANGEROUS" if score >= 50 else "SUSPICIOUS" if score >= 25 else "SAFE"
    flags_kk = [m["kk"] for m in matched]
    flags_ru = [m["ru"] for m in matched]
    if verdict == "SAFE":
        detail_kk = "Қоңырауда алаяқтыққа тән белгілер табылмады. Сақ болыңыз."
        detail_ru = "Явных признаков мошенничества в звонке не найдено. Будьте бдительны."
    else:
        detail_kk = "Телефон алаяқтығының белгілері: " + "; ".join(flags_kk)
        detail_ru = "Признаки телефонного мошенничества: " + "; ".join(flags_ru)
    return {
        "verdict": verdict,
        "threat_score": score,
        "threat_type": "call_scam",
        "source": "voice_scam",
        "detail": detail_kk if lang == "kk" else detail_ru,
        "detail_kk": detail_kk,
        "detail_ru": detail_ru,
        "indicators": [m["kk"] for m in matched],
        "red_flags": matched,
    }


async def analyze_voice(audio: bytes, filename: str = "audio.ogg", lang: str = "kk") -> dict:
    """Full pipeline: transcribe + pattern analysis (+ AI situation layer)."""
    transcript = await transcribe_audio(audio, filename)
    if not transcript:
        return {"verdict": "UNKNOWN", "source": "voice_scam",
                "error": "Аудио мәтінге айналмады (транскрипция қатесі)"}

    result = analyze_transcript(transcript, lang)
    result["transcript"] = transcript[:1500]

    # AI layer: enrich with the scam-advisor on the transcript (best-effort)
    try:
        from .ai_analyzer import analyze_situation
        ai = await analyze_situation(transcript, lang=lang)
        if isinstance(ai, dict) and ai.get("verdict"):
            # take the more severe verdict
            order = {"SAFE": 0, "SUSPICIOUS": 1, "DANGEROUS": 2, "UNKNOWN": 0}
            if order.get(ai["verdict"], 0) > order.get(result["verdict"], 0):
                result["verdict"] = ai["verdict"]
                result["threat_score"] = max(result["threat_score"], ai.get("threat_score", 0))
            if ai.get("advice"):
                result["advice"] = ai["advice"]
    except Exception as e:
        logger.debug(f"voice AI layer skipped: {e}")

    return result
