"""Deterministic demo verdicts for DEMO_MODE (known URLs).
Extracted from index.py to slim the app module."""

_DEMO_RESULTS: dict[str, dict] = {
    "kaspi.kz": {
        "verdict": "SAFE", "threat_score": 0, "risk_level": "low", "threat_type": "safe", "source": "demo_cache",
        "detail": "Сенімді сайт — Kaspi Bank ресми порталы",
        "detail_kk": "Сенімді сайт — Kaspi Bank ресми порталы",
        "detail_ru": "Надёжный сайт — официальный портал Kaspi Bank",
        "detail_en": "Trusted site — official Kaspi Bank portal",
        "indicators": [], "cached": False,
        "explanation": {"top_factors": [], "safe_factors": [{"factor": "trusted_domain", "value": "kaspi.kz", "impact": -30, "direction": "safe"}], "confidence": 0.99}
    },
    "egov.kz": {
        "verdict": "SAFE", "threat_score": 0, "risk_level": "low", "threat_type": "safe", "source": "demo_cache",
        "detail": "Сенімді сайт — eGov.kz мемлекеттік портал",
        "detail_kk": "Сенімді сайт — eGov.kz мемлекеттік портал",
        "detail_ru": "Надёжный сайт — государственный портал eGov.kz",
        "detail_en": "Trusted site — eGov.kz government portal",
        "indicators": [], "cached": False,
        "explanation": {"top_factors": [], "safe_factors": [{"factor": "trusted_domain", "value": "egov.kz", "impact": -30, "direction": "safe"}], "confidence": 0.99}
    },
    "halykbank.kz": {
        "verdict": "SAFE", "threat_score": 0, "risk_level": "low", "threat_type": "safe", "source": "demo_cache",
        "detail": "Сенімді сайт — Halyk Bank ресми порталы",
        "detail_kk": "Сенімді сайт — Halyk Bank ресми порталы",
        "detail_ru": "Надёжный сайт — официальный портал Halyk Bank",
        "detail_en": "Trusted site — official Halyk Bank portal",
        "indicators": [], "cached": False
    },
    "kaspi-login.tk": {
        "verdict": "DANGEROUS", "threat_score": 97, "risk_level": "critical", "threat_type": "phishing", "source": "demo_cache",
        "detail": "ФИШИНГ: Kaspi Bank-тың жалған сайты! Жеке деректерді енгізбеңіз!",
        "detail_kk": "ФИШИНГ: Kaspi Bank-тың жалған сайты! Жеке деректерді енгізбеңіз!",
        "detail_ru": "ФИШИНГ: Поддельный сайт Kaspi Bank! Не вводите личные данные!",
        "detail_en": "PHISHING: Fake Kaspi Bank site! Do not enter personal data!",
        "indicators": ["free_tld_tk", "brand_impersonation_kaspi", "new_domain_3d", "no_ssl"],
        "cached": False,
        "explanation": {
            "top_factors": [
                {"factor": "brand_impersonation", "value": "Similar to: kaspi (edit_dist=0)", "impact": 40, "direction": "risk"},
                {"factor": "domain_age", "value": "3 days", "impact": 35, "direction": "risk"},
                {"factor": "no_ssl", "value": "No SSL certificate", "impact": 30, "direction": "risk"},
                {"factor": "free_tld", "value": "TLD: .tk", "impact": 15, "direction": "risk"}
            ],
            "confidence": 0.99,
            "counterfactual": "Site would score <40 (SAFE) if: standard TLD AND valid SSL AND domain age > 365 days"
        }
    },
    "crowd1.com": {
        "verdict": "DANGEROUS", "threat_score": 95, "risk_level": "critical", "threat_type": "pyramid", "source": "demo_cache",
        "detail": "ҚАРЖЫЛЫҚ ПИРАМИДА: Crowd1 — танымал алаяқтық схема. Ақша салмаңыз!",
        "detail_kk": "ҚАРЖЫЛЫҚ ПИРАМИДА: Crowd1 — танымал алаяқтық схема. Ақша салмаңыз!",
        "detail_ru": "ФИНАНСОВАЯ ПИРАМИДА: Crowd1 — известная мошенническая схема. Не вкладывайте!",
        "detail_en": "FINANCIAL PYRAMID: Crowd1 — known scam scheme. Do not invest!",
        "indicators": ["pyramid_list_match", "mlm_scheme", "guaranteed_income_promise"],
        "cached": False
    },
    "1xbet.com": {
        "verdict": "DANGEROUS", "threat_score": 90, "risk_level": "critical", "threat_type": "gambling", "source": "demo_cache",
        "detail": "ҚҰМАР ОЙЫН: лицензиясыз букмекер, ҚР-да тыйым салынған",
        "detail_kk": "ҚҰМАР ОЙЫН: лицензиясыз букмекер, ҚР-да тыйым салынған",
        "detail_ru": "ГЕМБЛИНГ: нелицензированный букмекер, запрещён в РК",
        "detail_en": "GAMBLING: unlicensed bookmaker, banned in Kazakhstan",
        "indicators": ["gambling_list_match", "unlicensed_kz"],
        "cached": False
    },
    "verify-account.ml": {
        "verdict": "DANGEROUS", "threat_score": 94, "risk_level": "critical", "threat_type": "phishing", "source": "demo_cache",
        "detail": "ФИШИНГ: жалған верификация беті — жеке деректерді ұрлау",
        "detail_kk": "ФИШИНГ: жалған верификация беті — жеке деректерді ұрлау",
        "detail_ru": "ФИШИНГ: поддельная страница верификации для кражи данных",
        "detail_en": "PHISHING: fake verification page designed to steal personal data",
        "indicators": ["free_tld_ml", "suspicious_keywords", "no_ssl", "new_domain"],
        "cached": False
    },
    "egov-login.kz": {
        "verdict": "DANGEROUS", "threat_score": 98, "risk_level": "critical", "threat_type": "phishing", "source": "demo_cache",
        "detail": "ФИШИНГ: eGov.kz мемлекеттік порталының жалған сайты! ЭЦП деректерін енгізбеңіз!",
        "detail_kk": "ФИШИНГ: eGov.kz мемлекеттік порталының жалған сайты! ЭЦП деректерін енгізбеңіз!",
        "detail_ru": "ФИШИНГ: Поддельный сайт государственного портала eGov.kz! Не вводите данные ЭЦП!",
        "detail_en": "PHISHING: Fake eGov.kz government portal! Do not enter your digital signature credentials!",
        "indicators": ["phishing_list_match", "brand_impersonation_egov", "gov_portal_clone"],
        "cached": False,
        "explanation": {
            "top_factors": [
                {"factor": "known_phishing_domain", "value": "egov-login.kz — eGov impersonator", "impact": 95, "direction": "risk"},
                {"factor": "brand_impersonation", "value": "Similar to: egov (edit dist=1)", "impact": 40, "direction": "risk"},
                {"factor": "government_portal_clone", "value": "Fake government login page", "impact": 35, "direction": "risk"}
            ],
            "confidence": 0.99,
            "counterfactual": "This domain is in the Qalqan KZ phishing database — always DANGEROUS"
        }
    },
    "mostbet-kz.com": {
        "verdict": "DANGEROUS", "threat_score": 90, "risk_level": "critical", "threat_type": "gambling", "source": "demo_cache",
        "detail": "ҚҰМАР ОЙЫН: Mostbet — лицензиясыз букмекер, ҚР-да тыйым салынған",
        "detail_kk": "ҚҰМАР ОЙЫН: Mostbet — лицензиясыз букмекер, ҚР-да тыйым салынған",
        "detail_ru": "ГЕМБЛИНГ: Mostbet — нелицензированный букмекер, запрещён в РК",
        "detail_en": "GAMBLING: Mostbet — unlicensed bookmaker, prohibited in Kazakhstan",
        "indicators": ["gambling_list_match", "unlicensed_kz", "mostbet"],
        "cached": False
    },
    "finiko.com": {
        "verdict": "DANGEROUS", "threat_score": 96, "risk_level": "critical", "threat_type": "pyramid", "source": "demo_cache",
        "detail": "ҚАРЖЫЛЫҚ ПИРАМИДА: Finiko — Ресей мен Қазақстанда мыңдаған адамды алдаған схема",
        "detail_kk": "ҚАРЖЫЛЫҚ ПИРАМИДА: Finiko — Ресей мен Қазақстанда мыңдаған адамды алдаған схема",
        "detail_ru": "ФИНАНСОВАЯ ПИРАМИДА: Finiko — схема обманула тысячи людей в России и Казахстане",
        "detail_en": "FINANCIAL PYRAMID: Finiko — scheme defrauded thousands in Russia and Kazakhstan",
        "indicators": ["pyramid_list_match", "mlm_scheme", "crypto_exit_scam"],
        "cached": False
    },
    "google.com": {
        "verdict": "SAFE", "threat_score": 0, "risk_level": "low", "threat_type": "safe", "source": "demo_cache",
        "detail": "Сенімді сайт — Google ресми порталы",
        "detail_kk": "Сенімді сайт — Google ресми порталы",
        "detail_ru": "Надёжный сайт — официальный портал Google",
        "detail_en": "Trusted site — official Google portal",
        "indicators": [], "cached": False
    },
    "hellcase.com": {
        "verdict": "DANGEROUS", "threat_score": 85, "risk_level": "high", "threat_type": "gambling", "source": "demo_cache",
        "detail": "КЕЙС-БАТ: CS2 кейстерін ашу — азартты ойын, жасөспірімдерге қауіпті",
        "detail_kk": "КЕЙС-БАТ: CS2 кейстерін ашу — азартты ойын, жасөспірімдерге қауіпті",
        "detail_ru": "КЕЙС-БАТЛ: Открытие кейсов CS2 — азартная игра, опасна для несовершеннолетних",
        "detail_en": "CASE BATTLE: CS2 case opening — gambling, dangerous for minors",
        "indicators": ["case_battle_match", "gambling", "minor_risk"],
        "cached": False
    },
    "bit.ly": {
        "verdict": "SUSPICIOUS", "threat_score": 45, "risk_level": "medium", "threat_type": "suspicious_infrastructure",
        "source": "demo_cache",
        "detail": "URL-қысқартқыш: қайда апаратыны белгісіз. Шертпес бұрын тексеріңіз.",
        "detail_kk": "URL-қысқартқыш: қайда апаратыны белгісіз. Шертпес бұрын тексеріңіз.",
        "detail_ru": "URL-сокращатель: назначение скрыто. Проверьте перед переходом.",
        "detail_en": "URL shortener: destination hidden. Verify before clicking.",
        "indicators": ["url_shortener", "destination_hidden"],
        "cached": False
    },
}
