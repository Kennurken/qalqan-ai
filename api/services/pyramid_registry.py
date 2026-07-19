# Qalqan AI — AFM/ARDFM financial-pyramid registry
# Name-based lookup: user types a company/brand name → match against the
# pyramid registry (АФМ/АРРФР официальный список + известные схемы).
# Complements the domain-based check_pyramid_domain() in pyramid_detector.py.

import json
import os
import re
import unicodedata
from .url_features import _levenshtein

_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
_registry: list[dict] | None = None

# Legal-form / generic tokens stripped before matching (ТОО «Финико» == Финико)
_LEGAL_FORMS = {
    "тоо", "жшс", "ип", "ооо", "оао", "зао", "ао", "пао", "llp", "llc", "ltd",
    "inc", "corp", "co", "group", "групп", "invest", "инвест", "company",
    "компания", "холдинг", "holding", "trade", "трейд", "capital", "капитал", "ag",
}

_STATUS_RU = {
    "collapsed": "крах / схема закрыта",
    "investigated": "под расследованием",
    "suspected": "подозревается в признаках пирамиды",
    "convicted": "признана пирамидой (суд)",
    "court_blocked": "заблокирована по решению суда",
    "known_scheme": "в базе известных схем",
}
_STATUS_KK = {
    "collapsed": "схема жабылды / күйреді",
    "investigated": "тергеу жүріп жатыр",
    "suspected": "пирамида белгілері бойынша күдікті",
    "convicted": "сот пирамида деп таныды",
    "court_blocked": "сот шешімімен бұғатталған",
    "known_scheme": "белгілі схемалар базасында",
}
_OFFICIAL_LINK = "https://www.gov.kz/memleket/entities/ardfm"  # АРРФР — реестр финпирамид


def _normalize(s: str) -> str:
    """Lowercase, NFKC, drop punctuation + legal-form tokens, collapse spaces."""
    s = unicodedata.normalize("NFKC", s or "").lower().strip()
    s = re.sub(r"[«»\"'`.,/\\()\[\]_+\-–—]", " ", s)
    tokens = [t for t in s.split() if t and t not in _LEGAL_FORMS]
    return " ".join(tokens)


def _load() -> list[dict]:
    global _registry
    if _registry is not None:
        return _registry
    reg: list[dict] = []

    # 1) AFM/ARDFM name-only entities
    try:
        with open(os.path.join(_data_dir, "afm_pyramids.json"), encoding="utf-8") as f:
            afm = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        afm = {"entities": []}
    for e in afm.get("entities", []):
        forms = set()
        for n in e.get("names", []) + e.get("aliases", []):
            nn = _normalize(n)
            if nn:
                forms.add(nn)
        if forms:
            reg.append({
                "name": e.get("names", ["?"])[0], "forms": forms,
                "status": e.get("status", "suspected"), "year": e.get("year"),
                "note": e.get("note", ""), "source": "afm_registry",
            })

    # 2) Reuse existing domain-based schemes (pyramid / mlm / scam_broker) as name entries
    try:
        with open(os.path.join(_data_dir, "pyramid_schemes.json"), encoding="utf-8") as f:
            ps = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        ps = {"known_schemes": []}
    for s in ps.get("known_schemes", []):
        if s.get("type") in ("pyramid", "mlm", "scam_broker"):
            forms = set()
            nn = _normalize(s.get("name", ""))
            if nn:
                forms.add(nn)
            for d in s.get("domains", []):
                root = _normalize(d.split(".")[0])
                if root:
                    forms.add(root)
            if forms:
                reg.append({
                    "name": s.get("name"), "forms": forms, "status": "known_scheme",
                    "year": None, "note": f"Известная схема ({s.get('type')})",
                    "source": "pyramid_list",
                })
    _registry = reg
    return reg


def _match_conf(q: str, form: str) -> float:
    """0.0–1.0 confidence that normalized query `q` refers to registry `form`."""
    if q == form:
        return 1.0
    if len(q) >= 4 and (q in form or form in q):
        return 0.85
    qt, ft = set(q.split()), set(form.split())
    if qt and ft and (qt & ft) and len(qt & ft) == min(len(qt), len(ft)):
        return 0.8
    a, b = q.replace(" ", ""), form.replace(" ", "")
    if len(a) >= 4 and len(b) >= 4:
        dist = _levenshtein(a, b)
        sim = 1 - dist / max(len(a), len(b))
        if dist <= 2 and sim >= 0.7:
            return round(sim, 2)
    return 0.0


def check_pyramid_name(query: str, lang: str = "ru") -> dict | None:
    """Look up a company/brand name in the pyramid registry. Returns verdict dict or None."""
    q = _normalize(query)
    if not q or len(q) < 3:
        return None
    best, best_conf = None, 0.0
    for entry in _load():
        for form in entry["forms"]:
            c = _match_conf(q, form)
            if c > best_conf:
                best_conf, best = c, entry
                if c >= 1.0:
                    break
    if best is None or best_conf < 0.7:
        return None
    return _format(best, best_conf, query, lang)


def _format(entry: dict, conf: float, query: str, lang: str) -> dict:
    status = entry["status"]
    yr = f" ({entry['year']})" if entry.get("year") else ""
    score = 95 if status in ("convicted", "court_blocked", "collapsed", "known_scheme") else 80
    verdict = "DANGEROUS" if score >= 90 else "SUSPICIOUS"
    st_ru = _STATUS_RU.get(status, status)
    st_kk = _STATUS_KK.get(status, status)
    return {
        "verdict": verdict,
        "threat_score": score,
        "threat_type": "pyramid",
        "source": entry["source"],
        "match": entry["name"],
        "confidence": conf,
        "status": status,
        "note": entry.get("note", ""),
        "official_link": _OFFICIAL_LINK,
        "reason_kk": f"«{entry['name']}»{yr} — {st_kk}. Ақша салмаңыз! Тексеру: АРРФР тізімі.",
        "reason_ru": f"«{entry['name']}»{yr} — {st_ru}. Не вкладывайте деньги! Проверьте по реестру АРРФР.",
        "reason_en": f"«{entry['name']}»{yr} — flagged in the pyramid registry. Do not invest; verify with ARDFM.",
        "indicators": ["pyramid_registry_match", f"status_{status}"],
    }


def registry_size() -> int:
    return len(_load())
