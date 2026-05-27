# Qalqan AI v5.0
# Domain Intelligence: RDAP (домен жасы) + SSL сертификат тексеру
# RDAP: толық тегін, лимитсіз, кілт жоқ — rdap.org + IANA bootstrap fallback
# SSL: Python stdlib арқылы, API жоқ

import ssl
import socket
import asyncio
import httpx
import logging
from datetime import datetime, timezone
from urllib.parse import urlparse

logger = logging.getLogger("qalqan")

# IANA RDAP bootstrap — TLD-specific servers for better accuracy
_RDAP_BOOTSTRAP = {
    "kz": "https://rdap.nic.kz/domain/",
    "com": "https://rdap.verisign.com/com/v1/domain/",
    "net": "https://rdap.verisign.com/net/v1/domain/",
    "org": "https://rdap.publicinterestregistry.org/rdap/domain/",
    "io":  "https://rdap.nic.io/domain/",
    "ru":  "https://rdap.tcinet.ru/domain/",
}
_RDAP_FALLBACK = "https://rdap.org/domain/"

# Known free CAs used disproportionately by phishing sites
_FREE_CA_ORGS = {"let's encrypt", "zerossl", "buypass", "sectigo"}


async def check_domain_intelligence(domain: str, url: str) -> dict | None:
    """RDAP + SSL тексеру. Қосымша threat_score қайтарады."""
    score_adjust = 0
    indicators = []
    details = {}

    # Run RDAP and SSL concurrently
    loop = asyncio.get_running_loop()
    age_task = asyncio.create_task(_get_domain_age_rdap(domain))
    ssl_task = loop.run_in_executor(None, _check_ssl_cert, domain)
    age_days, ssl_info = await asyncio.gather(age_task, ssl_task, return_exceptions=True)

    # --- RDAP: домен жасы ---
    if isinstance(age_days, int):
        details["domain_age_days"] = age_days
        if age_days < 7:
            score_adjust += 35
            indicators.append(f"domain_age_{age_days}d")
        elif age_days < 30:
            score_adjust += 20
            indicators.append(f"domain_age_{age_days}d")
        elif age_days < 90:
            score_adjust += 10
            indicators.append(f"domain_age_{age_days}d")

    # --- SSL сертификат ---
    if isinstance(ssl_info, Exception) or ssl_info is None:
        ssl_info = {"status": "unknown"}
    details["ssl"] = ssl_info

    ssl_status = ssl_info.get("status", "unknown")
    if ssl_status == "no_ssl":
        score_adjust += 30
        indicators.append("no_ssl")
    elif ssl_status == "expired":
        score_adjust += 25
        indicators.append("ssl_expired")
    elif ssl_status == "self_signed":
        score_adjust += 15
        indicators.append("ssl_self_signed")
    elif ssl_status == "expiring_soon":
        score_adjust += 8
        indicators.append("ssl_expiring_soon")
    elif ssl_status == "valid":
        # Free CA = weak signal (Let's Encrypt widely used by phishing)
        issuer_org = ssl_info.get("issuer", "").lower()
        if any(ca in issuer_org for ca in _FREE_CA_ORGS):
            score_adjust += 5
            indicators.append("free_ca")
            details["ssl"]["free_ca"] = True

    if score_adjust == 0:
        # Still return metadata for informational use (non-threatening domains)
        return {"verdict": "SAFE", "threat_score": 0, "source": "domain_intel",
                "indicators": [], "domain_details": details} if details else None

    verdict = "DANGEROUS" if score_adjust >= 35 else "SUSPICIOUS" if score_adjust >= 15 else "SAFE"

    return {
        "verdict": verdict,
        "threat_score": min(score_adjust, 100),
        "threat_type": "suspicious_infrastructure",
        "source": "domain_intel",
        "reason_kk": _build_reason_kk(details),
        "reason_ru": _build_reason_ru(details),
        "reason_en": _build_reason_en(details),
        "indicators": indicators,
        "domain_details": details
    }


async def _get_domain_age_rdap(domain: str) -> int | None:
    """RDAP арқылы домен жасын анықтау. TLD-specific server → rdap.org fallback."""
    # Strip to apex domain
    parts = domain.split(".")
    if len(parts) > 2:
        domain = ".".join(parts[-2:])
    tld = parts[-1].lower()

    # Try TLD-specific RDAP first, fall back to rdap.org
    primary = _RDAP_BOOTSTRAP.get(tld, _RDAP_FALLBACK)
    urls_to_try = [primary]
    if primary != _RDAP_FALLBACK:
        urls_to_try.append(_RDAP_FALLBACK + domain)

    async with httpx.AsyncClient(timeout=5, follow_redirects=True) as client:
        for rdap_url in urls_to_try:
            try:
                url = rdap_url if rdap_url.endswith(domain) else f"{rdap_url}{domain}"
                res = await client.get(url)
                if res.status_code != 200:
                    continue
                data = res.json()

                # Prefer "registration", fallback to "last changed" or "expiration" for age calc
                reg_date = None
                for action in ("registration", "last changed"):
                    for event in data.get("events", []):
                        if event.get("eventAction") == action:
                            reg_date = event.get("eventDate")
                            break
                    if reg_date:
                        break

                if reg_date:
                    dt = datetime.fromisoformat(reg_date.replace("Z", "+00:00"))
                    age = (datetime.now(timezone.utc) - dt).days
                    return max(age, 0)
            except Exception as e:
                logger.debug(f"RDAP error ({rdap_url}): {e}")
                continue
    return None


