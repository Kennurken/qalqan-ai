# Qalqan AI v3.0
# Скоринг жүйесі: барлық деректерді біріктіріп, бірыңғай баға беру
# Шекаралар: ≥70 DANGEROUS (блоктау), 40-69 SUSPICIOUS (ескерту), <40 SAFE

from ..utils.i18n import get_detail


def calculate_final_verdict(
    db_results: list[dict],
    ai_result: dict | None,
    pyramid_domain_hit: dict | None,
    domain_info: dict | None = None,
    url_features: dict | None = None,
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
        best = dict(max(db_results, key=lambda r: r.get("threat_score", 0)))
        score = max(80, best.get("threat_score", 80))

        # Бірнеше DB-дан расталса, балл жоғарылайды
        if len(db_results) > 1:
            score = min(score + 10 * (len(db_results) - 1), 100)

        best["threat_score"] = score
        return _format_verdict(best, lang)

    # AI нәтижесі
    if ai_result:
        ai_result = {**ai_result, "indicators": list(ai_result.get("indicators", []))}
        verdict = ai_result.get("verdict", "SUSPICIOUS").upper()
        score = ai_result.get("threat_score", 50)

        if verdict == "DANGEROUS" and score >= 70:
            pass
        elif verdict == "SUSPICIOUS":
            score = int(score * 0.7)
        elif verdict == "SAFE":
            score = min(score, 30)

        # Domain intelligence бонус (RDAP age + SSL)
        if domain_info:
            di_score = domain_info.get("threat_score", 0)
            score = min(score + di_score, 100)
            ai_result.setdefault("indicators", []).extend(domain_info.get("indicators", []))

        # URL features бонус (ML lexical analysis)
        if url_features:
            uf_score = url_features.get("risk_score", 0)
            if uf_score >= 60:
                score = min(score + int(uf_score * 0.3), 100)
            if url_features.get("has_mixed_script"):
                score = min(score + 20, 100)
                ai_result.setdefault("indicators", []).append("homoglyph_attack")

        ai_result["threat_score"] = score

        if score >= 70:
            ai_result["verdict"] = "DANGEROUS"
        elif score >= 40:
            ai_result["verdict"] = "SUSPICIOUS"
        else:
            ai_result["verdict"] = "SAFE"

        return _format_verdict(ai_result, lang)

    # URL features standalone fallback (when AI unavailable — prevents false negatives on high-risk URLs)
    if url_features:
        uf_score = url_features.get("risk_score", 0)
        if uf_score >= 50:
            verdict = "DANGEROUS" if uf_score >= 70 else "SUSPICIOUS"
            indicators = []
            if url_features.get("has_ip_address"): indicators.append("ip_address")
            if url_features.get("is_free_tld"): indicators.append(f"free_tld_{url_features.get('tld', '').lstrip('.')}")
            if url_features.get("has_mixed_script"): indicators.append("homoglyph_attack")
            if url_features.get("brand_edit_distance", 999) <= 2 and url_features.get("brand_match"):
                indicators.append(f"brand_impersonation_{url_features['brand_match']}")
            if url_features.get("suspicious_keyword_count", 0) > 0:
                indicators.extend(url_features.get("suspicious_keywords_found", [])[:3])
            kw_str = ", ".join(indicators[:3]) if indicators else "URL structure"
            result_uf = {
                "verdict": verdict, "threat_score": uf_score,
                "threat_type": "suspicious_infrastructure", "source": "url_features",
                "reason_kk": f"URL белгілері бойынша күдікті: {kw_str}",
                "reason_ru": f"Подозрительный URL (признаки: {kw_str})",
                "reason_en": f"Suspicious URL features: {kw_str}",
                "indicators": indicators
            }
            return _format_verdict(result_uf, lang)

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


def _risk_level(verdict: str, score: int) -> str:
    """Human-readable risk level for UI display."""
    if verdict == "DANGEROUS":
        return "critical" if score >= 90 else "high"
    if verdict == "SUSPICIOUS":
        return "medium" if score >= 50 else "low-medium"
    return "low"


def _format_verdict(result: dict, lang: str) -> dict:
    """Нәтижені стандартты форматқа келтіру."""
    threat_type = result.get("threat_type", "unknown")
    verdict = result.get("verdict", "SUSPICIOUS")
    score = result.get("threat_score", 50)

    # AI-дан келген тілдік себептер немесе i18n қолдану
    reason_kk = result.get("reason_kk", get_detail(threat_type, "kk"))
    reason_ru = result.get("reason_ru", get_detail(threat_type, "ru"))
    reason_en = result.get("reason_en", get_detail(threat_type, "en"))

    # Негізгі тіл бойынша detail
    detail_map = {"kk": reason_kk, "ru": reason_ru, "en": reason_en}

    return {
        "verdict": verdict,
        "threat_score": score,
        "risk_level": _risk_level(verdict, score),
        "threat_type": threat_type,
        "source": result.get("source", "unknown"),
        "detail": detail_map.get(lang, reason_kk),
        "detail_kk": reason_kk,
        "detail_ru": reason_ru,
        "detail_en": reason_en,
        "indicators": result.get("indicators", []),
        "cached": result.get("cached", False)
    }
