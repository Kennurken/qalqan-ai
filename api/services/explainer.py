# Qalqan AI v5.0
# Explainability (XAI) Module — SHAP/LIME-style factor explanations
# Every verdict gets: top_factors, safe_factors, counterfactual, confidence

def generate_explanation(
    url_features: dict | None,
    domain_info: dict | None,
    db_results: list[dict],
    ai_result: dict | None,
    pyramid_hit: dict | None,
    final_score: int,
    lang: str = "kk"
) -> dict:
    """Generate human-readable explanation with factor breakdown."""
    risk_factors = []
    safe_factors = []
    evidence_sources = []

    # --- Gambling hit (new tier 1.8) ---
    # NOTE: gambling_hit is not passed as separate arg (uses db_results or pyramid_hit path)
    # But check db_results for gambling source
    for db in db_results:
        if db.get("source") in ("kz_intel_gambling", "gambling_list") or db.get("threat_type") == "gambling":
            risk_factors.append({
                "factor": "gambling_blacklist",
                "value": db.get("reason_en", "Unlicensed gambling site banned in Kazakhstan"),
                "impact": 88,
                "direction": "risk"
            })
            evidence_sources.append("KZ_Gambling_DB")
            break

    # --- Pyramid hit ---
    if pyramid_hit:
        risk_factors.append({
            "factor": "known_pyramid_scheme",
            "value": pyramid_hit.get("reason_en", "Known pyramid"),
            "impact": 95,
            "direction": "risk"
        })
        evidence_sources.append("Qalqan Pyramid DB")

    # --- Database hits ---
    for db in db_results:
        src = db.get("source", "unknown")
        risk_factors.append({
            "factor": f"database_hit_{src}",
            "value": db.get("threat_type", "malicious"),
            "impact": db.get("threat_score", 80),
            "direction": "risk"
        })
        evidence_sources.append(src)

    if not db_results and not pyramid_hit:
        safe_factors.append({
            "factor": "not_in_threat_databases",
            "value": "No matches in PhishTank/SafeBrowsing/URLhaus/OpenPhish",
            "impact": -10,
            "direction": "safe"
        })

    # --- Domain intelligence ---
    if domain_info:
        details = domain_info.get("domain_details", {})
        age = details.get("domain_age_days")
        ssl = details.get("ssl", {})

        if age is not None:
            if age < 7:
                risk_factors.append({"factor": "domain_age", "value": f"{age} days", "impact": 35, "direction": "risk"})
            elif age < 30:
                risk_factors.append({"factor": "domain_age", "value": f"{age} days", "impact": 20, "direction": "risk"})
            elif age < 90:
                risk_factors.append({"factor": "domain_age", "value": f"{age} days", "impact": 10, "direction": "risk"})
            else:
                safe_factors.append({"factor": "domain_age", "value": f"{age} days", "impact": -5, "direction": "safe"})
            evidence_sources.append("RDAP")

        ssl_status = ssl.get("status")
        if ssl_status == "no_ssl":
            risk_factors.append({"factor": "no_ssl", "value": "No SSL certificate", "impact": 30, "direction": "risk"})
        elif ssl_status == "expired":
            days_exp = ssl.get("days_expired", "?")
            risk_factors.append({"factor": "ssl_expired", "value": f"SSL expired {days_exp} day(s) ago", "impact": 25, "direction": "risk"})
        elif ssl_status == "self_signed":
            risk_factors.append({"factor": "ssl_self_signed", "value": "Self-signed certificate", "impact": 15, "direction": "risk"})
        elif ssl_status == "expiring_soon":
            days_left = ssl.get("days_left", "?")
            risk_factors.append({"factor": "ssl_expiring_soon", "value": f"SSL expires in {days_left} day(s)", "impact": 8, "direction": "risk"})
        elif ssl_status == "valid":
            issuer = ssl.get("issuer", "Unknown")
            days_left = ssl.get("days_left", "?")
            if ssl.get("free_ca"):
                risk_factors.append({"factor": "free_ca_ssl", "value": f"Free CA: {issuer} (phishing indicator)", "impact": 5, "direction": "risk"})
            else:
                safe_factors.append({"factor": "valid_ssl", "value": f"Issuer: {issuer} ({days_left}d remaining)", "impact": -5, "direction": "safe"})
            evidence_sources.append("SSL_check")

    # --- URL features ---
    if url_features:
        uf = url_features
        if uf.get("has_ip_address"):
            risk_factors.append({"factor": "ip_address_url", "value": "IP instead of domain", "impact": 25, "direction": "risk"})
        if uf.get("is_free_tld"):
            risk_factors.append({"factor": "free_tld", "value": f"TLD: {uf.get('tld')}", "impact": 15, "direction": "risk"})
        if uf.get("has_mixed_script"):
            risk_factors.append({"factor": "homoglyph_attack", "value": f"Mixed script: {uf.get('homoglyph_chars', [])}", "impact": 25, "direction": "risk"})
        if uf.get("brand_edit_distance", 999) <= 2 and uf.get("brand_match"):
            risk_factors.append({"factor": "brand_impersonation", "value": f"Similar to: {uf['brand_match']} (edit dist={uf['brand_edit_distance']})", "impact": 25, "direction": "risk"})
        if uf.get("brand_in_subdomain"):
            risk_factors.append({"factor": "brand_in_subdomain", "value": f"Brand '{uf.get('brand_match')}' in subdomain", "impact": 20, "direction": "risk"})
        if uf.get("suspicious_keyword_count", 0) > 0:
            risk_factors.append({"factor": "suspicious_keywords", "value": str(uf.get("suspicious_keywords_found", [])), "impact": min(uf["suspicious_keyword_count"] * 5, 20), "direction": "risk"})
        if uf.get("has_punycode"):
            risk_factors.append({"factor": "punycode_domain", "value": "IDN/Punycode detected", "impact": 15, "direction": "risk"})
        if not uf.get("is_https"):
            risk_factors.append({"factor": "no_https", "value": "HTTP only", "impact": 10, "direction": "risk"})
        if uf.get("has_port"):
            risk_factors.append({"factor": "non_standard_port", "value": "Non-standard port in URL", "impact": 10, "direction": "risk"})
        if uf.get("is_url_shortener"):
            risk_factors.append({"factor": "url_shortener", "value": f"URL shortener: {uf.get('tld', '')} — destination hidden", "impact": 8, "direction": "risk"})
        if uf.get("has_redirect_param"):
            risk_factors.append({"factor": "redirect_parameter", "value": "Open redirect parameter detected", "impact": 8, "direction": "risk"})
        hex_cnt = uf.get("hex_encoding_count", 0)
        if hex_cnt > 10:
            risk_factors.append({"factor": "heavy_hex_encoding", "value": f"{hex_cnt} encoded chars (obfuscation)", "impact": 15, "direction": "risk"})
        elif hex_cnt > 4:
            risk_factors.append({"factor": "hex_encoding", "value": f"{hex_cnt} encoded chars", "impact": 8, "direction": "risk"})
        if uf.get("many_query_params"):
            risk_factors.append({"factor": "many_query_params", "value": f"{len(uf.get('suspicious_keywords_found', []))}+ query parameters", "impact": 5, "direction": "risk"})
        if uf.get("has_data_uri"):
            risk_factors.append({"factor": "data_uri", "value": "data:/javascript: URI — code injection risk", "impact": 30, "direction": "risk"})
        if uf.get("has_login_path"):
            risk_factors.append({"factor": "credential_harvest_path", "value": "Login/verify/account path — possible phishing", "impact": 12, "direction": "risk"})
        if uf.get("has_suspicious_subdomain"):
            risk_factors.append({"factor": "suspicious_subdomain", "value": f"Unusually long subdomain ({uf.get('longest_subdomain_length')} chars)", "impact": 8, "direction": "risk"})
        # Exact brand on free TLD (strongest impersonation signal)
        if uf.get("brand_edit_distance") == 0 and uf.get("is_free_tld") and uf.get("brand_match") and not uf.get("brand_in_subdomain"):
            risk_factors.append({"factor": "exact_brand_free_tld", "value": f"Exact match '{uf['brand_match']}' on free TLD {uf.get('tld')}", "impact": 35, "direction": "risk"})
        evidence_sources.append("URL_features")

    # --- AI verdict ---
    if ai_result and ai_result.get("source") not in (None, "ai_error"):
        ai_score = ai_result.get("threat_score", 50)
        ai_verdict = ai_result.get("verdict", "SUSPICIOUS")
        risk_factors.append({
            "factor": "ai_analysis",
            "value": f"{ai_verdict} (score={ai_score})",
            "impact": ai_score if ai_verdict == "DANGEROUS" else int(ai_score * 0.5),
            "direction": "risk" if ai_verdict != "SAFE" else "safe"
        })
        evidence_sources.append(ai_result.get("source", "AI"))

    # --- Sort by impact ---
    risk_factors.sort(key=lambda x: x["impact"], reverse=True)
    safe_factors.sort(key=lambda x: abs(x["impact"]), reverse=True)

    # --- Counterfactual ---
    counterfactual = _generate_counterfactual(risk_factors, final_score, lang)

    # --- Confidence ---
    num_sources = len(set(evidence_sources))
    confidence = min(0.5 + num_sources * 0.1, 0.99)
    if any(r["impact"] >= 80 for r in risk_factors):
        confidence = max(confidence, 0.9)

    return {
        "top_factors": risk_factors[:7],
        "safe_factors": safe_factors[:5],
        "counterfactual": counterfactual,
        "confidence": round(confidence, 2),
        "evidence_sources": list(set(evidence_sources)),
        "total_risk_signals": len(risk_factors),
        "total_safe_signals": len(safe_factors)
    }


