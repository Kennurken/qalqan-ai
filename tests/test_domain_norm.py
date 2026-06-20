"""Regression: bare domains must normalize to a non-empty domain.

Root cause of the /report empty-domain bug: extract_domain() returns "" for a
scheme-less host, so reports of bare domains were stored with an empty domain
and never surfaced in crowd stats. /report and /appeal now use _to_domain().
"""
import api.index as m
from api.services.threat_db import extract_domain


def test_extract_domain_empty_for_bare():
    # documents the trap _to_domain works around
    assert extract_domain("scam.kz") == ""
    assert extract_domain("https://scam.kz") == "scam.kz"


def test_to_domain_handles_bare():
    assert m._to_domain("scam.kz") == "scam.kz"
    assert m._to_domain("kaspi-bonus.kz/login") == "kaspi-bonus.kz"
    assert m._to_domain("https://halyk.com") == "halyk.com"
    assert m._to_domain("  AUDIT-scam.KZ  ") == "audit-scam.kz"
