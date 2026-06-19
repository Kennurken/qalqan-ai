# Qalqan AI v5.0
# ML Feature Extraction Engine: 30+ URL features for academic-grade analysis
# Lexical + Brand Similarity + Homoglyph + Statistical features
# No HTTP request needed — pure URL string analysis

import os
import re
import json
import math
import unicodedata
from urllib.parse import urlparse, parse_qs
from collections import Counter

# --- Known URL shorteners (destination hidden — mild risk) ---
_URL_SHORTENERS = frozenset({
    "bit.ly", "bitly.com", "t.ly", "tinyurl.com", "ow.ly", "short.io",
    "rebrand.ly", "is.gd", "buff.ly", "cutt.ly", "lnk.bio", "goo.gl",
    # Fix #12: removed youtu.be (legitimate YouTube short domain — false positive)
    "fb.me", "vk.cc", "qr.ae", "rb.gy", "shorturl.at",
    "s.id", "tiny.cc", "snip.ly", "soo.gd", "clck.ru"
})

# --- Load brand data ---
_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
_brands_data = None

def _load_brands():
    global _brands_data
    if _brands_data is None:
        try:
            with open(os.path.join(_data_dir, "kz_brands.json"), "r", encoding="utf-8") as f:
                _brands_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            _brands_data = {"brands": [], "free_tlds": [], "suspicious_keywords": []}
    return _brands_data

# --- Cyrillic↔Latin homoglyph map ---
HOMOGLYPHS = {
    "\u0430": "a", "\u0435": "e", "\u043e": "o", "\u0440": "p",
    "\u0441": "c", "\u0443": "y", "\u0445": "x", "\u043d": "h",
    "\u0456": "i", "\u049b": "k", "\u04af": "u", "\u0451": "e",
    "\u0410": "A", "\u0415": "E", "\u041e": "O", "\u0420": "P",
    "\u0421": "C", "\u0423": "Y", "\u0425": "X", "\u041d": "H",
}


