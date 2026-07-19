DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Панель регулятора</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0e16;--panel:#111827;--panel2:#0d1424;--cyan:#7aa2f7;--red:#f7768e;--amber:#e0af68;--green:#9ece6a;--tx:#e7ebf3;--mut:#7d8aa0;--bd:#1e293b}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:24px;max-width:1280px;margin:0 auto}
a{color:var(--cyan);text-decoration:none}
.top{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:6px}
h1{font-size:24px;font-weight:800;letter-spacing:-.02em}
.sub{color:var(--mut);font-size:13px;margin-bottom:20px}
.badge{font-size:11px;font-weight:700;padding:4px 10px;border-radius:999px;border:1px solid var(--bd)}
.badge.live{color:var(--green);border-color:#14532d;background:#052e16}
#src:empty{display:none}
.badge.demo{color:var(--amber);border-color:#713f12;background:#1f1505}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:20px}
.kpi{background:var(--panel);border:1px solid var(--bd);border-radius:14px;padding:16px}
.kpi .v{font-size:28px;font-weight:800;font-variant-numeric:tabular-nums}
.kpi .l{color:var(--mut);font-size:12px;margin-top:4px;text-transform:uppercase;letter-spacing:.04em}
.kpi.red .v{color:var(--red)}.kpi.amber .v{color:var(--amber)}.kpi.cyan .v{color:var(--cyan)}
.grid{display:grid;grid-template-columns:2fr 1fr;gap:16px}
.card{background:var(--panel);border:1px solid var(--bd);border-radius:14px;padding:18px;margin-bottom:16px}
.card h3{font-size:14px;font-weight:700;margin-bottom:14px;color:var(--tx)}
.bar-row{display:flex;align-items:center;gap:10px;margin-bottom:9px;font-size:13px}
.bar-row .nm{width:160px;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bar-track{flex:1;height:18px;background:var(--panel2);border-radius:6px;overflow:hidden}
.bar-fill{height:100%;border-radius:6px;background:linear-gradient(90deg,#0891b2,var(--cyan))}
.bar-row .vv{width:46px;text-align:right;font-variant-numeric:tabular-nums;font-weight:700}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:8px 6px;border-bottom:1px solid var(--bd)}
th{color:var(--mut);font-weight:600;font-size:11px;text-transform:uppercase}
td.dom{font-family:ui-monospace,monospace;color:var(--red)}
td.n{text-align:right;font-weight:700;font-variant-numeric:tabular-nums}
.legend{display:flex;gap:16px;font-size:12px;color:var(--mut);margin-top:8px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:middle}
.foot{color:var(--mut);font-size:12px;margin-top:24px;text-align:center}
.kzmap{display:grid;grid-template-columns:repeat(7,1fr);grid-template-rows:repeat(5,46px);gap:6px;margin-top:6px}
.kzt{border-radius:8px;display:flex;flex-direction:column;align-items:center;justify-content:center;border:1px solid var(--bd);overflow:hidden;padding:2px;line-height:1.1}
.kzt b{font-size:13px;font-variant-numeric:tabular-nums}
.kzt .rn{font-size:9px;white-space:nowrap;opacity:.85}
.maplegend{display:flex;align-items:center;gap:8px;font-size:11px;color:var(--mut);margin-top:10px}
.maplegend .grad{height:10px;width:120px;border-radius:5px;background:linear-gradient(90deg,#0d1424,#f7768e)}
@media(max-width:820px){.grid{grid-template-columns:1fr}.kzmap{grid-template-rows:repeat(5,40px)}}
.skel{background:linear-gradient(90deg,rgba(255,255,255,.03) 25%,rgba(255,255,255,.08) 37%,rgba(255,255,255,.03) 63%);background-size:400% 100%;animation:shmr 1.4s ease infinite;border-radius:8px}
@keyframes shmr{0%{background-position:100% 0}100%{background-position:-100% 0}}
@media(prefers-reduced-motion:reduce){.skel{animation:none}}
.qi{width:1em;height:1em;vertical-align:-0.14em;display:inline-block}
:focus-visible{outline:2px solid #7aa2f7;outline-offset:2px;border-radius:4px}
::selection{background:rgba(122,162,247,.32)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
*{scrollbar-width:thin;scrollbar-color:#2a3550 transparent}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-thumb{background:#2a3550;border-radius:5px}::-webkit-scrollbar-track{background:transparent}
</style>
</head>
<body>
<div class="top">
  <div>
    <h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg> Панель регулятора <span id="src" class="badge demo"></span></h1>
    <div class="sub">Qalqan AI · Мониторинг кибер-экономических угроз Республики Казахстан</div>
  </div>
  <div><a href="/">← На главную</a> &nbsp; <a href="/dashboard/data">JSON API</a></div>
</div>

<div class="kpis" id="kpis"><div class="kpi"><div class="skel" style="height:30px;width:62%"></div><div class="skel" style="height:11px;width:85%;margin-top:9px"></div></div><div class="kpi"><div class="skel" style="height:30px;width:62%"></div><div class="skel" style="height:11px;width:85%;margin-top:9px"></div></div><div class="kpi"><div class="skel" style="height:30px;width:62%"></div><div class="skel" style="height:11px;width:85%;margin-top:9px"></div></div><div class="kpi"><div class="skel" style="height:30px;width:62%"></div><div class="skel" style="height:11px;width:85%;margin-top:9px"></div></div><div class="kpi"><div class="skel" style="height:30px;width:62%"></div><div class="skel" style="height:11px;width:85%;margin-top:9px"></div></div><div class="kpi"><div class="skel" style="height:30px;width:62%"></div><div class="skel" style="height:11px;width:85%;margin-top:9px"></div></div></div>

<div class="card">
  <h3><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Қауіп картасы — облыстар бойынша (KZ regional threat map)</h3>
  <div style="position:relative">
    <svg id="kzsvg" viewBox="0 0 1000 550" style="width:100%;height:auto;display:block"></svg>
    <div id="maptip" style="position:absolute;pointer-events:none;display:none;background:#0d1424;border:1px solid var(--bd);border-radius:8px;padding:8px 12px;font-size:12px;z-index:5;box-shadow:0 8px 24px rgba(0,0,0,.5)"></div>
  </div>
  <div class="maplegend"><span>аз қауіп</span><div class="grad"></div><span>көп қауіп</span><span style="margin-left:auto">ОCHA COD-AB 2023 · 20 регионов · Vercel geo</span></div>
</div>

<div class="grid">
  <div>
    <div class="card">
      <h3>Динамика проверок и угроз (30 дней)</h3>
      <svg id="line" viewBox="0 0 640 220" style="width:100%;height:auto"></svg>
      <div class="legend"><span><span class="dot" style="background:#7aa2f7"></span>Всего проверок</span><span><span class="dot" style="background:#f7768e"></span>Угрозы (опасн.+подозр.)</span></div>
    </div>
    <div class="card">
      <h3><svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#f7768e"/></svg> Топ опасных доменов</h3>
      <table><thead><tr><th>Домен</th><th style="text-align:right">Блокировок</th></tr></thead><tbody id="domains"></tbody></table>
    </div>
  </div>
  <div>
    <div class="card">
      <h3>Распределение вердиктов</h3>
      <svg id="donut" viewBox="0 0 200 200" style="width:160px;height:160px;display:block;margin:0 auto"></svg>
      <div id="donut-leg" style="margin-top:10px"></div>
    </div>
    <div class="card">
      <h3>Типы угроз</h3>
      <div id="types"></div>
    </div>
    <div class="card">
      <h3>Эффективность уровней детекции</h3>
      <div id="tiers"></div>
    </div>
  </div>
</div>

<div class="foot">Qalqan AI · Республиканский конкурс ДЭР 2026 · данные агрегируются анонимно (url_hash/ip_hash)</div>

<script src="/kz-regions.js"></script>
<script src="/static/dashboard.js?v=__V__" defer></script>
</body>
</html>"""
