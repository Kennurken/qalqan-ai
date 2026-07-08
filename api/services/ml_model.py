# Qalqan AI — Tier 2.8: fine-tuned XLM-RoBERTa URL classifier (ml/serve_model.py)
# The 279M-param model can't run inside a Vercel function, so it's served as a
# separate service (VPS / home GPU / HF Space) and called over HTTP.
# Set ML_SERVICE_URL (e.g. http://localhost:8001 or https://ml.qalqan.kz) to enable;
# unset → the tier is skipped and the pipeline works exactly as before.

import os
import time
import logging

from ..utils.http import get_client

logger = logging.getLogger("qalqan")

# Only act on confident calls — the model is a signal, not an oracle.
ML_DANGEROUS_MIN_CONF = 0.85   # DANGEROUS верификация табалдырығы
ML_TIMEOUT = 3.0               # never let a slow ML box stall the pipeline

# Circuit breaker: if the service is down, skip it for a while instead of
# paying the timeout on every request.
_fail_count = 0
_open_until = 0.0
_FAILS_TO_OPEN = 3
_COOLDOWN = 60.0


def _service_url() -> str:
    return os.getenv("ML_SERVICE_URL", "").rstrip("/")


def ml_enabled() -> bool:
    return bool(_service_url())


def _breaker_open() -> bool:
    return time.time() < _open_until


def _record_failure() -> None:
    global _fail_count, _open_until
    _fail_count += 1
    if _fail_count >= _FAILS_TO_OPEN:
        _open_until = time.time() + _COOLDOWN
        logger.warning(f"ML service circuit OPEN {_COOLDOWN}s after {_fail_count} fails")


def _record_success() -> None:
    global _fail_count
    _fail_count = 0


async def ml_predict(url: str) -> dict | None:
    """Call the external ML service. Returns a pipeline-style hit dict when the
    model confidently says DANGEROUS, else None (safe / unsure / disabled / down)."""
    base = _service_url()
    if not base or _breaker_open():
        return None
    try:
        r = await get_client().post(f"{base}/predict", json={"url": url},
                                    timeout=ML_TIMEOUT)
        if r.status_code != 200:
            _record_failure()
            return None
        _record_success()
        d = r.json()
    except Exception as e:
        _record_failure()
        logger.debug(f"ml_predict failed: {e}")
        return None

    if d.get("verdict") != "DANGEROUS":
        return None
    conf = float(d.get("confidence", 0.0))
    if conf < ML_DANGEROUS_MIN_CONF:
        return None
    score = max(70, min(int(d.get("threat_score", int(conf * 100))), 97))
    pct = int(conf * 100)
    return {
        "verdict": "DANGEROUS",
        "threat_score": score,
        "threat_type": "phishing",
        "source": "ml_model",
        "reason_kk": f"ML моделі (XLM-RoBERTa) фишинг деп жіктеді ({pct}% сенімділік)",
        "reason_ru": f"ML-модель (XLM-RoBERTa) классифицировала как фишинг ({pct}% уверенности)",
        "reason_en": f"ML model (XLM-RoBERTa) classified as phishing ({pct}% confidence)",
        "indicators": [f"ml_confidence_{pct}pct"],
        "ml": {"confidence": conf, "latency_ms": d.get("latency_ms")},
    }


async def ml_health() -> dict:
    """Health status for /health. 'disabled' when ML_SERVICE_URL unset."""
    base = _service_url()
    if not base:
        return {"status": "disabled", "reason": "ML_SERVICE_URL not set"}
    if _breaker_open():
        return {"status": "error", "reason": "circuit open (service failing)"}
    try:
        r = await get_client().get(f"{base}/", timeout=ML_TIMEOUT)
        if r.status_code == 200:
            d = r.json()
            return {"status": "ok", "model": d.get("model"), "device": d.get("device")}
        return {"status": "error", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:80]}
