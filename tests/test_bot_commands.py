# Bot command dispatch tests. send_message + Supabase are stubbed so we assert
# routing/side-effects without touching Telegram or the network.
import asyncio

import pytest

import api.services.bot_handler as bh


class _Capture:
    def __init__(self):
        self.sent = []

    async def __call__(self, chat_id, text, **kw):
        self.sent.append((chat_id, text))
        return True


@pytest.fixture
def sent(monkeypatch):
    cap = _Capture()
    monkeypatch.setattr(bh, "send_message", cap)
    return cap


def _msg(text):
    return {"message": {"chat": {"id": 42}, "message_id": 1,
                        "from": {"first_name": "T"}, "text": text}}


def _run(coro):
    return asyncio.run(coro)


def test_start_lists_watch_and_subscribe(sent):
    _run(bh.dispatch(_msg("/start")))
    body = " ".join(t for _, t in sent.sent)
    assert "/watch" in body and "/subscribe" in body and "/sos" in body


def test_help_lists_new_commands(sent):
    _run(bh.dispatch(_msg("/help")))
    body = " ".join(t for _, t in sent.sent)
    assert "/watchlist" in body and "/leak" in body


def test_watch_requires_domain(sent):
    _run(bh.dispatch(_msg("/watch")))
    assert any("watch" in t.lower() for _, t in sent.sent)


def test_watch_valid_domain_degrades_without_storage(sent, monkeypatch):
    async def _ok(*a, **k):
        return False
    monkeypatch.setattr("api.utils.supabase.add_brand_watch", _ok)
    monkeypatch.setattr("api.utils.supabase.add_brand_watch_chat", _ok)
    _run(bh.dispatch(_msg("/watch kaspi.kz")))
    assert sent.sent  # replied, no exception


def test_unwatch_replies(sent, monkeypatch):
    async def _ok(*a, **k):
        return True
    monkeypatch.setattr("api.utils.supabase.remove_brand_watch_chat", _ok)
    _run(bh.dispatch(_msg("/unwatch kaspi.kz")))
    assert sent.sent


def test_subscribe_replies(sent, monkeypatch):
    async def _ok(*a, **k):
        return True
    monkeypatch.setattr("api.utils.supabase.add_digest_sub", _ok)
    _run(bh.dispatch(_msg("/subscribe")))
    assert any("дайджест" in t.lower() for _, t in sent.sent)


def test_plain_url_triggers_check(monkeypatch):
    calls = []

    async def _fake_check(chat_id, url, message_id=None):
        calls.append(url)
    monkeypatch.setattr(bh, "handle_check", _fake_check)
    # send_message stub too (start of flow may message)
    monkeypatch.setattr(bh, "send_message", _Capture())
    _run(bh.dispatch(_msg("kaspi-bonus.top")))
    assert calls and "kaspi-bonus.top" in calls[0]
