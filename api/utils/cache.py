import os
import hashlib
import time
import json
import logging
from collections import OrderedDict
import httpx

logger = logging.getLogger("qalqan")

# TTL seconds per verdict type
TTL_SAFE      = 21600   # 6h  — safe sites rarely change
TTL_SUSPICIOUS = 7200   # 2h  — re-check sooner
TTL_DANGEROUS  = 86400  # 24h — dangerous sites persist

# In-memory fallback (used when Redis not configured or down)
_mem: OrderedDict[str, tuple[dict, float]] = OrderedDict()
MAX_MEM = 500  # smaller limit since it's just a fallback


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


# ── Redis ops ─────────────────────────────────────────────────────────────────

async def _redis_get(key: str) -> dict | None:
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            r = await client.get(
                f"{_redis_url()}/get/{_redis_key(key)}",
                headers=_redis_headers(),
            )
            data = r.json()
            if data.get("result"):
                return json.loads(data["result"])
    except Exception as e:
        logger.warning(f"Redis GET failed: {e}")
    return None

async def _redis_set(key: str, value: dict, ttl: int) -> None:
    try:
        payload = json.dumps(value, ensure_ascii=False)
        async with httpx.AsyncClient(timeout=3) as client:
            await client.get(
                f"{_redis_url()}/set/{_redis_key(key)}/{httpx.URL(payload)}/ex/{ttl}",
                headers=_redis_headers(),
            )
    except Exception as e:
        logger.warning(f"Redis SET failed: {e}")


async def _redis_set_proper(key: str, value: dict, ttl: int) -> None:
    """POST-based SET with EX — handles large payloads and special chars safely."""
    try:
        payload = json.dumps(value, ensure_ascii=False)
        async with httpx.AsyncClient(timeout=3) as client:
            await client.post(
                f"{_redis_url()}/set/{_redis_key(key)}",
                headers={**_redis_headers(), "Content-Type": "application/json"},
                json=["SET", _redis_key(key), payload, "EX", str(ttl)],
            )
    except Exception as e:
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
    if _redis_available():
        result = await _redis_get(key)
        if result:
            result["cached"] = True
            return result
        return None
    return _mem_get(key)


async def set_cached(key: str, result: dict) -> None:
    ttl = _ttl_for(result.get("verdict", ""))
    if _redis_available():
        await _redis_set_proper(key, result, ttl)
    _mem_set(key, result, ttl)  # always write mem as local L1


def clear_cache() -> None:
    _mem.clear()


async def check_rate_limit(ip: str, limit: int, endpoint: str = "", window: int = 60) -> bool:
    """True = allowed. Uses Redis INCR+EXPIRE sliding window when available, else in-memory."""
    ip_part = hashlib.md5(ip.encode()).hexdigest()[:12]
    key = f"rl:{endpoint}:{ip_part}" if endpoint else f"rl:{ip_part}:{limit}"
    if _redis_available():
        try:
            async with httpx.AsyncClient(timeout=2) as client:
                # INCR returns new count; set TTL only on first request (NX)
                r = await client.post(
                    f"{_redis_url()}",
                    headers={**_redis_headers(), "Content-Type": "application/json"},
                    json=["INCR", key],
                )
                count = r.json().get("result", 1)
                if count == 1:
                    # First request — set expiry
                    await client.post(
                        f"{_redis_url()}",
                        headers={**_redis_headers(), "Content-Type": "application/json"},
                        json=["EXPIRE", key, str(window)],
                    )
                return int(count) <= limit
        except Exception as e:
            logger.warning(f"Redis rate limit failed, falling back to mem: {e}")
    # In-memory fallback
    now = time.time()
    if key not in _mem:
        _mem[key] = ([now], now + window)
        return True
    timestamps, expires = _mem[key]
    if time.time() > expires:
        _mem[key] = ([now], now + window)
        return True
    timestamps = [t for t in timestamps if now - t < window]
    timestamps.append(now)
    _mem[key] = (timestamps, expires)
    return len(timestamps) <= limit


async def check_health() -> dict:
    if not _redis_available():
        return {"status": "disabled", "reason": "env vars not set", "mem_entries": len(_mem)}
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            r = await client.get(
                f"{_redis_url()}/ping",
                headers=_redis_headers(),
            )
            data = r.json()
            if data.get("result") == "PONG":
                return {"status": "ok", "mem_entries": len(_mem)}
            return {"status": "error", "response": str(data)[:80]}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:80]}