def _check_ssl_cert(domain: str) -> dict:
    """SSL сертификатын тексеру (stdlib, API жоқ). Expiry + issuer."""
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=3) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                not_after_ts = ssl.cert_time_to_seconds(cert["notAfter"])
                now = datetime.now().timestamp()

                if not_after_ts < now:
                    return {"status": "expired", "days_expired": int((now - not_after_ts) // 86400)}

                days_left = int((not_after_ts - now) // 86400)
                issuer_dict = dict(x[0] for x in cert.get("issuer", ()))
                org = issuer_dict.get("organizationName", "Unknown")

                if days_left < 14:
                    return {"status": "expiring_soon", "days_left": days_left, "issuer": org}

                return {"status": "valid", "days_left": days_left, "issuer": org}
    except ssl.SSLCertVerificationError:
        return {"status": "self_signed"}
    except (socket.timeout, ConnectionRefusedError, OSError):
        return {"status": "no_ssl"}
    except Exception as e:
        logger.debug(f"SSL check error for {domain}: {e}")
        return {"status": "unknown"}


def _build_reason_kk(details: dict) -> str:
    parts = []
    age = details.get("domain_age_days")
    if age is not None and age < 90:
        parts.append(f"Домен жасы: {age} күн (жаңа домен — қауіпті белгі)")
    ssl = details.get("ssl", {})
    ssl_s = ssl.get("status")
    if ssl_s == "no_ssl":
        parts.append("SSL сертификаты жоқ — деректер қорғалмаған")
    elif ssl_s == "expired":
        days = ssl.get("days_expired", "?")
        parts.append(f"SSL сертификатының мерзімі {days} күн бұрын өтіп кеткен")
    elif ssl_s == "self_signed":
        parts.append("Өзі қол қойған SSL сертификат — сенімсіз")
    elif ssl_s == "expiring_soon":
        days = ssl.get("days_left", "?")
        parts.append(f"SSL сертификатының мерзімі {days} күнде аяқталады")
    elif ssl.get("free_ca"):
        parts.append(f"Тегін CA сертификаты ({ssl.get('issuer', '')}) — фишингте жиі қолданылады")
    return ". ".join(parts) or "Домен инфрақұрылымы тексерілді"


def _build_reason_ru(details: dict) -> str:
    parts = []
    age = details.get("domain_age_days")
    if age is not None and age < 90:
        parts.append(f"Возраст домена: {age} дн. (новый домен — признак опасности)")
    ssl = details.get("ssl", {})
    ssl_s = ssl.get("status")
    if ssl_s == "no_ssl":
        parts.append("Нет SSL сертификата — данные не защищены")
    elif ssl_s == "expired":
        days = ssl.get("days_expired", "?")
        parts.append(f"SSL сертификат просрочен на {days} дн.")
    elif ssl_s == "self_signed":
        parts.append("Самоподписанный SSL сертификат — ненадёжный")
    elif ssl_s == "expiring_soon":
        days = ssl.get("days_left", "?")
        parts.append(f"SSL сертификат истекает через {days} дн.")
    elif ssl.get("free_ca"):
        parts.append(f"Бесплатный CA ({ssl.get('issuer', '')}) — часто используется в фишинге")
    return ". ".join(parts) or "Инфраструктура домена проверена"


def _build_reason_en(details: dict) -> str:
    parts = []
    age = details.get("domain_age_days")
    if age is not None and age < 90:
        parts.append(f"Domain age: {age} days (new domain — risk indicator)")
    ssl = details.get("ssl", {})
    ssl_s = ssl.get("status")
    if ssl_s == "no_ssl":
        parts.append("No SSL certificate — data not encrypted")
    elif ssl_s == "expired":
        days = ssl.get("days_expired", "?")
        parts.append(f"SSL certificate expired {days} day(s) ago")
    elif ssl_s == "self_signed":
        parts.append("Self-signed SSL certificate — untrusted")
    elif ssl_s == "expiring_soon":
        days = ssl.get("days_left", "?")
        parts.append(f"SSL certificate expires in {days} day(s)")
    elif ssl.get("free_ca"):
        parts.append(f"Free CA certificate ({ssl.get('issuer', '')}) — commonly used in phishing")
    return ". ".join(parts) or "Domain infrastructure verified"
