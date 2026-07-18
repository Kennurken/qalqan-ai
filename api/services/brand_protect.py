# Qalqan AI — Brand-protection / typosquatting radar.
# Given a brand's real domain (kaspi.kz), generate the phishing look-alikes that
# scammers actually register, and classify each by risk. Pure/deterministic — no
# network, no external API — so it's instant and never fails in a live demo.
# This is the B2G/B2B angle for the ДЭР economic-security framing: banks and
# agencies see their own attack surface.

import re

# Cyrillic homoglyphs (visually identical Latin → Cyrillic) — the highest-severity
# attack: the domain looks pixel-identical to the real one.
_HOMOGLYPH = {
    "a": "а", "e": "е", "o": "о", "p": "р", "c": "с", "x": "х",
    "y": "у", "k": "к", "b": "ь", "h": "н", "m": "м", "t": "т",
}

# Free / abuse-prone TLDs disproportionately used for phishing.
_FREE_TLDS = ["tk", "ml", "ga", "cf", "gq", "xyz", "top", "online", "site", "click", "shop"]
# Plausible "official-looking" alternative TLDs.
_ALT_TLDS = ["com", "net", "org", "info", "kz", "com.kz"]
# Phishing prefixes/suffixes in Kazakhstan (login/verify/bonus lures).
_AFFIXES = ["login", "secure", "verify", "account", "bonus", "cabinet", "online", "kz", "bank", "help"]

_ADJACENT = {
    "a": "sqzw", "s": "adwxze", "d": "sferxc", "k": "jlimo", "i": "uokj",
    "p": "ol", "e": "wrsd", "o": "iplk", "n": "bmhj", "l": "kop",
}


def _split_domain(domain: str) -> tuple[str, str]:
    """Return (name, tld) — name is the registrable label, tld the rest."""
    domain = (domain or "").strip().lower().replace("https://", "").replace("http://", "")
    domain = domain.split("/")[0].replace("www.", "")
    parts = domain.split(".")
    if len(parts) >= 3 and parts[-2] in ("com", "gov", "org", "net"):
        return parts[-3], ".".join(parts[-2:])   # kaspi.com.kz
    if len(parts) >= 2:
        return parts[-2], parts[-1]
    return domain, "kz"


def _homoglyph_variants(name: str, tld: str) -> list[dict]:
    out = []
    for i, ch in enumerate(name):
        if ch in _HOMOGLYPH:
            v = name[:i] + _HOMOGLYPH[ch] + name[i + 1:]
            out.append({"domain": f"{v}.{tld}", "kind": "homoglyph",
                        "risk": "critical", "note": f"кириллица «{_HOMOGLYPH[ch]}» вместо «{ch}»"})
            if len(out) >= 4:
                break
    return out


def _omission_variants(name: str, tld: str) -> list[dict]:
    out = []
    seen = set()
    for i in range(len(name)):
        v = name[:i] + name[i + 1:]
        if len(v) >= 3 and v != name and v not in seen:
            seen.add(v)
            out.append({"domain": f"{v}.{tld}", "kind": "omission",
                        "risk": "medium", "note": "пропущена буква"})
    return out[:3]


def _duplication_variants(name: str, tld: str) -> list[dict]:
    out = []
    for i in range(len(name)):
        v = name[:i + 1] + name[i] + name[i + 1:]
        out.append({"domain": f"{v}.{tld}", "kind": "duplication",
                    "risk": "medium", "note": "удвоенная буква"})
    return out[:2]


def _adjacent_variants(name: str, tld: str) -> list[dict]:
    out = []
    for i, ch in enumerate(name):
        for r in _ADJACENT.get(ch, ""):
            v = name[:i] + r + name[i + 1:]
            out.append({"domain": f"{v}.{tld}", "kind": "typo",
                        "risk": "medium", "note": "опечатка (соседняя клавиша)"})
            break
    return out[:3]


def _tld_swap_variants(name: str, tld: str) -> list[dict]:
    out = []
    for t in _FREE_TLDS[:5]:
        out.append({"domain": f"{name}.{t}", "kind": "free_tld",
                    "risk": "high", "note": f"бесплатный домен .{t} — типичен для фишинга"})
    for t in _ALT_TLDS:
        if t != tld:
            out.append({"domain": f"{name}.{t}", "kind": "tld_swap",
                        "risk": "medium", "note": f"подмена зоны .{tld} → .{t}"})
    return out[:7]


def _affix_variants(name: str, tld: str) -> list[dict]:
    out = []
    for a in _AFFIXES[:5]:
        out.append({"domain": f"{name}-{a}.{tld}", "kind": "affix",
                    "risk": "high", "note": f"приманка «{a}» в домене"})
    out.append({"domain": f"my-{name}.com", "kind": "affix",
                "risk": "medium", "note": "префикс перед брендом"})
    return out[:6]


def generate_typosquats(domain: str, limit: int = 40) -> dict:
    """Generate + classify phishing look-alikes of a brand domain."""
    name, tld = _split_domain(domain)
    if not name or not re.match(r"^[a-z0-9-]+$", name):
        return {"error": "invalid_domain", "brand": domain}

    variants: list[dict] = []
    variants += _homoglyph_variants(name, tld)
    variants += _tld_swap_variants(name, tld)
    variants += _affix_variants(name, tld)
    variants += _omission_variants(name, tld)
    variants += _duplication_variants(name, tld)
    variants += _adjacent_variants(name, tld)

    # De-dup by domain, drop the real one, cap.
    real = f"{name}.{tld}"
    seen = set()
    clean = []
    for v in variants:
        d = v["domain"]
        if d == real or d in seen or "." not in d:
            continue
        seen.add(d)
        clean.append(v)
        if len(clean) >= limit:
            break

    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    clean.sort(key=lambda v: order.get(v["risk"], 9))
    counts = {r: sum(1 for v in clean if v["risk"] == r) for r in ("critical", "high", "medium", "low")}

    return {
        "brand": real,
        "brand_name": name,
        "total": len(clean),
        "risk_counts": counts,
        "variants": clean,
        "advice_ru": ("Зарегистрируйте ключевые варианты сами, включите мониторинг доменов "
                      "и оспаривайте фишинговые регистрации через UDRP/KZ-CERT."),
        "advice_kk": ("Маңызды нұсқаларды өзіңіз тіркеңіз, домен мониторингін қосыңыз "
                      "және фишингтік тіркеулерге KZ-CERT арқылы шағымданыңыз."),
        "disclaimer_ru": "Показаны шаблоны, которые используют мошенники — не факт регистрации.",
    }
