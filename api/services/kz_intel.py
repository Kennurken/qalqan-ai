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


# Unlicensed gambling / case-battle sites banned in Kazakhstan
_GAMBLING_DOMAINS: set[str] = {
    # 1xBet family
    "1xbet.com", "1xbet.kz", "1xbet.net", "1xbet.co", "1xbet.ru", "1xbet.org",
    "1xslots.com", "1xgames.com",
    # Mostbet family
    "mostbet.com", "mostbet-kz.com", "mostbet.kz", "mostbet.ru", "mostbet.uz",
    # Bet365 / Betway / Bwin
    "bet365.com", "betway.com", "bwin.com", "bwin.net",
    # PokerDom
    "pokerdom.com", "poker-dom.com",
    # Pin-Up
    "pin-up.casino", "pin-up.bet", "pinup.kz", "pin-up.kz", "pinupcasino.com",
    # Melbet
    "melbet.com", "melbet.kz", "melbet.ru",
    # Parimatch
    "parimatch.com", "parimatch.kz", "parimatch.ru",
    # Olimp
    "olimp.bet", "olimp.com", "olimp.kz",
    # Crypto casinos
    "bcgame.com", "stake.com", "stake.us", "rollbit.com", "roobet.com",
    "duelbits.com", "jackbit.com", "cloudbet.com", "primedice.com",
    # CS case battles (underage risk)
    "hellcase.com", "hellcase.org", "farmskins.com",
    "csgo500.com", "datdrop.com", "gamdom.com", "csgoempire.com",
    "csgobig.com", "csgopolygon.com", "key-drop.com", "skinsback.com",
    # Misc casinos
    "casinogorilla.com", "vavada.com", "vavada.ru", "vavada.casino",
    "joycasino.com", "joycasino.ru",
    "volcanobet.net", "slotsvulkan.com", "vulkanvegas.com",
    # 1Win
    "1win.com", "1win.xyz", "1win.kz", "1win.ru", "1win.pro",
    # Betwinner
    "betwinner.com", "betwinner.kz", "betwinner.ru",
    # 22Bet
    "22bet.com", "22bet.kz",
    # Betsafe / Betsson / Leonbets
    "betsafe.com", "betsson.com", "leon.bet", "leonbets.com",
    # Fonbet
    "fonbet.kz", "fonbet.com", "fonbet.ru",
    # Others
    "xbet.kz", "linebet.com",
    "vbet.com", "vbet.kz",
    "betmaster.io", "betmaster.com",
    "rox.casino", "rox.kz",
    "nbet.kz", "betboro.com",
    "vulkan.com", "slot-v.com",
    "casinoroom.com", "comeon.com",
    "winline.ru", "marathonbet.com",
}

_GAMBLING_KEYWORDS = [
    "casino", "казино", "букмекер", "ставки", "слоты", "slots",
    "jackpot", "джекпот", "poker", "покер", "bet", "betting",
    "gambling", "roulette", "рулетка", "баккара", "baccarat",
    "case-battle", "кейс-батл", "case battle", "case opening",
    "sports-bet", "sportsbet", "crashgame", "crash-game",
]

# Gambling partial domain patterns (subdomain or keyword in hostname)
_GAMBLING_PARTIAL = [
    "casino", "gambl", "betting", "sportsbet", "pokerdom", "1xbet",
    "mostbet", "melbet", "parimatch", "pin-up", "pinup", "vulkan",
    "slotv", "joycasino", "rox-casino",
]


def check_gambling_domain(domain: str) -> dict | None:
    """Check if domain is an unlicensed gambling site banned in Kazakhstan."""
    if not domain:
        return None
    domain_lower = domain.lower().replace("www.", "")

    # Exact match
    if domain_lower in _GAMBLING_DOMAINS:
        return {
            "verdict": "DANGEROUS",
            "threat_score": 88,
            "threat_type": "gambling",
            "source": "kz_intel_gambling",
            "reason_kk": "ҚҰМАР ОЙЫН: Лицензиясыз букмекер немесе онлайн казино. ҚР-да тыйым салынған.",
            "reason_ru": "ГЕМБЛИНГ: Нелицензированный букмекер или онлайн-казино. Запрещён в РК.",
            "reason_en": "GAMBLING: Unlicensed bookmaker / online casino. Prohibited in Kazakhstan.",
            "indicators": [f"gambling_match_{domain_lower}", "unlicensed_kz"]
        }

    # Subdomain match (e.g. promo.1xbet.com)
    for blocked in _GAMBLING_DOMAINS:
        if domain_lower.endswith("." + blocked):
            return {
                "verdict": "DANGEROUS",
                "threat_score": 85,
                "threat_type": "gambling",
                "source": "kz_intel_gambling",
                "reason_kk": f"ҚҰМАР ОЙЫН: {blocked} сайтының тармағы — ҚР-да тыйым салынған.",
                "reason_ru": f"ГЕМБЛИНГ: Поддомен {blocked} — запрещён в РК.",
                "reason_en": f"GAMBLING: Subdomain of banned {blocked}.",
                "indicators": [f"gambling_subdomain_{blocked}", "unlicensed_kz"]
            }

    # Partial keyword match in domain (e.g. casino-xyz.com, my1xbetmirror.com)
    for kw in _GAMBLING_PARTIAL:
        if kw in domain_lower:
            return {
                "verdict": "SUSPICIOUS",
                "threat_score": 70,
                "threat_type": "gambling",
                "source": "kz_intel_gambling",
                "reason_kk": f"ҚҰМАР ОЙЫН: Домен атауында ойын сайты белгісі бар: «{kw}»",
                "reason_ru": f"ГЕМБЛИНГ: В домене обнаружен признак азартного сайта: «{kw}»",
                "reason_en": f"GAMBLING: Domain contains gambling keyword: '{kw}'",
                "indicators": [f"gambling_keyword_{kw}", "unlicensed_kz"]
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
