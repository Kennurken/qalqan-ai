"""AFM/ARDFM pyramid name-lookup tests (pure, loads bundled JSON)."""
import pytest

from api.services.pyramid_registry import check_pyramid_name, registry_size, _normalize


def test_registry_loaded():
    assert registry_size() > 30  # AFM seed + reused domain schemes


@pytest.mark.parametrize("name", ["Финико", "finiko", "ТОО «Финико»", "  finiko  "])
def test_finiko_variants_flagged(name):
    r = check_pyramid_name(name, "ru")
    assert r is not None
    assert r["verdict"] == "DANGEROUS"
    assert r["threat_score"] == 95
    assert r["match"] == "Finiko"


def test_fuzzy_match_below_one():
    r = check_pyramid_name("Финіко", "ru")  # Cyrillic і typo
    assert r is not None
    assert r["match"] == "Finiko"
    assert r["confidence"] < 1.0


@pytest.mark.parametrize("name", ["Каспи Банк", "мой магазин", "Halyk Bank", "", "ab"])
def test_clean_names_not_listed(name):
    assert check_pyramid_name(name, "ru") is None


def test_normalize_strips_legal_forms():
    assert _normalize("ТОО «Финико»") == "финико"
    assert _normalize("Questra World LLP") == "questra world"
