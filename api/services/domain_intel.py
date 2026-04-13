# клауд Елдоса N1 — Qalqan AI v4.0
# Domain Intelligence: RDAP (домен жасы) + SSL сертификат тексеру
# RDAP: толық тегін, лимитсіз, кілт жоқ
# SSL: Python stdlib арқылы, API жоқ

import ssl
import socket
import httpx
import logging
from datetime import datetime, timezone
from urllib.parse import urlparse

logger = logging.getLogger("qalqan")


async def check_domain_intelligence(domain: str, url: str) -> dict | None:
    """RDAP + SSL тексеру. Қосымша threat_score қайтарады."""
    score_adjust = 0
    indicators = []
    details = {}

    # --- RDAP: домен жасы ---
    age_days = await _get_domain_age_rdap(domain)
    if age_days is not None:
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
    ssl_info = _check_ssl_cert(domain)
    details["ssl"] = ssl_info
    if ssl_info["status"] == "no_ssl":
        score_adjust += 30
        indicators.append("no_ssl")
    elif ssl_info["status"] == "expired":
        score_adjust += 25
        indicators.append("ssl_expired")
    elif ssl_info["status"] == "self_signed":
        score_adjust += 15
        indicators.append("ssl_self_signed")

    if score_adjust == 0:
        return None  # Ешқандай қауіп белгісі жоқ

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
    """RDAP арқылы домен жасын анықтау (тегін, лимитсіз)."""
    # Тек негізгі доменді алу (subdomain жою)
    parts = domain.split(".")
    if len(parts) > 2:
        # foo.bar.com → bar.com
        domain = ".".join(parts[-2:])

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            res = await client.get(f"https://rdap.org/domain/{domain}")
            if res.status_code != 200:
                return None
            data = res.json()

            # RDAP events ішінен "registration" табу
            for event in data.get("events", []):
                if event.get("eventAction") == "registration":
                    reg_date = event["eventDate"]
                    # ISO 8601 parse
                    dt = datetime.fromisoformat(reg_date.replace("Z", "+00:00"))
                    age = (datetime.now(timezone.utc) - dt).days
                    return max(age, 0)
            return None
    except Exception as e:
        logger.debug(f"RDAP error for {domain}: {e}")
        return None


def _check_ssl_cert(domain: str) -> dict:
    """SSL сертификатын тексеру (stdlib, API жоқ)."""
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=3) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                # Мерзімін тексеру
                not_after = ssl.cert_time_to_seconds(cert["notAfter"])
                if not_after < datetime.now().timestamp():
                    return {"status": "expired", "issuer": str(cert.get("issuer", ""))}
                issuer = dict(x[0] for x in cert.get("issuer", ()))
                org = issuer.get("organizationName", "Unknown")
                return {"status": "valid", "issuer": org}
    except ssl.SSLCertVerificationError:
        return {"status": "self_signed"}
    except (socket.timeout, ConnectionRefusedError, OSError):
        return {"status": "no_ssl"}
    except Exception:
        return {"status": "unknown"}


def _build_reason_kk(details: dict) -> str:
    parts = []
    age = details.get("domain_age_days")
    if age is not None and age < 90:
        parts.append(f"Домен жасы: {age} күн (жаңа домен — қауіпті белгі)")
    ssl_s = details.get("ssl", {}).get("status")
    if ssl_s == "no_ssl":
        parts.append("SSL сертификаты жоқ — деректер қорғалмаған")
    elif ssl_s == "expired":
        parts.append("SSL сертификатының мерзімі өтіп кеткен")
    elif ssl_s == "self_signed":
        parts.append("Өзі қол қойған SSL сертификат — сенімсіз")
    return ". ".join(parts) or "Домен инфрақұрылымы тексерілді"


def _build_reason_ru(details: dict) -> str:
    parts = []
    age = details.get("domain_age_days")
    if age is not None and age < 90:
        parts.append(f"Возраст домена: {age} дн. (новый домен — признак опасности)")
    ssl_s = details.get("ssl", {}).get("status")
    if ssl_s == "no_ssl":
        parts.append("Нет SSL сертификата — данные не защищены")
    elif ssl_s == "expired":
        parts.append("SSL сертификат просрочен")
    elif ssl_s == "self_signed":
        parts.append("Самоподписанный SSL сертификат — ненадёжный")
    return ". ".join(parts) or "Инфраструктура домена проверена"


def _build_reason_en(details: dict) -> str:
    parts = []
    age = details.get("domain_age_days")
    if age is not None and age < 90:
        parts.append(f"Domain age: {age} days (new domain — risk indicator)")
    ssl_s = details.get("ssl", {}).get("status")
    if ssl_s == "no_ssl":
        parts.append("No SSL certificate — data not encrypted")
    elif ssl_s == "expired":
        parts.append("SSL certificate expired")
    elif ssl_s == "self_signed":
        parts.append("Self-signed SSL certificate — untrusted")
    return ". ".join(parts) or "Domain infrastructure verified"
