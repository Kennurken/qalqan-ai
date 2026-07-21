# Features round 7: brand monitoring, channel dedupe, email leak, batch UI, feed cron.
import asyncio

from fastapi.testclient import TestClient

from api.index import app

client = TestClient(app)


# --- Brand live-scan / watch ---

def test_brand_live_scan_invalid_domain():
    r = client.post("/brand/live-scan", json={"domain": "!!!"})
    assert r.status_code == 200
    assert r.json().get("error") == "invalid_domain"


def test_brand_watch_invalid_domain():
    r = client.post("/brand/watch", json={"domain": "###"})
    assert r.status_code == 422


def test_brand_watch_valid_domain_no_storage():
    # Without Supabase env the subscribe endpoint degrades gracefully
    r = client.post("/brand/watch", json={"domain": "kaspi.kz"})
    assert r.status_code == 200
    body = r.json()
    assert body["domain"] == "kaspi.kz"
    assert "ok" in body


def test_registered_set_snapshot():
    from api.services.brand_watch import registered_set
    scan = {"registered": [{"domain": "kaspi.tk"}, {"domain": "kaspi-login.kz"}]}
    assert registered_set(scan) == {"kaspi.tk", "kaspi-login.kz"}
    assert registered_set({}) == set()


# --- Cron endpoints fail closed without CRON_SECRET ---

def test_cron_brand_watch_forbidden():
    assert client.get("/cron/brand-watch").status_code == 403


def test_cron_refresh_feeds_forbidden():
    assert client.get("/cron/refresh-feeds").status_code == 403


# --- Channel-post dedupe (memory fallback) ---

def test_once_per_dedupes():
    from api.utils.cache import once_per

    async def _run():
        first = await once_per("test:dedupe-xyz", ttl=60)
        second = await once_per("test:dedupe-xyz", ttl=60)
        return first, second

    first, second = asyncio.run(_run())
    assert first is True
    assert second is False


# --- Email leak ---

def test_leak_email_invalid():
    r = client.get("/leak/email", params={"email": "not-an-email"})
    assert r.status_code == 422


def test_leak_page_has_email_tab():
    t = client.get("/leak").text
    assert "card-em" in t
    assert "XposedOrNot" in t
    assert '/static/leak.js' in t


# --- Batch page ---

def test_batch_check_page():
    r = client.get("/batch-check")
    assert r.status_code == 200
    assert "Массовая проверка" in r.text
    assert "/batch" in r.text
    assert "/batch-check" in client.get("/sitemap.xml").text


# --- Landing: advisor widget + QR ---

def test_landing_has_advisor_and_qr():
    t = client.get("/", headers={"accept": "text/html"}).text
    assert "advPanel" in t          # advisor chat widget
    assert "qrBtn" in t             # QR check button
    js = client.get("/static/landing.js").text
    assert "BarcodeDetector" in js  # native decoder path


def test_brand_page_has_live_scan():
    t = client.get("/brand").text
    assert "livego" in t
    assert "watchgo" in t
    assert "/brand/live-scan" in client.get("/static/brand.js").text


# --- Round 8: screen page, badge, quiz removal, phone crowd ---

def test_screen_page():
    r = client.get("/screen")
    assert r.status_code == 200
    assert "/static/screen.js" in r.text
    assert "analyze-screen" in client.get("/static/screen.js").text
    assert "/screen" in client.get("/sitemap.xml").text


def test_badge_svg():
    r = client.get("/badge/definitely-not-a-domain")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("image/svg")
    assert "Qalqan" in r.text


def test_quiz_removed():
    assert client.get("/quiz").status_code == 404
    assert "/quiz" not in client.get("/sitemap.xml").text
    t = client.get("/", headers={"accept": "text/html"}).text
    assert "/quiz" not in t


def test_leak_has_generator():
    assert "genout" in client.get("/leak").text
    assert "getRandomValues" in client.get("/static/leak.js").text


def test_landing_check_deeplink():
    js = client.get("/static/landing.js").text
    assert "URLSearchParams" in js and "'check'" in js


def test_static_route_hardened():
    assert client.get("/static/../index.py").status_code in (404, 422)
    assert client.get("/static/nope.js").status_code == 404
    r = client.get("/static/landing.js")
    assert r.status_code == 200
    assert "javascript" in r.headers["content-type"]