def extract_features(url: str) -> dict:
    """Extract 30+ ML features from URL string. Returns feature dict + risk_score."""
    try:
        parsed = urlparse(url)
    except Exception:
        # Parse failure carries no threat signal — return 0, not a biasing 50
        return {"error": "invalid_url", "risk_score": 0}

    domain = (parsed.netloc or "").lower().replace("www.", "")
    path = parsed.path or ""
    query = parsed.query or ""
    full_url = url.lower()

    features = {}

    # === 1. LENGTH FEATURES ===
    features["url_length"] = len(url)
    features["domain_length"] = len(domain)
    features["path_length"] = len(path)
    features["query_length"] = len(query)

    # === 2. CHARACTER COUNT FEATURES ===
    features["num_dots"] = full_url.count(".")
    features["num_hyphens"] = full_url.count("-")
    features["num_underscores"] = full_url.count("_")
    features["num_slashes"] = full_url.count("/")
    features["num_at"] = full_url.count("@")
    features["num_ampersand"] = full_url.count("&")
    features["num_digits"] = sum(c.isdigit() for c in full_url)
    features["digit_ratio"] = features["num_digits"] / max(len(full_url), 1)
    features["letter_ratio"] = sum(c.isalpha() for c in full_url) / max(len(full_url), 1)

    # === 3. STRUCTURAL FEATURES ===
    features["has_ip_address"] = 1 if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain) else 0
    features["has_at_symbol"] = 1 if "@" in url else 0
    features["has_double_slash"] = 1 if "//" in path else 0
    features["is_https"] = 1 if parsed.scheme == "https" else 0
    features["num_subdomains"] = max(domain.count(".") - 1, 0)
    features["num_params"] = len(parse_qs(query))
    features["has_port"] = 1 if parsed.port is not None else 0

    # === 4. TLD FEATURES ===
    data = _load_brands()
    tld = "." + domain.split(".")[-1] if "." in domain else ""
    features["tld"] = tld
    features["is_free_tld"] = 1 if tld in data.get("free_tlds", []) else 0

    # === 5. ENTROPY FEATURES ===
    features["url_entropy"] = _shannon_entropy(full_url)
    features["domain_entropy"] = _shannon_entropy(domain)

    # === 6. WORD FEATURES ===
    words = re.split(r"[^a-zA-Z]+", full_url)
    words = [w for w in words if len(w) > 1]
    features["num_words"] = len(words)
    features["longest_word_length"] = max((len(w) for w in words), default=0)
    features["avg_word_length"] = sum(len(w) for w in words) / max(len(words), 1)

    # === 7. SUSPICIOUS KEYWORDS ===
    keywords = data.get("suspicious_keywords", [])
    features["suspicious_keyword_count"] = sum(1 for kw in keywords if kw in full_url)
    features["suspicious_keywords_found"] = [kw for kw in keywords if kw in full_url]

    # === 8. PUNYCODE / IDN ===
    features["has_punycode"] = 1 if "xn--" in domain else 0

    # === 8.5. URL SHORTENER ===
    features["is_url_shortener"] = 1 if domain in _URL_SHORTENERS else 0

    # === 8.6. REDIRECT PARAMETER ===
    _redirect_params = {"redirect", "url", "goto", "next", "return", "returnurl", "redir", "out", "link", "to"}
    features["has_redirect_param"] = 1 if any(p in _redirect_params for p in parse_qs(query).keys()) else 0

    # === 8.7. HEX ENCODING ===
    # Legitimate URLs rarely have many % encodings (excluding %20 for spaces)
    hex_count = len(re.findall(r"%[0-9a-fA-F]{2}", url.replace("%20", "").replace("%2F", "").replace("%3A", "")))
    features["hex_encoding_count"] = hex_count

    # === 8.8. MANY QUERY PARAMS ===
    features["many_query_params"] = 1 if len(parse_qs(query)) > 8 else 0

    # === 8.9. FAKE LOGIN / CREDENTIAL HARVEST PATH ===
    _login_paths = {
        "login", "signin", "sign-in", "logon", "log-in", "auth", "authenticate",
        "account", "secure", "security", "verify", "verification", "confirm",
        "update", "recover", "reset", "password", "credentials", "wallet",
        "banking", "payment", "checkout", "card", "id-confirm", "identity",
        "personal-info", "user-data",
    }
    path_lower = path.lower()
    features["has_login_path"] = 1 if any(f"/{p}" in path_lower or path_lower.startswith(p) for p in _login_paths) else 0

    # === 8.10. DATA: / JAVASCRIPT: URI ===
    features["has_data_uri"] = 1 if full_url.startswith(("data:", "javascript:", "vbscript:")) else 0

    # === 8.11. EXCESSIVE SUBDOMAIN DEPTH ===
    features["subdomain_depth"] = domain.count(".")

    # === 8.12. LONG SUBDOMAIN ===
    subdomains = domain.split(".")[:-2] if domain.count(".") > 1 else []
    features["longest_subdomain_length"] = max((len(s) for s in subdomains), default=0)
    features["has_suspicious_subdomain"] = 1 if features["longest_subdomain_length"] > 20 else 0

    # === 9. HOMOGLYPH DETECTION (Cyrillic↔Latin) ===
    homoglyph_result = _detect_homoglyphs(domain)
    features["homoglyph_count"] = homoglyph_result["count"]
    features["has_mixed_script"] = homoglyph_result["has_mixed"]
    features["homoglyph_chars"] = homoglyph_result["chars"]

    # === 9.5. HOMOGLYPH/IDN BRAND IMPERSONATION (normalized domain == known brand) ===
    hg_attack = _homoglyph_brand_attack(domain)
    features["homoglyph_brand_target"] = hg_attack["target"] if hg_attack else None
    features["homoglyph_brand_normalized"] = hg_attack["normalized"] if hg_attack else None

    # === 10. BRAND SIMILARITY ===
    brand_result = _check_brand_similarity(domain, full_url)
    features["brand_match"] = brand_result["brand"]
    features["brand_edit_distance"] = brand_result["distance"]
    features["brand_in_subdomain"] = brand_result["in_subdomain"]
    features["brand_category"] = brand_result["category"]

    # === RISK SCORE CALCULATION ===
    features["risk_score"] = _calculate_risk_score(features)

    return features


