import os
import hashlib
import time
import json
import logging
from collections import OrderedDict

from .http import get_client

logger = logging.getLogger("qalqan")

# TTL seconds per verdict type
TTL_SAFE      = 21600   # 6h  — safe sites rarely change
TTL_SUSPICIOUS = 7200   # 2h  — re-check sooner
TTL_DANGEROUS  = 86400  # 24h — dangerous sites persist

# In-memory verdict cache fallback (used when Redis not configured or down)
_mem: OrderedDict[str, tuple[dict, float]] = OrderedDict()
MAX_MEM = 500  # smaller limit since it's just a fallback

# Separate in-memory rate-limit store — different value shape ([timestamps], expires).
# Kept apart from _mem so cache eviction and the `cache_entries` metric aren't polluted.
_rl: OrderedDict[str, tuple[list[float], float]] = OrderedDict()
MAX_RL = 5000


def url_hash(url: str) -> str:
    return hashlib.sha256(url.lower().strip().encode()).hexdigest()


def _redis_url() -> str:
    return os.getenv("UPSTASH_REDIS_REST_URL", "").rstrip("/")

def _redis_token() -> str:
    return os.getenv("UPSTASH_REDIS_REST_TOKEN", "")

def _redis_available() -> bool:
    return bool(_redis_url() and _redis_token())

def _redis_headers() -> dict:
    return {"Authorization": f"Bearer {_redis_token()}"}

def _ttl_for(verdict: str) -> int:
    v = verdict.upper()
    if "DANGEROUS" in v or "ҚАУІПТІ" in v:
        return TTL_DANGEROUS
    if "SAFE" in v or "СЕНІМДІ" in v or "ТАЗА" in v:
        return TTL_SAFE
    return TTL_SUSPICIOUS

def _redis_key(key: str) -> str:
    return f"verdict:{key[:16]}"


# ── Circuit breaker — stop hammering a dead Redis (each call would burn a full
#    timeout otherwise; under an outage that adds seconds to every request) ─────
_cb_failures = 0
_cb_open_until = 0.0
_CB_THRESHOLD = 3      # consecutive failures to trip the breaker
_CB_COOLDOWN = 30.0    # seconds to skip Redis entirely after tripping


def _redis_ok() -> bool:
    return _redis_available() and time.time() >= _cb_open_until


def _cb_fail() -> None:
    global _cb_failures, _cb_open_until
    _cb_failures += 1
    if _cb_failures >= _CB_THRESHOLD:
        _cb_open_until = time.time() + _CB_COOLDOWN
        logger.warning(f"Redis circuit OPEN {_CB_COOLDOWN}s after {_cb_failures} fails")


def _cb_ok() -> None:
    global _cb_failures
    _cb_failures = 0


# ── Redis ops (shared pooled client) ──────────────────────────────────────────

async def _redis_get(key: str) -> dict | None:
    try:
        r = await get_client().get(f"{_redis_url()}/get/{_redis_key(key)}",
                                   headers=_redis_headers(), timeout=3)
        _cb_ok()
        data = r.json()
        if data.get("result"):
            return json.loads(data["result"])
    except Exception as e:
        _cb_fail()
        logger.warning(f"Redis GET failed: {e}")
    return None


async def _redis_set_proper(key: str, value: dict, ttl: int) -> None:
    """Pipeline SET with EX — stores only the JSON payload, not the command array."""
    try:
        payload = json.dumps(value, ensure_ascii=False)
        await get_client().post(
            f"{_redis_url()}/pipeline",
            headers={**_redis_headers(), "Content-Type": "application/json"},
            json=[["SET", _redis_key(key), payload, "EX", str(ttl)]], timeout=3)
        _cb_ok()
    except Exception as e:
        _cb_fail()
        logger.warning(f"Redis SET failed: {e}")


# ── Mem fallback ──────────────────────────────────────────────────────────────

def _mem_get(key: str) -> dict | None:
    if key in _mem:
        data, expires = _mem[key]
        if time.time() < expires:
            _mem.move_to_end(key)
            result = data.copy()
            result["cached"] = True
            return result
        del _mem[key]
    return None

