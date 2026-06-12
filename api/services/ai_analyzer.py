# Qalqan AI v3.0
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
GROQ_MODEL = "llama-3.3-70b-versatile"   # Best quality free model — 6k tokens/min, 14,400 req/day
GROQ_MODEL_FAST = "llama-3.1-8b-instant"  # Fallback if 70b rate-limited
GROQ_VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# Vision models — ordered by preference, deprecated ones removed
GEMINI_VISION_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

# --- System Prompts ---
SYSTEM_PROMPT_URL = """You are Qalqan AI — an elite cybersecurity expert system specialized in Kazakhstan's digital threat landscape.
Your mission: protect Kazakhstani users from phishing, pyramid schemes, illegal gambling, and scams.
Be DECISIVE. When signals are present, call DANGEROUS. Do not hedge.

━━━ ALWAYS DANGEROUS ━━━
GAMBLING (illegal in Kazakhstan):
  1xbet.com, mostbet.com, pin-up.casino, vavada.com, 1win.com, melbet.com, pokerdom.com, vulkan*.com, hellcase.com, rollbit.com
  ANY site matching: *bet.*, *casino.*, *slots.*, *poker.*, *gambling.*

FINANCIAL PYRAMIDS / MLM:
  crowd1.com, finiko.com, onecoin.eu, forsage.io, bitconnect.co, qubittech.ai, antares.trade
  Signals: "passive income", "guaranteed profit", "MLM", "referral bonus", "crypto signals"

PHISHING — KZ Brand Impersonation:
  Pattern: [brand]-[action].[tld] → kaspi-login.tk, egov-verify.ga, halyk-bonus.ml
  Free TLDs with KZ brands: .tk .ml .ga .cf .gq .xyz .top .pw .cc = ALWAYS phishing if KZ brand present
  Exact matches on wrong TLD: kaspi.com (not .kz), halykbank.com (not .kz) = phishing

━━━ SUSPICIOUS SIGNALS ━━━
- Brand name in subdomain: kaspi.evil.com, egov.attacker.net
- Login/verify/secure/account in path on non-official domain
- Newly registered domain (< 30 days old) with financial content
- HTTP (not HTTPS) for any financial/government service
- IP address URL: http://192.168.x.x/...
- Punycode / homoglyph: xn-- domains, Cyrillic lookalikes

━━━ ALWAYS SAFE ━━━
Official .kz government: egov.kz, salyk.kz, enbek.kz, gov.kz, minjust.gov.kz
Official KZ banks: kaspi.kz, halykbank.kz, jysanbank.kz, bcc.kz, berekebank.kz
Major global: google.com, youtube.com, github.com, wikipedia.org, microsoft.com, apple.com

━━━ SCORING GUIDE ━━━
95-100: Known blacklisted domain (pyramid, gambling, phishing DB hit)
80-94:  Strong phishing signals (free TLD + brand, homoglyph, exact brand on wrong TLD)
60-79:  Multiple suspicious signals (suspicious keywords + free TLD, brand in subdomain)
40-59:  Mild signals (new domain, HTTP only, suspicious keywords)
0-39:   Safe or insufficient evidence

Respond ONLY in this exact JSON format — no extra text:
{
  "verdict": "DANGEROUS" | "SAFE" | "SUSPICIOUS",
  "threat_score": 0-100,
  "threat_type": "phishing" | "malware" | "pyramid" | "scam" | "gambling" | "fake_shop" | "social_engineering" | "suspicious_infrastructure" | "safe",
  "reason_kk": "Нақты қазақша түсіндірме (1-2 сөйлем)",
  "reason_ru": "Конкретное объяснение на русском (1-2 предложения)",
  "reason_en": "Specific English explanation (1-2 sentences)",
  "indicators": ["specific_signal_1", "specific_signal_2"]
}"""

