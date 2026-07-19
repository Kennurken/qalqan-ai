GRAPH_HTML = """<!DOCTYPE html>
<html lang="ru"><head>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Граф госзакупок</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0e16;--panel:#111827;--bd:#1e293b;--tx:#e7ebf3;--mut:#7d8aa0;--cyan:#7aa2f7;--red:#f7768e}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:20px;max-width:1280px;margin:0 auto}
a{color:var(--cyan);text-decoration:none}
.top{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}
h1{font-size:22px;font-weight:800}
.sub{color:var(--mut);font-size:13px;margin:4px 0 16px}
.wrap{display:grid;grid-template-columns:1fr 360px;gap:16px}
.card{background:var(--panel);border:1px solid var(--bd);border-radius:14px;padding:14px}
svg{width:100%;height:auto;background:#0d1424;border-radius:10px}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--mut);margin-top:10px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:middle}
.risk{font-size:15px;margin-bottom:12px}
.risk b{color:var(--red);font-size:20px}
.DANGEROUS{color:var(--red);font-weight:800}.SUSPICIOUS{color:#e0af68;font-weight:800}.SAFE{color:#9ece6a;font-weight:800}
.finding{font-size:13px;padding:9px 10px;border:1px solid var(--bd);border-radius:9px;margin-bottom:8px;display:flex;gap:8px;align-items:flex-start}
.finding .sc{color:var(--red);font-weight:800;font-variant-numeric:tabular-nums}
.foot{color:var(--mut);font-size:12px;margin-top:20px;text-align:center}
@media(max-width:860px){.wrap{grid-template-columns:1fr}}
.qi{width:1em;height:1em;vertical-align:-0.14em;display:inline-block}
:focus-visible{outline:2px solid #7aa2f7;outline-offset:2px;border-radius:4px}
::selection{background:rgba(122,162,247,.32)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
*{scrollbar-width:thin;scrollbar-color:#2a3550 transparent}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-thumb{background:#2a3550;border-radius:5px}::-webkit-scrollbar-track{background:transparent}
</style></head><body>
<div class="top">
  <div><h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="4.5" r="2.5"/><path d="m10.2 6.3-3.9 3.9"/><circle cx="4.5" cy="12" r="2.5"/><path d="M7 12h10"/><circle cx="19.5" cy="12" r="2.5"/><path d="m13.8 17.7 3.9-3.9"/><circle cx="12" cy="19.5" r="2.5"/></svg> Граф госзакупок — аффилированность и сговор</h1>
  <div class="sub">Qalqan AI · экономические угрозы (ДЭР) · <span id="src">—</span></div></div>
  <div><a href="/">← На главную</a> &nbsp; <a href="/goszakup/graph/demo">JSON</a></div>
</div>
<div class="wrap">
  <div class="card">
    <svg id="graph" viewBox="0 0 900 600"></svg>
    <div class="legend">
      <span><span class="dot" style="background:#7aa2f7"></span>Заказчик</span>
      <span><span class="dot" style="background:#bb9af7"></span>Поставщик</span>
      <span><span class="dot" style="background:#e0af68"></span>Учредитель</span>
      <span><span class="dot" style="background:#9ece6a"></span>Адрес</span>
      <span><span class="dot" style="background:#f7768e"></span>Чиновник</span>
      <span><span class="dot" style="background:#f7768e"></span>— красная связь = подозрение</span>
    </div>
  </div>
  <div class="card"><h3 style="font-size:14px;margin-bottom:12px"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 22V4a1 1 0 0 1 .4-.8A6 6 0 0 1 8 2c3 0 5 2 7.333 2q2 0 3.067-.8A1 1 0 0 1 20 4v10a1 1 0 0 1-.4.8A6 6 0 0 1 16 16c-3 0-5-2-7.333-2q-2 0-3.067.8"/><path d="M4 22h16"/></svg> Найденные схемы</h3><div id="findings"></div></div>
</div>
<div class="foot">Qalqan AI · граф строится из данных закупок (заказчик↔поставщик↔учредитель↔адрес↔чиновник)</div>
<script src="/static/graph.js?v=__V__" defer></script></body></html>"""
