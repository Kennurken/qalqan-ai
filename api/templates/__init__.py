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
    img = "https://qalqan-ai-nu.vercel.app/og.png"
    tags = (
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{desc}">\n'
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:site_name" content="Qalqan AI">\n'
        f'<meta property="og:image" content="{img}">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{title}">\n'
        f'<meta name="twitter:description" content="{desc}">\n'
        f'<meta name="twitter:image" content="{img}">\n'
    )
    return html.replace("</head>", tags + "</head>", 1)


# Template → canonical route, for <link rel=canonical> + og:url (dedupe ?param
# variants in search, give social cards a real URL). NOTFOUND has no canonical.
_ROUTES = {
    'LANDING_HTML': '/', 'DASHBOARD_HTML': '/dashboard', 'INSTALL_HTML': '/install',
    'MINIAPP_HTML': '/app', 'GRAPH_HTML': '/goszakup/graph', 'MOBILE_HTML': '/m',
    'PARTNERS_HTML': '/partners', 'LEAK_HTML': '/leak', 'HELP_HTML': '/help',
    'BRAND_HTML': '/brand', 'SCAN_HTML': '/scan', 'IMPACT_HTML': '/impact',
    'BATCH_HTML': '/batch-check', 'SCREEN_HTML': '/screen',
}
_ORIGIN = "https://qalqan-ai-nu.vercel.app"

for _n in ['LANDING_HTML', 'DASHBOARD_HTML', 'INSTALL_HTML', 'MINIAPP_HTML', 'GRAPH_HTML', 'MOBILE_HTML', 'SW_JS', 'PARTNERS_HTML', 'NOTFOUND_HTML', 'LEAK_HTML', 'HELP_HTML', 'BRAND_HTML', 'SCAN_HTML', 'IMPACT_HTML', 'BATCH_HTML', 'SCREEN_HTML']:
    if _n != "SW_JS" and "beacon.js" not in _g[_n]:
        _g[_n] = _g[_n].replace("</body>", _BEACON, 1)
    if _n != "SW_JS":
        _g[_n] = _og_block(_g[_n])
    if _n != "SW_JS" and "apple-touch-icon" not in _g[_n]:
        _g[_n] = _g[_n].replace(
            "</head>", '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n</head>', 1)
    if _n in _ROUTES:
        _url = _ORIGIN + _ROUTES[_n]
        _head = ""
        if 'rel="canonical"' not in _g[_n]:
            _head += f'<link rel="canonical" href="{_url}">\n'
        if 'og:url' not in _g[_n]:
            _head += f'<meta property="og:url" content="{_url}">\n'
        if _head:
            _g[_n] = _g[_n].replace("</head>", _head + "</head>", 1)
    _g[_n] = _g[_n].replace("__V__", _V)

__all__ = ['LANDING_HTML', 'DASHBOARD_HTML', 'INSTALL_HTML', 'MINIAPP_HTML', 'GRAPH_HTML', 'MOBILE_HTML', 'SW_JS', 'PARTNERS_HTML', 'NOTFOUND_HTML', 'LEAK_HTML', 'HELP_HTML', 'BRAND_HTML', 'SCAN_HTML', 'IMPACT_HTML', 'BATCH_HTML', 'SCREEN_HTML']
