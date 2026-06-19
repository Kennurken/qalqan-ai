"""Import smoke tests — catch the import/wiring errors the extension-only CI misses."""
import importlib

import pytest

API_MODULES = [
    "api.index",
    "api.services.scoring",
    "api.services.url_features",
    "api.services.domain_intel",
    "api.services.pyramid_detector",
    "api.services.pyramid_registry",
    "api.services.kz_intel",
    "api.services.threat_db",
    "api.services.goszakup",
    "api.services.ai_analyzer",
    "api.services.bot_handler",
    "api.services.explainer",
    "api.services.threat_report",
    "api.utils.cache",
    "api.utils.supabase",
    "api.utils.i18n",
    "api.utils.telegram",
]


@pytest.mark.parametrize("mod", API_MODULES)
def test_module_imports(mod):
    importlib.import_module(mod)


def test_app_has_expected_routes():
    from api.index import app
    paths = {getattr(r, "path", "") for r in app.routes}
    for p in ["/check", "/pyramid/check", "/dashboard", "/dashboard/data", "/vote", "/community/{domain}"]:
        assert p in paths, f"route {p} missing"


def test_to_domain_normalizes():
    from api.index import _to_domain
    assert _to_domain("kaspi.kz") == "kaspi.kz"
    assert _to_domain("https://x.kz/a?b=1") == "x.kz"
    assert _to_domain("http://www.foo.kz") == "foo.kz"
    assert _to_domain("") == ""
