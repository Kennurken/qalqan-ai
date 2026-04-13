# клауд Елдоса N1 — Qalqan AI v3.0
# Кэш-слой: in-memory для serverless (сбрасывается при cold start)
# TTL: SAFE=1h, DANGEROUS=24h, UNKNOWN=5min

import hashlib
import time

_cache: dict[str, tuple[dict, float]] = {}

TTL_SAFE = 3600
TTL_DANGEROUS = 86400
TTL_UNKNOWN = 300


def url_hash(url: str) -> str:
    return hashlib.sha256(url.lower().strip().encode()).hexdigest()


def get_cached(key: str) -> dict | None:
    if key in _cache:
        data, expires = _cache[key]
        if time.time() < expires:
            data["cached"] = True
            return data
        del _cache[key]
    return None


def set_cached(key: str, result: dict):
    verdict = result.get("verdict", "").upper()
    if "DANGEROUS" in verdict or "ҚАУІПТІ" in verdict:
        ttl = TTL_DANGEROUS
    elif "SAFE" in verdict or "СЕНІМДІ" in verdict or "ТАЗА" in verdict:
        ttl = TTL_SAFE
    else:
        ttl = TTL_UNKNOWN
    _cache[key] = (result, time.time() + ttl)


def clear_cache():
    _cache.clear()
