# клауд Елдоса N1 — Qalqan AI v4.0
# LRU кэш: max 10,000 записей, TTL: SAFE=1h, DANGEROUS=24h

import hashlib
import time
from collections import OrderedDict

MAX_CACHE_SIZE = 10_000
TTL_SAFE = 3600
TTL_DANGEROUS = 86400
TTL_UNKNOWN = 300

_cache: OrderedDict[str, tuple[dict, float]] = OrderedDict()


def url_hash(url: str) -> str:
    return hashlib.sha256(url.lower().strip().encode()).hexdigest()


def get_cached(key: str) -> dict | None:
    if key in _cache:
        data, expires = _cache[key]
        if time.time() < expires:
            _cache.move_to_end(key)  # LRU: жаңадан қолданылған
            result = data.copy()
            result["cached"] = True
            return result
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

    # LRU eviction: ескілерді жою
    while len(_cache) >= MAX_CACHE_SIZE:
        _cache.popitem(last=False)

    _cache[key] = (result, time.time() + ttl)


def clear_cache():
    """Clear all cache entries (for benchmarking)."""
    _cache.clear()
