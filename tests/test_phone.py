"""KZ phone-number scam analysis."""
from fastapi.testclient import TestClient

import api.index as m
from api.services.phone_sms import analyze_phone, normalize_kz_phone, extract_urls

client = TestClient(m.app)


def test_normalize_8_prefix():
    assert normalize_kz_phone("8 701 234 56 78") == "77012345678"
    assert normalize_kz_phone("+7 (777) 000-00-00") == "77770000000"
    assert normalize_kz_phone("12345") is None


def test_vanity_scam_number():
    r = analyze_phone("+7 777 700 00 00", "ru")
    assert r["verdict"] == "SUSPICIOUS"
    assert "formatted" in r


def test_normal_number_safe():
    r = analyze_phone("+7 701 345 67 12", "ru")
    assert r["verdict"] == "SAFE"
    assert r["threat_score"] <= 20


def test_invalid_number():
    r = analyze_phone("hello", "kk")
    assert r["verdict"] == "UNKNOWN"
    assert r["error"] == "invalid_kz_phone"


def test_phone_endpoint():
    r = client.post("/phone", json={"phone": "+7 700 111 11 11", "lang": "ru"})
    assert r.status_code == 200
    assert r.json()["source"] == "phone_check"


def test_extract_urls():
    urls = extract_urls("Срочно перейдите kaspi-fake.kz и halyk.com/login")
    assert any("kaspi-fake.kz" in u for u in urls)