def _mem_set(key: str, result: dict, ttl: int) -> None:
    while len(_mem) >= MAX_MEM:
        _mem.popitem(last=False)
    _mem[key] = (result, time.time() + ttl)


# ── Public API ────────────────────────────────────────────────────────────────

async def get_cached(key: str) -> dict | None:
    # Try Redis (L2) when healthy; always fall through to the in-memory L1 cache
    if _redis_ok():
        result = await _redis_get(key)
        if result and isinstance(result, dict):
            result["cached"] = True
            return result
    return _mem_get(key)


async def set_cached(key: str, result: dict) -> None:
    ttl = _ttl_for(result.get("verdict", ""))
    if _redis_ok():
        await _redis_set_proper(key, result, ttl)
    _mem_set(key, result, ttl)  # always write mem as local L1


def clear_cache() -> None:
    _mem.clear()


async def check_rate_limit(ip: str, limit: int, endpoint: str = "", window: int = 60) -> bool:
    """True = allowed. Uses Redis INCR+EXPIRE sliding window when available, else in-memory."""
    ip_part = hashlib.md5(ip.encode()).hexdigest()[:12]
    key = f"rl:{endpoint}:{ip_part}" if endpoint else f"rl:{ip_part}:{limit}"
    if _redis_ok():
        try:
            client = get_client()
            r = await client.post(f"{_redis_url()}",
                                  headers={**_redis_headers(), "Content-Type": "application/json"},
                                  json=["INCR", key], timeout=2)
            count = r.json().get("result", 1)
            if count == 1:
                await client.post(f"{_redis_url()}",
                                  headers={**_redis_headers(), "Content-Type": "application/json"},
                                  json=["EXPIRE", key, str(window)], timeout=2)
            _cb_ok()
            return int(count) <= limit
        except Exception as e:
            _cb_fail()
            logger.warning(f"Redis rate limit failed, falling back to mem: {e}")
    # In-memory fallback (dedicated _rl store, not the verdict cache)
    now = time.time()
    if len(_rl) >= MAX_RL:
        _rl.popitem(last=False)
    if key not in _rl:
        _rl[key] = ([now], now + window)
        return True
    timestamps, expires = _rl[key]
    if now > expires:
        _rl[key] = ([now], now + window)
        return True
    timestamps = [t for t in timestamps if now - t < window]
    timestamps.append(now)
    _rl[key] = (timestamps, expires)
    return len(timestamps) <= limit


async def check_health() -> dict:
    if not _redis_available():
        return {"status": "disabled", "reason": "env vars not set", "mem_entries": len(_mem)}
    try:
        r = await get_client().get(f"{_redis_url()}/ping", headers=_redis_headers(), timeout=3)
        data = r.json()
        if data.get("result") == "PONG":
            return {"status": "ok", "mem_entries": len(_mem)}
        return {"status": "error", "response": str(data)[:80]}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:80]}


# ── One-shot guard (dedupe): True only the first time `key` is seen within ttl.
#    Redis SET NX EX when available (shared across serverless instances),
#    in-memory fallback otherwise. Used to avoid re-posting the same domain to
#    the public threat channel on every repeat check. ─────────────────────────
_once: OrderedDict[str, float] = OrderedDict()
_MAX_ONCE = 2000


async def once_per(key: str, ttl: int = 86400) -> bool:
    now = time.time()
    if _redis_ok():
        try:
            r = await get_client().post(
                f"{_redis_url()}/set/once:{key}/1",
                params={"nx": "true", "ex": str(ttl)},
                headers=_redis_headers(), timeout=2)
            if r.status_code == 200:
                _cb_ok()
                return r.json().get("result") == "OK"   # None → already existed
        except Exception:
            _cb_fail()
    # Memory fallback (per-instance)
    exp = _once.get(key)
    if exp and exp > now:
        return False
    _once[key] = now + ttl
    while len(_once) > _MAX_ONCE:
        _once.popitem(last=False)
    return True
