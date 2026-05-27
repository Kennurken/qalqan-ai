# Qalqan AI v5.0
# Benchmark: fast-path only (pyramid + URL features), no external API calls

import time
from ..services.pyramid_detector import check_pyramid_domain
from ..services.kz_intel import check_kz_impersonation_url, check_gambling_domain
from ..services.url_features import extract_features
from ..services.scoring import calculate_final_verdict
from .metrics import calculate_metrics
from ..services.threat_db import extract_domain as _extract_domain


TEST_URLS = {
    # === SAFE — KZ trusted domains ===
    "https://google.com": "SAFE",
    "https://kaspi.kz": "SAFE",
    "https://egov.kz": "SAFE",
    "https://youtube.com": "SAFE",
    "https://github.com": "SAFE",
    "https://wikipedia.org": "SAFE",
    "https://halykbank.kz": "SAFE",
    "https://kcell.kz": "SAFE",
    "https://salyk.kz": "SAFE",
    "https://enbek.kz": "SAFE",

    # === DANGEROUS — Pyramids/MLM ===
    "https://crowd1.com": "DANGEROUS",
    "https://finiko.com": "DANGEROUS",
    "https://onecoin.eu": "DANGEROUS",
    "https://forsage.io": "DANGEROUS",
    "https://bitconnect.co": "DANGEROUS",
    "https://qubittech.ai": "DANGEROUS",
    "https://antares.trade": "DANGEROUS",

    # === DANGEROUS — Gambling (banned in KZ) ===
    "https://1xbet.com": "DANGEROUS",
    "https://mostbet.com": "DANGEROUS",
    "https://pin-up.casino": "DANGEROUS",
    "https://hellcase.com": "DANGEROUS",
    "https://vavada.com": "DANGEROUS",
    "https://1win.com": "DANGEROUS",

    # === DANGEROUS — Phishing (KZ brands) ===
    "https://kaspi-login.tk": "DANGEROUS",
    "https://verify-account.ml": "DANGEROUS",
    "https://egov-login.ga": "DANGEROUS",
    "https://egov-verify.kz": "DANGEROUS",
    "https://kaspi-verify.com": "DANGEROUS",
    "https://halyk-bank.com": "DANGEROUS",

    # === DANGEROUS — URL feature signals ===
    "http://192.168.1.1/phish": "DANGEROUS",    # IP address URL
    "https://kаspi.kz": "DANGEROUS",             # Cyrillic 'а' homoglyph
}


async def run_benchmark(test_urls: dict | None = None) -> dict:
    urls = test_urls or TEST_URLS
    results = []

    for url, actual_label in urls.items():
        start = time.time()
        domain = _extract_domain(url)
        pyramid_hit = check_pyramid_domain(url)
        kz_hit = check_kz_impersonation_url(domain)
        gambling_hit = check_gambling_domain(domain)
        url_feats = extract_features(url)

        if pyramid_hit:
            verdict_data = calculate_final_verdict([], None, pyramid_hit, lang="en")
        elif kz_hit:
            verdict_data = calculate_final_verdict([], kz_hit, None, url_features=url_feats, lang="en")
        elif gambling_hit:
            verdict_data = calculate_final_verdict([], gambling_hit, None, url_features=url_feats, lang="en")
        else:
            risk = url_feats.get("risk_score", 0)
            verdict_data = {
                "verdict": "DANGEROUS" if risk >= 70 else "SUSPICIOUS" if risk >= 40 else "SAFE",
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
