# Features round 7: brand monitoring, channel dedupe, email leak, batch UI, feed cron.
import asyncio

import pytest
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
    assert "BarcodeDetector" in t   # native decoder path


def test_brand_page_has_live_scan():
    t = client.get("/brand").text
    assert "livego" in t
    assert "/brand/live-scan" in t
    assert "watchgo" in t
