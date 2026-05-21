# Qalqan AI v5.0
# KZ Intelligence: Казахстандық әлеуметтік инженерия паттерндерін анықтау
# Дереккөз: api/data/kz_phishing_patterns.json

import json
import os
import logging

logger = logging.getLogger("qalqan")

_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
_kz_patterns: dict | None = None


def _load_patterns() -> dict:
    global _kz_patterns
    if _kz_patterns is None:
        try:
            path = os.path.join(_data_dir, "kz_phishing_patterns.json")
            with open(path, "r", encoding="utf-8") as f:
                _kz_patterns = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            _kz_patterns = {}
    return _kz_patterns


_HARDCODED_KZ_PATTERNS = {
    "kk": [
        "карта нөміріңізді жіберіңіз", "жсн енгізіңіз", "құпиясөзді беріңіз",
        "kaspi gold картаңыз", "шотыңыз бұғатталды", "жүлдеңізді алу үшін",
        "сіз ұтып алдыңыз", "тез арада жіберіңіз", "уақыт шектеулі",
        "банк қызметкері", "тегін ақша", "пассивті кіріс", "криптовалюта тегін",
        "инвестиция салыңыз", "пайда гарантиялы"
    ],
    "ru": [
        "отправьте номер карты", "введите иин", "назовите пароль",
        "ваш счёт заблокирован", "служба безопасности банка",
        "вы выиграли", "для получения приза", "срочно переведите",
        "пассивный доход", "гарантированный заработок", "удвоение средств",
        "бесплатная криптовалюта", "вложи и получай", "заработок без вложений",
        "служба безопасности kaspi", "звонит сотрудник банка"
    ]
}


def check_kz_impersonation_url(domain: str) -> dict | None:
    """
    URL домені Қазақстан брендтерінің жалған сайттар тізіміне кіреді ме — тексеру.
    Returns DANGEROUS result if domain matches known KZ phishing domains.
    """
    if not domain:
        return None

    patterns = _load_patterns()
    domain_lower = domain.lower().replace("www.", "")

    _IMPERSONATION_KEYS = {
        "egov_impersonation": ("egov", "eGov мемлекеттік порталы"),
        "kaspi_impersonation": ("kaspi", "Kaspi Bank"),
        "halyk_impersonation": ("halyk", "Halyk Bank / Homebank"),
        "jysan_impersonation": ("jysan", "Jysan Bank"),
        "kcell_beeline_impersonation": ("kcell", "Kcell / Beeline"),
    }

    for key, (brand_id, brand_name) in _IMPERSONATION_KEYS.items():
        for fake_domain in patterns.get(key, []):
            if domain_lower == fake_domain.lower() or domain_lower.endswith("." + fake_domain.lower()):
                return {
                    "verdict": "DANGEROUS",
                    "threat_score": 97,
                    "threat_type": "phishing",
                    "source": "kz_intel",
                    "reason_kk": f"ФИШИНГ: {brand_name} ресми сайтының жалған домені анықталды!",
                    "reason_ru": f"ФИШИНГ: Обнаружен поддельный домен официального сайта {brand_name}!",
                    "reason_en": f"PHISHING: Fake domain impersonating {brand_name} detected!",
                    "indicators": [f"kz_impersonation_{brand_id}", f"fake_domain_{fake_domain}"]
                }

    return None


def check_kz_social_engineering(text: str) -> dict | None:
    """
    Мәтінде Қазақстандық алаяқтық паттерндерін тексеру.
    Telegram/WhatsApp хабарламаларындағы жіп-жіп жалғанған сөздер.
    Returns None if no patterns found.
    """
    if not text or len(text) < 10:
        return None

    patterns = _load_patterns()
    text_lower = text.lower()
    hits = []
    score = 0

    # KK social engineering patterns (from JSON)
    for pattern in patterns.get("social_engineering_kk", []):
        if pattern.lower() in text_lower:
            hits.append(f"kk:{pattern[:30]}")
            score += 20

    # KK hardcoded patterns (high-confidence)
    for pattern in _HARDCODED_KZ_PATTERNS["kk"]:
        if pattern.lower() in text_lower and f"kk:{pattern[:30]}" not in hits:
            hits.append(f"kk:{pattern[:30]}")
            score += 25  # Higher confidence — specific KZ scam phrases

    # RU social engineering patterns (from JSON)
    for pattern in patterns.get("social_engineering_ru", []):
        if pattern.lower() in text_lower:
            hits.append(f"ru:{pattern[:30]}")
            score += 15

    # RU hardcoded patterns (high-confidence)
    for pattern in _HARDCODED_KZ_PATTERNS["ru"]:
        if pattern.lower() in text_lower and f"ru:{pattern[:30]}" not in hits:
            hits.append(f"ru:{pattern[:30]}")
            score += 20

    # Telegram scam patterns
    for pattern in patterns.get("telegram_scam_patterns", []):
        if pattern.lower() in text_lower:
            hits.append(f"tg:{pattern[:30]}")
            score += 15

    # WhatsApp scam patterns (short words — match with word boundary check)
    for pattern in patterns.get("whatsapp_scam_patterns", []):
        if f" {pattern.lower()} " in f" {text_lower} ":
            hits.append(f"wa:{pattern}")
            score += 10

    # Pyramid text patterns
    for pattern in patterns.get("pyramid_text_patterns", []):
        if pattern.lower() in text_lower:
            hits.append(f"pyramid:{pattern[:30]}")
            score += 12

    if not hits:
        return None

    score = min(score, 95)
    verdict = "DANGEROUS" if score >= 60 else "SUSPICIOUS"

    hit_count = len(hits)
    return {
        "verdict": verdict,
        "threat_score": score,
        "threat_type": "social_engineering",
        "source": "kz_intel",
        "reason_kk": f"Қазақстандық алаяқтық паттерні анықталды ({hit_count} белгі)",
        "reason_ru": f"Обнаружен казахстанский паттерн мошенничества ({hit_count} признаков)",
        "reason_en": f"Kazakhstan social engineering pattern detected ({hit_count} signals)",
        "indicators": hits[:7]
    }
