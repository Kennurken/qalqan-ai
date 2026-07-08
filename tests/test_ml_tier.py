"""ML model tier (Tier 2.8) — external XLM-RoBERTa service client."""
import asyncio

import api.services.ml_model as ml


class _FakeResp:
    def __init__(self, data, status=200):
        self._data = data
        self.status_code = status

    def json(self):
        return self._data


class _FakeClient:
    def __init__(self, data, status=200):
        self._resp = _FakeResp(data, status)

    async def post(self, *a, **k):
        return self._resp

    async def get(self, *a, **k):
        return self._resp


def _reset_breaker():
    ml._fail_count = 0
    ml._open_until = 0.0


def test_disabled_without_env(monkeypatch):
    monkeypatch.delenv("ML_SERVICE_URL", raising=False)
    assert ml.ml_enabled() is False
    assert asyncio.run(ml.ml_predict("https://evil.example")) is None


def test_confident_dangerous_becomes_hit(monkeypatch):
    monkeypatch.setenv("ML_SERVICE_URL", "http://localhost:8001")
    _reset_breaker()
    monkeypatch.setattr(ml, "get_client", lambda: _FakeClient(
        {"verdict": "DANGEROUS", "confidence": 0.97, "threat_score": 97}))
    hit = asyncio.run(ml.ml_predict("https://kaspi-fake.tk"))
    assert hit is not None
    assert hit["verdict"] == "DANGEROUS"
    assert hit["source"] == "ml_model"
    assert 70 <= hit["threat_score"] <= 97


def test_low_confidence_is_ignored(monkeypatch):
    monkeypatch.setenv("ML_SERVICE_URL", "http://localhost:8001")
    _reset_breaker()
    monkeypatch.setattr(ml, "get_client", lambda: _FakeClient(
        {"verdict": "DANGEROUS", "confidence": 0.6, "threat_score": 60}))
    assert asyncio.run(ml.ml_predict("https://maybe.example")) is None


def test_safe_verdict_is_ignored(monkeypatch):
    monkeypatch.setenv("ML_SERVICE_URL", "http://localhost:8001")
    _reset_breaker()
    monkeypatch.setattr(ml, "get_client", lambda: _FakeClient(
        {"verdict": "SAFE", "confidence": 0.99, "threat_score": 1}))
    assert asyncio.run(ml.ml_predict("https://kaspi.kz")) is None


def test_health_disabled(monkeypatch):
    monkeypatch.delenv("ML_SERVICE_URL", raising=False)
    assert asyncio.run(ml.ml_health())["status"] == "disabled"


def test_run_pipeline_internal_in_process():
    """Bot path: whole pipeline callable without Request/BackgroundTasks."""
    from api.index import run_pipeline_internal
    r = asyncio.run(run_pipeline_internal("https://google.com", "ru"))
    assert r["verdict"] == "SAFE"
    assert r["source"] == "whitelist"
