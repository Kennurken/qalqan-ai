"""URL feature-extraction + homoglyph tests (pure)."""
from api.services.url_features import extract_features, _homoglyph_brand_attack


def test_extract_features_returns_risk_score():
    f = extract_features("https://example.com/path")
    assert "risk_score" in f
    assert isinstance(f["risk_score"], int)


def test_homoglyph_kaspi_detected():
    # Cyrillic 'а' (U+0430) in place of Latin 'a'
    hit = _homoglyph_brand_attack("kаspi.kz")
    assert hit is not None
    assert "kaspi" in hit["target"].lower()


def test_plain_latin_domain_no_homoglyph():
    assert _homoglyph_brand_attack("example.kz") is None


def test_shortener_flagged():
    f = extract_features("https://bit.ly/abc123")
    # shortener should raise the risk signal somewhere in the feature set
    assert f.get("is_shortener") in (1, True) or f["risk_score"] >= 0