def _shannon_entropy(text: str) -> float:
    """Shannon entropy — жоғары = кездейсоқ/обфускацияланған URL."""
    if not text:
        return 0.0
    freq = Counter(text)
    length = len(text)
    return -sum((c / length) * math.log2(c / length) for c in freq.values() if c > 0)


def _detect_homoglyphs(domain: str) -> dict:
    """Cyrillic↔Latin аралас символдарды анықтау."""
    has_latin = False
    has_cyrillic = False
    mixed_chars = []

    for char in domain:
        if char in ".-/":
            continue
        cat = unicodedata.category(char)
        if cat.startswith("L"):
            try:
                name = unicodedata.name(char, "")
                if "CYRILLIC" in name:
                    has_cyrillic = True
                    if char in HOMOGLYPHS:
                        mixed_chars.append(f"{char}→{HOMOGLYPHS[char]}")
                elif "LATIN" in name or char.isascii():
                    has_latin = True
            except ValueError:
                if char.isascii():
                    has_latin = True

    return {
        "count": len(mixed_chars),
        "has_mixed": 1 if (has_latin and has_cyrillic) else 0,
        "chars": mixed_chars[:5]  # Top 5
    }


def _normalize_homoglyphs(s: str) -> str:
    """Map Cyrillic/visual-confusable chars to their Latin look-alike."""
    return "".join(HOMOGLYPHS.get(ch, ch) for ch in s)


def _homoglyph_brand_attack(domain: str) -> dict | None:
    """High-confidence homoglyph/IDN impersonation: a domain that — once Cyrillic↔Latin
    homoglyphs are normalized (and punycode decoded) — collapses onto a known KZ brand.
    Example: kаspi.kz (Cyrillic 'а') → normalizes to 'kaspi' → impersonates Kaspi.
    This is the real attack the plain mixed-script flag misses."""
    if not domain:
        return None
    name_part = domain.split(".")[0]

    # Decode punycode/IDN so xn-- look-alikes become visible unicode
    decoded = name_part
    if name_part.startswith("xn--"):
        try:
            decoded = name_part.encode("ascii").decode("idna")
        except Exception:
            decoded = name_part

    normalized = _normalize_homoglyphs(decoded).lower()
    # Only meaningful when normalization actually changed the string (real homoglyph/IDN present)
    if normalized == name_part.lower():
        return None

    for brand in _load_brands().get("brands", []):
        bname = brand["name"].lower()
        if len(bname) < 4:
            continue
        if normalized == bname or _levenshtein(normalized, bname) <= 1:
            return {
                "target": brand["name"],
                "normalized": normalized,
                "category": brand.get("category", "unknown"),
            }
    return None


def _check_brand_similarity(domain: str, full_url: str) -> dict:
    """Домен мен белгілі бренд атауларын салыстыру."""
    data = _load_brands()
    best = {"brand": None, "distance": 999, "in_subdomain": 0, "category": None}

    # Доменнің негізгі бөлігі (TLD-сіз)
    domain_parts = domain.split(".")
    domain_name = domain_parts[0] if domain_parts else domain

    for brand in data.get("brands", []):
        name = brand["name"]
        # Edit distance — skip fuzzy matches on short brands (≤4 chars) to avoid
        # false typosquats (e.g. a 4-letter legit domain 1 edit from a 4-letter brand).
        # Exact matches still count for any length (brand name == domain = impersonation).
        if len(name) >= 5 or domain_name == name:
            dist = _levenshtein(domain_name, name)
            if dist < best["distance"]:
                best = {
                    "brand": name,
                    "distance": dist,
                    "in_subdomain": 0,
                    "category": brand.get("category", "unknown")
                }

        # Brand in subdomain (kaspi.evil.com)
        if len(domain_parts) > 2 and name in ".".join(domain_parts[:-2]):
            best["in_subdomain"] = 1
            best["brand"] = name
            best["distance"] = 0
            best["category"] = brand.get("category", "unknown")

        # Brand-with-separator in domain: kaspi-login.tk, login-kaspi.com
        if (domain_name.startswith(name + "-") or domain_name.endswith("-" + name)
                or domain_name.startswith(name + ".") or ("." + name + ".") in domain):
            if best["distance"] > 1:
                best = {"brand": name, "distance": 1, "in_subdomain": 0,
                        "category": brand.get("category", "unknown")}

        # Brand in path (not in domain itself)
        if name in full_url and name not in domain:
            if best["distance"] > 2:
                best["brand"] = name
                best["distance"] = 1
                best["category"] = brand.get("category", "unknown")

    return best


