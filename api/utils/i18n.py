# клауд Елдоса N1 — Qalqan AI v3.0
# Интернационализация: қазақша / русский / English

TRANSLATIONS = {
    "phishing": {
        "kk": "Фишинг сайт анықталды! Жеке мәліметтеріңізді енгізбеңіз.",
        "ru": "Обнаружен фишинговый сайт! Не вводите личные данные.",
        "en": "Phishing site detected! Do not enter personal information."
    },
    "malware": {
        "kk": "Зиянды бағдарлама таратылатын сайт анықталды!",
        "ru": "Обнаружен сайт, распространяющий вредоносное ПО!",
        "en": "Malware distribution site detected!"
    },
    "pyramid": {
        "kk": "Қаржылық пирамида белгілері анықталды! Ақша салмаңыз.",
        "ru": "Обнаружены признаки финансовой пирамиды! Не вкладывайте деньги.",
        "en": "Financial pyramid scheme detected! Do not invest money."
    },
    "scam": {
        "kk": "Алаяқтық сайт анықталды! Абай болыңыз.",
        "ru": "Обнаружен мошеннический сайт! Будьте осторожны.",
        "en": "Scam site detected! Be cautious."
    },
    "gambling": {
        "kk": "Құмар ойын сайты анықталды. ҚР заңнамасына сай тыйым салынған.",
        "ru": "Обнаружен сайт азартных игр. Запрещён по законодательству РК.",
        "en": "Gambling site detected. Prohibited under KZ legislation."
    },
    "safe": {
        "kk": "Бұл сайт қауіпсіз деп танылды.",
        "ru": "Этот сайт признан безопасным.",
        "en": "This site is considered safe."
    },
    "suspicious": {
        "kk": "Бұл сайт күдікті. Абай болыңыз.",
        "ru": "Этот сайт подозрительный. Будьте осторожны.",
        "en": "This site is suspicious. Be cautious."
    },
    "unknown": {
        "kk": "Сайт туралы ақпарат жеткіліксіз.",
        "ru": "Недостаточно информации о сайте.",
        "en": "Insufficient information about this site."
    },
    "appeal_sent": {
        "kk": "Апелляция сәтті жіберілді!",
        "ru": "Апелляция успешно отправлена!",
        "en": "Appeal submitted successfully!"
    },
    "api_error": {
        "kk": "Сервер қатесі. Кейінірек қайталаңыз.",
        "ru": "Ошибка сервера. Попробуйте позже.",
        "en": "Server error. Please try again later."
    },
    "social_engineering": {
        "kk": "Әлеуметтік инженерия белгілері анықталды! Сізді алдауға тырысуда.",
        "ru": "Обнаружены признаки социальной инженерии! Вас пытаются обмануть.",
        "en": "Social engineering indicators detected! Someone is trying to deceive you."
    },
    "fake_shop": {
        "kk": "Жалған интернет-дүкен белгілері анықталды! Тапсырыс бермеңіз.",
        "ru": "Обнаружены признаки поддельного интернет-магазина! Не оформляйте заказ.",
        "en": "Fake online store indicators detected! Do not place an order."
    },
}


def t(key: str, lang: str = "kk") -> str:
    return TRANSLATIONS.get(key, {}).get(lang, TRANSLATIONS.get(key, {}).get("en", key))


def get_detail(threat_type: str, lang: str = "kk") -> str:
    type_map = {
        "phishing": "phishing",
        "malware": "malware",
        "pyramid": "pyramid",
        "scam": "scam",
        "gambling": "gambling",
        "safe": "safe",
        "suspicious": "suspicious",
        "social_engineering": "social_engineering",
        "fake_shop": "fake_shop",
    }
    key = type_map.get(threat_type, "unknown")
    return t(key, lang)
