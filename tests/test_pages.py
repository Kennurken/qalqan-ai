"""HTML pages still render after the templates.py extraction."""
from fastapi.testclient import TestClient

import api.index as m

client = TestClient(m.app)


def test_landing_renders_for_browser():
    r = client.get("/", headers={"Accept": "text/html"})
    assert r.status_code == 200
    assert "6-деңгейлі" in r.text          # honest 6-tier pipeline
    assert "XLM-RoBERTa" not in r.text      # ML marketing stays removed
    assert len(r.text) > 5000


def test_root_serves_json_to_api_clients():
    r = client.get("/")  # no text/html Accept → JSON
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/json")


def test_dashboard_and_install_render():
    assert 'id="kzmap"' in client.get("/dashboard").text
    assert "<!DOCTYPE html>" in client.get("/install").text


def test_templates_module_exposes_constants():
    from api import templates
    assert all(isinstance(getattr(templates, n), str)
               for n in ("LANDING_HTML", "DASHBOARD_HTML", "INSTALL_HTML"))