SYSTEM_PROMPT_TEXT = """You are Qalqan AI — a cybersecurity expert specialized in Kazakhstan.
Analyze the given text for fraud, phishing, and social engineering.

KAZAKHSTAN-SPECIFIC THREATS to detect:
- Fake Kaspi Bank messages: card blocked, suspicious transaction, bonus/cashback
- eGov (electronic government) impersonation: "your account blocked", "confirm IIN"
- "Bank security department" asking for card number, PIN, or IIN (ЖСН)
- Telegram/WhatsApp messages recruiting for MLM/pyramid: "passive income", "invest 50,000 tenge"
- Crypto investment scams: "guaranteed 30% daily profit", "double your Bitcoin"
- Fake prize/lottery: "you won 500,000 tenge", "Kaspi Gold lottery"
- Kcell/Beeline fake bonus notifications

Urgency red flags in Kazakh/Russian:
- "Шұғыл", "Дереу", "Срочно", "Немедленно" + financial request
- "Шотыңыз бұғатталды" / "Ваш счёт заблокирован" — classic bank impersonation
- "Жүлдеңізді алу үшін карта нөмірін жіберіңіз" — prize claim scam

Check for:
- Requests for personal data (passwords, card numbers, IIN/ЖСН)
- Urgency pressure ("шұғыл", "срочно", "act now", "limited time")
- Pyramid scheme indicators (пассивный доход, пассивті кіріс, guaranteed profit)
- Bank/government impersonation (Kaspi, Halyk, eGov, Kcell)
- Emotional manipulation and fear tactics

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

SYSTEM_PROMPT_SCREEN = """You are Qalqan AI — a cybersecurity expert specialized in Kazakhstan.
Analyze this screenshot for scam/fraud indicators.

KAZAKHSTAN-SPECIFIC THREATS to detect:
- Fake Kaspi Bank or Halyk Bank login/verification pages
- Fake eGov.kz login page (electronic government portal clone)
- Kaspi QR code page with suspicious text
- "Your account is blocked" alerts in Kazakh or Russian
- Fake lottery win screens ("Вы выиграли 1,000,000 тенге")
- Crypto investment/doubling scam UI
- 1xBet, Mostbet, Vulkan, Pin-Up gambling interfaces (illegal in Kazakhstan)
- Telegram "investment bot" screenshots
- Fake Beeline/Kcell account pages

General checks:
- Fake login forms (bank/service impersonation)
- Urgent messages ("You won!", "Virus detected!", "Your PC is infected!")
- Fake popups and browser warnings
- Government site clones requesting digital signature (ЭЦП/EDS)
- Suspicious payment forms asking for card details
- Social engineering tactics and pressure