def _levenshtein(s1: str, s2: str) -> int:
    """Levenshtein edit distance — бренд ұқсастығын өлшеу."""
    if len(s1) < len(s2):
        return _levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (c1 != c2)))
        prev = curr
    return prev[len(s2)]


def _calculate_risk_score(features: dict) -> int:
    """Features негізінде risk score (0-100) есептеу."""
    score = 0

    # URL length
    if features["url_length"] > 200: score += 10
    elif features["url_length"] > 100: score += 5

    # IP address instead of domain
    if features["has_ip_address"]: score += 25

    # @ symbol
    if features["has_at_symbol"]: score += 20

    # Free TLD
    if features["is_free_tld"]: score += 15

    # No HTTPS
    if not features["is_https"]: score += 10

    # High entropy (obfuscated URL)
    if features["url_entropy"] > 4.5: score += 10

    # Many subdomains
    if features["num_subdomains"] > 3: score += 10
    elif features["num_subdomains"] > 1: score += 5

    # Suspicious keywords
    score += min(features["suspicious_keyword_count"] * 5, 20)

    # Punycode
    if features["has_punycode"]: score += 15

    # Homoglyphs (Cyrillic↔Latin mix)
    if features["has_mixed_script"]: score += 25
    score += min(features["homoglyph_count"] * 10, 30)

    # Homoglyph/IDN brand impersonation — normalized domain collapses onto a real
    # KZ brand (kаspi→kaspi). Confirmed attack, not a heuristic → heavy weight.
    if features.get("homoglyph_brand_target"): score += 45

    # Brand similarity (low edit distance = typosquatting)
    dist = features["brand_edit_distance"]
    if dist == 0 and features["is_free_tld"] and not features["brand_in_subdomain"]:
        score += 35  # kaspi.tk — exact brand on free TLD = confirmed impersonation
    elif dist == 0 and features["brand_in_subdomain"]:
        score += 20  # brand.evil.com — brand in subdomain
    elif 1 <= dist <= 2:
        score += 25  # kаspi → kaspi (1 edit) typosquatting
    elif 3 <= dist <= 4:
        score += 10

    # High digit ratio
    if features["digit_ratio"] > 0.3: score += 10

    # Double slash in path
    if features["has_double_slash"]: score += 5

    # Non-standard port
    if features["has_port"]: score += 10

    # URL shortener (destination hidden)
    if features["is_url_shortener"]: score += 8

    # Redirect parameter (open redirect vector)
    if features.get("has_redirect_param"): score += 8

    # Heavy hex encoding (obfuscation)
    hex_cnt = features.get("hex_encoding_count", 0)
    if hex_cnt > 10: score += 15
    elif hex_cnt > 4: score += 8

    # Many query params
    if features.get("many_query_params"): score += 5

    # Fake login/credential harvest path
    if features.get("has_login_path"):
        # Only penalize if combined with other risk signals
        if score >= 15:
            score += 12

    # data: / javascript: URI
    if features.get("has_data_uri"): score += 30

    # Excessive subdomain depth
    depth = features.get("subdomain_depth", 0)
    if depth >= 4: score += 10
    elif depth == 3: score += 5

    # Very long subdomain (often used to embed fake brand)
    if features.get("has_suspicious_subdomain"): score += 8

    return min(score, 100)
