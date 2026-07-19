# Qalqan AI v3.0
# Tier 2: Сыртқы қауіп базалары — PhishTank, Google Safe Browsing, URLhaus, OpenPhish
# Барлығы тегін API, параллель asyncio.gather арқылы тексеріледі

import os
import time
import asyncio
import httpx
from urllib.parse import urlparse

from ..utils.http import get_client

def _phishtank_key() -> str:
    return os.getenv("PHISHTANK_API_KEY", "")

def _safebrowsing_key() -> str:
    return os.getenv("GOOGLE_SAFE_BROWSING_KEY", "")

# Threat feeds — жадта сақталады, 12 сағат сайын жаңартылады
_openphish_urls: set[str] = set()          # exact-URL set (OpenPhish)
_feed_domains: set[str] = set()            # domain set across feeds → O(1) lookup
_feed_counts: dict[str, int] = {}          # per-feed domain counts (for /feed stats)
_openphish_loaded_at: float = 0.0
_OPENPHISH_TTL = 12 * 3600  # 12 hours
_openphish_lock = asyncio.Lock()
_URLHAUS_FEED_CAP = 80000   # bound memory / cold-start cost on serverless


def extract_domain(url: str) -> str:
    """Fix #6: use parsed.hostname (strips port) instead of netloc (includes :port).
    netloc='evil.com:8080' would bypass whitelist/DB checks that compare by domain."""
    try:
        parsed = urlparse(url)
        # hostname strips port; netloc includes it — use hostname
        host = (parsed.hostname or "").lower()
        return host.removeprefix("www.")
    except Exception:
        return url.lower()


async def check_phishtank(url: str) -> dict | None:
    """PhishTank API — фишинг URL базасы (тегін, API key қажет)."""
    if not _phishtank_key():
        return None
    try:
        data = {
            "url": url,
            "format": "json",
            "app_key": _phishtank_key()
        }
        res = await get_client().post(
            "https://checkurl.phishtank.com/checkurl/", data=data, timeout=8)
        if res.status_code != 200:
            return None
        result = res.json()
        results = result.get("results", {})
        if results.get("in_database") and results.get("verified"):
            return {
                "verdict": "DANGEROUS",
                "threat_score": 95,
                "threat_type": "phishing",
                "source": "phishtank",
                "reason_kk": "PhishTank базасында тіркелген фишинг сайт",
                "reason_ru": "Фишинговый сайт из базы PhishTank",
                "reason_en": "Verified phishing site in PhishTank database",
                "indicators": ["phishtank_verified"]
            }
        return None
    except Exception:
        return None


