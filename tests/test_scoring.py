"""Unit tests for the verdict scoring engine (pure, no network)."""
from api.services.scoring import calculate_final_verdict


def test_empty_inputs_are_safe():
    r = calculate_final_verdict([], None, None, lang="ru")
    assert r["verdict"] == "SAFE"
    assert r["threat_score"] == 0


def test_pyramid_hit_preserved():
    hit = {"verdict": "DANGEROUS", "threat_score": 95, "threat_type": "pyramid", "source": "pyramid_list"}
    r = calculate_final_verdict([], None, hit, lang="ru")
    assert r["verdict"] == "DANGEROUS"
    assert r["threat_score"] == 95
    assert r["source"] == "pyramid_list"


def test_deterministic_hit_not_cut_by_ai_branch():
    """Regression: gambling SUSPICIOUS/70 must stay 70, not be cut to 49 by *0.7."""
    gambling = {"verdict": "SUSPICIOUS", "threat_score": 70, "threat_type": "gambling", "source": "gambling_list"}
    r = calculate_final_verdict([], None, None, lang="ru", deterministic_hit=gambling)
    assert r["threat_score"] == 70
    assert r["verdict"] == "SUSPICIOUS"
    assert r["source"] == "gambling_list"


def test_db_result_floor_80():
    db = [{"verdict": "DANGEROUS", "threat_score": 90, "threat_type": "phishing", "source": "phishtank"}]
    r = calculate_final_verdict(db, None, None, lang="ru")
    assert r["threat_score"] >= 80
    assert r["verdict"] == "DANGEROUS"


def test_ai_suspicious_is_discounted():
    ai = {"verdict": "SUSPICIOUS", "threat_score": 60, "threat_type": "fraud", "source": "groq_ai"}
    r = calculate_final_verdict([], ai, None, lang="ru")
    assert r["threat_score"] == int(60 * 0.7)
    assert r["verdict"] == "SUSPICIOUS"


def test_url_features_standalone_high_risk():
    uf = {"risk_score": 75, "has_ip_address": False, "is_free_tld": True, "tld": ".tk"}
    r = calculate_final_verdict([], None, None, url_features=uf, lang="ru")
    assert r["verdict"] == "DANGEROUS"
    assert r["threat_score"] == 75


def test_priority_pyramid_over_db_and_ai():
    pyramid = {"verdict": "DANGEROUS", "threat_score": 95, "threat_type": "pyramid", "source": "pyramid_list"}
    db = [{"verdict": "DANGEROUS", "threat_score": 99, "source": "x"}]
    ai = {"verdict": "DANGEROUS", "threat_score": 99, "source": "groq_ai"}
    r = calculate_final_verdict(db, ai, pyramid, lang="ru")
    assert r["source"] == "pyramid_list"
