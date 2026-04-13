# клауд Елдоса N1 — Qalqan AI v5.0
# Academic-grade evaluation metrics: accuracy, precision, recall, F1, MCC, confusion matrix

import math


def calculate_metrics(results: list[dict]) -> dict:
    """
    Calculate academic evaluation metrics from test results.
    Each result: {"url": str, "predicted": "DANGEROUS"|"SAFE", "actual": "DANGEROUS"|"SAFE",
                  "score": int, "source": str, "latency_ms": int}
    """
    if not results:
        return {"error": "No results to evaluate"}

    tp = fp = tn = fn = 0
    latencies = []
    tier_hits = {}

    for r in results:
        pred = r.get("predicted", "").upper()
        actual = r.get("actual", "").upper()
        is_dangerous_pred = pred in ("DANGEROUS", "SUSPICIOUS")
        is_dangerous_actual = actual == "DANGEROUS"

        if is_dangerous_pred and is_dangerous_actual:
            tp += 1
        elif is_dangerous_pred and not is_dangerous_actual:
            fp += 1
        elif not is_dangerous_pred and not is_dangerous_actual:
            tn += 1
        else:
            fn += 1

        if "latency_ms" in r:
            latencies.append(r["latency_ms"])

        source = r.get("source", "unknown")
        tier_hits[source] = tier_hits.get(source, 0) + 1

    total = tp + fp + tn + fn

    # Core metrics
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0

    # Matthews Correlation Coefficient (better for imbalanced data)
    mcc_denom = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    mcc = (tp * tn - fp * fn) / mcc_denom if mcc_denom > 0 else 0

    # Latency stats
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    p50_latency = sorted(latencies)[len(latencies) // 2] if latencies else 0
    p95_latency = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0

    # Per-tier coverage
    total_hits = sum(tier_hits.values())
    tier_coverage = {k: round(v / total_hits * 100, 1) for k, v in tier_hits.items()} if total_hits > 0 else {}

    return {
        "total_samples": total,
        "confusion_matrix": {"tp": tp, "fp": fp, "tn": tn, "fn": fn},
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "fpr": round(fpr, 4),
        "fnr": round(fnr, 4),
        "mcc": round(mcc, 4),
        "latency": {
            "avg_ms": round(avg_latency),
            "p50_ms": p50_latency,
            "p95_ms": p95_latency,
        },
        "tier_coverage": tier_coverage,
    }
