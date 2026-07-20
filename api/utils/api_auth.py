# Qalqan AI — Partner (B2G) API key auth
# Banks / regulators (Нацбанк Antifraud, KZ-CERT, АФМ) query via X-API-Key.
# Keys from env QALQAN_API_KEYS="key1:Halyk Bank,key2:KZ-CERT" (+ a built-in
# rate-limited demo key so the partner API is testable without config).

import os
import hmac
import hashlib

DEMO_KEY = "qalqan-demo-2026"
_DEMO_PARTNER = "Demo (rate-limited)"


def _registered_keys() -> dict[str, str]:
    """Parse QALQAN_API_KEYS env → {key: partner_name}. Demo key always present."""
    out: dict[str, str] = {DEMO_KEY: _DEMO_PARTNER}
    for pair in os.getenv("QALQAN_API_KEYS", "").split(","):
        pair = pair.strip()
        if not pair:
            continue
        if ":" in pair:
            k, name = pair.split(":", 1)
            if k.strip():
                out[k.strip()] = name.strip() or k.strip()
        else:
            out[pair] = pair
    return out


# In-memory usage counters (per process; Supabase logging optional elsewhere)
_usage: dict[str, int] = {}


def verify_api_key(key: str) -> str | None:
    """Return the partner name for a valid key, else None. Counts usage.
    Constant-time match against every registered key so response timing does not
    leak which (or how many) keys exist."""
    if not key:
        return None
    matched: str | None = None
    for k, name in _registered_keys().items():
        if hmac.compare_digest(key, k):
            matched = name
    if matched:
        _usage[key] = _usage.get(key, 0) + 1
    return matched


def is_demo(key: str) -> bool:
    return key == DEMO_KEY


def key_id(key: str) -> str:
    """Short stable id for rate-limit / logging (never the raw key)."""
    return hashlib.sha256((key or "").encode()).hexdigest()[:12]


def usage_for(key: str) -> int:
    return _usage.get(key, 0)


def partner_count() -> int:
    return len(_registered_keys())


async def verify_api_key_full(key: str) -> str | None:
    """Env-registered keys first (constant-time), then self-service trial keys
    stored hashed in Supabase (category='api_key', domain=sha256(key)[:16]).
    Returns partner name / 'Trial: <org>' / None."""
    name = verify_api_key(key)
    if name:
        return name
    if not key or not key.startswith("qk_") or len(key) > 80:
        return None
    try:
        from .http import get_client
        from .supabase import _available, _headers, _url
        if not _available():
            return None
        khash = hashlib.sha256(key.encode()).hexdigest()[:16]
        r = await get_client().get(
            f"{_url()}/rest/v1/reports", headers=_headers(),
            params={"category": "eq.api_key", "domain": f"eq.{khash}",
                    "select": "comment", "limit": "1"})
        if r.status_code == 200 and r.json():
            org = (r.json()[0].get("comment") or "").strip() or "unknown"
            _usage[key] = _usage.get(key, 0) + 1
            return f"Trial: {org[:60]}"
    except Exception:
        return None
    return None


def is_trial(partner_name: str | None) -> bool:
    return bool(partner_name and partner_name.startswith("Trial:"))
