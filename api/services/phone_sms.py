# Qalqan AI — KZ phone-number scam analysis
# Telephone fraud is KZ's #1 threat. First-class (API + mobile + bot).

import re

# KZ mobile prefixes commonly used by scam call-centers (KNB/ДКНБ reports)
_KZ_MOBILE_PREFIXES = {
    "700", "701", "702", "705", "706", "707", "708", "709",
    "747", "771", "775", "776", "777", "778",
}


def normalize_kz_phone(raw: str) -> str | None:
    """Normalize to 7XXXXXXXXXX, or None if not a valid KZ mobile number."""
    raw = re.sub(r"[\s\-()+]", "", raw or "")
    if raw.startswith("8") and len(raw) == 11:
        raw = "7" + raw[1:]
    return raw if re.match(r"^7\d{10}$", raw) else None


def analyze_phone(number: str, lang: str = "kk") -> dict:
    """Heuristic scam check for a KZ phone number."""
    raw = normalize_kz_phone(number)
    if not raw:
        kk = "Нөмір қате. ҚР форматы: +7 7XX XXX XX XX"
        ru = "Неверный номер. Формат РК: +7 7XX XXX XX XX"
        en = "Invalid number. KZ format: +7 7XX XXX XX XX"
        return {
            "verdict": "UNKNOWN", "threat_score": 0, "source": "phone_check",
            "error": "invalid_kz_phone",
            "detail": {"kk": kk, "ru": ru, "en": en}.get(lang, kk),
            "detail_kk": kk, "detail_ru": ru, "detail_en": en,
            "indicators": [],
        }

    prefix3 = raw[1:4]
    valid_mobile = prefix3 in _KZ_MOBILE_PREFIXES
    indicators: list[str] = []
    if raw == raw[0] * len(raw):
        indicators.append("all_same_digit")
    if raw[1:5] in ("7000", "7777", "0000"):
        indicators.append("vanity_number")
    if len(set(raw[1:])) <= 3:
        indicators.append("few_unique_digits")

    if indicators and valid_mobile:
        verdict, score = "SUSPICIOUS", 55
        kk = "Қайталанатын цифрлар немесе алаяқтыққа тән үлгі"
        ru = "Повторяющиеся цифры или подозрительный паттерн"
        en = "Repeated digits or a scam-typical pattern"
    elif not valid_mobile:
        verdict, score = "SUSPICIOUS", 40
        indicators.append("unknown_prefix")
        kk = "Белгісіз ҚР мобилдік префикс"
        ru = "Неизвестный мобильный префикс РК"
        en = "Unknown Kazakhstan mobile prefix"
    else:
        verdict, score = "SAFE", 10
        kk = "Стандартты ҚР мобилдік нөмір"
        ru = "Стандартный мобильный номер РК"
        en = "Standard Kazakhstan mobile number"

    return {
        "verdict": verdict, "threat_score": score, "threat_type": "scam_phone",
        "source": "phone_check",
        "formatted": f"+7 {raw[1:4]} {raw[4:7]} {raw[7:9]} {raw[9:11]}",
        "detail": {"kk": kk, "ru": ru, "en": en}.get(lang, kk),
        "detail_kk": kk, "detail_ru": ru, "detail_en": en, "indicators": indicators,
    }


def extract_urls(text: str) -> list[str]:
    """Pull candidate URLs/domains out of an SMS/message body."""
    return re.findall(
        r"(?:https?://[^\s]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)", text or "")