_FACTOR_NAMES = {
    "kk": {
        "domain_age": "домен жасы > 365 күн",
        "no_ssl": "жарамды SSL сертификаты",
        "ssl_expired": "жарамды SSL сертификаты",
        "ssl_self_signed": "сенімді SSL сертификаты",
        "free_tld": "стандартты домен (.com/.kz/.org)",
        "homoglyph_attack": "кирилл/латын аралас таңбалар жоқ",
        "brand_impersonation": "брендке ұқсастық жоқ",
        "brand_in_subdomain": "субдоменде бренд жоқ",
        "ip_address_url": "тіркелген домен аты",
        "no_https": "HTTPS қосылған",
        "url_shortener": "URL қысқартқыш сервис емес",
        "non_standard_port": "стандартты порт (80/443)",
        "suspicious_keywords": "URL-де күмәнді сөздер жоқ",
        "ai_analysis": "AI анализі SAFE қайтарды",
        "known_pyramid_scheme": "пирамида базасында жоқ",
        "redirect_parameter": "redirect/goto параметрлер жоқ",
        "heavy_hex_encoding": "URL шифрлауы жоқ",
        "hex_encoding": "минималды URL кодтауы",
        "exact_brand_free_tld": "брендке сәйкес домен",
        "many_query_params": "аз query параметрлер",
        "ssl_expiring_soon": "ұзақ мерзімді SSL",
        "free_ca_ssl": "сенімді CA сертификаты",
        "gambling_blacklist": "белгілі құмар сайт емес",
        "data_uri": "data:/javascript: URI жоқ",
        "credential_harvest_path": "login/verify жолы жоқ",
        "suspicious_subdomain": "қысқа субдомен",
        "database_hit_phishtank": "PhishTank базасында жоқ",
        "database_hit_urlhaus": "URLhaus базасында жоқ",
        "not_in_threat_databases": "қауіп базаларында жоқ",
        "trusted_domain": "сенімді домен",
    },
    "ru": {
        "domain_age": "возраст домена > 365 дней",
        "no_ssl": "действующий SSL сертификат",
        "ssl_expired": "действующий SSL сертификат",
        "ssl_self_signed": "доверенный SSL сертификат",
        "free_tld": "стандартный домен (.com/.kz/.org)",
        "homoglyph_attack": "нет смешения кирилл/латиница",
        "brand_impersonation": "нет сходства с брендом",
        "brand_in_subdomain": "нет бренда в поддомене",
        "ip_address_url": "зарегистрированное доменное имя",
        "no_https": "HTTPS включён",
        "url_shortener": "не сервис сокращения URL",
        "non_standard_port": "стандартный порт (80/443)",
        "suspicious_keywords": "нет подозрительных слов в URL",
        "ai_analysis": "AI анализ вернул SAFE",
        "known_pyramid_scheme": "не в базе пирамид",
        "redirect_parameter": "нет параметров redirect/goto",
        "heavy_hex_encoding": "нет обфускации URL",
        "hex_encoding": "минимальное кодирование URL",
        "exact_brand_free_tld": "правильный домен для бренда",
        "many_query_params": "меньше query параметров",
        "ssl_expiring_soon": "долгосрочный SSL",
        "free_ca_ssl": "сертификат от надёжного CA",
        "gambling_blacklist": "не известный игровой сайт",
        "data_uri": "нет data:/javascript: URI",
        "credential_harvest_path": "нет пути login/verify",
        "suspicious_subdomain": "короткий поддомен",
        "database_hit_phishtank": "нет в базе PhishTank",
        "database_hit_urlhaus": "нет в базе URLhaus",
        "not_in_threat_databases": "нет в базах угроз",
        "trusted_domain": "доверенный домен",
    },
    "en": {
        "domain_age": "domain age > 365 days",
        "no_ssl": "valid SSL certificate",
        "ssl_expired": "valid SSL certificate",
        "ssl_self_signed": "trusted SSL certificate",
        "free_tld": "standard TLD (.com/.kz/.org)",
        "homoglyph_attack": "no mixed Cyrillic/Latin characters",
        "brand_impersonation": "no brand name similarity",
        "brand_in_subdomain": "no brand in subdomain",
        "ip_address_url": "proper domain name",
        "no_https": "HTTPS enabled",
        "url_shortener": "not a URL shortener service",
        "non_standard_port": "standard port (80/443)",
        "suspicious_keywords": "no suspicious keywords in URL",
        "ai_analysis": "AI analysis returned SAFE",
        "known_pyramid_scheme": "not in pyramid scheme database",
        "redirect_parameter": "no redirect/goto parameters",
        "heavy_hex_encoding": "no URL obfuscation encoding",
        "hex_encoding": "minimal URL encoding",
        "exact_brand_free_tld": "proper TLD for the brand",
        "many_query_params": "fewer query parameters",
        "ssl_expiring_soon": "valid long-term SSL certificate",
        "free_ca_ssl": "certificate from trusted paid CA",
        "gambling_blacklist": "not a known gambling site",
        "data_uri": "no data:/javascript: URI",
        "credential_harvest_path": "no login/verify/account path",
        "suspicious_subdomain": "shorter subdomain names",
        "database_hit_phishtank": "not in PhishTank database",
        "database_hit_urlhaus": "not in URLhaus database",
        "not_in_threat_databases": "not in threat databases",
        "trusted_domain": "trusted domain",
    },
}

