# клауд Елдоса N1 — Qalqan AI v3.0
# Қаржылық пирамида / MLM детекторы — Қазақстанға бағытталған
# Tier 1: Жергілікті база + паттерн анализ

import json
import os
import re
from .threat_db import extract_domain

_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
_pyramid_data: dict | None = None


def _load_data() -> dict:
    global _pyramid_data
    if _pyramid_data is None:
        path = os.path.join(_data_dir, "pyramid_schemes.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                _pyramid_data = json.load(f)
        except FileNotFoundError:
            _pyramid_data = {"known_schemes": [], "pyramid_indicators_kk": [],
                             "pyramid_indicators_ru": [], "pyramid_indicators_en": []}
    return _pyramid_data


def check_pyramid_domain(url: str) -> dict | None:
    """Доменді белгілі пирамидалар тізімімен салыстыру."""
    data = _load_data()
    domain = extract_domain(url)

    for scheme in data.get("known_schemes", []):
        for d in scheme.get("domains", []):
            if d in domain or domain in d:
                return {
                    "verdict": "DANGEROUS",
                    "threat_score": 95,
                    "threat_type": "pyramid",
                    "source": "pyramid_list",
                    "reason_kk": f"Белгілі қаржылық пирамида: {scheme['name']}. Ақша салмаңыз!",
                    "reason_ru": f"Известная финансовая пирамида: {scheme['name']}. Не вкладывайте деньги!",
                    "reason_en": f"Known financial pyramid: {scheme['name']}. Do not invest!"
                }
    return None


def detect_pyramid_patterns(text: str) -> float:
    """Мәтінде пирамида белгілерін іздеу. 0.0-1.0 сенімділік балы."""
    if not text:
        return 0.0

    data = _load_data()
    text_lower = text.lower()
    hits = 0
    total_indicators = 0

    for lang_key in ["pyramid_indicators_kk", "pyramid_indicators_ru", "pyramid_indicators_en"]:
        indicators = data.get(lang_key, [])
        total_indicators += len(indicators)
        for indicator in indicators:
            if indicator.lower() in text_lower:
                hits += 1

    if total_indicators == 0:
        return 0.0

    # Нормализация: 3+ хит = жоғары сенімділік
    score = min(hits / 3.0, 1.0)
    return round(score, 2)


# Жергілікті blacklist тексеру
_blacklist: set[str] | None = None


def _load_blacklist() -> set[str]:
    global _blacklist
    if _blacklist is None:
        # Болашақта blacklist.json қосылуы мүмкін
        _blacklist = set()
    return _blacklist


def check_local_blacklist(url: str) -> dict | None:
    """Жергілікті қара тізім тексеру."""
    blacklist = _load_blacklist()
    domain = extract_domain(url)
    if domain in blacklist:
        return {
            "verdict": "DANGEROUS",
            "threat_score": 90,
            "threat_type": "scam",
            "source": "local_blacklist",
            "reason_kk": "Жергілікті қара тізімде тіркелген сайт",
            "reason_ru": "Сайт в локальном чёрном списке",
            "reason_en": "Site is in local blacklist"
        }
    return None
