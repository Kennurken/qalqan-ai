"""Monitoring, public-channel broadcast, partner phone endpoint."""
import asyncio

from fastapi.testclient import TestClient

import api.index as m
from api.utils.api_auth import DEMO_KEY

client = TestClient(m.app)
H = {"X-API-Key": DEMO_KEY}


def test_v1_phone_requires_key():
    assert client.post("/v1/phone", json={"phone": "+77001234567"}).status_code == 401


def test_v1_phone_with_key():
    r = client.post("/v1/phone", json={"phone": "+7 777 700 00 00", "lang": "ru"}, headers=H)
    assert r.status_code == 200
    assert r.json()["partner"] == "Demo (rate-limited)"
    assert r.json()["result"]["source"] == "phone_check"


def test_health_check_closed_when_no_cron_secret(monkeypatch):
    # Fail-closed: without CRON_SECRET the cron-gated endpoint is DENIED
    # (it broadcasts to Telegram, so it must not be open).
    monkeypatch.delenv("CRON_SECRET", raising=False)
    monkeypatch.delenv("ALLOW_UNAUTHENTICATED_CRON", raising=False)
    assert client.get("/health/check").status_code == 403


def test_health_check_open_with_explicit_optout(monkeypatch):
    # Opt-out flag restores the old open behavior when explicitly set.
    monkeypatch.delenv("CRON_SECRET", raising=False)
    monkeypatch.setenv("ALLOW_UNAUTHENTICATED_CRON", "true")
    r = client.get("/health/check")
    assert r.status_code == 200
    assert "status" in r.json()


def test_health_check_gated_with_cron_secret(monkeypatch):
    monkeypatch.setenv("CRON_SECRET", "topsecret")
    assert client.get("/health/check").status_code == 403
    assert client.get("/health/check?secret=topsecret").status_code == 200


def test_channel_broadcast_no_token_is_safe(monkeypatch):
    # no TELEGRAM_CHANNEL_ID / token → must not raise
    monkeypatch.delenv("TELEGRAM_CHANNEL_ID", raising=False)
    from api.utils.telegram import notify_channel, health_alert
    asyncio.run(notify_channel("evil.kz", "DANGEROUS", 95))
    assert asyncio.run(health_alert("test")) is False
