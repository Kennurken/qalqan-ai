"""Mobile PWA: app shell, service worker, manifest."""
from fastapi.testclient import TestClient

import api.index as m

client = TestClient(m.app)


def test_mobile_app_shell():
    r = client.get("/m")
    assert r.status_code == 200
    assert "serviceWorker" in client.get("/static/mobile.js").text or "serviceWorker" in r.text          # SW registration present
    assert "manifest.webmanifest" in r.text
    assert r.text.count("data-t=") == 4        # 4 bottom-nav tabs


def test_service_worker():
    r = client.get("/sw.js")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/javascript")
    assert r.headers.get("service-worker-allowed") == "/"
    assert "caches.open" in r.text


def test_manifest_is_installable():
    d = client.get("/manifest.webmanifest").json()
    assert d["start_url"] == "/m"
    assert d["display"] == "standalone"
    assert d["scope"] == "/"
    assert len(d["icons"]) >= 2


def test_landing_links_to_mobile():
    r = client.get("/", headers={"accept": "text/html"})
    assert '/m"' in r.text
