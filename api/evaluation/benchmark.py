# клауд Елдоса N1 — Qalqan AI v5.0
# Benchmark: fast-path only (pyramid + URL features), no external API calls

import time
from ..services.pyramid_detector import check_pyramid_domain
from ..services.url_features import extract_features
from ..services.scoring import calculate_final_verdict
from .metrics import calculate_metrics


TEST_URLS = {
    "https://google.com": "SAFE",
    "https://kaspi.kz": "SAFE",
    "https://egov.kz": "SAFE",
    "https://youtube.com": "SAFE",
    "https://github.com": "SAFE",
    "https://wikipedia.org": "SAFE",
    "https://crowd1.com": "DANGEROUS",
    "https://finiko.com": "DANGEROUS",
    "https://onecoin.eu": "DANGEROUS",
    "https://forsage.io": "DANGEROUS",
    "https://bitconnect.co": "DANGEROUS",
    "https://1xbet.com": "DANGEROUS",
    "https://kaspi-login.tk": "DANGEROUS",
    "https://verify-account.ml": "DANGEROUS",
    "https://egov-login.ga": "DANGEROUS",
}


async def run_benchmark(test_urls: dict | None = None) -> dict:
    urls = test_urls or TEST_URLS
    results = []

    for url, actual_label in urls.items():
        start = time.time()
        pyramid_hit = check_pyramid_domain(url)
        url_feats = extract_features(url)

        if pyramid_hit:
            verdict_data = calculate_final_verdict([], None, pyramid_hit, lang="en")
        else:
            risk = url_feats.get("risk_score", 0)
            verdict_data = {
                "verdict": "DANGEROUS" if risk >= 60 else "SUSPICIOUS" if risk >= 30 else "SAFE",
                "threat_score": risk,
                "source": "url_features",
            }

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
