BATCH_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Массовая проверка URL</title>
<meta name="description" content="Проверка списка URL на фишинг и мошенничество. Для банков, регуляторов и СБ компаний.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0e16;--card:#111827;--card2:#0d1424;--cyan:#7aa2f7;--red:#f7768e;--amber:#e0af68;--green:#9ece6a;--tx:#e7ebf3;--mut:#7d8aa0;--bd:#1e293b}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font-family:'Inter',-apple-system,sans-serif;min-height:100vh;padding:20px}
.wrap{max-width:860px;margin:0 auto}
.top{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
.top a{color:var(--mut);text-decoration:none;font-size:14px}.top a:hover{color:var(--cyan)}
h1{font-size:24px;font-weight:800}
.sub{color:var(--mut);font-size:13.5px;margin:8px 0 18px;line-height:1.6}
.card{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:20px;margin-bottom:16px}
textarea{width:100%;height:140px;background:var(--card2);border:1px solid var(--bd);border-radius:10px;color:var(--tx);font-family:ui-monospace,monospace;font-size:12.5px;padding:12px;resize:vertical}
.row{display:flex;gap:10px;margin-top:12px;flex-wrap:wrap}
.btn{flex:1;min-width:180px;background:var(--cyan);border:none;border-radius:10px;color:#04121a;font-weight:800;font-size:14px;padding:12px;cursor:pointer;font-family:inherit}
.btn.sec{background:transparent;border:1px solid var(--bd);color:var(--tx)}
.btn:disabled{opacity:.5;cursor:default}
#file{display:none}
.prog{height:8px;background:var(--card2);border-radius:99px;overflow:hidden;margin-top:14px;display:none}
.prog i{display:block;height:100%;background:linear-gradient(90deg,var(--cyan),var(--green));width:0%;transition:width .3s}
.sum{display:none;gap:10px;margin-top:14px;flex-wrap:wrap}
.pill{padding:7px 13px;border-radius:99px;font-size:12.5px;font-weight:700;border:1px solid var(--bd)}
.pill.d{color:var(--red);border-color:rgba(247,118,142,.4)}
.pill.s{color:var(--amber);border-color:rgba(224,175,104,.4)}
.pill.ok{color:var(--green);border-color:rgba(158,206,106,.4)}
.tblwrap{overflow-x:auto;margin-top:14px;display:none}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{color:var(--mut);text-align:left;font-weight:600;padding:8px;border-bottom:1px solid var(--bd)}
td{padding:8px;border-bottom:1px solid rgba(30,41,59,.5);word-break:break-all}
.v-DANGEROUS{color:var(--red);font-weight:700}
.v-SUSPICIOUS{color:var(--amber);font-weight:700}
.v-SAFE{color:var(--green);font-weight:700}
.hint{font-size:12px;color:var(--mut);margin-top:10px;line-height:1.6}
.foot{text-align:center;color:var(--mut);font-size:12px;margin-top:22px}.foot a{color:var(--cyan);text-decoration:none}
.qi{width:1em;height:1em;vertical-align:-0.14em;display:inline-block}
:focus-visible{outline:2px solid #7aa2f7;outline-offset:2px;border-radius:4px}
::selection{background:rgba(122,162,247,.32)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
*{scrollbar-width:thin;scrollbar-color:#2a3550 transparent}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-thumb{background:#2a3550;border-radius:5px}::-webkit-scrollbar-track{background:transparent}
</style>
</head>
<body>
<div class="wrap">
  <div class="top"><h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/></svg> Массовая проверка URL</h1><a href="/">← Qalqan AI</a></div>
  <div class="sub">Для банков, регуляторов и служб безопасности: вставьте список ссылок (по одной на строку) или загрузите CSV — каждый URL пройдёт полный 7-уровневый pipeline. До 15 URL параллельно, крупные списки идут батчами.</div>

  <div class="card">
    <textarea id="urls" placeholder="kaspi-bonus.tk&#10;1xbet.com&#10;https://example.com/login&#10;..."></textarea>
    <div class="row">
      <button class="btn sec" id="upload"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg> Загрузить CSV/TXT</button>
      <button class="btn" id="go">Проверить список</button>
      <input id="file" type="file" accept=".csv,.txt">
    </div>
    <div class="prog" id="prog"><i id="progbar"></i></div>
    <div class="sum" id="sum"></div>
    <div class="tblwrap" id="tblwrap">
      <table><thead><tr><th>URL</th><th>Вердикт</th><th>Балл</th><th>Источник</th></tr></thead><tbody id="tbody"></tbody></table>
    </div>
    <div class="row" id="dlrow" style="display:none"><button class="btn sec" id="dl"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/></svg> Скачать отчёт CSV</button></div>
    <div class="hint">Лимит: 15 URL за запрос, крупные списки проверяются частями с паузой (rate-limit). Для интеграции без лимитов — <a href="/partners" style="color:var(--cyan)">B2G API с X-API-Key</a>.</div>
  </div>

  <div class="foot">Qalqan AI · Bulk URL screening · <a href="/partners">Партнёрам</a> · <a href="/">Главная</a></div>
</div>

<script src="/static/batch.js?v=__V__" defer></script>
</body>
</html>"""
