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
    assert "pwnedpasswords.com" in client.get("/static/leak.js").text
    assert "SHA-1" in r.text


def test_landing_has_no_stale_tier_count():
    t = client.get("/", headers={"Accept": "text/html"}).text
    assert "6-tier" not in t and "6-деңгей" not in t and "6-уровн" not in t


def test_localhost_any_port_origin_allowed():
    import api.index as _m
    assert _m._cors_origin_allowed("http://localhost:8899") is True
    assert _m._cors_origin_allowed("http://127.0.0.1:5500") is True
    assert _m._cors_origin_allowed("https://evil.example.com") is False


def test_robots_and_sitemap():
    r = client.get("/robots.txt")
    assert r.status_code == 200 and "Disallow: /admin" in r.text
    s = client.get("/sitemap.xml")
    assert s.status_code == 200 and "/leak" in s.text


def test_hero_has_seven_tiers_and_chips():
    t = client.get("/", headers={"Accept": "text/html"}).text
    assert 'data-to="7">7' in t          # hero stat
    assert 'class="chip"' in t           # mobile-visible feature chips
    assert 'chip_leak' in t              # i18n wired


def test_help_resources_page():
    r = client.get("/help")
    assert r.status_code == 200
    assert "1477" in r.text          # Нацбанк antifraud hotline
    assert "102" in r.text           # police
    assert "cert.gov.kz" in r.text   # KZ-CERT
    assert "/help" in client.get("/sitemap.xml").text


def test_brand_protection():
    r = client.post("/brand/scan", json={"domain": "kaspi.kz"})
    assert r.status_code == 200
    d = r.json()
    assert d["total"] > 5
    assert d["risk_counts"]["critical"] >= 1   # homoglyph variants
    assert any(v["kind"] == "homoglyph" for v in d["variants"])
    # invalid domain handled
    assert client.post("/brand/scan", json={"domain": "!!!"}).json().get("error") == "invalid_domain"
    assert client.get("/brand").status_code == 200


def test_security_scan_grade():
    r = client.get("/scan/github.com")
    assert r.status_code == 200
    d = r.json()
    assert d["grade"] in ("A+", "A", "B", "C", "D", "E", "F")
    assert "factors" in d and len(d["factors"]) >= 4
    assert client.get("/scan").status_code == 200


def test_scan_and_brand_in_sitemap():
    s = client.get("/sitemap.xml").text
    assert "/brand" in s and "/scan" in s


def test_landing_has_accuracy_proof():
    t = client.get("/", headers={"Accept": "text/html"}).text
    assert 'class="proof' in t and "97%" in t


def test_impact_calculator_page():
    r = client.get("/impact")
    assert r.status_code == 200
    assert "16,4 млрд" in r.text            # KZ 2025 fraud stat
    assert "applyLang" in client.get("/static/impact.js").text   # kk/ru toggle wired
    assert "/impact" in client.get("/sitemap.xml").text


