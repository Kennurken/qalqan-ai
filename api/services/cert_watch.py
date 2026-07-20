# Qalqan AI — Certificate-transparency watch (crt.sh).
# Phishing infrastructure gets an SSL cert before it gets victims: CT logs are
# public, so "every new cert whose name contains the brand keyword" is an early
# warning that no blacklist can give. crt.sh is free but slow and flaky, so:
# hard timeout, 1h cache per brand, graceful degradation, best-effort in cron.

import logging
from datetime import datetime, timedelta

from ..utils.cache import get_cached, set_cached
from ..utils.http import get_client
from .brand_protect import _split_domain

logger = logging.getLogger("qalqan")

_CRTSH = "https://crt.sh/"
_WINDOW_DAYS = 7
_MAX_RESULTS = 20


def _fresh(not_before: str | None, days: int = _WINDOW_DAYS) -> bool:
    if not not_before:
        return False
    try:
        dt = datetime.fromisoformat(not_before.replace("T", " ").split(".")[0])
        return dt >= datetime.utcnow() - timedelta(days=days)
    except ValueError:
        return False


async def recent_brand_certs(domain: str) -> dict:
    """Fresh (7d) certificates whose names contain the brand keyword but are NOT
    the brand's own domain — candidate phishing infrastructure.
    Returns {"status": "ok"|"unavailable", ...}; cached 1-2h per brand."""
    name, tld = _split_domain(domain)
    if not name or len(name) < 3:
        return {"status": "error", "error": "invalid_domain"}
    legit = f"{name}.{tld}"

    cache_key = f"certs:{name}"
    cached = await get_cached(cache_key)
    if cached and cached.get("status") == "ok":
        return cached

    entries = None
    for attempt in range(2):   # crt.sh 5xx-flaps; one retry is usually enough
        try:
            r = await get_client().get(
                _CRTSH, params={"q": f"%{name}%", "output": "json"},
                timeout=20, follow_redirects=True)
            if r.status_code == 200:
                entries = r.json()
                break
            last_code = r.status_code
        except Exception as e:
            logger.info(f"cert_watch crt.sh attempt {attempt+1} failed for {name}: {e}")
            last_code = None
    if entries is None:
        return {"status": "unavailable", "source": "crt.sh", "code": last_code}

    hits = _filter_entries(entries, name, legit)

    result = {"status": "ok", "brand": legit, "window_days": _WINDOW_DAYS,
              "count": len(hits), "certs": hits,
              "note_ru": ("Свежие SSL-сертификаты из публичных CT-логов, содержащие имя бренда. "
                          "Новый сертификат на чужом домене — ранний признак подготовки фишинга.")}
    await set_cached(cache_key, dict(result))
    return result


def _filter_entries(entries: list, name: str, legit: str) -> list[dict]:
    """Pure filter: fresh certs, brand keyword present, own domain excluded."""
    seen: set[str] = set()
    hits: list[dict] = []
    for e in entries:
        if not _fresh(e.get("not_before")):
            continue
        for cand in str(e.get("name_value", "")).splitlines():
            cand = cand.strip().lower().lstrip("*.")
            if (not cand or name not in cand or cand in seen
                    or cand == legit or cand.endswith("." + legit)):
                continue
            seen.add(cand)
            hits.append({
                "domain": cand,
                "issued": (e.get("not_before") or "")[:10],
                "issuer": (e.get("issuer_name") or "").split("CN=")[-1][:40],
            })
            if len(hits) >= _MAX_RESULTS:
                return hits
    return hits


def cert_domains(result: dict) -> set[str]:
    """Comparable snapshot for cron diffing."""
    if result.get("status") != "ok":
        return set()
    return {c["domain"] for c in result.get("certs", [])}
