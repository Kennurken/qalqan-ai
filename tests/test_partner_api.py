"""Partner (B2G) API: key auth, endpoints, demo key."""
from fastapi.testclient import TestClient

import api.index as m
from api.utils.api_auth import DEMO_KEY

client = TestClient(m.app)
H = {"X-API-Key": DEMO_KEY}


def test_check_requires_key():
    r = client.post("/v1/check", json={"url": "google.com", "lang": "ru"})
    assert r.status_code == 401


def test_check_with_demo_key():
    # google.com is whitelisted → fast SAFE, no external calls
    r = client.post("/v1/check", json={"url": "google.com", "lang": "ru"}, headers=H)
    assert r.status_code == 200
    d = r.json()
    assert d["partner"] == "Demo (rate-limited)"
    assert "request_id" in d
    assert d["result"]["verdict"] == "SAFE"


def test_feed_requires_key():
    assert client.get("/v1/feed").status_code == 401
    r = client.get("/v1/feed", headers=H)
    assert r.status_code == 200
    assert r.json()["count"] > 50


def test_usage_counter():
    r = client.get("/v1/usage", headers=H)
    assert r.status_code == 200
    assert r.json()["partner"] == "Demo (rate-limited)"
    assert r.json()["rate_limit_per_min"] == 30


def test_partner_docs_page():
    r = client.get("/partners")
    assert r.status_code == 200
    assert "X-API-Key" in r.text
    assert "qalqan-demo-2026" in r.text


def test_env_keys_parsed(monkeypatch):
    monkeypatch.setenv("QALQAN_API_KEYS", "bankkey:Halyk Bank")
    from api.utils.api_auth import verify_api_key
    assert verify_api_key("bankkey") == "Halyk Bank"
