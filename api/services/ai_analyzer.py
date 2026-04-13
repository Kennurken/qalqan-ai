# клауд Елдоса N1 — Qalqan AI v3.0
# Gemini AI анализатор: URL, мәтін, скриншот талдау
# Тек Tier 2 нәтиже бермегенде қолданылады

import os
import re
import json
import httpx
from google import genai
from google.genai import types

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

MODEL_ID = "gemini-2.5-flash"

SYSTEM_PROMPT_URL = """Сен Qalqan AI — киберқауіпсіздік жүйесісің.
Сайтты немесе сілтемені талдап, оның қауіпті екенін анықта.

Міндетті ережелер:
- Казино, құмар ойын, бәс тігу = DANGEROUS
- Қаржылық пирамида, MLM, гарантированный доход = DANGEROUS
- Фишинг, жеке деректерді сұрау = DANGEROUS
- Жалған интернет-дүкен = DANGEROUS
- Зиянды бағдарлама, вирус = DANGEROUS

Жауапты ТЕК JSON форматында қайтар:
{
  "verdict": "DANGEROUS" немесе "SAFE" немесе "SUSPICIOUS",
  "threat_score": 0-100,
  "threat_type": "phishing|malware|pyramid|scam|gambling|fake_shop|social_engineering|safe",
  "reason_kk": "Қазақша түсіндірме",
  "reason_ru": "Русское объяснение",
  "reason_en": "English explanation",
  "indicators": ["белгі1", "белгі2"]
}"""

SYSTEM_PROMPT_TEXT = """Сен Qalqan AI — киберқауіпсіздік жүйесісің.
Берілген мәтінді талдап, алаяқтық, фишинг, әлеуметтік инженерия белгілерін анықта.

Тексеретін нәрселер:
- Жеке деректерді сұрау (пароль, карта нөмірі, ЖСН)
- Жалған ұтыс, сыйлық уәделері
- Жедел шешім қабылдауға мәжбүрлеу
- Қаржылық пирамида белгілері
- Банк/мемлекет қызметкері ретінде көрсету

Жауапты ТЕК JSON форматында қайтар:
{
  "verdict": "DANGEROUS" немесе "SAFE" немесе "SUSPICIOUS",
  "threat_score": 0-100,
  "threat_type": "phishing|scam|pyramid|social_engineering|safe",
  "reason_kk": "Қазақша түсіндірме",
  "reason_ru": "Русское объяснение",
  "reason_en": "English explanation",
  "indicators": ["белгі1", "белгі2"]
}"""

SYSTEM_PROMPT_SCREEN = """Сен Qalqan AI — киберқауіпсіздік жүйесісің.
Скриншотты талдап, алаяқтық белгілерін анықта.

Тексеретін нәрселер:
- Жалған логин формалары (банк, қызмет имитациясы)
- Жедел хабарламалар ("Сіз ұтып алдыңыз!", "Вирус анықталды!")
- Жалған попаптар мен ескертулер
- Банк/мемлекет сайттарын көшіру
- Күдікті төлем формалары

Жауапты ТЕК JSON форматында қайтар:
{
  "verdict": "DANGEROUS" немесе "SAFE" немесе "SUSPICIOUS",
  "threat_score": 0-100,
  "threat_type": "phishing|scam|fake_shop|social_engineering|safe",
  "reason_kk": "Қазақша түсіндірме",
  "reason_ru": "Русское объяснение",
  "reason_en": "English explanation",
  "indicators": ["белгі1", "белгі2"]
}"""


def _parse_ai_json(raw_text: str) -> dict:
    """AI жауабынан JSON шығарып алу."""
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    # Fallback: regex pattern matching (qalqanai стилі)
    verdict_match = re.search(r"verdict[\"']?\s*[:=]\s*[\"']?(DANGEROUS|SAFE|SUSPICIOUS)", raw_text, re.I)
    score_match = re.search(r"(?:threat_score|score|confidence)[\"']?\s*[:=]\s*(\d+)", raw_text, re.I)

    return {
        "verdict": verdict_match.group(1).upper() if verdict_match else "SUSPICIOUS",
        "threat_score": int(score_match.group(1)) if score_match else 50,
        "threat_type": "unknown",
        "reason_kk": raw_text[:200],
        "reason_ru": raw_text[:200],
        "reason_en": raw_text[:200],
        "indicators": []
    }


async def analyze_url(url: str) -> dict:
    """URL-ді Gemini AI арқылы тексеру."""
    if not client:
        return {"verdict": "SUSPICIOUS", "threat_score": 50, "threat_type": "unknown",
                "reason_kk": "AI қызметі қолжетімсіз", "source": "ai_error"}
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[f"{SYSTEM_PROMPT_URL}\n\nСілтеме: {url}"],
            config=types.GenerateContentConfig(temperature=0.1)
        )
        parsed = _parse_ai_json(response.text)
        parsed["source"] = "ai"
        return parsed
    except Exception as e:
        return {"verdict": "SUSPICIOUS", "threat_score": 50, "threat_type": "unknown",
                "reason_kk": f"AI қатесі: {str(e)[:80]}", "source": "ai_error"}


async def analyze_text(text: str) -> dict:
    """Мәтінді AI арқылы тексеру (хабарламалар, электрондық пошта)."""
    if not client:
        return {"verdict": "SUSPICIOUS", "threat_score": 50, "threat_type": "unknown",
                "reason_kk": "AI қызметі қолжетімсіз", "source": "ai_error"}
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[f"{SYSTEM_PROMPT_TEXT}\n\nМәтін: {text}"],
            config=types.GenerateContentConfig(temperature=0.1)
        )
        parsed = _parse_ai_json(response.text)
        parsed["source"] = "ai"
        return parsed
    except Exception as e:
        return {"verdict": "SUSPICIOUS", "threat_score": 50, "threat_type": "unknown",
                "reason_kk": f"AI қатесі: {str(e)[:80]}", "source": "ai_error"}


async def analyze_screenshot(image_base64: str) -> dict:
    """Скриншотты Gemini Vision арқылы тексеру."""
    if not api_key:
        return {"verdict": "SUSPICIOUS", "threat_score": 50, "threat_type": "unknown",
                "reason_kk": "AI қызметі қолжетімсіз", "source": "ai_error"}
    try:
        # Vision API — REST арқылы (detectAI тәсілі)
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": SYSTEM_PROMPT_SCREEN},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
                ]
            }]
        }
        async with httpx.AsyncClient(timeout=30) as http:
            res = await http.post(gemini_url, json=payload)
            if res.status_code != 200:
                return {"verdict": "SUSPICIOUS", "threat_score": 50, "source": "ai_error",
                        "reason_kk": f"Vision API қатесі: {res.status_code}"}

            data = res.json()
            if "candidates" not in data or not data["candidates"]:
                return {"verdict": "SUSPICIOUS", "threat_score": 50, "source": "ai_error",
                        "reason_kk": "AI жауап бермеді"}

            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = _parse_ai_json(raw_text)
            parsed["source"] = "ai_vision"
            return parsed
    except Exception as e:
        return {"verdict": "SUSPICIOUS", "threat_score": 50, "threat_type": "unknown",
                "reason_kk": f"Vision қатесі: {str(e)[:80]}", "source": "ai_error"}