_SAFE_TEMPLATE = {
    "kk": "Ағымдағы деректер бойынша сайт қауіпсіз деп саналады.",
    "ru": "Сайт считается безопасным по текущим данным.",
    "en": "This site is considered safe based on current evidence.",
}

_CF_TEMPLATE = {
    "kk": "Сайт <40 (ҚАУІПСІЗ) болар еді, егер: {}",
    "ru": "Сайт получил бы <40 (БЕЗОПАСНО), если бы: {}",
    "en": "This site would score <40 (SAFE) if: {}",
}

_CF_AND = {
    "kk": " ЖӘНЕ ",
    "ru": " И ",
    "en": " AND ",
}


def _generate_counterfactual(risk_factors: list, current_score: int, lang: str = "kk") -> str:
    """Counterfactual: 'Site would be SAFE if...'"""
    if current_score < 40:
        return _SAFE_TEMPLATE.get(lang, _SAFE_TEMPLATE["en"])

    removable = []
    remaining_score = current_score
    for f in risk_factors:
        removable.append(f["factor"])
        remaining_score -= f["impact"]
        if remaining_score < 40:
            break

    names = _FACTOR_NAMES.get(lang, _FACTOR_NAMES["en"])
    conditions = [names.get(f, f.replace("_", " ")) for f in removable[:3]]
    return _CF_TEMPLATE.get(lang, _CF_TEMPLATE["en"]).format(
        _CF_AND.get(lang, " AND ").join(conditions)
    )
