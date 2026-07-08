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


# ── H1: stored-XSS defense (domain sanitization + HTML escaping) ──────────────
def test_to_domain_strips_html_metacharacters():
    # urlparse().hostname passes through '<'/'>' — a crafted URL must NOT yield a
    # domain containing HTML metacharacters that could break out in /admin or /stats.
    dom = m._to_domain("https://abc<script>alert(1)</script>.kz")
    assert "<" not in dom and ">" not in dom
    assert m._DOMAIN_SANITIZE_RE.search(dom) is None


def test_report_payload_cannot_inject_html_into_domain(monkeypatch):
    # A report with an XSS-shaped URL is stored with a sanitized domain.
    monkeypatch.setattr(m, "_whitelist", set())
    dom = m._to_domain("javascript:alert(1)//<img src=x onerror=alert(1)>.kz")
    assert "<" not in dom and '"' not in dom and "'" not in dom


def test_stats_html_renders_with_data(monkeypatch):
    # Regression: a local var named `html` shadowed the `import html`, 500-ing the
    # page whenever there was data to escape. Must render 200 with populated trends.
    async def fake_trends(*a, **k):
        return {"total_checks": 83,
                "verdict_distribution": {"DANGEROUS": 45, "SAFE": 23, "SUSPICIOUS": 15},
                "top_domains_checked": [{"domain": "kaspi.kz", "checks": 10}],
                "top_reported_domains": [{"domain": "1xbet.com", "reports": 7, "auto_blocked": True}]}
    monkeypatch.setattr(m, "supabase_trends", fake_trends)
    r = client.get("/stats", headers={"Accept": "text/html"})
    assert r.status_code == 200
    assert "kaspi.kz" in r.text


def test_admin_escapes_stored_xss_in_rows(monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET", "s3cret")
    async def fake_admin(*a, **k):
        return {"reports": [{"domain": "x<script>alert(1)</script>.kz", "category": "scam",
                             "comment": "<img src=x onerror=alert(1)>", "lang": "ru",
                             "created_at": "2026-07-02T00:00:00"}],
                "appeals": [], "check_logs": []}
    monkeypatch.setattr(m, "get_admin_data", fake_admin)
    r = client.get("/admin", headers={"X-Admin-Key": "s3cret"})
    assert r.status_code == 200
    assert "<script>alert(1)" not in r.text
    assert "&lt;script&gt;" in r.text


# ── N7: security headers on the (primary) Vercel deploy ───────────────────────
def test_security_headers_present_on_all_responses():
    r = client.get("/ping")
    assert r.headers.get("x-content-type-options") == "nosniff"
    assert r.headers.get("referrer-policy") == "strict-origin-when-cross-origin"
    assert "max-age=" in r.headers.get("strict-transport-security", "")


def test_admin_is_frame_denied_but_miniapp_is_not(monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET", "s3cret")
    a = client.get("/admin")  # 401 page still carries the frame guard
    assert a.headers.get("x-frame-options") == "DENY"
    mini = client.get("/app")  # Telegram Mini App must remain iframe-embeddable
    assert mini.headers.get("x-frame-options") != "DENY"
