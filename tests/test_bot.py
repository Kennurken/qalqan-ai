"""Bot dispatcher routing + voice pipeline (mocked — no network)."""
import asyncio

import api.services.bot_handler as bh
import api.services.voice_scam as vs


def _run(coro):
    return asyncio.run(coro)


def test_dispatch_routes_voice(monkeypatch):
    called = {}
    async def fake_voice(chat_id, file_id, message_id=None):
        called["voice"] = (chat_id, file_id)
    monkeypatch.setattr(bh, "handle_voice", fake_voice)
    _run(bh.dispatch({"message": {"chat": {"id": 5}, "message_id": 1,
                                  "voice": {"file_id": "VOICE123"}}}))
    assert called.get("voice") == (5, "VOICE123")


def test_dispatch_routes_callback(monkeypatch):
    called = {}
    async def fake_cb(cb):
        called["cb"] = cb.get("data")
    monkeypatch.setattr(bh, "handle_callback", fake_cb)
    _run(bh.dispatch({"callback_query": {"id": "x", "data": "v:c:scam.kz",
                                         "from": {"id": 9}}}))
    assert called.get("cb") == "v:c:scam.kz"


def test_dispatch_routes_command(monkeypatch):
    sent = []
    async def fake_send(chat_id, text, **kw):
        sent.append(text)
        return {}
    monkeypatch.setattr(bh, "send_message", fake_send)
    _run(bh.dispatch({"message": {"chat": {"id": 7}, "message_id": 2, "text": "/help",
                                  "from": {"first_name": "A"}}}))
    assert any("Қалай" in t or "Нұсқаулық" in t or "/check" in t for t in sent)


def test_dispatch_ignores_empty():
    # no message / no text — must not raise
    _run(bh.dispatch({}))
    _run(bh.dispatch({"message": {"chat": {"id": 1}, "message_id": 1}}))


def test_transcribe_no_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    assert _run(vs.transcribe_audio(b"\x00\x01")) is None


def test_analyze_voice_transcription_fail(monkeypatch):
    async def fake_transcribe(audio, filename="a.ogg"):
        return None
    monkeypatch.setattr(vs, "transcribe_audio", fake_transcribe)
    r = _run(vs.analyze_voice(b"data", "a.ogg"))
    assert r["verdict"] == "UNKNOWN"
    assert "error" in r
