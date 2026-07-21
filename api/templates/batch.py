BATCH_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<script>document.documentElement.dataset.theme=localStorage.getItem("qtheme")||"dark";</script>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Массовая проверка URL</title>
<meta name="description" content="Проверка списка URL на фишинг и мошенничество. Для банков, регуляторов и СБ компаний.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:oklch(16% .02 255);--card:oklch(21.5% .025 260);--card2:oklch(19% .028 258);--cyan:oklch(72% .12 265);--red:oklch(70% .15 15);--amber:oklch(78% .11 78);--green:oklch(80% .13 130);--tx:oklch(93% .01 250);--mut:oklch(63% .02 250);--bd:oklch(30% .03 258);--panel:var(--card);--s1:4px;--s2:8px;--s3:12px;--s4:16px;--s5:24px;--s6:36px}
[data-theme="light"]{--bg:oklch(96.5% .006 250);--card:oklch(99.2% .003 250);--card2:oklch(94.5% .008 250);--cyan:oklch(50% .15 262);--red:oklch(54% .17 18);--amber:oklch(58% .12 78);--green:oklch(52% .12 140);--tx:oklch(26% .02 255);--mut:oklch(48% .02 250);--bd:oklch(87% .012 250)}
[data-theme="light"] body{background:var(--bg)}
.qtgl{background:var(--card2);border:1px solid var(--bd);border-radius:9px;color:var(--mut);cursor:pointer;padding:7px 9px;line-height:0;transition:color .2s,border-color .2s}
.qtgl:hover{color:var(--tx);border-color:var(--cyan)}
.qtgl .sun{display:none}.qtgl .moon{display:block}
[data-theme="light"] .qtgl .sun{display:block}[data-theme="light"] .qtgl .moon{display:none}
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
  <div class="top"><h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/></svg> <span data-qtl="h1">Массовая проверка URL</span></h1><button class="qtgl" id="qtgl" aria-label="Тема / Theme"><svg class="moon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg><svg class="sun" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg></button> <a href="/">← Qalqan AI</a></div>
  <div class="sub" data-qtl="sub">Для банков, регуляторов и служб безопасности: вставьте список ссылок (по одной на строку) или загрузите CSV — каждый URL пройдёт полный 7-уровневый pipeline.</div>

  <div class="card">
    <textarea id="urls" placeholder="kaspi-bonus.tk&#10;1xbet.com&#10;https://example.com/login&#10;..."></textarea>
    <div class="row">
      <button class="btn sec" id="upload" data-qtl="upload"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg> Загрузить CSV/TXT</button>
      <button class="btn" id="go" data-qtl="go">Проверить список</button>
      <input id="file" type="file" accept=".csv,.txt">
    </div>
    <div class="prog" id="prog"><i id="progbar"></i></div>
    <div class="sum" id="sum" role="status" aria-live="polite"></div>
    <div class="tblwrap" id="tblwrap">
      <table><thead><tr><th>URL</th><th data-qtl="th_v">Вердикт</th><th data-qtl="th_s">Балл</th><th data-qtl="th_src">Источник</th></tr></thead><tbody id="tbody"></tbody></table>
    </div>
    <div class="row" id="dlrow" style="display:none"><button class="btn sec" id="dl" data-qtl="dl"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/></svg> Скачать отчёт CSV</button></div>
    <div class="hint">Лимит: 15 URL за запрос, крупные списки проверяются частями с паузой (rate-limit). Для интеграции без лимитов — <a href="/partners" style="color:var(--cyan)">B2G API с X-API-Key</a>.</div>
  </div>

  <div class="foot">Qalqan AI · Bulk URL screening · <a href="/partners">Партнёрам</a> · <a href="/">Главная</a></div>
</div>

<script src="/static/qtl.js?v=__V__" defer></script>
<script src="/static/batch.js?v=__V__" defer></script>
<script>document.getElementById("qtgl").onclick=function(){var d=document.documentElement,t=d.dataset.theme==="dark"?"light":"dark";d.dataset.theme=t;localStorage.setItem("qtheme",t)};</script>
</body>
</html>"""
