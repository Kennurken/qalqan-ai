# Qalqan AI — Brand monitoring: which typosquat variants are ACTUALLY registered.
# Live RDAP presence-check over the generated look-alikes (brand_protect), plus the
# daily watch scan that alerts when a NEW look-alike appears. This is the B2B hook:
# a bank subscribes its domain and gets a Telegram alert the day kaspi-bonus.kz
# gets registered by someone else.

import asyncio
import logging

from ..utils.http import get_client
from .brand_protect import generate_typosquats
from .domain_intel import _RDAP_BOOTSTRAP, _RDAP_FALLBACK

logger = logging.getLogger("qalqan")

_SCAN_CONCURRENCY = 8
_MAX_VARIANTS = 14          # keep a live scan under ~10 s on serverless


async def check_domain_registered(domain: str) -> dict | None:
    """RDAP presence probe: 200 → registered (with age if present), 404 → free.
    Returns None when RDAP can't answer (unknown TLD, timeout) — never guesses."""
    tld = domain.rsplit(".", 1)[-1].lower()
    base = _RDAP_BOOTSTRAP.get(tld, _RDAP_FALLBACK)
    client = get_client()
    for rdap_url in dict.fromkeys([base, _RDAP_FALLBACK]):   # keep order, dedupe
        try:
            res = await client.get(f"{rdap_url}{domain}", timeout=4, follow_redirects=True)
            if res.status_code == 404:
                return {"domain": domain, "registered": False}
            if res.status_code == 200:
                age_days = None
                try:
                    from datetime import datetime, timezone
                    for ev in res.json().get("events", []):
                        if ev.get("eventAction") == "registration" and ev.get("eventDate"):
                            dt = datetime.fromisoformat(ev["eventDate"].replace("Z", "+00:00"))
                            age_days = max((datetime.now(timezone.utc) - dt).days, 0)
                            break
                except Exception:
                    pass
                return {"domain": domain, "registered": True, "age_days": age_days}
        except Exception as e:
            logger.debug(f"brand_watch RDAP {rdap_url}{domain}: {e}")
            continue
    return None


async def scan_brand(domain: str, max_variants: int = _MAX_VARIANTS) -> dict:
    """Generate the highest-risk look-alikes and RDAP-check which ones exist.
    Returns registered variants (the real attack surface) + scan coverage stats."""
    gen = generate_typosquats(domain)
    if gen.get("error"):
        return gen

    # Highest-risk first (generate_typosquats already sorts critical→high→medium)
    candidates = [v for v in gen["variants"]][:max_variants]

    sem = asyncio.Semaphore(_SCAN_CONCURRENCY)

    async def _probe(v: dict) -> dict | None:
        async with sem:
            r = await check_domain_registered(v["domain"])
        if r is None:
            return None
        return {**v, "registered": r["registered"], "age_days": r.get("age_days")}

    probed = await asyncio.gather(*[_probe(v) for v in candidates])
    checked = [p for p in probed if p is not None]
    registered = [p for p in checked if p["registered"]]

    return {
        "brand": gen["brand"],
        "scanned": len(candidates),
        "answered": len(checked),
        "registered_count": len(registered),
        "registered": registered,
        "note_ru": ("Проверка по RDAP-реестрам в реальном времени. "
                    "«Зарегистрирован» = домен реально существует — потенциальный фишинг-клон."),
    }


def registered_set(scan: dict) -> set[str]:
    """Comparable snapshot of a scan — the set of registered look-alike domains."""
    return {r["domain"] for r in scan.get("registered", [])}
