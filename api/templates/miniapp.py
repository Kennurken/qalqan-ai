MINIAPP_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>Qalqan AI</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0e16;--card:#111827;--card2:#0d1424;--cyan:#7aa2f7;--red:#f7768e;--amber:#e0af68;--green:#9ece6a;--tx:#e7ebf3;--mut:#7d8aa0;--bd:#1e293b}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--tx);font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:14px;min-height:100vh}
.hd{display:flex;align-items:center;gap:8px;margin-bottom:14px}
.hd .logo{font-size:22px}.hd h1{font-size:18px;font-weight:800}
.tabs{display:flex;gap:6px;margin-bottom:14px;background:var(--card2);padding:4px;border-radius:12px}
.tab{flex:1;text-align:center;padding:9px;border-radius:9px;font-size:13px;font-weight:700;color:var(--mut);cursor:pointer}
.tab.on{background:var(--cyan);color:#04121a}
.panel{display:none}.panel.on{display:block}
input,textarea{width:100%;background:var(--card2);border:1px solid var(--bd);border-radius:12px;padding:13px;color:var(--tx);font-size:15px;outline:none;font-family:inherit}
textarea{min-height:84px;resize:vertical}
.btn{width:100%;margin-top:10px;background:linear-gradient(90deg,#0891b2,var(--cyan));color:#04121a;border:none;border-radius:12px;padding:14px;font-size:15px;font-weight:800;cursor:pointer}
.btn:active{opacity:.85}
.btn-qr{background:var(--card);color:var(--cyan);border:1.5px solid var(--cyan)}
.hint{color:var(--mut);font-size:12px;margin:8px 2px}
.res{margin-top:14px;border-radius:14px;padding:16px;border:1px solid var(--bd);background:var(--card);display:none}
.res.show{display:block}
.verdict{font-size:20px;font-weight:800;margin-bottom:4px}
.score{color:var(--mut);font-size:13px;margin-bottom:10px}
.bar{height:8px;border-radius:5px;background:var(--card2);overflow:hidden;margin-bottom:12px}
.bar > div{height:100%;border-radius:5px}
.detail{font-size:14px;line-height:1.5}
.meta{margin-top:10px;font-size:12px;color:var(--mut)}
.kzmap{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px}
.kzt{border-radius:9px;padding:8px 4px;text-align:center;border:1px solid var(--bd);font-size:10px}
.kzt b{display:block;font-size:14px;margin-top:2px}
.kpis{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px}
.kpi{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:12px}
.kpi .v{font-size:22px;font-weight:800}.kpi .l{font-size:11px;color:var(--mut);text-transform:uppercase}
.spin{text-align:center;color:var(--mut);padding:14px;font-size:13px}
.qi{width:1em;height:1em;vertical-align:-0.14em;display:inline-block}
:focus-visible{outline:2px solid #7aa2f7;outline-offset:2px;border-radius:4px}
::selection{background:rgba(122,162,247,.32)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
*{scrollbar-width:thin;scrollbar-color:#2a3550 transparent}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-thumb{background:#2a3550;border-radius:5px}::-webkit-scrollbar-track{background:transparent}
</style>
</head>
<body>
<div class="hd"><span class="logo"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg></span><h1>Qalqan AI</h1></div>

<div class="tabs">
  <div class="tab on" data-p="check"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg> Тексеру</div>
  <div class="tab" data-p="ask"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="8" width="16" height="12" rx="2"/><path d="M12 8V4"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg> AI-кеңес</div>
  <div class="tab" data-p="map"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Карта</div>
</div>

<div class="panel on" id="p-check">
  <input id="url" aria-label="URL тексеру" placeholder="kaspi-bonus.kz немесе https://..." autocapitalize="off" autocomplete="off">
  <button class="btn" id="btn-check">Тексеру</button>
  <button class="btn btn-qr" id="btn-qr" style="display:none"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg> QR-код сканерлеу</button>
  <div class="hint">Сілтемені қой немесе QR-кодты сканерле — фишинг, клон, гемблингті тексеремін. Жалған Kaspi QR — жиі алаяқтық!</div>
  <div class="res" id="res-check"></div>
</div>

<div class="panel" id="p-ask">
  <textarea id="situation" placeholder="Жағдайды сипаттаңыз: «Каспиден қоңырау шалып, SMS-кодты сұрап жатыр...»"></textarea>
  <button class="btn" id="btn-ask">AI-кеңес сұрау</button>
  <div class="hint">Не болғанын сөзбен жаз — AI алаяқтық па екенін айтады</div>
  <div class="res" id="res-ask"></div>
</div>

<div class="panel" id="p-map">
  <div class="kpis" id="kpis"></div>
  <div style="font-size:13px;font-weight:700;margin-bottom:6px">Облыстар бойынша қауіп</div>
  <svg id="kzsvg" viewBox="0 0 1000 550" style="width:100%;height:auto;display:block;background:var(--card2);border-radius:12px"></svg>
  <div class="kzmap" id="kzmap" style="margin-top:8px"></div>
</div>

<div style="display:flex;gap:8px;margin-top:14px">
  <a href="/leak" style="flex:1;text-align:center;background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:12px;color:var(--tx);text-decoration:none;font-size:13px;font-weight:700"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> Пароль утёк?</a>
  <a href="/screen" style="flex:1;text-align:center;background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:12px;color:var(--tx);text-decoration:none;font-size:13px;font-weight:700"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg> Скриншот</a>
  <a href="/help" style="flex:1;text-align:center;background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:12px;color:var(--tx);text-decoration:none;font-size:13px;font-weight:700"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m4.93 19.07 4.24-4.24"/></svg> Помощь</a>
</div>

<script src="/static/miniapp.js?v=__V__" defer></script>
</body></html>"""
