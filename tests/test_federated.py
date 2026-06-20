"""Federated threat-sharing: partner contribution + federated feed."""
from fastapi.testclient import TestClient

import api.index as m
from api.utils.api_auth import DEMO_KEY

client = TestClient(m.app)
H = {"X-API-Key": DEMO_KEY}


def test_contribute_requires_key():
    r = client.post("/v1/contribute", json={"indicator": "scam.kz", "type": "phishing"})
    assert r.status_code == 401


def test_contribute_with_key():
    r = client.post("/v1/contribute",
                    json={"indicator": "https://fake-egov.kz/login", "type": "phishing",
                          "evidence": "credential harvesting"},
                    headers=H)
    assert r.status_code == 200
    d = r.json()
    assert d["accepted"] is True
    assert d["indicator"] == "fake-egov.kz"
    assert d["type"] == "phishing"


def test_federated_feed_public():
    d = client.get("/feed/federated").json()
    assert d["license"] == "CC-BY-4.0"
    assert d["curated_count"] > 50
    assert "partner_contributions" in d["sources"]
    assert isinstance(d["contributed"], list)


def test_feed_index_lists_federated():
    d = client.get("/feed").json()
    assert "federated_feed" in d
