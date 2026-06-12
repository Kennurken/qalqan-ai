import os
import hashlib
import logging
import httpx

logger = logging.getLogger("qalqan")

def _url() -> str:
    return os.getenv("SUPABASE_URL", "").rstrip("/")

def _key() -> str:
    return os.getenv("SUPABASE_SERVICE_KEY", "")

def _headers() -> dict:
    return {
        "apikey": _key(),
        "Authorization": f"Bearer {_key()}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }

def _available() -> bool:
    return bool(_url() and _key())

def _hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:16]


async def log_report(domain: str, url: str, category: str, comment: str,
                     lang: str, reporter_ip: str) -> bool:
    if not _available():
        return False
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.post(
                f"{_url()}/rest/v1/reports",
                headers=_headers(),
                json={
                    "domain": domain,
                    "url_hash": _hash(url),
                    "category": category,
                    "comment": comment[:500] if comment else None,
                    "lang": lang,
                    "reporter_ip_hash": _hash(reporter_ip),
                }
            )
            return r.status_code in (200, 201)
    except Exception as e:
        logger.warning(f"Supabase log_report failed: {e}")
        return False


async def log_appeal(domain: str, verdict_received: str, reason: str) -> bool:
    if not _available():
        return False
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.post(
                f"{_url()}/rest/v1/appeals",
                headers=_headers(),
                json={
                    "domain": domain,
                    "verdict_received": verdict_received,
                    "reason": reason[:500] if reason else None,
                }
            )
            return r.status_code in (200, 201)
    except Exception as e:
        logger.warning(f"Supabase log_appeal failed: {e}")
        return False


async def log_check(domain: str, verdict: str, score: int, top_source: str,
                    ai_used: bool, ai_skipped: bool, latency_ms: int) -> None:
    if not _available():
        return
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            await client.post(
                f"{_url()}/rest/v1/check_logs",
                headers=_headers(),
                json={
                    "domain": domain,
                    "verdict": verdict,
                    "score": score,
                    "top_source": top_source,
                    "ai_used": ai_used,
                    "ai_skipped": ai_skipped,
                    "latency_ms": latency_ms,
                }
            )
    except Exception as e:
        logger.warning(f"Supabase log_check failed: {e}")


async def check_health() -> dict:
    if not _available():
        return {"status": "disabled", "reason": "env vars not set"}
    try:
        async with httpx.AsyncClient(timeout=4) as client:
            r = await client.get(
                f"{_url()}/rest/v1/check_logs?select=id&limit=1",
                headers=_headers(),
            )
            if r.status_code == 200:
                return {"status": "ok"}
            return {"status": "error", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:80]}
