"""Published KZ threat feed + feed plumbing tests."""
from fastapi.testclient import TestClient

import api.index as m

client = TestClient(m.app)


def test_kz_feed_has_entries():
    d = client.get("/feed/kz").json()
    assert d["license"] == "CC-BY-4.0"
    assert d["count"] > 50
    assert all("domain" in e and "type" in e for e in d["entries"][:20])


def test_kz_feed_txt_format():
    r = client.get("/feed/kz?format=txt")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/plain")
    assert len(r.text.splitlines()) > 50


def test_feed_index():
    d = client.get("/feed").json()
    assert "kz_feed" in d and "live_threat_feeds" in d
    assert d["kz_feed"]["count"] > 50


def test_feed_stats_shape():
    from api.services.threat_db import feed_stats
    s = feed_stats()
    assert set(s) == {"domains", "openphish_urls", "sources", "age_sec"}
