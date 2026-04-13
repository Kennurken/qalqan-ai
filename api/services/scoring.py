# клауд Елдоса N1 — Qalqan AI v3.0
# Скоринг жүйесі: барлық деректерді біріктіріп, бірыңғай баға беру
# Шекаралар: ≥70 DANGEROUS (блоктау), 40-69 SUSPICIOUS (ескерту), <40 SAFE

from ..utils.i18n import get_detail


def calculate_final_verdict(
    db_results: list[dict],
    ai_result: dict | None,
    pyramid_domain_hit: dict | None,
    pyramid_text_score: float = 0.0,
    lang: str = "kk"
) -> dict:
    """
    Барлық деректерді біріктіріп, соңғы вердикт беру.

    Салмақтар:
    - DB хит: score = max(80, db_score)
    - Пирамида тізім: score = 95
    - AI DANGEROUS + score>70: score = ai_score
    - AI SUSPICIOUS: score = ai_score * 0.7
    - Бірнеше DB хит: +10 әрбір қосымша көзге
    """

    # Пирамида тізімі — ең жоғары приоритет
    if pyramid_domain_hit:
        return _format_verdict(pyramid_domain_hit, lang)

    # DB нәтижелері
    if db_results:
        best = max(db_results, key=lambda r: r.get("threat_score", 0))
        score = max(80, best.get("threat_score", 80))

        # Бірнеше DB-дан расталса, балл жоғарылайды
        if len(db_results) > 1:
            score = min(score + 10 * (len(db_results) - 1), 100)

        best["threat_score"] = score
        return _format_verdict(best, lang)

    # AI нәтижесі
    if ai_result:
        verdict = ai_result.get("verdict", "SUSPICIOUS").upper()
        score = ai_result.get("threat_score", 50)

        if verdict == "DANGEROUS" and score >= 70:
            pass  # AI бағасын сақтаймыз
        elif verdict == "SUSPICIOUS":
            score = int(score * 0.7)
        elif verdict == "SAFE":
            score = min(score, 30)

        ai_result["threat_score"] = score

        if score >= 70:
            ai_result["verdict"] = "DANGEROUS"
        elif score >= 40:
            ai_result["verdict"] = "SUSPICIOUS"
        else:
            ai_result["verdict"] = "SAFE"

        return _format_verdict(ai_result, lang)

    # Ешқандай деректер жоқ
    return {
        "verdict": "SAFE",
        "threat_score": 0,
        "threat_type": "safe",
        "source": "no_data",
        "detail": get_detail("safe", lang),
        "detail_kk": get_detail("safe", "kk"),
        "detail_ru": get_detail("safe", "ru"),
        "detail_en": get_detail("safe", "en"),
        "indicators": [],
        "cached": False
    }


def _format_verdict(result: dict, lang: str) -> dict:
    """Нәтижені стандартты форматқа келтіру."""
    threat_type = result.get("threat_type", "unknown")

    # AI-дан келген тілдік себептер немесе i18n қолдану
    reason_kk = result.get("reason_kk", get_detail(threat_type, "kk"))
    reason_ru = result.get("reason_ru", get_detail(threat_type, "ru"))
    reason_en = result.get("reason_en", get_detail(threat_type, "en"))

    # Негізгі тіл бойынша detail
    detail_map = {"kk": reason_kk, "ru": reason_ru, "en": reason_en}

    return {
        "verdict": result.get("verdict", "SUSPICIOUS"),
        "threat_score": result.get("threat_score", 50),
        "threat_type": threat_type,
        "source": result.get("source", "unknown"),
        "detail": detail_map.get(lang, reason_kk),
        "detail_kk": reason_kk,
        "detail_ru": reason_ru,
        "detail_en": reason_en,
        "indicators": result.get("indicators", []),
        "cached": result.get("cached", False)
    }
