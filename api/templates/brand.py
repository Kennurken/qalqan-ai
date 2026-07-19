BRAND_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<script>document.documentElement.dataset.theme=localStorage.getItem("qtheme")||"dark";</script>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Защита бренда от фишинга</title>
<meta name="description" content="Radar фишинговых доменов-двойников вашего бренда: гомоглифы, бесплатные TLD, приманки. Для банков, госорганов, бизнеса Казахстана.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:oklch(16% .02 255);--card:oklch(21.5% .025 260);--card2:oklch(19% .028 258);--cyan:oklch(72% .12 265);--red:oklch(70% .15 15);--amber:oklch(78% .11 78);--green:oklch(80% .13 130);--tx:oklch(93% .01 250);--mut:oklch(63% .02 250);--bd:oklch(30% .03 258);--panel:var(--card);--s1:4px;--s2:8px;--s3:12px;--s4:16px;--s5:24px;--s6:36px}
[data-theme="light"]{--bg:oklch(96.5% .006 250);--card:oklch(99.2% .003 250);--card2:oklch(94.5% .008 250);--cyan:oklch(50% .15 262);--red:oklch(54% .17 18);--amber:oklch(58% .12 78);--green:oklch(52% .12 140);--tx:oklch(26% .02 255);--mut:oklch(48% .02 250);--bd:oklch(87% .012 250)}
[data-theme="light"] body{background:var(--bg)}
.skl{position:relative;overflow:hidden;background:var(--card2);border-radius:8px;min-height:14px}
.skl::after{content:"";position:absolute;inset:0;transform:translateX(-100%);background:linear-gradient(90deg,transparent,oklch(100% 0 0/.07),transparent);animation:sklsh 1.1s infinite}
@keyframes sklsh{to{transform:translateX(100%)}}
.qtgl{background:var(--card2);border:1px solid var(--bd);border-radius:9px;color:var(--mut);cursor:pointer;padding:7px 9px;line-height:0;transition:color .2s,border-color .2s}
.qtgl:hover{color:var(--tx);border-color:var(--cyan)}
.qtgl .sun{display:none}.qtgl .moon{display:block}
[data-theme="light"] .qtgl .sun{display:block}[data-theme="light"] .qtgl .moon{display:none}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--tx);font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;min-height:100vh;padding:20px}
.wrap{max-width:760px;margin:0 auto}
.top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.top a{color:var(--mut);text-decoration:none;font-size:14px}.top a:hover{color:var(--cyan)}
h1{font-size:23px;font-weight:800;line-height:1.2}
.sub{color:var(--mut);font-size:13.5px;margin:8px 0 20px;line-height:1.6}
.b2b{display:inline-block;font-size:11px;font-weight:700;color:var(--cyan);border:1px solid var(--cyan);border-radius:6px;padding:2px 8px;margin-bottom:12px}
.inrow{display:flex;gap:8px}
.inrow input{min-width:0}
@media(max-width:430px){.inrow{flex-direction:column}.inrow .btn{width:100%}}
input{flex:1;background:var(--card2);border:1px solid var(--bd);border-radius:12px;padding:14px;color:var(--tx);font-size:16px;outline:none;font-family:inherit}
input:focus{border-color:var(--cyan)}
.btn{background:linear-gradient(90deg,#0891b2,var(--cyan));color:#04121a;border:none;border-radius:12px;padding:0 22px;font-size:15px;font-weight:800;cursor:pointer;font-family:inherit;white-space:nowrap}
.btn:disabled{opacity:.6;cursor:wait}
.ex{color:var(--mut);font-size:12px;margin-top:8px}
.ex b{color:var(--cyan);cursor:pointer}
.summary{display:none;gap:8px;margin:18px 0 6px;flex-wrap:wrap}
.summary.show{display:flex}
.pill{border-radius:10px;padding:9px 14px;font-size:13px;font-weight:700;border:1px solid}
.pill.c{background:rgba(247,118,142,.12);color:var(--red);border-color:rgba(247,118,142,.4)}
.pill.h{background:rgba(224,175,104,.12);color:var(--amber);border-color:rgba(224,175,104,.4)}
.pill.m{background:rgba(122,162,247,.1);color:var(--cyan);border-color:rgba(122,162,247,.35)}
.grid{display:none;grid-template-columns:1fr;gap:7px;margin-top:10px}
.grid.show{display:grid}
@media(min-width:560px){.grid.show{grid-template-columns:1fr 1fr}}
.row{display:flex;align-items:center;gap:10px;background:var(--card);border:1px solid var(--bd);border-radius:11px;padding:11px 13px}
.row .dot{width:9px;height:9px;border-radius:50%;flex-shrink:0}
.dot.critical{background:var(--red);box-shadow:0 0 8px var(--red)}.dot.high{background:var(--amber)}.dot.medium{background:var(--cyan)}
.row .dm{font-family:'SF Mono',ui-monospace,monospace;font-size:13.5px;font-weight:600;word-break:break-all}
.row .nt{font-size:11.5px;color:var(--mut);margin-top:1px}
.advice{display:none;background:rgba(158,206,106,.07);border:1px solid rgba(158,206,106,.25);border-radius:12px;padding:14px;margin-top:16px;font-size:13px;line-height:1.6;color:var(--tx)}
.advice.show{display:block}
.advice b{color:var(--green)}
.disc{color:var(--mut);font-size:11.5px;margin-top:10px;line-height:1.5}
.spin{color:var(--mut);font-size:13px;margin-top:14px}
.foot{text-align:center;color:var(--mut);font-size:12px;margin-top:24px}.foot a{color:var(--cyan);text-decoration:none}
.liveok{background:rgba(158,206,106,.1);border:1px solid rgba(158,206,106,.3);border-radius:10px;padding:12px;font-size:13.5px;color:var(--green,#9ece6a)}
.livebad{color:var(--red,#f7768e);font-weight:700;font-size:14px;margin-bottom:8px}
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
  <div class="top"><h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> Защита бренда от фишинга</h1><button class="qtgl" id="qtgl" aria-label="Тема / Theme"><svg class="moon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg><svg class="sun" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg></button> <a href="/">← Qalqan AI</a></div>
  <div class="b2b">ДЛЯ БАНКОВ · ГОСОРГАНОВ · БИЗНЕСА</div>
  <div class="sub">Брендіңіздің фишингтік домен-егіздерін табыңыз. · Введите домен вашего бренда — покажем домены-двойники, которые регистрируют мошенники, чтобы красть у ваших клиентов.</div>

  <div class="inrow">
    <input id="dom" aria-label="Домен бренда" placeholder="kaspi.kz" autocapitalize="off" autocomplete="off" spellcheck="false">
    <button class="btn" id="go">Сканировать</button>
  </div>
  <div class="ex">Примеры: <b data-d="kaspi.kz">kaspi.kz</b> · <b data-d="halykbank.kz">halykbank.kz</b> · <b data-d="egov.kz">egov.kz</b></div>

  <div class="summary" id="summary"></div>
  <div class="grid" id="grid"></div>
  <div id="status"></div>
  <div class="advice" id="advice"></div>
  <div id="liveblock" style="display:none;margin-top:14px">
    <div style="display:flex;gap:10px;flex-wrap:wrap">
      <button class="btn" id="livego" style="flex:1 1 100%;min-width:0"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg> Live-проверка регистраций</button>
      <button class="btn" id="watchgo" style="flex:1 1 100%;min-width:0;background:transparent;border:1px solid var(--bd);color:var(--tx)"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/></svg> На ежедневный мониторинг</button>
    </div>
    <div id="liveres" style="margin-top:12px"></div>
  </div>
</div>

<script src="/static/brand.js?v=__V__" defer></script>
<div class="foot">Qalqan AI · Domain typosquatting radar · <a href="/partners">B2G API</a> · <a href="/">Проверить сайт</a></div>
<script>document.getElementById("qtgl").onclick=function(){var d=document.documentElement,t=d.dataset.theme==="dark"?"light":"dark";d.dataset.theme=t;localStorage.setItem("qtheme",t)};</script>
</body>
</html>"""
