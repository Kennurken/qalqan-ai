# Qalqan AI — Website security grade (A–F), SSL-Labs-style but consumer-friendly.
# Aggregates signals we already compute (verdict pipeline + domain intel + URL
# features) into one letter grade with a pass/warn/fail factor breakdown.

def _letter(score: int) -> tuple[str, str]:
    """0 = perfect, 100 = worst. Return (grade, color)."""
    if score <= 5:   return "A+", "#22c55e"
    if score <= 15:  return "A",  "#22c55e"
    if score <= 30:  return "B",  "#84cc16"
    if score <= 50:  return "C",  "#eab308"
    if score <= 70:  return "D",  "#f59e0b"
    if score <= 85:  return "E",  "#f97316"
    return "F", "#ef4444"


def build_grade(verdict_result: dict, domain_info: dict | None, url_feats: dict) -> dict:
    """Compose the grade card. verdict_result = pipeline output for the URL."""
    factors: list[dict] = []
    penalty = 0

    def add(status: str, label_ru: str, label_kk: str, weight: int = 0):
        nonlocal penalty
        factors.append({"status": status, "ru": label_ru, "kk": label_kk})
        penalty += weight

    verdict = (verdict_result or {}).get("verdict", "SAFE")
    tscore = (verdict_result or {}).get("threat_score", 0)

    # 1) Overall threat verdict (dominant factor)
    if verdict == "DANGEROUS":
        add("fail", "Обнаружена угроза (фишинг/скам/гемблинг)", "Қауіп анықталды", 70)
    elif verdict == "SUSPICIOUS":
        add("warn", "Подозрительные признаки", "Күдікті белгілер", 35)
    else:
        add("pass", "В известных угрозах не числится", "Белгілі қауіптерде жоқ", 0)

    dd = (domain_info or {}).get("domain_details", {}) if domain_info else {}
    ssl = dd.get("ssl", {})
    ssl_status = ssl.get("status", "unknown")
    age = dd.get("domain_age_days")

    # 2) HTTPS / TLS
    if url_feats.get("is_https"):
        if ssl_status == "valid":
            add("pass", "HTTPS с действительным сертификатом", "Жарамды сертификатты HTTPS", 0)
        elif ssl_status == "expired":
            add("fail", "SSL-сертификат просрочен", "SSL мерзімі өткен", 20)
        elif ssl_status == "self_signed":
            add("warn", "Самоподписанный сертификат", "Өзі қол қойған сертификат", 15)
        elif ssl_status == "expiring_soon":
            add("warn", "Сертификат скоро истекает", "Сертификат жақында бітеді", 5)
        else:
            add("pass", "Соединение по HTTPS", "HTTPS қосылымы", 0)
    else:
        add("fail", "Нет HTTPS — данные не шифруются", "HTTPS жоқ — деректер шифрланбайды", 25)

    # 3) Domain age
    if isinstance(age, int):
        if age < 30:
            add("fail", f"Домен создан недавно ({age} дн.) — частый признак фишинга", f"Домен жаңа ({age} күн)", 20)
        elif age < 180:
            add("warn", f"Домену {age} дн. — относительно новый", f"Доменге {age} күн", 8)
        else:
            yrs = round(age / 365, 1)
            add("pass", f"Устоявшийся домен (~{yrs} лет)", f"Тұрақты домен (~{yrs} жыл)", 0)
    else:
        add("warn", "Возраст домена не определён", "Домен жасы белгісіз", 3)

    # 4) TLD reputation
    if url_feats.get("is_free_tld"):
        add("fail", f"Бесплатная доменная зона .{url_feats.get('tld','').lstrip('.')}", "Тегін домен зонасы", 20)
    else:
        add("pass", "Обычная доменная зона", "Қалыпты домен зонасы", 0)

    # 5) Homoglyph / brand impersonation
    if url_feats.get("has_mixed_script") or url_feats.get("homoglyph_brand_target"):
        add("fail", "Гомоглиф-атака (кириллица под латиницу)", "Гомоглиф шабуылы", 30)
    elif url_feats.get("brand_edit_distance", 99) <= 2 and url_feats.get("brand_match"):
        add("warn", f"Похож на бренд «{url_feats.get('brand_match')}»", "Брендке ұқсас", 12)
    else:
        add("pass", "Признаков подделки бренда нет", "Бренд бұрмалау белгісі жоқ", 0)

    # 6) Infra: hosting/proxy
    ip = dd.get("ip_intel", {})
    if ip.get("proxy"):
        add("warn", "Хостинг через прокси/анонимайзер", "Прокси/анонимайзер хостинг", 8)
    elif ip.get("country"):
        add("pass", f"Хостинг: {ip.get('country')}", f"Хостинг: {ip.get('country')}", 0)

    penalty = max(0, min(penalty, 100))
    # Pull toward the pipeline's own score so the grade agrees with the verdict.
    combined = round(0.6 * penalty + 0.4 * tscore)
    grade, color = _letter(combined)
    return {
        "grade": grade,
        "grade_color": color,
        "risk_score": combined,
        "verdict": verdict,
        "factors": factors,
        "passed": sum(1 for f in factors if f["status"] == "pass"),
        "total_checks": len(factors),
    }
