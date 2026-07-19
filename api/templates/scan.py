SCAN_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<script>document.documentElement.dataset.theme=localStorage.getItem("qtheme")||"dark";</script>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Оценка безопасности сайта</title>
<meta name="description" content="Оценка безопасности любого сайта от A+ до F: HTTPS/SSL, возраст домена, репутация, гомоглифы, инфраструктура. Бесплатно.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:oklch(16% .02 255);--card:oklch(21.5% .025 260);--card2:oklch(19% .028 258);--cyan:oklch(72% .12 265);--red:oklch(70% .15 15);--amber:oklch(78% .11 78);--green:oklch(80% .13 130);--tx:oklch(93% .01 250);--mut:oklch(63% .02 250);--bd:oklch(30% .03 258);--panel:var(--card);--s1:4px;--s2:8px;--s3:12px;--s4:16px;--s5:24px;--s6:36px}
[data-theme="light"]{--bg:oklch(96.5% .006 250);--card:oklch(99.2% .003 250);--card2:oklch(94.5% .008 250);--cyan:oklch(50% .15 262);--red:oklch(54% .17 18);--amber:oklch(58% .12 78);--green:oklch(52% .12 140);--tx:oklch(26% .02 255);--mut:oklch(48% .02 250);--bd:oklch(87% .012 250)}
[data-theme="light"] body{background:var(--bg)}
.qtgl{background:var(--card2);border:1px solid var(--bd);border-radius:9px;color:var(--mut);cursor:pointer;padding:7px 9px;line-height:0;transition:color .2s,border-color .2s}
.qtgl:hover{color:var(--tx);border-color:var(--cyan)}
.qtgl .sun{display:none}.qtgl .moon{display:block}
[data-theme="light"] .qtgl .sun{display:block}[data-theme="light"] .qtgl .moon{display:none}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--tx);font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;min-height:100vh;padding:20px}
.wrap{max-width:620px;margin:0 auto}
.top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.top a{color:var(--mut);text-decoration:none;font-size:14px}.top a:hover{color:var(--cyan)}
h1{font-size:23px;font-weight:800}
.sub{color:var(--mut);font-size:13.5px;margin:8px 0 20px;line-height:1.6}
.inrow{display:flex;gap:8px}
input{flex:1;background:var(--card2);border:1px solid var(--bd);border-radius:12px;padding:14px;color:var(--tx);font-size:16px;outline:none;font-family:inherit}
input:focus{border-color:var(--cyan)}
.btn{background:linear-gradient(90deg,#0891b2,var(--cyan));color:#04121a;border:none;border-radius:12px;padding:0 22px;font-size:15px;font-weight:800;cursor:pointer;font-family:inherit}
.btn:disabled{opacity:.6;cursor:wait}
.ex{color:var(--mut);font-size:12px;margin-top:8px}.ex b{color:var(--cyan);cursor:pointer}
.card{display:none;margin-top:20px;background:var(--card);border:1px solid var(--bd);border-radius:18px;overflow:hidden}
.card.show{display:block}
.hd{display:flex;align-items:center;gap:18px;padding:22px;border-bottom:1px solid var(--bd)}
.badge{width:92px;height:92px;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:46px;font-weight:800;color:#04121a;flex-shrink:0}
.hd .dm{font-family:'SF Mono',ui-monospace,monospace;font-size:16px;font-weight:700;word-break:break-all}
.hd .vv{font-size:13px;color:var(--mut);margin-top:4px}
.hd .pc{font-size:13px;margin-top:6px}
.factors{padding:12px 18px 18px}
.f{display:flex;gap:11px;align-items:flex-start;padding:9px 0;border-bottom:1px solid rgba(30,41,59,.5);font-size:13.5px;line-height:1.5}
.f:last-child{border-bottom:none}
.f .i{flex-shrink:0;font-size:15px;margin-top:1px}
.f.pass .i{color:var(--green)}.f.warn .i{color:var(--amber)}.f.fail .i{color:var(--red)}
.spin{color:var(--mut);font-size:13px;margin-top:16px}
.foot{text-align:center;color:var(--mut);font-size:12px;margin-top:22px}.foot a{color:var(--cyan);text-decoration:none}
.disc{color:var(--mut);font-size:11px;text-align:center;padding:0 18px 16px}
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
  <div class="top"><h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 1 0 0-14h-1"/><path d="M9 14h2"/><path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z"/><path d="M12 6V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3"/></svg> Оценка безопасности сайта</h1><button class="qtgl" id="qtgl" aria-label="Тема / Theme"><svg class="moon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg><svg class="sun" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg></button> <a href="/">← Qalqan AI</a></div>
  <div class="sub">Сайттың қауіпсіздік бағасы: A+ ден F дейін. · Комплексная оценка любого сайта: HTTPS/SSL, возраст домена, репутация, гомоглифы, хостинг.</div>

  <div class="inrow">
    <input id="dom" aria-label="Домен сайта" placeholder="example.kz" autocapitalize="off" autocomplete="off" spellcheck="false">
    <button class="btn" id="go">Оценить</button>
  </div>
  <div class="ex">Примеры: <b data-d="kaspi.kz">kaspi.kz</b> · <b data-d="1xbet.com">1xbet.com</b> · <b data-d="github.com">github.com</b></div>

  <div id="status"></div>
  <div class="card" id="card">
    <div class="hd">
      <div class="badge" id="badge">—</div>
      <div>
        <div class="dm" id="dm"></div>
        <div class="vv" id="vv"></div>
        <div class="pc" id="pc"></div>
      </div>
    </div>
    <div class="factors" id="factors"></div>
    <div class="disc">Оценка основана на публичных сигналах (TLS, WHOIS/RDAP, репутация). Не является аудитом.</div>
  </div>
</div>

<script src="/static/scan.js?v=__V__" defer></script>
<div class="foot">Qalqan AI · Website security grade · <a href="/brand">Защита бренда</a> · <a href="/">Главная</a></div>
<script>document.getElementById("qtgl").onclick=function(){var d=document.documentElement,t=d.dataset.theme==="dark"?"light":"dark";d.dataset.theme=t;localStorage.setItem("qtheme",t)};</script>
</body>
</html>"""
