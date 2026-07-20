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


def _og_block(html: str) -> str:
    """Derive OpenGraph/Twitter card tags from the page's <title> and meta
    description — social shares get a proper card on every page."""
    import re as _re
    if 'og:title' in html:
        return html
    t = _re.search(r"<title>([^<]{3,90})</title>", html)
    d = _re.search(r'<meta name="description" content="([^"]{3,220})"', html)
    if not t:
        return html
    title = t.group(1).strip()
    desc = d.group(1).strip() if d else "AI-қорғаныс: фишинг, алаяқтық, пирамидалар — Qalqan AI"
    tags = (
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{desc}">\n'
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:site_name" content="Qalqan AI">\n'
        f'<meta name="twitter:card" content="summary">\n'
        f'<meta name="twitter:title" content="{title}">\n'
        f'<meta name="twitter:description" content="{desc}">\n'
    )
    return html.replace("</head>", tags + "</head>", 1)


for _n in ['LANDING_HTML', 'DASHBOARD_HTML', 'INSTALL_HTML', 'MINIAPP_HTML', 'GRAPH_HTML', 'MOBILE_HTML', 'SW_JS', 'PARTNERS_HTML', 'NOTFOUND_HTML', 'LEAK_HTML', 'HELP_HTML', 'BRAND_HTML', 'SCAN_HTML', 'IMPACT_HTML', 'BATCH_HTML', 'SCREEN_HTML']:
    if _n != "SW_JS" and "beacon.js" not in _g[_n]:
        _g[_n] = _g[_n].replace("</body>", _BEACON, 1)
    if _n != "SW_JS":
        _g[_n] = _og_block(_g[_n])
    _g[_n] = _g[_n].replace("__V__", _V)

__all__ = ['LANDING_HTML', 'DASHBOARD_HTML', 'INSTALL_HTML', 'MINIAPP_HTML', 'GRAPH_HTML', 'MOBILE_HTML', 'SW_JS', 'PARTNERS_HTML', 'NOTFOUND_HTML', 'LEAK_HTML', 'HELP_HTML', 'BRAND_HTML', 'SCAN_HTML', 'IMPACT_HTML', 'BATCH_HTML', 'SCREEN_HTML']
