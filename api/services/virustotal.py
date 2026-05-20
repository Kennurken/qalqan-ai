# Qalqan AI v5.0
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
            phishing_count = 0
            results_data = attrs.get("last_analysis_results", {})
            for engine, eng_result in list(results_data.items()):
                if eng_result.get("category") in ("malicious", "suspicious"):
                    eng_verdict = (eng_result.get("result") or "").lower()
                    if "phish" in eng_verdict:
                        phishing_count += 1
                    if len(threat_names) < 5:
                        threat_names.append(f"{engine}: {eng_result.get('result', 'detected')}")

            # Determine threat type: phishing if majority of flagging engines say so
            threat_type = "phishing" if phishing_count >= max(1, (malicious + suspicious) // 2) else "malware"

            return {
                "verdict": "DANGEROUS" if malicious >= 5 else "SUSPICIOUS",
                "threat_score": score,
                "threat_type": threat_type,
                "source": "virustotal",
                "reason_kk": f"VirusTotal: {malicious}/{total} антивирус қауіпті деп таныды",
                "reason_ru": f"VirusTotal: {malicious}/{total} антивирусов обнаружили угрозу",
                "reason_en": f"VirusTotal: {malicious}/{total} engines flagged as malicious",
                "indicators": threat_names[:5]
            }
    except Exception as e:
        logger.debug(f"VirusTotal error: {e}")
        return None
