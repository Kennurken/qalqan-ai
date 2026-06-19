"""Security regression tests: CORS extension pinning (P0-5) + admin auth (P0-4)."""
from fastapi.testclient import TestClient

import api.index as m

client = TestClient(m.app)


# ── P0-5: CORS extension allowlist ────────────────────────────────────────────
def test_cors_dev_allows_any_extension(monkeypatch):
    monkeypatch.delenv("QALQAN_EXTENSION_IDS", raising=False)
    assert m._cors_origin_allowed("chrome-extension://anyrandomid") is True


def test_cors_prod_pins_extension_ids(monkeypatch):
    monkeypatch.setenv("QALQAN_EXTENSION_IDS", "goodid111,goodid222")
    assert m._cors_origin_allowed("chrome-extension://goodid111") is True
    assert m._cors_origin_allowed("chrome-extension://evil999") is False


def test_cors_rejects_random_web_origin():
    assert m._cors_origin_allowed("https://evil.example.com") is False


# ── P0-4: admin auth ──────────────────────────────────────────────────────────
def test_admin_requires_secret(monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET", "s3cret")
    assert client.get("/admin").status_code == 401
    assert client.get("/admin?key=wrong").status_code == 401


def test_admin_query_key_redirects_and_sets_cookie(monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET", "s3cret")
    r = client.get("/admin?key=s3cret", follow_redirects=False)
    assert r.status_code == 303
    assert r.headers["location"] == "/admin"
    assert "qadmin" in r.headers.get("set-cookie", "")
    assert "httponly" in r.headers.get("set-cookie", "").lower()


def test_admin_header_key_authorizes(monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET", "s3cret")
    r = client.get("/admin", headers={"X-Admin-Key": "s3cret"})
    assert r.status_code == 200
    assert "401" not in r.text[:200]