def test_partners_badge_docs():
    t = client.get("/partners").text
    assert "/badge/" in t


# --- H2: cert watch, trial keys, ops beacons ---

def test_brand_certs_invalid():
    r = client.post("/brand/certs", json={"domain": "!!"})
    assert r.status_code == 200
    assert r.json().get("error") == "invalid_domain"


def test_request_key_validates_email():
    r = client.post("/v1/request-key", json={"org": "TestBank", "email": "nope"})
    assert r.status_code == 422


def test_client_error_beacon_accepts():
    r = client.post("/client-error", json={"k": "err", "m": "x is not defined",
                                           "s": "/static/x.js", "l": 10, "p": "/scan"})
    assert r.status_code == 200


def test_pv_counts_memory_fallback():
    import asyncio
    from api.utils.cache import pv_incr, pv_counts

    async def _run():
        await pv_incr("/scan")
        await pv_incr("/scan")
        return await pv_counts(["/scan"])

    res = asyncio.run(_run())
    assert res.get("/scan") and sum(res["/scan"].values()) >= 2


def test_admin_pv_gated():
    assert client.get("/admin/pv").status_code == 401


def test_beacon_on_pages():
    for p in ["/scan", "/leak", "/partners"]:
        assert "beacon.js" in client.get(p).text
    assert client.get("/static/beacon.js").status_code == 200


def test_partners_selfservice_form():
    t = client.get("/partners").text
    assert "korg" in t and "/static/partners.js" in t


def test_cert_filter_logic():
    from datetime import datetime, timedelta
    from api.services.cert_watch import _filter_entries
    fresh = (datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S")
    stale = (datetime.utcnow() - timedelta(days=40)).strftime("%Y-%m-%dT%H:%M:%S")
    entries = [
        {"name_value": "kaspi-bonus.top\n*.kaspi-bonus.top", "not_before": fresh,
         "issuer_name": "C=US, O=Let's Encrypt, CN=R11"},
        {"name_value": "login.kaspi.kz", "not_before": fresh},      # own domain — excluded
        {"name_value": "kaspi-old.ru", "not_before": stale},        # stale — excluded
        {"name_value": "unrelated.kz", "not_before": fresh},        # no keyword — excluded
    ]
    hits = _filter_entries(entries, "kaspi", "kaspi.kz")
    assert [h["domain"] for h in hits] == ["kaspi-bonus.top"]
    assert hits[0]["issuer"] == "R11"


# --- S1/S2: admin ops rendering + XSS ---

def test_admin_client_error_escaped_and_sectioned():
    from api.pages import render_admin_page
    data = {"check_logs": [], "appeals": [],
            "reports": [
                {"category": "client_error", "domain": "page:/scan",
                 "comment": "[err] <img src=x onerror=alert(1)>", "created_at": "2026-07-20T09:00:00", "lang": "ru"},
                {"category": "api_key", "domain": "h", "comment": "SecretBank",
                 "created_at": "2026-07-20T09:00:00", "lang": "ru"},
            ],
            "pageviews": {"/scan": {"20260720": 5}}}
    h = render_admin_page(data)
    assert "<img src=x onerror" not in h        # escaped
    assert "&lt;img src=x" in h
    assert "SecretBank" not in h                # internal api_key not in reports view
    assert "Frontend Errors" in h and "Pageviews" in h


# --- S5: public status page ---

def test_status_page():
    r = client.get("/status")
    assert r.status_code == 200
    assert "Статус систем" in r.text
    assert "pipeline" in r.text.lower()
    assert "/status" in client.get("/sitemap.xml").text


def test_og_image_endpoint():
    r = client.get("/og.png")
    assert r.status_code == 200
    assert r.headers["content-type"] == "image/png"
    assert r.content[:8] == b"\x89PNG\r\n\x1a\n"   # PNG magic
    assert len(r.content) > 5000


def test_og_image_on_all_pages():
    for p in ["/", "/scan", "/leak", "/brand", "/impact", "/screen", "/batch-check"]:
        t = client.get(p, headers={"accept": "text/html"}).text
        assert '/og.png' in t, p
        assert 'summary_large_image' in t, p