async def check_google_safe_browsing(url: str) -> dict | None:
    """Google Safe Browsing API v4 — зиянды URL базасы (тегін 10k/күн)."""
    if not _safebrowsing_key():
        return None
    try:
        api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={_safebrowsing_key()}"
        payload = {
            "client": {"clientId": "qalqan-ai", "clientVersion": "3.0"},
            "threatInfo": {
                "threatTypes": [
                    "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION"
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }
        res = await get_client().post(api_url, json=payload, timeout=8)
        if res.status_code != 200:
            return None
        data = res.json()
        matches = data.get("matches", [])
        if matches:
            threat_type_map = {
                "MALWARE": "malware",
                "SOCIAL_ENGINEERING": "phishing",
                "UNWANTED_SOFTWARE": "malware",
                "POTENTIALLY_HARMFUL_APPLICATION": "malware"
            }
            goog_type = matches[0].get("threatType", "MALWARE")
            mapped_type = threat_type_map.get(goog_type, "malware")
            return {
                "verdict": "DANGEROUS",
                "threat_score": 90,
                "threat_type": mapped_type,
                "source": "google_safe_browsing",
                "reason_kk": f"Google Safe Browsing: {goog_type} анықталды",
                "reason_ru": f"Google Safe Browsing: обнаружен {goog_type}",
                "reason_en": f"Google Safe Browsing: {goog_type} detected",
                "indicators": [f"gsb_{goog_type.lower()}"]
            }
        return None
    except Exception:
        return None


async def check_urlhaus(url: str) -> dict | None:
    """URLhaus by abuse.ch — зиянды URL базасы (толық тегін, кілт қажет емес)."""
    try:
        res = await get_client().post(
            "https://urlhaus-api.abuse.ch/v1/url/", data={"url": url}, timeout=8)
        if res.status_code != 200:
            return None
        data = res.json()
        if data.get("query_status") == "listed":
            threat = data.get("threat", "malware_download")
            return {
                "verdict": "DANGEROUS",
                "threat_score": 92,
                "threat_type": "malware",
                "source": "urlhaus",
                "reason_kk": f"URLhaus базасында тіркелген: {threat}",
                "reason_ru": f"Найден в базе URLhaus: {threat}",
                "reason_en": f"Listed in URLhaus database: {threat}",
                "indicators": ["urlhaus_listed"]
            }
        return None
    except Exception:
        return None


async def load_openphish_feed():
    """OpenPhish + URLhaus community feeds жүктеу (12 сағат сайын жаңарту).
    Kept under the old name so the lifespan preload import keeps working."""
    await load_threat_feeds()


async def _fetch_feed(client: httpx.AsyncClient, url: str, cap: int | None = None) -> list[str]:
    res = await client.get(url, timeout=15)
    if res.status_code != 200:
        return []
    lines = [ln.strip() for ln in res.text.splitlines()
             if ln.strip() and not ln.startswith("#")]
    return lines[:cap] if cap else lines


async def load_threat_feeds():
    """Load OpenPhish + URLhaus bulk feeds into in-memory sets.
    Builds a domain set for O(1) lookups (avoids per-request O(n) scans)."""
    global _openphish_urls, _feed_domains, _feed_counts, _openphish_loaded_at
    op_urls: set[str] = set()
    domains: set[str] = set()
    counts: dict[str, int] = {}
    client = get_client()
    # OpenPhish (exact URLs, small)
    try:
        op = await _fetch_feed(client, "https://openphish.com/feed.txt")
        op_urls = set(op)
        op_doms = {extract_domain(u) for u in op_urls if extract_domain(u)}
        domains |= op_doms
        counts["openphish"] = len(op_doms)
    except Exception:
        pass
    # URLhaus online bulk feed (large → domain set only, bounded)
    try:
        uh = await _fetch_feed(client, "https://urlhaus.abuse.ch/downloads/text_online/",
                               cap=_URLHAUS_FEED_CAP)
        uh_doms = {extract_domain(u) for u in uh if extract_domain(u)}
        domains |= uh_doms
        counts["urlhaus"] = len(uh_doms)
    except Exception:
        pass
    if op_urls or domains:
        _openphish_urls = op_urls
        _feed_domains = domains
        _feed_counts = counts
        _openphish_loaded_at = time.time()


def feed_stats() -> dict:
    """Loaded-feed stats for /feed and /health."""
    return {"domains": len(_feed_domains), "openphish_urls": len(_openphish_urls),
            "sources": dict(_feed_counts),
            "age_sec": int(time.time() - _openphish_loaded_at) if _openphish_loaded_at else None}


async def check_openphish(url: str) -> dict | None:
    """Threat-feed check — exact OpenPhish URL, then O(1) domain match across feeds."""
    now = time.time()
    if now - _openphish_loaded_at > _OPENPHISH_TTL:
        async with _openphish_lock:
            if now - _openphish_loaded_at > _OPENPHISH_TTL:
                await load_threat_feeds()

    if url in _openphish_urls:
        return {
            "verdict": "DANGEROUS", "threat_score": 88, "threat_type": "phishing",
            "source": "openphish",
            "reason_kk": "OpenPhish фишинг тізімінде тіркелген",
            "reason_ru": "Найден в списке фишинговых сайтов OpenPhish",
            "reason_en": "Listed in OpenPhish phishing feed",
            "indicators": ["openphish_exact"],
        }

    domain = extract_domain(url)
    if domain and domain in _feed_domains:
        return {
            "verdict": "DANGEROUS", "threat_score": 84, "threat_type": "phishing",
            "source": "threat_feed",
            "reason_kk": "Қауіп feed-терінде (OpenPhish/URLhaus) тіркелген домен",
            "reason_ru": "Домен в threat-feed (OpenPhish/URLhaus)",
            "reason_en": "Domain listed in threat feeds (OpenPhish/URLhaus)",
            "indicators": ["threat_feed_domain"],
        }
    return None


async def check_all_databases(url: str) -> list[dict]:
    """Барлық базаларды параллель тексеру. Max 5 секунд timeout."""
    from .virustotal import check_virustotal
    try:
        results = await asyncio.wait_for(
            asyncio.gather(
                check_phishtank(url),
                check_google_safe_browsing(url),
                check_urlhaus(url),
                check_openphish(url),
                check_virustotal(url),
                return_exceptions=True
            ),
            timeout=5.0
        )
    except TimeoutError:
        results = []
    return [r for r in results if isinstance(r, dict)]
