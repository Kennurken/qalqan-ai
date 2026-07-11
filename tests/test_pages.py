"""HTML pages still render after the templates.py extraction."""
from fastapi.testclient import TestClient

import api.index as m

client = TestClient(m.app)


def test_landing_renders_for_browser():
    r = client.get("/", headers={"Accept": "text/html"})
    assert r.status_code == 200
    assert "7-деңгейлі" in r.text          # 7-tier pipeline (community + ML added)
    assert "XLM-RoBERTa" not in r.text      # ML marketing stays removed
    assert len(r.text) > 5000


def test_root_serves_json_to_api_clients():
    r = client.get("/")  # no text/html Accept → JSON
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/json")


def test_dashboard_and_install_render():
    assert 'id="kzsvg"' in client.get("/dashboard").text  # real SVG choropleth (was grid tiles)
    assert "<!DOCTYPE html>" in client.get("/install").text


def test_templates_module_exposes_constants():
    from api import templates
    assert all(isinstance(getattr(templates, n), str)
               for n in ("LANDING_HTML", "DASHBOARD_HTML", "INSTALL_HTML"))


def test_quiz_page_renders():
    r = client.get("/quiz")
    assert r.status_code == 200
    assert "Скам-тренажёр" in r.text
    assert "QUESTIONS" in r.text


def test_kz_regions_geometry():
    r = client.get("/kz-regions.js")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/javascript")
    # all 20 post-2022 regions present (incl. the three new oblasts + Shymkent)
    for name in ("Қызылорда", "Абай", "Жетісу", "Ұлытау", "Шымкент"):
        assert name in r.text


def test_leak_page_renders():
    r = client.get("/leak")
    assert r.status_code == 200
    assert "pwnedpasswords.com" in r.text
    assert "SHA-1" in r.text


def test_landing_has_no_stale_tier_count():
    t = client.get("/", headers={"Accept": "text/html"}).text
    assert "6-tier" not in t and "6-деңгей" not in t and "6-уровн" not in t


def test_localhost_any_port_origin_allowed():
    import api.index as _m
    assert _m._cors_origin_allowed("http://localhost:8899") is True
    assert _m._cors_origin_allowed("http://127.0.0.1:5500") is True
    assert _m._cors_origin_allowed("https://evil.example.com") is False
