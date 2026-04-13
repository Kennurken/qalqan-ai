# клауд Елдоса N1 — Qalqan AI v5.0
# Explainability (XAI) Module — SHAP/LIME-style factor explanations
# Every verdict gets: top_factors, safe_factors, counterfactual, confidence

def generate_explanation(
    url_features: dict | None,
    domain_info: dict | None,
    db_results: list[dict],
    ai_result: dict | None,
    pyramid_hit: dict | None,
    final_score: int
) -> dict:
    """Generate human-readable explanation with factor breakdown."""
    risk_factors = []
    safe_factors = []
    evidence_sources = []

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
            risk_factors.append({"factor": "ssl_expired", "value": "SSL certificate expired", "impact": 25, "direction": "risk"})
        elif ssl_status == "self_signed":
            risk_factors.append({"factor": "ssl_self_signed", "value": "Self-signed certificate", "impact": 15, "direction": "risk"})
        elif ssl_status == "valid":
            safe_factors.append({"factor": "valid_ssl", "value": f"Issuer: {ssl.get('issuer', 'Unknown')}", "impact": -5, "direction": "safe"})
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
    counterfactual = _generate_counterfactual(risk_factors, final_score)

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


def _generate_counterfactual(risk_factors: list, current_score: int) -> str:
    """Counterfactual: 'Site would be SAFE if...'"""
    if current_score < 40:
        return "This site is considered safe based on current evidence."

    # Find factors to remove to get below 40
    removable = []
    remaining_score = current_score
    for f in risk_factors:
        removable.append(f["factor"])
        remaining_score -= f["impact"]
        if remaining_score < 40:
            break

    factor_names = {
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
        "suspicious_keywords": "no suspicious keywords in URL",
        "ai_analysis": "AI analysis returned SAFE",
        "known_pyramid_scheme": "not in pyramid scheme database",
    }

    conditions = [factor_names.get(f, f) for f in removable[:3]]
    return f"This site would score <40 (SAFE) if: {' AND '.join(conditions)}"
