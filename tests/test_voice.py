"""Voice / call-scam transcript analysis (offline — no Groq needed)."""
from api.services.voice_scam import analyze_transcript


def test_scam_call_flagged():
    t = ("Это служба безопасности банка, ваша карта заблокирована, срочно "
         "назовите код из SMS и переведите деньги на безопасный счёт, никому не говорите")
    r = analyze_transcript(t, "ru")
    assert r["verdict"] == "DANGEROUS"
    assert r["threat_score"] >= 50
    assert len(r["red_flags"]) >= 3


def test_clean_call_safe():
    r = analyze_transcript("Привет, встретимся завтра в кафе в три часа", "ru")
    assert r["verdict"] == "SAFE"
    assert r["threat_score"] == 0


def test_kazakh_patterns():
    r = analyze_transcript("банк қауіпсіздік қызметі, картаңыз бұғатталды, дереу код айтыңыз", "kk")
    assert r["verdict"] in ("SUSPICIOUS", "DANGEROUS")
    assert r["threat_score"] >= 25


def test_voice_route_registered():
    routes = {r.path for r in __import__("api.index", fromlist=["app"]).app.routes if hasattr(r, "path")}
    assert "/voice" in routes
