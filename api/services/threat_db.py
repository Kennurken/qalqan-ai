# клауд Елдоса N1 — Qalqan AI v3.0
# Tier 2: Сыртқы қауіп базалары — PhishTank, Google Safe Browsing, URLhaus, OpenPhish
# Барлығы тегін API, параллель asyncio.gather арқылы тексеріледі

import os
import asyncio
import httpx
from urllib.parse import urlparse

def _phishtank_key() -> str:
    return os.getenv("PHISHTANK_API_KEY", "")

def _safebrowsing_key() -> str:
    return os.getenv("GOOGLE_SAFE_BROWSING_KEY", "")

# OpenPhish feed — жадта сақталады, 12 сағат сайын жаңартылады
_openphish_urls: set[str] = set()
_openphish_loaded: bool = False
_openphish_lock = asyncio.Lock()


def extract_domain(url: str) -> str:
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower().replace("www.", "")
    except Exception:
        return url.lower()


async def check_phishtank(url: str) -> dict | None:
    """PhishTank API — фишинг URL базасы (тегін, API key қажет)."""
    if not _phishtank_key():
        return None
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            data = {
                "url": url,
                "format": "json",
                "app_key": _phishtank_key()
            }
            res = await client.post(
                "https://checkurl.phishtank.com/checkurl/",
                data=data
            )
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
        async with httpx.AsyncClient(timeout=8) as client:
            res = await client.post(api_url, json=payload)
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
        async with httpx.AsyncClient(timeout=8) as client:
            res = await client.post(
                "https://urlhaus-api.abuse.ch/v1/url/",
                data={"url": url}
            )
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
    """OpenPhish community feed жүктеу (12 сағат сайын жаңарту)."""
    global _openphish_urls, _openphish_loaded
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            res = await client.get("https://openphish.com/feed.txt")
            if res.status_code == 200:
                _openphish_urls = set(line.strip() for line in res.text.splitlines() if line.strip())
                _openphish_loaded = True
    except Exception:
        pass


async def check_openphish(url: str) -> dict | None:
    """OpenPhish — тегін фишинг feed (жадтағы set арқылы тексеру)."""
    global _openphish_loaded
    if not _openphish_loaded:
        async with _openphish_lock:
            if not _openphish_loaded:
                await load_openphish_feed()

    if url in _openphish_urls:
        return {
            "verdict": "DANGEROUS",
            "threat_score": 88,
            "threat_type": "phishing",
            "source": "openphish",
            "reason_kk": "OpenPhish фишинг тізімінде тіркелген",
            "reason_ru": "Найден в списке фишинговых сайтов OpenPhish",
            "reason_en": "Listed in OpenPhish phishing feed",
            "indicators": ["openphish_exact"]
        }

    # Домен бойынша да тексеру
    domain = extract_domain(url)
    for phish_url in _openphish_urls:
        if domain in phish_url:
            return {
                "verdict": "DANGEROUS",
                "threat_score": 82,
                "threat_type": "phishing",
                "source": "openphish",
                "reason_kk": f"OpenPhish тізімінде осы доменнен фишинг табылды",
                "reason_ru": f"В OpenPhish найден фишинг с этого домена",
                "reason_en": f"OpenPhish has phishing records from this domain",
                "indicators": ["openphish_domain"]
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
    except asyncio.TimeoutError:
        results = []
    return [r for r in results if isinstance(r, dict)]
