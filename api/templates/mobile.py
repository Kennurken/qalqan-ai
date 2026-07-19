MOBILE_HTML = """<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,viewport-fit=cover">
<title>Qalqan AI</title>
<meta name="theme-color" content="#0a0e16">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0e16;--panel:#111827;--bd:#1e293b;--tx:#e7ebf3;--mut:#8194ad;--cyan:#7aa2f7;--red:#f7768e;--amber:#e0af68;--green:#9ece6a}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--tx);font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding-bottom:calc(72px + env(safe-area-inset-bottom))}
header{position:sticky;top:0;z-index:10;background:rgba(10,14,26,.95);backdrop-filter:blur(10px);border-bottom:1px solid var(--bd);padding:calc(12px + env(safe-area-inset-top)) 16px 12px;display:flex;align-items:center;justify-content:space-between}
.logo{font-weight:800;font-size:18px;color:var(--cyan);display:flex;align-items:center;gap:7px}
.net{font-size:11px;color:var(--green);display:flex;align-items:center;gap:5px}
.net .d{width:8px;height:8px;border-radius:50%;background:var(--green)}
.net.off{color:var(--amber)} .net.off .d{background:var(--amber)}
#install{display:none;background:var(--cyan);color:#06121a;border:none;border-radius:8px;padding:7px 12px;font-weight:700;font-size:12px}
main{padding:16px}
.panel{display:none} .panel.on{display:block;animation:f .2s ease}
@keyframes f{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
h2{font-size:16px;margin-bottom:12px}
.sub{color:var(--mut);font-size:13px;margin-bottom:16px;line-height:1.5}
input,textarea{width:100%;background:var(--panel);border:1px solid var(--bd);border-radius:12px;padding:14px;color:var(--tx);font-size:16px;outline:none}
textarea{min-height:120px;resize:vertical;font-family:inherit}
button.go{width:100%;margin-top:12px;background:var(--cyan);color:#06121a;border:none;border-radius:12px;padding:15px;font-weight:800;font-size:15px}
button.go:disabled{opacity:.5}
.res{margin-top:16px;border-radius:14px;padding:16px;border:1px solid var(--bd);display:none}
.res.show{display:block}
.res.DANGEROUS{border-color:#7f1d2e;background:#1a0a0f}.res.SUSPICIOUS{border-color:#7c5210;background:#1a1305}.res.SAFE{border-color:#14532d;background:#05140b}
.verdict{font-size:20px;font-weight:800;display:flex;align-items:center;gap:8px}
.DANGEROUS .verdict{color:var(--red)}.SUSPICIOUS .verdict{color:var(--amber)}.SAFE .verdict{color:var(--green)}
.score{font-size:13px;color:var(--mut);margin:4px 0 10px}
.detail{font-size:14px;line-height:1.55}
.flags{margin-top:10px} .flag{font-size:13px;padding:6px 0;border-top:1px solid var(--bd);color:var(--mut)}
.region{display:flex;align-items:center;gap:10px;margin-bottom:9px;font-size:13px}
.region .nm{width:96px;color:var(--mut)} .region .tk{flex:1;height:18px;background:var(--panel);border-radius:6px;overflow:hidden}
.region .fl{height:100%;background:linear-gradient(90deg,#7c2d12,var(--red))} .region .vv{width:42px;text-align:right;font-weight:700}
.hist{font-size:13px;padding:11px;background:var(--panel);border:1px solid var(--bd);border-radius:10px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;gap:8px}
.hist .u{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-family:ui-monospace,monospace}
.dot2{width:9px;height:9px;border-radius:50%;flex:0 0 auto}
.muted{color:var(--mut);font-size:13px;text-align:center;padding:24px}
nav{position:fixed;bottom:0;left:0;right:0;background:rgba(10,14,26,.97);backdrop-filter:blur(10px);border-top:1px solid var(--bd);display:flex;padding-bottom:env(safe-area-inset-bottom)}
nav button{flex:1;background:none;border:none;color:var(--mut);padding:11px 0;font-size:11px;display:flex;flex-direction:column;align-items:center;gap:3px}
nav button.on{color:var(--cyan)} nav button svg{width:22px;height:22px;stroke:currentColor;fill:none;stroke-width:2}
.spin{display:inline-block;width:16px;height:16px;border:2px solid #06121a;border-top-color:transparent;border-radius:50%;animation:s .7s linear infinite;vertical-align:-3px}
@keyframes s{to{transform:rotate(360deg)}}
.qi{width:1em;height:1em;vertical-align:-0.14em;display:inline-block}
:focus-visible{outline:2px solid #7aa2f7;outline-offset:2px;border-radius:4px}
::selection{background:rgba(122,162,247,.32)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
*{scrollbar-width:thin;scrollbar-color:#2a3550 transparent}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-thumb{background:#2a3550;border-radius:5px}::-webkit-scrollbar-track{background:transparent}
</style></head>
<body>
<header>
  <div class="logo"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg> Qalqan AI</div>
  <div style="display:flex;gap:10px;align-items:center">
    <button id="install">Орнату</button>
    <span class="net" id="net"><span class="d"></span><span id="nett">онлайн</span></span>
  </div>
</header>
<main>
  <section class="panel on" id="p-check">
    <h2>Сілтеме / нөмір тексеру</h2>
    <div class="sub">URL, домен немесе телефон нөмірін енгізіңіз — фишинг, скам, гемблинг, алаяқ нөмір.</div>
    <input id="url" placeholder="kaspi-bonus.kz немесе +7 700 123 45 67" autocapitalize="off" autocomplete="off">
    <button class="go" id="btn-check">Тексеру</button>
    <div class="res" id="r-check"></div>
  </section>

  <section class="panel" id="p-ai">
    <h2>AI кеңесші</h2>
    <div class="sub">Жағдайды сипаттаңыз (қоңырау, SMS, ұсыныс) — алаяқтық па екенін айтамыз.</div>
    <textarea id="sit" placeholder="Мысалы: банктен қоңырау шалып, SMS кодын сұрап жатыр..."></textarea>
    <button class="go" id="btn-ai">Талдау</button>
    <div class="res" id="r-ai"></div>
  </section>

  <section class="panel" id="p-map">
    <h2>Қауіп картасы</h2>
    <div class="sub">Облыстар бойынша скам белсенділігі.</div>
    <div id="regions"><div class="muted">Жүктелуде…</div></div>
  </section>

  <section class="panel" id="p-hist">
    <h2>Тарих</h2>
    <div id="hist"><div class="muted">Тексерулер әзірге жоқ</div></div>
  </section>
</main>

<nav>
  <button class="on" data-t="check"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>Тексеру</button>
  <button data-t="ai"><svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-4 12.7V17a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-2.3A7 7 0 0 0 12 2z"/><path d="M9 22h6"/></svg>AI</button>
  <button data-t="map"><svg viewBox="0 0 24 24"><path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z"/><path d="M9 4v14M15 6v14"/></svg>Карта</button>
  <button data-t="hist"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>Тарих</button>
</nav>

<script src="/static/mobile.js?v=__V__" defer></script>
</body></html>"""
