# Qalqan AI — shared async HTTP client (connection pooling)
# Replaces per-call `httpx.AsyncClient()` create/teardown (new TCP+TLS each
# time) with one pooled client reused across the warm serverless instance.
# Pass per-call `timeout=` / `follow_redirects=` as kwargs to .get()/.post().

import httpx

_client: httpx.AsyncClient | None = None

# Sensible default; individual calls override via timeout= kwarg
_DEFAULT_TIMEOUT = httpx.Timeout(10.0, connect=5.0)
_LIMITS = httpx.Limits(max_connections=100, max_keepalive_connections=20,
                       keepalive_expiry=30.0)


def get_client() -> httpx.AsyncClient:
    """Shared pooled AsyncClient. Created lazily, reused while the instance is warm."""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            timeout=_DEFAULT_TIMEOUT, limits=_LIMITS, follow_redirects=False,
            headers={"User-Agent": "QalqanAI/1.0"},
        )
    return _client


async def aclose() -> None:
    """Close the shared client (call on app shutdown)."""
    global _client
    if _client is not None and not _client.is_closed:
        await _client.aclose()
    _client = None