Respond in STRICT JSON format ONLY:
{
  "verdict": "DANGEROUS" or "SAFE" or "SUSPICIOUS",
  "threat_score": 0-100,
  "threat_type": "phishing|scam|fake_shop|social_engineering|gambling|safe",
  "reason_kk": "Қазақша түсіндірме",
  "reason_ru": "Объяснение на русском",
  "reason_en": "English explanation",
  "indicators": ["indicator1", "indicator2"]
}"""


def _parse_ai_json(raw_text: str) -> dict:
    """AI жауабынан JSON шығарып алу — depth-tracked extraction."""
    if not raw_text:
        return _fallback_result("Empty AI response")

    # Try direct parse first
    try:
        return json.loads(raw_text.strip())
    except json.JSONDecodeError:
        pass

    # Depth-tracking JSON extraction (handles nested objects correctly)
    start = raw_text.find("{")
    if start != -1:
        depth = 0
        for i, c in enumerate(raw_text[start:], start):
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(raw_text[start:i + 1])
                    except json.JSONDecodeError:
                        break

    # Last-resort: extract verdict + score from plain text
    verdict_match = re.search(r"\b(DANGEROUS|SAFE|SUSPICIOUS)\b", raw_text, re.I)
    score_match = re.search(r"\b(\d{1,3})\b", raw_text)

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

async def _call_groq(system_prompt: str, user_content: str, fast: bool = False) -> dict | None:
    """Groq API шақыру (OpenAI-compatible). fast=True uses 8b model for rate-limit fallback."""
    if not _groq_key():
        return None
    model = GROQ_MODEL_FAST if fast else GROQ_MODEL
    try:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.05,   # Near-deterministic for security classification
            "max_tokens": 512,
            "response_format": {"type": "json_object"}  # Force JSON output
        }
        async with httpx.AsyncClient(timeout=15) as client:
            res = await client.post(GROQ_URL, json=payload, headers={
                "Authorization": f"Bearer {_groq_key()}",
                "Content-Type": "application/json"
            })
            if res.status_code == 429 and not fast:
                # 70b rate-limited → retry with 8b fast model
                logger.warning(f"Groq 70b rate limited, falling back to 8b")
                return await _call_groq(system_prompt, user_content, fast=True)
            if res.status_code != 200:
                logger.warning(f"Groq API error: {res.status_code} {res.text[:200]}")
                return None
            data = res.json()
            raw_text = data["choices"][0]["message"]["content"]
            parsed = _parse_ai_json(raw_text)
            parsed["source"] = "groq_ai"
            parsed["model"] = model
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

def _sanitize_for_prompt(text: str, max_len: int = 300) -> str:
    """Fix #11: Strip prompt injection attempts from URL before inserting into AI prompt.
    Removes newlines, common injection patterns, limits length."""
    # Remove newlines/carriage returns (main injection vector)
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    # Remove common injection prefixes
    _inject_patterns = [
        "ignore previous", "ignore above", "disregard", "forget instructions",
        "new instructions", "system:", "assistant:", "user:", "human:",
        "###", "---", "===", "```"
    ]
    text_lower = text.lower()
    for pat in _inject_patterns:
        if pat in text_lower:
            # Replace with sanitized version
            text = text[:text_lower.index(pat)] + "[sanitized]"
            break
    return text[:max_len]


def _build_url_context(url: str, features: dict | None) -> str:
    """Build enriched prompt with URL feature signals for better AI accuracy."""
    # Fix #11: sanitize URL before inserting into prompt
    safe_url = _sanitize_for_prompt(url, max_len=300)
    msg = f"Analyze this URL for cybersecurity threats: {safe_url}"
    if not features:
        return msg

    flags = []
    risk = features.get("risk_score", 0)

    if features.get("has_ip_address"):
        flags.append("⚠️  IP address used instead of domain name")
    if features.get("has_mixed_script"):
        chars = features.get("homoglyph_chars", [])
        flags.append(f"🚨 HOMOGLYPH ATTACK — mixed Cyrillic/Latin: {chars}")
    if features.get("brand_edit_distance", 999) <= 2 and features.get("brand_match"):
        ed = features.get("brand_edit_distance")
        brand = features.get("brand_match")
        flags.append(f"🚨 BRAND IMPERSONATION — '{brand}' (edit_distance={ed})")
    if features.get("brand_edit_distance") == 0 and features.get("is_free_tld") and features.get("brand_match"):
        flags.append(f"🚨 EXACT BRAND ON FREE TLD — '{features['brand_match']}' on .{features.get('tld')} = definite phishing")
    if features.get("brand_in_subdomain") and features.get("brand_match"):
        flags.append(f"⚠️  Brand '{features['brand_match']}' appears in subdomain (subdomain hijack pattern)")
    if features.get("is_free_tld"):
        flags.append(f"⚠️  Free/suspicious TLD: .{features.get('tld')} (commonly used in phishing)")
    if features.get("suspicious_keyword_count", 0) > 0:
        kws = features.get("suspicious_keywords_found", [])[:4]
        flags.append(f"⚠️  Suspicious keywords in URL: {kws}")
    if features.get("has_login_path"):
        flags.append("⚠️  Login/verify/account path detected (credential harvesting pattern)")
    if features.get("has_data_uri"):
        flags.append("🚨 DATA URI / javascript: — code injection risk")
    if features.get("has_punycode"):
        flags.append("⚠️  Punycode/IDN encoding detected")
    if not features.get("is_https"):
        flags.append("⚠️  HTTP only — no encryption")
    if features.get("has_suspicious_subdomain"):
        length = features.get("longest_subdomain_length", 0)
        flags.append(f"⚠️  Unusually long subdomain ({length} chars)")
    if features.get("is_url_shortener"):
        flags.append("⚠️  URL shortener service — hides final destination")
    if features.get("has_redirect_param"):
        flags.append("⚠️  Open redirect parameter (redirect=/goto=/url=)")
    hex_cnt = features.get("hex_encoding_count", 0)
    if hex_cnt > 4:
        flags.append(f"⚠️  Heavy URL hex-encoding ({hex_cnt} chars) — obfuscation attempt")

    if flags:
        msg += "\n\n📊 URL FEATURE ANALYSIS RESULTS:\n" + "\n".join(flags)
        msg += f"\n\nURL risk score from lexical analysis: {risk}/100"
        if risk >= 70 or any("🚨" in f for f in flags):
            msg += "\n\n⚡ CRITICAL: Multiple high-confidence threat signals detected. This URL should be classified as DANGEROUS."
        elif risk >= 40:
            msg += "\n\nModerate risk signals present. Classify conservatively."

    return msg


async def analyze_url(url: str, context: dict | None = None) -> dict:
    """URL тексеру: Groq 70b → Gemini → Groq 8b fallback."""
    user_msg = _build_url_context(url, context)

    # 1. Groq 70b (негізгі — best quality)
    result = await _call_groq(SYSTEM_PROMPT_URL, user_msg)
    if result and result.get("source") != "ai_error":
        return result

    # 2. Gemini (backup — 250/day)
    result2 = await _call_gemini(SYSTEM_PROMPT_URL, user_msg)
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


async def _call_groq_vision(system_prompt: str, image_base64: str) -> dict | None:
    """Groq Vision API — tries multiple vision models."""
    if not _groq_key():
        logger.warning("Groq Vision: GROQ_API_KEY not configured")
        return None

    vision_models = [
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "llama-3.2-90b-vision-preview",  # legacy fallback
    ]

    for model in vision_models:
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": [
                        {"type": "text", "text": "Analyze this screenshot for scam, phishing, or fraud indicators. Respond in the JSON format specified:"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]}
                ],
                "temperature": 0.1,
                "max_tokens": 500
            }
            async with httpx.AsyncClient(timeout=30) as client:
                res = await client.post(GROQ_URL, json=payload, headers={
                    "Authorization": f"Bearer {_groq_key()}",
                    "Content-Type": "application/json"
                })
                if res.status_code != 200:
                    logger.warning(f"Groq Vision {model}: {res.status_code} {res.text[:200]}")
                    continue
                data = res.json()
                raw_text = data["choices"][0]["message"]["content"]
                parsed = _parse_ai_json(raw_text)
                parsed["source"] = "groq_vision"
                logger.info(f"Groq Vision success with model: {model}")
                return parsed
        except Exception as e:
            logger.warning(f"Groq Vision {model} exception: {e}")
            continue

    return None


async def analyze_screenshot(image_base64: str) -> dict:
    """Скриншот тексеру: Groq Vision → Gemini Vision → fallback."""
    # 1. Groq Vision (primary — llama-3.2-90b-vision)
    result = await _call_groq_vision(SYSTEM_PROMPT_SCREEN, image_base64)
    if result:
        return result

    # 2. Gemini Vision (fallback — tries multiple models)
    result2, error_detail = await _call_gemini_vision_with_detail(SYSTEM_PROMPT_SCREEN, image_base64)
    if result2:
        return result2

    return _fallback_result(f"Vision AI қатесі: {error_detail}")


async def _call_gemini_vision_with_detail(system_prompt: str, image_base64: str) -> tuple[dict | None, str]:
    """Gemini Vision with model fallback chain."""
    if not _gemini_key():
        return None, "GEMINI_API_KEY орнатылмаған"

    models_to_try = GEMINI_VISION_MODELS
    last_error = ""

    for model in models_to_try:
        try:
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={_gemini_key()}"
            payload = {
                "contents": [{
                    "parts": [
                        {"text": system_prompt},
                        {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
                    ]
                }]
            }
            async with httpx.AsyncClient(timeout=30) as client:
                res = await client.post(api_url, json=payload)
                if res.status_code == 404:
                    last_error = f"{model}: 404 not found"
                    logger.info(f"Gemini Vision: model {model} not found, trying next...")
                    continue
                if res.status_code != 200:
                    last_error = f"{model}: {res.status_code}"
                    logger.warning(f"Gemini Vision {model} error: {res.status_code} {res.text[:200]}")
                    continue
                data = res.json()
                if "candidates" not in data or not data["candidates"]:
                    last_error = f"{model}: no candidates"
                    continue
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = _parse_ai_json(raw_text)
                parsed["source"] = "gemini_vision"
                logger.info(f"Gemini Vision success with model: {model}")
                return parsed, ""
        except Exception as e:
            last_error = f"{model}: {str(e)[:80]}"
            logger.warning(f"Gemini Vision {model} exception: {e}")
            continue

    return None, f"Барлық модельдер сәтсіз: {last_error}"
