# клауд Елдоса N1 — Qalqan AI v3.0
# Мульти-провайдер AI анализатор: Groq (негізгі) → Gemini (backup) → Vision
# Groq: 14,400 req/day (тегін, карта жоқ) — URL + мәтін талдау
# Gemini: 250 req/day (тегін) — backup + скриншот Vision

import os
import re
import json
import logging
import httpx

logger = logging.getLogger("qalqan")

# --- API Keys (runtime-да оқылады, import кезінде емес) ---
def _groq_key() -> str:
    return os.getenv("GROQ_API_KEY", "")

def _gemini_key() -> str:
    return os.getenv("GEMINI_API_KEY", "")

# --- Model configs ---
GROQ_MODEL = "llama-3.1-8b-instant"  # Ең жылдам, 14,400 req/day тегін
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
GEMINI_VISION_MODEL = "gemini-2.0-flash"
GEMINI_VISION_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_VISION_MODEL}:generateContent"

# --- System Prompts ---
SYSTEM_PROMPT_URL = """You are Qalqan AI — a cybersecurity expert system.
Analyze the given URL/link and determine if it's dangerous.

MANDATORY RULES:
- Casino, gambling, betting = DANGEROUS
- Financial pyramid, MLM, guaranteed income = DANGEROUS
- Phishing, personal data harvesting = DANGEROUS
- Fake online store = DANGEROUS
- Malware, virus distribution = DANGEROUS
- Social engineering, manipulation = DANGEROUS

Respond in STRICT JSON format ONLY:
{
  "verdict": "DANGEROUS" or "SAFE" or "SUSPICIOUS",
  "threat_score": 0-100,
  "threat_type": "phishing|malware|pyramid|scam|gambling|fake_shop|social_engineering|safe",
  "reason_kk": "Қазақша түсіндірме",
  "reason_ru": "Объяснение на русском",
  "reason_en": "English explanation",
  "indicators": ["indicator1", "indicator2"]
}"""

SYSTEM_PROMPT_TEXT = """You are Qalqan AI — a cybersecurity expert system.
Analyze the given text for fraud, phishing, and social engineering.

Check for:
- Requests for personal data (passwords, card numbers, ID)
- Fake prizes/gifts promises
- Urgency pressure ("act now", "limited time")
- Pyramid scheme indicators
- Bank/government impersonation
- Emotional manipulation

Respond in STRICT JSON format ONLY:
{
  "verdict": "DANGEROUS" or "SAFE" or "SUSPICIOUS",
  "threat_score": 0-100,
  "threat_type": "phishing|scam|pyramid|social_engineering|safe",
  "reason_kk": "Қазақша түсіндірме",
  "reason_ru": "Объяснение на русском",
  "reason_en": "English explanation",
  "indicators": ["indicator1", "indicator2"]
}"""

SYSTEM_PROMPT_SCREEN = """You are Qalqan AI — a cybersecurity expert.
Analyze this screenshot for scam/fraud indicators.

Check for:
- Fake login forms (bank/service impersonation)
- Urgent messages ("You won!", "Virus detected!")
- Fake popups and warnings
- Bank/government site clones
- Suspicious payment forms
- Social engineering tactics

Respond in STRICT JSON format ONLY:
{
  "verdict": "DANGEROUS" or "SAFE" or "SUSPICIOUS",
  "threat_score": 0-100,
  "threat_type": "phishing|scam|fake_shop|social_engineering|safe",
  "reason_kk": "Қазақша түсіндірме",
  "reason_ru": "Объяснение на русском",
  "reason_en": "English explanation",
  "indicators": ["indicator1", "indicator2"]
}"""


def _parse_ai_json(raw_text: str) -> dict:
    """AI жауабынан JSON шығарып алу."""
    if not raw_text:
        return _fallback_result("Empty AI response")

    # JSON блогын іздеу
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    # Fallback regex
    verdict_match = re.search(r"(DANGEROUS|SAFE|SUSPICIOUS)", raw_text, re.I)
    score_match = re.search(r"(\d{1,3})", raw_text)

    return {
        "verdict": verdict_match.group(1).upper() if verdict_match else "SUSPICIOUS",
        "threat_score": min(int(score_match.group(1)), 100) if score_match else 50,
        "threat_type": "unknown",
        "reason_kk": raw_text[:200],
        "reason_ru": raw_text[:200],
        "reason_en": raw_text[:200],
        "indicators": []
    }


def _fallback_result(error_msg: str) -> dict:
    return {
        "verdict": "SUSPICIOUS", "threat_score": 50, "threat_type": "unknown",
        "reason_kk": f"AI қатесі: {error_msg[:80]}",
        "reason_ru": f"Ошибка AI: {error_msg[:80]}",
        "reason_en": f"AI error: {error_msg[:80]}",
        "indicators": [], "source": "ai_error"
    }


# ============================================================
# GROQ — Негізгі AI (14,400 req/day, ~330 RPM, карта жоқ)
# ============================================================

