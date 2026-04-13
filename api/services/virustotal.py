# клауд Елдоса N1 — Qalqan AI v5.0
# VirusTotal API: 70+ антивирус одним запросом (500 req/day free, no credit card)
# URL scan via v3 API

import os
import hashlib
import base64
import httpx
import logging

logger = logging.getLogger("qalqan")


def _vt_key() -> str:
    return os.getenv("VIRUSTOTAL_API_KEY", "")


async def check_virustotal(url: str) -> dict | None:
    """Check URL against VirusTotal (70+ antivirus engines)."""
    key = _vt_key()
    if not key:
        return None

    try:
        # VT v3: URL ID = base64(url) without padding
        url_id = base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")

        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(
                f"https://www.virustotal.com/api/v3/urls/{url_id}",
                headers={"x-apikey": key}
            )

            if res.status_code == 404:
                # URL not in VT database — submit for scanning
                submit_res = await client.post(
                    "https://www.virustotal.com/api/v3/urls",
                    headers={"x-apikey": key},
                    data={"url": url}
                )
                if submit_res.status_code != 200:
                    return None
                # After submission, results take time — return None for now
                return None

            if res.status_code != 200:
                return None

            data = res.json()
            attrs = data.get("data", {}).get("attributes", {})
            stats = attrs.get("last_analysis_stats", {})

            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            total = sum(stats.values())

            if malicious + suspicious == 0:
                return None  # Clean — no signal

            score = min(int((malicious + suspicious) / max(total, 1) * 100), 100)
            # At least 2 engines flagged = meaningful signal
            if malicious + suspicious < 2:
                return None

            threat_names = []
            results = attrs.get("last_analysis_results", {})
            for engine, result in list(results.items())[:5]:
                if result.get("category") in ("malicious", "suspicious"):
                    threat_names.append(f"{engine}: {result.get('result', 'detected')}")

            return {
                "verdict": "DANGEROUS" if score >= 30 else "SUSPICIOUS",
                "threat_score": max(score, 75),
                "threat_type": "malware",
                "source": "virustotal",
                "reason_kk": f"VirusTotal: {malicious}/{total} антивирус қауіпті деп таныды",
                "reason_ru": f"VirusTotal: {malicious}/{total} антивирусов обнаружили угрозу",
                "reason_en": f"VirusTotal: {malicious}/{total} engines flagged as malicious",
                "indicators": threat_names[:5]
            }
    except Exception as e:
        logger.debug(f"VirusTotal error: {e}")
        return None
