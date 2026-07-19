NOTFOUND_HTML = """<!DOCTYPE html>
<html lang="kk"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>404 — Qalqan AI</title>
<meta name="theme-color" content="#0a0e16">
<link rel="icon" type="image/svg+xml" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
*{margin:0;box-sizing:border-box}
body{min-height:100vh;display:grid;place-items:center;background:#0a0e16;color:#e7ebf3;font-family:'Inter',-apple-system,sans-serif;text-align:center;padding:24px;overflow:hidden}
.bg{position:fixed;inset:0;z-index:-1;background:radial-gradient(900px 600px at 50% 20%,#101725,#0a0e16 65%)}
.bg::before,.bg::after{content:"";position:absolute;border-radius:50%;filter:blur(90px)}
.bg::before{width:420px;height:420px;background:radial-gradient(circle,rgba(122,162,247,.4),transparent 70%);top:-80px;left:20%;animation:f 22s ease-in-out infinite alternate}
.bg::after{width:380px;height:380px;background:radial-gradient(circle,rgba(110,231,211,.28),transparent 70%);bottom:-60px;right:18%;animation:f 26s ease-in-out infinite alternate-reverse}
@keyframes f{to{transform:translate(60px,40px)}}
.shield{width:60px;height:60px;margin:0 auto 8px}
.code{font-size:clamp(80px,18vw,150px);font-weight:800;line-height:1;letter-spacing:-.04em;background:linear-gradient(120deg,#7aa2f7,#6ee7d3,#bb9af7,#6ee7d3);background-size:220% auto;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:sh 7s linear infinite}
@keyframes sh{to{background-position:220% center}}
h1{font-size:22px;font-weight:600;margin:6px 0 10px}
p{color:#aab3c6;max-width:380px;margin:0 auto 28px;line-height:1.6}
.btn{display:inline-flex;align-items:center;gap:8px;background:linear-gradient(135deg,#7aa2f7,#5b87e8);color:#06101f;font-weight:700;padding:13px 26px;border-radius:13px;text-decoration:none;transition:transform .25s cubic-bezier(.16,1,.3,1),box-shadow .25s}
.btn:hover{transform:translateY(-2px);box-shadow:0 14px 36px rgba(122,162,247,.35)}
.links{margin-top:22px;font-size:14px;color:#6f7a8f}.links a{color:#7aa2f7;text-decoration:none;margin:0 9px}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
.qi{width:1em;height:1em;vertical-align:-0.14em;display:inline-block}
:focus-visible{outline:2px solid #7aa2f7;outline-offset:2px;border-radius:4px}
::selection{background:rgba(122,162,247,.32)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
*{scrollbar-width:thin;scrollbar-color:#2a3550 transparent}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-thumb{background:#2a3550;border-radius:5px}::-webkit-scrollbar-track{background:transparent}
</style></head>
<body>
<div class="bg"></div>
<div>
<svg class="shield" viewBox="0 0 24 24" fill="none"><path d="M12 2 4 5v6c0 5 3.4 8.6 8 10 4.6-1.4 8-5 8-10V5z" stroke="url(#g)" stroke-width="1.4" fill="rgba(122,162,247,.1)"/><defs><linearGradient id="g" x1="4" y1="2" x2="20" y2="22"><stop stop-color="#7aa2f7"/><stop offset="1" stop-color="#6ee7d3"/></linearGradient></defs></svg>
<div class="code">404</div>
<h1>Бет табылмады</h1>
<p>Бұл сілтеме жоқ немесе жылжытылған. Бастапқы бетке оралыңыз.</p>
<a class="btn" href="/">← Басты бетке</a>
<div class="links"><a href="/dashboard?demo=1">Панель</a>·<a href="/m">Мобилка</a>·<a href="/leak"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> Пароль</a>·<a href="https://t.me/QalqanAI_bot">Бот</a></div>
</div>
</body></html>"""