async def _call_groq(system_prompt: str, user_content: str) -> dict | None:
    """Groq API шақыру (OpenAI-compatible)."""
    if not _groq_key():
        return None
    try:
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.1,
            "max_tokens": 500
        }
        async with httpx.AsyncClient(timeout=15) as client:
            res = await client.post(GROQ_URL, json=payload, headers={
                "Authorization": f"Bearer {_groq_key()}",
                "Content-Type": "application/json"
            })
            if res.status_code != 200:
                logger.warning(f"Groq API error: {res.status_code} {res.text[:200]}")
                return None
            data = res.json()
            raw_text = data["choices"][0]["message"]["content"]
            parsed = _parse_ai_json(raw_text)
            parsed["source"] = "groq_ai"
            return parsed
    except Exception as e:
        logger.warning(f"Groq exception: {e}")
        return None


# ============================================================
# GEMINI — Backup AI (250 req/day) + Vision (скриншот)
# ============================================================

async def _call_gemini(system_prompt: str, user_content: str) -> dict | None:
    """Gemini API шақыру (REST)."""
    if not _gemini_key():
        return None
    try:
        url = f"{GEMINI_URL}?key={_gemini_key()}"
        payload = {
            "contents": [{"parts": [{"text": f"{system_prompt}\n\n{user_content}"}]}]
        }
        async with httpx.AsyncClient(timeout=20) as client:
            res = await client.post(url, json=payload)
            if res.status_code != 200:
                return None
            data = res.json()
            if "candidates" not in data or not data["candidates"]:
                return None
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = _parse_ai_json(raw_text)
            parsed["source"] = "gemini_ai"
            return parsed
    except Exception:
        return None


async def _call_gemini_vision(system_prompt: str, image_base64: str) -> dict | None:
    """Gemini Vision API — скриншот талдау."""
    if not _gemini_key():
        logger.warning("Gemini Vision: GEMINI_API_KEY not configured")
        return None
    try:
        url = f"{GEMINI_VISION_URL}?key={_gemini_key()}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": system_prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
                ]
            }]
        }
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(url, json=payload)
            if res.status_code != 200:
                logger.warning(f"Gemini Vision error: {res.status_code} {res.text[:300]}")
                return None
            data = res.json()
            if "candidates" not in data or not data["candidates"]:
                logger.warning(f"Gemini Vision: no candidates in response")
                return None
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = _parse_ai_json(raw_text)
            parsed["source"] = "gemini_vision"
            return parsed
    except Exception as e:
        logger.warning(f"Gemini Vision exception: {e}")
        return None


# ============================================================
# PUBLIC API — Мульти-провайдер fallback chain
# ============================================================

async def analyze_url(url: str) -> dict:
    """URL тексеру: Groq → Gemini → fallback."""
    # 1. Groq (негізгі — 14,400/day)
    result = await _call_groq(SYSTEM_PROMPT_URL, f"Analyze this URL: {url}")
    if result and result.get("source") != "ai_error":
        return result

    # 2. Gemini (backup — 250/day)
    result2 = await _call_gemini(SYSTEM_PROMPT_URL, f"Сілтеме: {url}")
    if result2 and result2.get("source") != "ai_error":
        return result2

    # 3. Return Groq error if available (for debugging), else generic
    return result or _fallback_result("Барлық AI провайдерлері қолжетімсіз")


async def analyze_text(text: str) -> dict:
    """Мәтін тексеру: Groq → Gemini → fallback."""
    result = await _call_groq(SYSTEM_PROMPT_TEXT, f"Analyze this text: {text}")
    if result and result.get("source") != "ai_error":
        return result

    result2 = await _call_gemini(SYSTEM_PROMPT_TEXT, f"Мәтін: {text}")
    if result2 and result2.get("source") != "ai_error":
        return result2

    return result or _fallback_result("Барлық AI провайдерлері қолжетімсіз")


async def analyze_screenshot(image_base64: str) -> dict:
    """Скриншот тексеру: Gemini Vision (2.0-flash) → Gemini (2.5-flash) → fallback."""
    # 1. Gemini Vision model (2.0-flash — supports inline images)
    result = await _call_gemini_vision(SYSTEM_PROMPT_SCREEN, image_base64)
    if result:
        return result

    # 2. Fallback: try main Gemini model with image
    result2 = await _call_gemini_vision_fallback(SYSTEM_PROMPT_SCREEN, image_base64)
    if result2:
        return result2

    return _fallback_result("Vision AI қолжетімсіз. GEMINI_API_KEY тексеріңіз.")


async def _call_gemini_vision_fallback(system_prompt: str, image_base64: str) -> dict | None:
    """Fallback: try main Gemini model (2.5-flash) with image."""
    if not _gemini_key():
        return None
    try:
        url = f"{GEMINI_URL}?key={_gemini_key()}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": system_prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
                ]
            }]
        }
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(url, json=payload)
            if res.status_code != 200:
                logger.warning(f"Gemini Vision fallback error: {res.status_code}")
                return None
            data = res.json()
            if "candidates" not in data or not data["candidates"]:
                return None
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = _parse_ai_json(raw_text)
            parsed["source"] = "gemini_vision"
            return parsed
    except Exception as e:
        logger.warning(f"Gemini Vision fallback exception: {e}")
        return None
