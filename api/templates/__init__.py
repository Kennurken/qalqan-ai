# Qalqan AI page templates — one module per page (HTML only; JS lives in api/static).
import os

from .landing import LANDING_HTML
from .dashboard import DASHBOARD_HTML
from .install import INSTALL_HTML
from .miniapp import MINIAPP_HTML
from .graph import GRAPH_HTML
from .mobile import MOBILE_HTML
from .sw import SW_JS
from .partners import PARTNERS_HTML
from .notfound import NOTFOUND_HTML
from .leak import LEAK_HTML
from .help_page import HELP_HTML
from .brand import BRAND_HTML
from .scan import SCAN_HTML
from .impact import IMPACT_HTML
from .batch import BATCH_HTML
from .screen import SCREEN_HTML

# Cache-busting token for /static assets: substituted into every page at import.
# Prod: commit sha (stable per deploy). Dev: startup time, so local edits are
# never pinned by the immutable cache.
_V = (os.getenv("VERCEL_GIT_COMMIT_SHA") or "").strip()[:8] or f"dev{int(__import__('time').time())}"
_g = globals()
_BEACON = '<script src="/static/beacon.js?v=__V__" defer></script>\n</body>'
for _n in ['LANDING_HTML', 'DASHBOARD_HTML', 'INSTALL_HTML', 'MINIAPP_HTML', 'GRAPH_HTML', 'MOBILE_HTML', 'SW_JS', 'PARTNERS_HTML', 'NOTFOUND_HTML', 'LEAK_HTML', 'HELP_HTML', 'BRAND_HTML', 'SCAN_HTML', 'IMPACT_HTML', 'BATCH_HTML', 'SCREEN_HTML']:
    if _n != "SW_JS" and "beacon.js" not in _g[_n]:
        _g[_n] = _g[_n].replace("</body>", _BEACON, 1)
    _g[_n] = _g[_n].replace("__V__", _V)

__all__ = ['LANDING_HTML', 'DASHBOARD_HTML', 'INSTALL_HTML', 'MINIAPP_HTML', 'GRAPH_HTML', 'MOBILE_HTML', 'SW_JS', 'PARTNERS_HTML', 'NOTFOUND_HTML', 'LEAK_HTML', 'HELP_HTML', 'BRAND_HTML', 'SCAN_HTML', 'IMPACT_HTML', 'BATCH_HTML', 'SCREEN_HTML']
