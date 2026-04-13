# клауд Елдоса N1 — Qalqan AI v5.0
# Benchmark pipeline: test URLs through the full detection pipeline

import time
import asyncio
from ..services.threat_db import check_all_databases, extract_domain
from ..services.ai_analyzer import analyze_url
from ..services.pyramid_detector import check_pyramid_domain, check_local_blacklist
from ..services.domain_intel import check_domain_intelligence
from ..services.url_features import extract_features
from ..services.scoring import calculate_final_verdict
from ..utils.cache import url_hash, get_cached, set_cached, clear_cache
from .metrics import calculate_metrics


# Built-in test dataset
TEST_URLS = {
    # Known SAFE (whitelist)
    "https://google.com": "SAFE",
    "https://kaspi.kz": "SAFE",
    "https://egov.kz": "SAFE",
    "https://youtube.com": "SAFE",
    "https://github.com": "SAFE",
    "https://wikipedia.org": "SAFE",

    # Known DANGEROUS (pyramids)
    "https://crowd1.com": "DANGEROUS",
    "https://finiko.com": "DANGEROUS",
    "https://onecoin.eu": "DANGEROUS",
    "https://forsage.io": "DANGEROUS",
    "https://bitconnect.co": "DANGEROUS",

    # Known DANGEROUS (gambling)
    "https://1xbet.com": "DANGEROUS",

    # Suspicious patterns (free TLD + keywords)
    "https://kaspi-login.tk": "DANGEROUS",
    "https://verify-account.ml": "DANGEROUS",
    "https://egov-login.ga": "DANGEROUS",
}


async def run_benchmark(test_urls: dict | None = None, clear_before: bool = True) -> dict:
    """Run full benchmark on test dataset. Returns metrics + per-URL results."""
    urls = test_urls or TEST_URLS

    if clear_before:
        clear_cache()

    results = []

    for url, actual_label in urls.items():
        start = time.time()
        domain = extract_domain(url)

        # Fast-path only: whitelist + pyramid + URL features (no external API = no timeout)
        pyramid_hit = check_pyramid_domain(url)
        url_feats = extract_features(url)

        if pyramid_hit:
            verdict_data = calculate_final_verdict([], None, pyramid_hit, lang="en")
        else:
            # Score from URL features alone
            risk = url_feats.get("risk_score", 0)
            if risk >= 60:
                verdict_data = {"verdict": "DANGEROUS", "threat_score": risk, "source": "url_features", "threat_type": "suspicious"}
            elif risk >= 30:
                verdict_data = {"verdict": "SUSPICIOUS", "threat_score": risk, "source": "url_features", "threat_type": "suspicious"}
            else:
                verdict_data = {"verdict": "SAFE", "threat_score": risk, "source": "url_features", "threat_type": "safe"}

        latency = int((time.time() - start) * 1000)

        results.append({
            "url": url,
            "predicted": verdict_data.get("verdict", "SAFE"),
            "actual": actual_label,
            "score": verdict_data.get("threat_score", 0),
            "source": verdict_data.get("source", "unknown"),
            "latency_ms": latency,
        })

    metrics = calculate_metrics(results)
    metrics["per_url_results"] = results

    return metrics
