"""HTML page templates for Qalqan AI.
Extracted from index.py to slim the app module (static pages, no per-request data)."""

LANDING_HTML = """<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Qalqan AI — Қазақстандық киберқауіпсіздік</title>
<meta name="description" content="Qalqan AI — бесплатная AI-защита казахстанцев от фишинга, телефонного мошенничества, пирамид, гемблинга и фрода в госзакупках. Расширение, мобилка, Telegram-бот, дашборд регулятора.">
<meta name="keywords" content="киберқауіпсіздік, фишинг, алаяқтық, қаржылық пирамида, госзакупки фрод, Kaspi фейк, Қазақстан, cybersecurity Kazakhstan, scam detection">
<meta name="author" content="Qalqan AI">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://qalqan-ai-nu.vercel.app/">
<meta property="og:title" content="Qalqan AI — Казахстанский ИИ-щит от мошенников">
<meta property="og:description" content="Бесплатно: блокирует фишинг, пирамиды, гемблинг, телефонный скам и госзакуп-фрод. Расширение + мобилка + Telegram-бот + дашборд регулятора. 6-уровневый AI.">
<meta property="og:url" content="https://qalqan-ai-nu.vercel.app">
<meta property="og:type" content="website">
<meta property="og:image" content="https://raw.githubusercontent.com/Kennurken/qalqan-ai/master/extension/public/icons/icon128.png">
<meta property="og:locale" content="kk_KZ">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Qalqan AI — AI Cybersecurity for Kazakhstan">
<meta name="twitter:description" content="Blocks phishing, scams, gambling, phone fraud & procurement fraud. Extension + mobile + bot + regulator dashboard. 6-tier AI. kk/ru/en.">
<meta name="twitter:image" content="https://raw.githubusercontent.com/Kennurken/qalqan-ai/master/extension/public/icons/icon128.png">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/svg+xml" href="/favicon.ico">
<meta name="theme-color" content="#0a0e16">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Qalqan AI","applicationCategory":"SecurityApplication","operatingSystem":"Web, Chrome, Firefox, Android, iOS","offers":{"@type":"Offer","price":"0","priceCurrency":"KZT"},"inLanguage":["kk","ru","en"],"url":"https://qalqan-ai-nu.vercel.app","description":"AI cybersecurity for Kazakhstan: phishing, phone scam, financial pyramids, gambling and procurement-fraud detection."}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0a0e16; --bg2:#0b1019;
  --surface:rgba(255,255,255,.025); --surface2:rgba(255,255,255,.045);
  --border:rgba(255,255,255,.08); --border2:rgba(255,255,255,.14);
  --text:#e7ebf3; --text2:#aab3c6; --muted:#6f7a8f;
  --accent:#7aa2f7; --accent2:#6ee7d3; --accent3:#bb9af7;
  --soft:rgba(122,162,247,.12);
  --danger:#f7768e; --warn:#e0af68; --ok:#9ece6a;
  --radius:18px; --maxw:1140px;
  --ease:cubic-bezier(.16,1,.3,1);
}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.6;overflow-x:hidden;-webkit-font-smoothing:antialiased;letter-spacing:-.011em}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.aurora{position:fixed;inset:0;z-index:-2;overflow:hidden;background:radial-gradient(1200px 800px at 50% -10%, #101725 0%, var(--bg) 60%)}
.blob{position:absolute;border-radius:50%;filter:blur(90px);opacity:.5;will-change:transform}
.b1{width:560px;height:560px;background:radial-gradient(circle, rgba(122,162,247,.42), transparent 70%);top:-160px;left:-80px;animation:drift1 26s var(--ease) infinite alternate}
.b2{width:520px;height:520px;background:radial-gradient(circle, rgba(110,231,211,.30), transparent 70%);top:120px;right:-120px;animation:drift2 30s var(--ease) infinite alternate}
.b3{width:480px;height:480px;background:radial-gradient(circle, rgba(187,154,247,.26), transparent 70%);top:640px;left:30%;animation:drift3 34s var(--ease) infinite alternate}
@keyframes drift1{to{transform:translate(120px,80px) scale(1.1)}}
@keyframes drift2{to{transform:translate(-100px,60px) scale(1.05)}}
@keyframes drift3{to{transform:translate(80px,-70px) scale(1.12)}}
.grain{position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.025;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
nav{position:fixed;top:14px;left:0;right:0;z-index:50}
.navbar{max-width:var(--maxw);margin:0 auto;padding:11px 18px;display:flex;align-items:center;justify-content:space-between;background:rgba(13,18,28,.55);border:1px solid var(--border);border-radius:16px;backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px)}
.brand{display:flex;align-items:center;gap:9px;font-weight:700;font-size:16px}
.brand svg{width:24px;height:24px}
.nav-links{display:flex;gap:26px;font-size:14px;color:var(--text2)}
.nav-links a{transition:color .2s var(--ease)}
.nav-links a:hover{color:var(--text)}
.nav-cta{background:linear-gradient(135deg,var(--accent),#5b87e8);color:#06101f;font-weight:600;font-size:14px;padding:9px 16px;border-radius:11px;transition:transform .25s var(--ease),box-shadow .25s var(--ease)}
.nav-cta:hover{transform:translateY(-1px);box-shadow:0 8px 24px rgba(122,162,247,.35)}
@media(max-width:780px){.nav-links{display:none}}
.hero{padding:170px 0 80px;text-align:center;position:relative}
.badge{display:inline-flex;align-items:center;gap:7px;font-size:12.5px;color:var(--text2);background:var(--surface);border:1px solid var(--border);padding:6px 14px;border-radius:999px;margin-bottom:26px}
.badge .dot{width:7px;height:7px;border-radius:50%;background:var(--ok);box-shadow:0 0 0 3px rgba(158,206,106,.18)}
h1{font-size:clamp(40px,7vw,76px);font-weight:800;line-height:1.04;letter-spacing:-.035em;margin-bottom:22px}
h1 .grad{background:linear-gradient(120deg,var(--accent),var(--accent2),var(--accent3),var(--accent2));background-size:220% auto;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 7s linear infinite}
@keyframes shimmer{to{background-position:220% center}}
.lead{font-size:clamp(16px,2.2vw,20px);color:var(--text2);max-width:620px;margin:0 auto 38px;line-height:1.6}
.checker{max-width:560px;margin:0 auto;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:10px;display:flex;gap:9px;box-shadow:0 24px 60px -20px rgba(0,0,0,.6);transition:border-color .3s var(--ease)}
.checker:focus-within{border-color:var(--border2)}
.checker input{flex:1;background:transparent;border:none;outline:none;color:var(--text);font-size:15.5px;padding:13px 16px;font-family:inherit}
.checker input::placeholder{color:var(--muted)}
.checker button{background:linear-gradient(135deg,var(--accent),#5b87e8);color:#06101f;border:none;font-weight:700;font-size:14.5px;padding:0 24px;border-radius:12px;cursor:pointer;font-family:inherit;transition:transform .25s var(--ease),box-shadow .25s var(--ease)}
.checker button:hover{transform:translateY(-1px);box-shadow:0 10px 28px rgba(122,162,247,.35)}
.checker button:disabled{opacity:.6;cursor:default;transform:none}
.result{max-width:560px;margin:16px auto 0;border-radius:14px;border:1px solid var(--border);padding:16px 18px;text-align:left;display:none;animation:rise .5s var(--ease)}
.result.show{display:block}
.result.DANGEROUS{border-color:rgba(247,118,142,.4);background:rgba(247,118,142,.06)}
.result.SUSPICIOUS{border-color:rgba(224,175,104,.4);background:rgba(224,175,104,.06)}
.result.SAFE{border-color:rgba(158,206,106,.4);background:rgba(158,206,106,.06)}
.result .rv{font-size:16px;font-weight:700;display:flex;align-items:center;gap:9px}
.result.DANGEROUS .rv{color:var(--danger)}.result.SUSPICIOUS .rv{color:var(--warn)}.result.SAFE .rv{color:var(--ok)}
.result .rd{font-size:13.5px;color:var(--text2);margin-top:6px}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.stats{display:flex;flex-wrap:wrap;justify-content:center;gap:14px;margin-top:48px}
.stat{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:18px 26px;min-width:140px}
.stat .n{font-size:28px;font-weight:800;letter-spacing:-.02em;font-variant-numeric:tabular-nums;background:linear-gradient(120deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.stat .l{font-size:12.5px;color:var(--muted);margin-top:4px;text-transform:uppercase;letter-spacing:.05em}
section{position:relative}
.sec{padding:90px 0}
.eyebrow{font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;background:linear-gradient(120deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:14px}
.stitle{font-size:clamp(28px,4vw,42px);font-weight:800;letter-spacing:-.03em;line-height:1.1;margin-bottom:14px}
.ssub{color:var(--text2);font-size:16px;max-width:560px;margin-bottom:46px}
.bento{display:grid;grid-template-columns:repeat(6,1fr);gap:16px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:26px;position:relative;overflow:hidden;transition:transform .4s var(--ease),border-color .4s var(--ease),background .4s var(--ease)}
.card::before{content:"";position:absolute;inset:0;border-radius:inherit;opacity:0;background:radial-gradient(440px circle at var(--mx,50%) var(--my,0%),rgba(122,162,247,.12),transparent 45%);transition:opacity .4s var(--ease);pointer-events:none}
.card:hover{border-color:var(--border2);background:var(--surface2)}
.card:hover::before{opacity:1}
.card.span3{grid-column:span 3}.card.span2{grid-column:span 2}.card.span6{grid-column:span 6}
.ic{width:42px;height:42px;border-radius:12px;display:grid;place-items:center;background:var(--soft);border:1px solid var(--border);margin-bottom:16px}
.ic svg{width:22px;height:22px;stroke:var(--accent);fill:none;stroke-width:1.8}
.card h3{font-size:17px;font-weight:700;margin-bottom:8px;letter-spacing:-.01em}
.card p{font-size:14px;color:var(--text2);line-height:1.6}
.card .arrow{margin-top:16px;font-size:13px;font-weight:600;color:var(--accent);display:inline-flex;align-items:center;gap:5px}
a.card{display:block}
@media(max-width:900px){.bento{grid-template-columns:repeat(2,1fr)}.card.span3,.card.span2,.card.span6{grid-column:span 1}}
@media(max-width:560px){.bento{grid-template-columns:1fr}}
.pipe{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:8px}
.pstep{flex:1;min-width:150px;background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:18px 16px;text-align:center;position:relative;transition:transform .4s var(--ease),border-color .4s var(--ease)}
.pstep:hover{transform:translateY(-3px);border-color:var(--border2)}
.pstep .pn{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;margin:0 auto 10px;font-weight:700;font-size:14px;color:#06101f;background:linear-gradient(135deg,var(--accent),var(--accent2))}
.pstep .pnm{font-size:13.5px;color:var(--text2);font-weight:500}
.tg{background:linear-gradient(135deg,rgba(122,162,247,.1),rgba(110,231,211,.06));border:1px solid var(--border);border-radius:24px;padding:54px 32px;text-align:center}
.tg h3{font-size:26px;font-weight:800;letter-spacing:-.02em;margin-bottom:10px}
.tg p{color:var(--text2);max-width:440px;margin:0 auto 26px}
.tg-btn{display:inline-flex;align-items:center;gap:9px;background:#fff;color:#0a0e16;font-weight:700;font-size:15px;padding:14px 26px;border-radius:13px;transition:transform .25s var(--ease),box-shadow .25s var(--ease)}
.tg-btn:hover{transform:translateY(-2px);box-shadow:0 14px 36px rgba(255,255,255,.16)}
.pills{display:flex;flex-wrap:wrap;gap:10px}
.pill{font-size:13px;color:var(--text2);background:var(--surface);border:1px solid var(--border);padding:8px 15px;border-radius:999px;transition:border-color .3s var(--ease),color .3s var(--ease)}
.pill:hover{border-color:var(--border2);color:var(--text)}
footer{border-top:1px solid var(--border);padding:48px 0 40px;margin-top:60px;text-align:center}
.flinks{display:flex;flex-wrap:wrap;gap:22px;justify-content:center;font-size:14px;color:var(--text2);margin:18px 0}
.flinks a{transition:color .2s var(--ease)}.flinks a:hover{color:var(--accent)}
.fnote{color:var(--muted);font-size:13px;line-height:1.7}
.js .reveal{opacity:0;transform:translateY(22px);transition:opacity .8s var(--ease),transform .8s var(--ease)}
.js .reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){
  *{animation:none!important}
  .js .reveal{opacity:1;transform:none;transition:none}
  html{scroll-behavior:auto}
  .card,.pstep{transition:border-color .2s}
  .grad{animation:none!important}
  .packet{display:none}
}
.skip{position:fixed;top:-60px;left:14px;z-index:100;background:var(--accent);color:#06101f;padding:9px 16px;border-radius:10px;font-weight:600;transition:top .25s var(--ease)}
.skip:focus{top:14px}
.progress{position:fixed;top:0;left:0;height:2.5px;width:0;z-index:60;background:linear-gradient(90deg,var(--accent),var(--accent2));box-shadow:0 0 8px rgba(122,162,247,.5)}
.theme-btn{background:var(--surface);border:1px solid var(--border);color:var(--text2);width:38px;height:38px;border-radius:11px;display:grid;place-items:center;cursor:pointer;transition:.25s var(--ease);flex:0 0 auto}
.theme-btn:hover{color:var(--text);border-color:var(--border2)}
.theme-btn svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.8}
.lang{display:flex;background:var(--surface);border:1px solid var(--border);border-radius:11px;overflow:hidden;flex:0 0 auto}
.lang button{background:none;border:none;color:var(--muted);font-family:inherit;font-weight:600;font-size:12px;padding:8px 9px;cursor:pointer;transition:.2s var(--ease)}
.lang button.on{background:var(--accent);color:#06101f}
.lang button:hover:not(.on){color:var(--text)}
@media(max-width:560px){.lang{display:none}}
[data-theme="light"]{--bg:#f5f7fc;--surface:rgba(10,16,30,.035);--surface2:rgba(10,16,30,.06);--border:rgba(10,16,30,.1);--border2:rgba(10,16,30,.2);--text:#0f1828;--text2:#48566c;--muted:#8693a8;--accent:#4f72d6;--accent2:#1fa896;--accent3:#8b5cf6;--soft:rgba(79,114,214,.1)}
[data-theme="light"] .aurora{background:radial-gradient(1200px 800px at 50% -10%, #e7edfb 0%, var(--bg) 60%)}
[data-theme="light"] .blob{opacity:.3}
[data-theme="light"] .navbar,[data-theme="light"] .ibanner{background:rgba(255,255,255,.72)}
[data-theme="light"] .grain{opacity:.012}
[data-theme="light"] .tg-btn{background:#0f1828;color:#fff}
[data-theme="light"] .pstep .pn,[data-theme="light"] .nav-cta,[data-theme="light"] .checker button{color:#fff}
.prob{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;text-align:center}
.prob .pc{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:28px 16px;transition:transform .4s var(--ease),border-color .4s var(--ease)}
.prob .pc:hover{transform:translateY(-3px);border-color:var(--border2)}
.prob .pn{font-size:clamp(26px,3.6vw,40px);font-weight:800;letter-spacing:-.02em;background:linear-gradient(120deg,var(--danger),var(--accent3));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;font-variant-numeric:tabular-nums}
.prob .pl{font-size:13px;color:var(--text2);margin-top:8px;line-height:1.5}
@media(max-width:740px){.prob{grid-template-columns:repeat(2,1fr)}}
.packet{position:absolute;top:-5px;left:0;width:10px;height:10px;border-radius:50%;background:var(--accent2);box-shadow:0 0 14px var(--accent2),0 0 26px rgba(110,231,211,.5);opacity:0}
.js .packet{opacity:1;animation:flow 4.8s var(--ease) infinite}
@keyframes flow{0%,4%{left:1%}96%,100%{left:99%}}
.pstep.lit{border-color:var(--accent2);box-shadow:0 0 26px -8px rgba(110,231,211,.5);transform:translateY(-3px)}
.ibanner{position:fixed;left:50%;bottom:20px;transform:translateX(-50%) translateY(140px);z-index:55;background:rgba(13,18,28,.9);border:1px solid var(--border2);border-radius:16px;padding:13px 16px;display:flex;align-items:center;gap:14px;backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);box-shadow:0 20px 50px -12px rgba(0,0,0,.6);transition:transform .5s var(--ease);max-width:92vw}
.ibanner.show{transform:translateX(-50%) translateY(0)}
.ibanner b{font-size:14px;display:block}.ibanner .it{font-size:12.5px;color:var(--text2)}
.ibanner button{border:none;cursor:pointer;font-family:inherit;font-weight:600;font-size:13px;padding:9px 15px;border-radius:10px}
.ib-yes{background:var(--accent);color:#06101f}.ib-no{background:transparent;color:var(--muted)}
.faq{max-width:760px}
.fq{background:var(--surface);border:1px solid var(--border);border-radius:14px;margin-bottom:12px;overflow:hidden;transition:border-color .3s var(--ease)}
.fq[open]{border-color:var(--border2)}
.fq summary{list-style:none;cursor:pointer;padding:18px 22px;font-weight:600;font-size:15px;display:flex;align-items:center;justify-content:space-between;gap:14px}
.fq summary::-webkit-details-marker{display:none}
.fq summary i{width:18px;height:18px;flex:0 0 auto;position:relative}
.fq summary i::before,.fq summary i::after{content:"";position:absolute;background:var(--accent);border-radius:2px}
.fq summary i::before{top:8px;left:0;width:18px;height:2px}
.fq summary i::after{top:0;left:8px;width:2px;height:18px;transition:transform .3s var(--ease)}
.fq[open] summary i::after{transform:scaleY(0)}
.fa{padding:0 22px 20px;color:var(--text2);font-size:14px;line-height:1.65}
.fq[open] .fa{animation:fadein .35s var(--ease)}
@keyframes fadein{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}
.fa code{background:var(--surface2);border:1px solid var(--border);border-radius:5px;padding:1px 6px;font-size:12.5px;color:var(--accent)}
</style>
</head>
<body>
<a class="skip" href="#features">Мазмұнға өту</a>
<div class="progress" id="progress"></div>
<div class="aurora"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div></div>
<div class="grain"></div>
<nav>
  <div class="navbar">
    <div class="brand">
      <svg viewBox="0 0 24 24" fill="none"><path d="M12 2 4 5v6c0 5 3.4 8.6 8 10 4.6-1.4 8-5 8-10V5z" stroke="url(#g)" stroke-width="1.6" fill="rgba(122,162,247,.12)"/><defs><linearGradient id="g" x1="4" y1="2" x2="20" y2="22"><stop stop-color="#7aa2f7"/><stop offset="1" stop-color="#6ee7d3"/></linearGradient></defs></svg>
      Qalqan AI
    </div>
    <div class="nav-links">
      <a href="#features" data-i18n="nav_feat">Функциялар</a>
      <a href="#pipeline" data-i18n="nav_arch">Архитектура</a>
      <a href="#demo" data-i18n="nav_demo">Демо</a>
      <a href="#tech" data-i18n="nav_tech">Технологиялар</a>
      <a href="#faq">FAQ</a>
    </div>
    <div style="display:flex;align-items:center;gap:10px">
      <div class="lang" id="langSw" role="group" aria-label="Тіл / Язык / Language">
        <button data-lang="kk">KZ</button><button data-lang="ru">RU</button><button data-lang="en">EN</button>
      </div>
      <button class="theme-btn" id="themeBtn" aria-label="Тема ауыстыру" title="Light / Dark"></button>
      <a class="nav-cta mag" href="/install" data-i18n="nav_install">Орнату</a>
    </div>
  </div>
</nav>
<header class="hero">
  <div class="wrap">
    <div class="badge reveal"><span class="dot"></span><span data-i18n="badge">v5.1 · Қазақстан үшін · Open source</span></div>
    <h1 class="reveal"><span data-i18n="h1a">Алаяқтықтан</span><br><span class="grad" data-i18n="h1b">AI қорғанысы</span></h1>
    <p class="lead reveal" data-i18n="lead">Фишинг, телефон алаяқтығы, қаржылық пирамида, гемблинг және госзакуп фроды — бәрін бет жүктелмей тұрып анықтаймыз. Тегін.</p>
    <div class="checker reveal">
      <input id="urlInput" type="text" inputmode="url" placeholder="kaspi-bonus.kz немесе https://..." data-i18n-ph="checkPh" autocomplete="off" aria-label="URL тексеру">
      <button id="checkBtn" data-i18n="checkBtn">Тексеру</button>
    </div>
    <div class="result" id="resultBox"><div class="rv" id="resultVerdict"></div><div class="rd" id="resultDetail"></div></div>
    <div class="stats reveal">
      <div class="stat"><div class="n" id="statChecked" data-to="0">—</div><div class="l" data-i18n="st_checked">Тексерілді</div></div>
      <div class="stat"><div class="n" id="statBlocked" data-to="0">—</div><div class="l" data-i18n="st_blocked">Бұғатталды</div></div>
      <div class="stat"><div class="n" id="statDomains" data-to="390" data-suffix="+">390+</div><div class="l" data-i18n="st_offline">Офлайн база</div></div>
      <div class="stat"><div class="n" data-to="6">6</div><div class="l" data-i18n="st_levels">Деңгей</div></div>
    </div>
  </div>
</header>
<section class="sec" id="problem">
  <div class="wrap">
    <div class="eyebrow reveal">Неге керек</div>
    <h2 class="stitle reveal">Қазақстандағы цифрлық алаяқтық</h2>
    <p class="ssub reveal">2025 жылғы 10 айдағы ресми статистика — масштаб орасан.</p>
    <div class="prob">
      <div class="pc reveal"><div class="pn"><span data-to="16.4" data-dec="1">0</span> млрд ₸</div><div class="pl">ұрланған қаражат (10 айда)</div></div>
      <div class="pc reveal"><div class="pn">×<span data-to="29">0</span></div><div class="pl">2024 жылмен салыстырғанда өсім</div></div>
      <div class="pc reveal"><div class="pn"><span data-to="26300">0</span></div><div class="pl">тіркелген кибер-алаяқтық дерегі</div></div>
      <div class="pc reveal"><div class="pn">+<span data-to="86">0</span>%</div><div class="pl">оқиғалар санының өсуі</div></div>
    </div>
  </div>
</section>
<section class="sec" id="features">
  <div class="wrap">
    <div class="eyebrow reveal">Функционал</div>
    <h2 class="stitle reveal">Не қорғайды</h2>
    <p class="ssub reveal">6-деңгейлі pipeline — 1 мс кэш-тексеруден AI анализіне дейін.</p>
    <div class="bento">
      <div class="card span3 tilt reveal">
        <div class="ic"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg></div>
        <h3>Фишинг сайттары</h3><p>Kaspi, eGov, Halyk Bank клондарын анықтайды — homoglyph (кириллица әріптерін) және typosquat шабуылдарын қоса. Бет жүктелуіне дейін бұғаттайды.</p>
      </div>
      <div class="card span3 tilt reveal">
        <div class="ic"><svg viewBox="0 0 24 24"><path d="M3 18a9 9 0 0 1 18 0"/><path d="M12 3v3M5 9 7 11M19 9l-2 2"/><circle cx="12" cy="18" r="1.5"/></svg></div>
        <h3>Телефон алаяқтығы</h3><p>Дауыстық хабарламаны Whisper арқылы транскрипциялап, ҚР скам-паттерндерін табады. #1 қауіп — енді одан қорғаныс бар.</p>
      </div>
      <div class="card span2 tilt reveal">
        <div class="ic"><svg viewBox="0 0 24 24"><polygon points="12 2 15 9 22 9.3 16.5 14 18.5 21 12 17 5.5 21 7.5 14 2 9.3 9 9"/></svg></div>
        <h3>Қаржылық пирамидалар</h3><p>АФМ реестрі бойынша атау тексеру + Finiko, MMM, HYIP базасы.</p>
      </div>
      <div class="card span2 tilt reveal">
        <div class="ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M5 5l14 14"/></svg></div>
        <h3>Нелегал гемблинг</h3><p>80+ ҚР-да тыйым салынған сайт. 1xBet, Mostbet — браузерде ашылмайды.</p>
      </div>
      <div class="card span2 tilt reveal">
        <div class="ic"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h4"/></svg></div>
        <h3>Госзакуп фроды</h3><p>Заказчик↔поставщик↔учредитель граф: аффилированность, сговор, картель.</p>
      </div>
    </div>
  </div>
</section>
<section class="sec" id="pipeline">
  <div class="wrap">
    <div class="eyebrow reveal">Архитектура</div>
    <h2 class="stitle reveal">6-деңгейлі анықтау</h2>
    <p class="ssub reveal">Әр сұраныс алты қабаттан өтеді — жылдамнан тереңге.</p>
    <div class="pipe">
      <span class="packet" id="packet"></span>
      <div class="pstep reveal"><div class="pn">1</div><div class="pnm">Ақ тізім</div></div>
      <div class="pstep reveal"><div class="pn">2</div><div class="pnm">Redis кэш</div></div>
      <div class="pstep reveal"><div class="pn">3</div><div class="pnm">Офлайн DB</div></div>
      <div class="pstep reveal"><div class="pn">4</div><div class="pnm">KZ Intel</div></div>
      <div class="pstep reveal"><div class="pn">5</div><div class="pnm">Сыртқы DB + домен</div></div>
      <div class="pstep reveal"><div class="pn">6</div><div class="pnm">Groq / Gemini AI</div></div>
    </div>
  </div>
</section>
<section class="sec" id="demo">
  <div class="wrap">
    <div class="eyebrow reveal">Демо</div>
    <h2 class="stitle reveal">Бәрі тірі — ашып көріңіз</h2>
    <p class="ssub reveal">Жұмыс істеп тұрған платформалар мен панельдер.</p>
    <div class="bento">
      <a class="card span2 tilt reveal" href="/dashboard?demo=1">
        <div class="ic"><svg viewBox="0 0 24 24"><path d="M3 3v18h18"/><path d="M7 14l3-4 3 2 4-6"/></svg></div>
        <h3>Реттеуші панелі</h3><p>Облыстар бойынша қауіп картасы, динамика, топ домендер.</p><span class="arrow">Ашу →</span>
      </a>
      <a class="card span2 tilt reveal" href="/goszakup/graph">
        <div class="ic"><svg viewBox="0 0 24 24"><circle cx="5" cy="6" r="2.5"/><circle cx="19" cy="7" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M7 7l3 9M17 9l-3 7"/></svg></div>
        <h3>Госзакуп графы</h3><p>Аффилированность, сговор, картель — байланыс графы.</p><span class="arrow">Ашу →</span>
      </a>
      <a class="card span2 tilt reveal" href="/m">
        <div class="ic"><svg viewBox="0 0 24 24"><rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/></svg></div>
        <h3>Мобиль қосымша</h3><p>Офлайн жұмыс істейді, телефонға орнатылады (PWA).</p><span class="arrow">Ашу →</span>
      </a>
      <a class="card span2 tilt reveal" href="https://t.me/QalqanAI_bot" target="_blank" rel="noopener">
        <div class="ic"><svg viewBox="0 0 24 24"><path d="M21 5 3 12l5 2 2 5 3-4 4 3z"/></svg></div>
        <h3>Telegram бот</h3><p>Дауыс / SMS / сілтеме тексеру, KZ-CERT-ке хабарлау.</p><span class="arrow">Ашу →</span>
      </a>
      <a class="card span2 tilt reveal" href="/stats">
        <div class="ic"><svg viewBox="0 0 24 24"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg></div>
        <h3>Тірі статистика</h3><p>Нақты деректер: тексерулер, вердиктер, трендтер.</p><span class="arrow">Ашу →</span>
      </a>
      <a class="card span2 tilt reveal" href="/feed/kz">
        <div class="ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18"/></svg></div>
        <h3>KZ Threat Feed</h3><p>Ашық дерекқор (CC-BY) — басқа жүйелер пайдалана алады.</p><span class="arrow">Ашу →</span>
      </a>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="tg reveal">
      <h3>Telegram-да тексер</h3>
      <p>Кез келген сілтемені, нөмірді, дауыстық хабарламаны жіберіп, бірден жауап ал.</p>
      <a class="tg-btn" href="https://t.me/QalqanAI_bot" target="_blank" rel="noopener">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="#0a0e16"><path d="M21 5 3 12l5 2 2 5 3-4 4 3z"/></svg>@QalqanAI_bot ашу
      </a>
    </div>
  </div>
</section>
<section class="sec" id="tech">
  <div class="wrap">
    <div class="eyebrow reveal">Технологиялар</div>
    <h2 class="stitle reveal">Стек</h2>
    <div class="pills reveal">
      <span class="pill">Python · FastAPI</span><span class="pill">React 19</span><span class="pill">Chrome MV3</span>
      <span class="pill">Groq llama-3.3-70b</span><span class="pill">Gemini 2.5-flash</span><span class="pill">Whisper</span>
      <span class="pill">30+ URL features</span><span class="pill">Upstash Redis</span><span class="pill">Supabase</span>
      <span class="pill">PhishTank · URLhaus</span><span class="pill">Google Safe Browsing</span>
    </div>
  </div>
</section>
<section class="sec" id="faq">
  <div class="wrap">
    <div class="eyebrow reveal">Сұрақ-жауап</div>
    <h2 class="stitle reveal">Жиі қойылатын сұрақтар</h2>
    <p class="ssub reveal">Нақты жауаптар — артық сөзсіз.</p>
    <div class="faq reveal">
      <details class="fq"><summary>Тегін бе?<i></i></summary><div class="fa">Иә, азаматтарға толық тегін — жасырын ақы жоқ. Монетизация: банк пен реттеушіге арналған B2G API (<code>/v1</code>).</div></details>
      <details class="fq"><summary>Менің деректерім қауіпсіз бе?<i></i></summary><div class="fa">Сілтеме мен IP тек SHA-256 хэш түрінде сақталады — шикі дерек ешқашан жазылмайды. URL query-параметрлері логқа түспейді. Барлық агрегация анонимді.</div></details>
      <details class="fq"><summary>Қалай жұмыс істейді?<i></i></summary><div class="fa">6 деңгейлі pipeline: ақ тізім → Redis кэш → офлайн-база → KZ intel (бренд/пирамида/гемблинг) → сыртқы БД + домен анализі → Groq/Gemini AI. Қауіпті сайт бет жүктелмей тұрып бұғатталады.</div></details>
      <details class="fq"><summary>Қандай қауіптерді анықтайды?<i></i></summary><div class="fa">Фишинг (homoglyph/typosquat қоса), телефон/SMS алаяқтығы, қаржы пирамидалары (АФМ реестрі), нелегал гемблинг, госзакуп фроды (граф), дауыс-скам (Whisper). Офлайн-база: 390+ домен, тірі threat-feed: 1800+ домен.</div></details>
      <details class="fq"><summary>Қай тілдерде?<i></i></summary><div class="fa">Қазақша, орысша, ағылшынша — детекция да, түсіндірме де үш тілде.</div></details>
      <details class="fq"><summary>Интернетсіз жұмыс істей ме?<i></i></summary><div class="fa">Иә. Мобиль қосымша (PWA) мен браузер кеңейтімі офлайн-базамен жұмыс істейді — желісіз де негізгі тексеру жүреді.</div></details>
      <details class="fq"><summary>Банктер/реттеушілер қалай қосыла алады?<i></i></summary><div class="fa">B2G API: <code>X-API-Key</code> арқылы <code>/v1/check</code>, <code>/v1/batch</code>, <code>/v1/phone</code>. <code>/v1/contribute</code> арқылы CERT/банктер ортақ қауіп-базасын толтырады (federated).</div></details>
    </div>
  </div>
</section>
<div class="ibanner" id="ibanner" role="dialog" aria-label="Қосымшаны орнату">
  <div><b>Qalqan AI — телефоныңа</b><span class="it">Офлайн жұмыс істейді · PWA</span></div>
  <button class="ib-yes" id="ibYes">Орнату</button>
  <button class="ib-no" id="ibNo" aria-label="Жабу">✕</button>
</div>
<footer>
  <div class="wrap">
    <div class="brand" style="justify-content:center">
      <svg viewBox="0 0 24 24" fill="none"><path d="M12 2 4 5v6c0 5 3.4 8.6 8 10 4.6-1.4 8-5 8-10V5z" stroke="url(#g2)" stroke-width="1.6" fill="rgba(122,162,247,.12)"/><defs><linearGradient id="g2" x1="4" y1="2" x2="20" y2="22"><stop stop-color="#7aa2f7"/><stop offset="1" stop-color="#6ee7d3"/></linearGradient></defs></svg>
      Qalqan AI
    </div>
    <div class="flinks">
      <a href="https://github.com/Kennurken/qalqan-ai" target="_blank" rel="noopener">GitHub</a>
      <a href="/m">Мобилка</a><a href="/docs">API</a><a href="/dashboard">Панель</a><a href="/feed/kz">Feed</a><a href="/health">Health</a>
    </div>
    <div class="fnote">Қазақстандық пайдаланушыларды цифрлық қауіптерден қорғау · v5.1<br>Республикалық конкурс ДЭР 2026 · Деректер анонимді (url_hash / ip_hash)</div>
  </div>
</footer>
<script>
document.documentElement.classList.add('js');
const $=s=>document.querySelector(s);
const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const io=new IntersectionObserver((es)=>{es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
document.querySelectorAll('.reveal').forEach((el,i)=>{el.style.transitionDelay=(Math.min(i%6,5)*60)+'ms';io.observe(el)});
function countUp(el){
  const to=+el.dataset.to||0, suf=el.dataset.suffix||'', dec=+el.dataset.dec||0;
  const fmt=v=>dec?v.toLocaleString('ru-RU',{minimumFractionDigits:dec,maximumFractionDigits:dec}):Math.round(v).toLocaleString('ru-RU');
  if(reduce||!to){el.textContent=fmt(to)+suf;return}
  const dur=1200, t0=performance.now();
  (function tick(t){const p=Math.min((t-t0)/dur,1);const e=1-Math.pow(1-p,3);
    el.textContent=fmt(to*e)+suf;
    if(p<1)requestAnimationFrame(tick)})(t0);
}
const statIO=new IntersectionObserver((es)=>{es.forEach(e=>{if(e.isIntersecting){countUp(e.target);statIO.unobserve(e.target)}})},{threshold:.5});
document.querySelectorAll('.stat .n[data-to], .prob .pn [data-to]').forEach(el=>statIO.observe(el));
if(!reduce){
  document.querySelectorAll('.tilt').forEach(card=>{
    card.addEventListener('mousemove',e=>{
      const r=card.getBoundingClientRect();
      const px=(e.clientX-r.left)/r.width, py=(e.clientY-r.top)/r.height;
      card.style.transform=`perspective(900px) rotateX(${(py-.5)*-5}deg) rotateY(${(px-.5)*5}deg) translateY(-4px)`;
      card.style.setProperty('--mx',px*100+'%');card.style.setProperty('--my',py*100+'%');
    });
    card.addEventListener('mouseleave',()=>{card.style.transform=''});
  });
}
/* i18n — kk/ru/en. AI/verdict comes back in currentLang (sent to /check). */
const I18N={
 kk:{nav_feat:'Функциялар',nav_arch:'Архитектура',nav_demo:'Демо',nav_tech:'Технологиялар',nav_install:'Орнату',
     badge:'v5.1 · Қазақстан үшін · Open source',h1a:'Алаяқтықтан',h1b:'AI қорғанысы',
     lead:'Фишинг, телефон алаяқтығы, қаржылық пирамида, гемблинг және госзакуп фроды — бәрін бет жүктелмей тұрып анықтаймыз. Тегін.',
     checkPh:'kaspi-bonus.kz немесе https://...',checkBtn:'Тексеру',
     st_checked:'Тексерілді',st_blocked:'Бұғатталды',st_offline:'Офлайн база',st_levels:'Деңгей',err:'Қате',errd:'Кейінірек қайталаңыз'},
 ru:{nav_feat:'Функции',nav_arch:'Архитектура',nav_demo:'Демо',nav_tech:'Технологии',nav_install:'Установить',
     badge:'v5.1 · Для Казахстана · Open source',h1a:'Защита от',h1b:'мошенников · AI',
     lead:'Фишинг, телефонный скам, финансовые пирамиды, гемблинг и госзакуп-фрод — ловим до загрузки страницы. Бесплатно.',
     checkPh:'kaspi-bonus.kz или https://...',checkBtn:'Проверить',
     st_checked:'Проверено',st_blocked:'Заблокировано',st_offline:'Офлайн-база',st_levels:'Уровней',err:'Ошибка',errd:'Повторите позже'},
 en:{nav_feat:'Features',nav_arch:'Architecture',nav_demo:'Demo',nav_tech:'Tech',nav_install:'Install',
     badge:'v5.1 · For Kazakhstan · Open source',h1a:'AI shield',h1b:'against scams',
     lead:'Phishing, phone scams, financial pyramids, gambling and procurement fraud — caught before the page loads. Free.',
     checkPh:'kaspi-bonus.kz or https://...',checkBtn:'Check',
     st_checked:'Checked',st_blocked:'Blocked',st_offline:'Offline DB',st_levels:'Tiers',err:'Error',errd:'Try again later'}
};
let currentLang=localStorage.getItem('qlang')||(navigator.language||'kk').slice(0,2).toLowerCase();
if(!I18N[currentLang])currentLang='kk';
function applyLang(l){
  currentLang=I18N[l]?l:'kk'; localStorage.setItem('qlang',currentLang);
  const D=I18N[currentLang];
  document.querySelectorAll('[data-i18n]').forEach(el=>{const v=D[el.dataset.i18n];if(v!=null)el.textContent=v;});
  document.querySelectorAll('[data-i18n-ph]').forEach(el=>{const v=D[el.dataset.i18nPh];if(v!=null)el.placeholder=v;});
  document.documentElement.lang=currentLang;
  document.querySelectorAll('#langSw button').forEach(b=>b.classList.toggle('on',b.dataset.lang===currentLang));
}
document.querySelectorAll('#langSw button').forEach(b=>b.addEventListener('click',()=>applyLang(b.dataset.lang)));
applyLang(currentLang);

const box=$('#resultBox'),verdict=$('#resultVerdict'),detail=$('#resultDetail'),btn=$('#checkBtn'),input=$('#urlInput');
async function runCheck(){
  const url=input.value.trim(); if(!url)return;
  btn.disabled=true; const old=btn.textContent; btn.textContent='...';
  try{
    const res=await fetch('/check',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url,lang:currentLang})});
    const d=await res.json();
    box.className='result show '+(d.verdict||'SUSPICIOUS');
    const ic=d.verdict==='DANGEROUS'?'⛔':d.verdict==='SUSPICIOUS'?'⚠':'✓';
    verdict.textContent=ic+'  '+(d.verdict||'')+' · '+(d.threat_score||0)+'/100';
    detail.textContent=d.detail||d['detail_'+currentLang]||d.detail_kk||'';
  }catch(e){box.className='result show SUSPICIOUS';verdict.textContent='⚠  '+I18N[currentLang].err;detail.textContent=I18N[currentLang].errd;}
  btn.disabled=false; btn.textContent=old;
}
btn.addEventListener('click',runCheck);
input.addEventListener('keydown',e=>{if(e.key==='Enter')runCheck()});
fetch('/stats').then(r=>r.json()).then(t=>{
  const set=(id,v)=>{const el=document.getElementById(id);if(el&&v!=null){el.dataset.to=v;countUp(el)}};
  set('statChecked',t.total_checks); set('statBlocked',t.dangerous_blocked??t.dangerous);
}).catch(()=>{});

/* scroll progress */
const prog=document.getElementById('progress');
addEventListener('scroll',()=>{const h=document.documentElement;const m=h.scrollHeight-h.clientHeight;prog.style.width=(m>0?h.scrollTop/m*100:0)+'%';},{passive:true});

/* theme toggle (respects prefers-color-scheme; persists) */
const SUN='<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4 12H2M22 12h-2M5 5l1.4 1.4M17.6 17.6 19 19M19 5l-1.4 1.4M6.4 17.6 5 19"/></svg>';
const MOON='<svg viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
const tb=document.getElementById('themeBtn'), tcMeta=document.querySelector('meta[name=theme-color]');
function applyTheme(t){document.documentElement.dataset.theme=t;tb.innerHTML=t==='light'?MOON:SUN;if(tcMeta)tcMeta.setAttribute('content',t==='light'?'#f5f7fc':'#0a0e16');}
applyTheme(localStorage.getItem('qtheme')||(window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark'));
tb.addEventListener('click',()=>{const n=document.documentElement.dataset.theme==='light'?'dark':'light';localStorage.setItem('qtheme',n);applyTheme(n);});

/* magnetic buttons */
if(!reduce){document.querySelectorAll('.mag').forEach(b=>{
  b.addEventListener('mousemove',e=>{const r=b.getBoundingClientRect();b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.22}px,${(e.clientY-r.top-r.height/2)*.32}px)`;});
  b.addEventListener('mouseleave',()=>b.style.transform='');
});}

/* pipeline packet lights up steps as it flows */
if(!reduce){
  const steps=[...document.querySelectorAll('#pipeline .pstep')], pk=document.getElementById('packet');
  if(pk&&steps.length)setInterval(()=>{const x=pk.getBoundingClientRect().left+5;steps.forEach(s=>{const r=s.getBoundingClientRect();s.classList.toggle('lit',x>=r.left&&x<=r.right);});},90);
}

/* PWA install banner */
let dp; const ib=document.getElementById('ibanner');
addEventListener('beforeinstallprompt',e=>{e.preventDefault();dp=e;if(!localStorage.getItem('qib'))setTimeout(()=>ib.classList.add('show'),2800);});
document.getElementById('ibYes').addEventListener('click',async()=>{ib.classList.remove('show');if(dp){dp.prompt();await dp.userChoice;dp=null;}});
document.getElementById('ibNo').addEventListener('click',()=>{ib.classList.remove('show');localStorage.setItem('qib','1');});
</script>
</body>
</html>"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
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
</style>
</head>
<body>
<div class="top">
  <div>
    <h1>🛡️ Панель регулятора <span id="src" class="badge demo">—</span></h1>
    <div class="sub">Qalqan AI · Мониторинг кибер-экономических угроз Республики Казахстан</div>
  </div>
  <div><a href="/">← На главную</a> &nbsp; <a href="/dashboard/data">JSON API</a></div>
</div>

<div class="kpis" id="kpis"><div class="kpi"><div class="skel" style="height:30px;width:62%"></div><div class="skel" style="height:11px;width:85%;margin-top:9px"></div></div><div class="kpi"><div class="skel" style="height:30px;width:62%"></div><div class="skel" style="height:11px;width:85%;margin-top:9px"></div></div><div class="kpi"><div class="skel" style="height:30px;width:62%"></div><div class="skel" style="height:11px;width:85%;margin-top:9px"></div></div><div class="kpi"><div class="skel" style="height:30px;width:62%"></div><div class="skel" style="height:11px;width:85%;margin-top:9px"></div></div><div class="kpi"><div class="skel" style="height:30px;width:62%"></div><div class="skel" style="height:11px;width:85%;margin-top:9px"></div></div><div class="kpi"><div class="skel" style="height:30px;width:62%"></div><div class="skel" style="height:11px;width:85%;margin-top:9px"></div></div></div>

<div class="card">
  <h3>🗺️ Қауіп картасы — облыстар бойынша (KZ regional threat map)</h3>
  <div class="kzmap" id="kzmap"></div>
  <div class="maplegend"><span>аз қауіп</span><div class="grad"></div><span>көп қауіп</span><span style="margin-left:auto">Vercel geo · санақ бойынша</span></div>
</div>

<div class="grid">
  <div>
    <div class="card">
      <h3>Динамика проверок и угроз (30 дней)</h3>
      <svg id="line" viewBox="0 0 640 220" style="width:100%;height:auto"></svg>
      <div class="legend"><span><span class="dot" style="background:#7aa2f7"></span>Всего проверок</span><span><span class="dot" style="background:#f7768e"></span>Угрозы (опасн.+подозр.)</span></div>
    </div>
    <div class="card">
      <h3>🔴 Топ опасных доменов</h3>
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

<script>
const fmt = n => (n||0).toLocaleString('ru-RU');
const $ = id => document.getElementById(id);

function kpiCard(v,l,cls){return `<div class="kpi ${cls||''}"><div class="v">${v}</div><div class="l">${l}</div></div>`}

function renderBars(elId, obj, max){
  const entries = Object.entries(obj||{});
  const mx = max || Math.max(1, ...entries.map(e=>e[1]));
  $(elId).innerHTML = entries.map(([k,v])=>`
    <div class="bar-row"><div class="nm" title="${k}">${k}</div>
    <div class="bar-track"><div class="bar-fill" style="width:${Math.round(100*v/mx)}%"></div></div>
    <div class="vv">${fmt(v)}</div></div>`).join('') || '<div class="sub">нет данных</div>';
}

function renderLine(series){
  if(!series||!series.length){return}
  const W=640,H=220,pad=30, mx=Math.max(...series.map(s=>s.total),1);
  const X=i=>pad+i*(W-2*pad)/(series.length-1);
  const Y=v=>H-pad-(v/mx)*(H-2*pad);
  const path=arr=>arr.map((s,i)=>`${i?'L':'M'}${X(i).toFixed(1)},${Y(s).toFixed(1)}`).join(' ');
  const grid=[0,.25,.5,.75,1].map(f=>`<line x1="${pad}" y1="${H-pad-f*(H-2*pad)}" x2="${W-pad}" y2="${H-pad-f*(H-2*pad)}" stroke="#1e293b" stroke-width="1"/>`).join('');
  $('line').innerHTML = grid +
    `<path d="${path(series.map(s=>s.total))}" fill="none" stroke="#7aa2f7" stroke-width="2.5"/>`+
    `<path d="${path(series.map(s=>s.threats))}" fill="none" stroke="#f7768e" stroke-width="2.5"/>`+
    `<text x="${pad}" y="14" fill="#7d8aa0" font-size="11">${fmt(mx)}</text>`;
}

function renderDonut(vd){
  const order=[['DANGEROUS','#f7768e'],['SUSPICIOUS','#e0af68'],['SAFE','#9ece6a']];
  const total=Object.values(vd||{}).reduce((a,b)=>a+b,0)||1;
  let a0=-Math.PI/2, svg='', leg='';
  for(const [k,c] of order){
    const val=vd[k]||0; const frac=val/total; const a1=a0+frac*2*Math.PI;
    const r=80,cx=100,cy=100, lg=frac>.5?1:0;
    const x0=cx+r*Math.cos(a0),y0=cy+r*Math.sin(a0),x1=cx+r*Math.cos(a1),y1=cy+r*Math.sin(a1);
    if(val>0)svg+=`<path d="M${cx},${cy} L${x0.toFixed(1)},${y0.toFixed(1)} A${r},${r} 0 ${lg} 1 ${x1.toFixed(1)},${y1.toFixed(1)} Z" fill="${c}"/>`;
    leg+=`<div class="bar-row"><span><span class="dot" style="background:${c}"></span>${k}</span><div style="flex:1"></div><b>${fmt(val)}</b> <span class="sub">(${Math.round(frac*100)}%)</span></div>`;
    a0=a1;
  }
  svg+='<circle cx="100" cy="100" r="46" fill="#111827"/>';
  $('donut').innerHTML=svg; $('donut-leg').innerHTML=leg;
}

// Approximate geographic placement of KZ regions on a 7x5 grid
const KZ_LAYOUT={
  "Қостанай":{c:2,r:1},"СҚО":{c:3,r:1},"Павлодар":{c:5,r:1},
  "БҚО":{c:1,r:2},"Ақмола":{c:3,r:2},"Астана":{c:4,r:2},"Абай":{c:5,r:2},"ШҚО":{c:6,r:2},
  "Атырау":{c:1,r:3},"Ақтөбе":{c:2,r:3},"Ұлытау":{c:3,r:3},"Қарағанды":{c:4,r:3},
  "Маңғыстау":{c:1,r:4},"Қызылорда":{c:2,r:4},"Жамбыл":{c:4,r:4},"Жетісу":{c:6,r:4},
  "Түркістан":{c:3,r:5},"Шымкент":{c:4,r:5},"Алматы обл.":{c:5,r:5},"Алматы қ.":{c:6,r:5}
};
function heat(frac){
  const a=[13,20,36], b=[255,59,92];
  const c=a.map((v,i)=>Math.round(v+(b[i]-v)*frac));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}
function renderMap(regions){
  regions=regions||{};
  const mx=Math.max(1,...Object.values(regions).map(r=>r.threats||0));
  let html='';
  for(const [name,p] of Object.entries(KZ_LAYOUT)){
    const r=regions[name]||{total:0,threats:0};
    const frac=Math.min(1,(r.threats||0)/mx);
    const col=frac>0.45?'#fff':'#e7ebf3';
    html+=`<div class="kzt" style="grid-column:${p.c};grid-row:${p.r};background:${heat(frac)};color:${col}" title="${name}: ${r.threats} қауіп / ${r.total} тексеру"><span class="rn">${name}</span><b>${r.threats||0}</b></div>`;
  }
  $('kzmap').innerHTML=html;
}

fetch('/dashboard/data'+location.search).then(r=>r.json()).then(d=>{
  const src=$('src'); const live=d._source==='live';
  src.textContent = live?'● LIVE':'● DEMO'; src.className='badge '+(live?'live':'demo');
  const k=d.kpis||{};
  $('kpis').innerHTML =
    kpiCard(fmt(k.total_checks),'Всего проверок','cyan')+
    kpiCard(fmt(k.threats_blocked),'Заблокировано угроз','red')+
    kpiCard(fmt(k.suspicious),'Подозрительных','amber')+
    kpiCard((k.block_rate_pct||0)+'%','Доля угроз')+
    kpiCard(fmt(k.total_reports),'Жалоб граждан')+
    kpiCard(k.avg_score||0,'Средний риск-балл');
  renderLine(d.time_series);
  renderMap(d.regions);
  renderDonut(d.verdict_distribution);
  renderBars('types', d.threat_types);
  renderBars('tiers', d.tier_effectiveness);
  $('domains').innerHTML = (d.top_dangerous_domains||[]).map(x=>
    `<tr><td class="dom">${x.domain}</td><td class="n">${fmt(x.count)}</td></tr>`).join('')||'<tr><td class="sub">нет данных</td></tr>';
}).catch(e=>{ $('kpis').innerHTML='<div class="sub">Ошибка загрузки данных</div>'; });
</script>
</body>
</html>"""

INSTALL_HTML = """<!DOCTYPE html>
<html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Qalqan AI — Орнату / Установка</title>
<meta property="og:title" content="Qalqan AI — Установить расширение">
<meta property="og:description" content="Пошаговая инструкция установки Qalqan AI в Chrome и Firefox">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0e16;color:#e2e8f0;font-family:'Inter','Segoe UI',system-ui,sans-serif;min-height:100vh}
.navbar{background:rgba(10,14,26,.95);border-bottom:1px solid #1e2d4a;padding:16px 24px;display:flex;align-items:center;justify-content:space-between}
.logo{color:#7aa2f7;font-weight:700;font-size:18px;text-decoration:none}
a{color:#7aa2f7}
.page{max-width:800px;margin:0 auto;padding:48px 24px}
h1{font-size:32px;font-weight:800;margin-bottom:8px}
.subtitle{color:#64748b;margin-bottom:48px}
.tab-bar{display:flex;gap:4px;margin-bottom:32px;background:#0f1629;border-radius:10px;padding:4px}
.tab{flex:1;text-align:center;padding:10px;border-radius:7px;cursor:pointer;font-size:14px;font-weight:600;color:#64748b;transition:all .2s}
.tab.active{background:#131d35;color:#7aa2f7}
.panel{display:none}
.panel.active{display:block}
.step{display:flex;gap:16px;margin-bottom:24px;align-items:flex-start}
.step-num{width:36px;height:36px;border-radius:50%;background:rgba(122,162,247,.1);border:2px solid rgba(122,162,247,.3);color:#7aa2f7;font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px}
.step-body h3{font-size:15px;font-weight:600;margin-bottom:6px}
.step-body p{font-size:14px;color:#94a3b8;line-height:1.6}
code{background:#131d35;border:1px solid #1e2d4a;border-radius:4px;padding:2px 7px;font-family:monospace;font-size:13px;color:#7aa2f7}
.dl-btn{display:inline-flex;align-items:center;gap:8px;background:#7aa2f7;color:#0a0e16;padding:13px 28px;border-radius:10px;font-weight:700;font-size:15px;text-decoration:none;margin:12px 0}
.dl-btn:hover{opacity:.85}
.warn{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:8px;padding:12px 16px;font-size:13px;color:#e0af68;margin:16px 0}
.note{background:rgba(122,162,247,.06);border:1px solid rgba(122,162,247,.15);border-radius:8px;padding:12px 16px;font-size:13px;color:#94a3b8;margin:16px 0}
</style></head>
<body>
<div class="navbar">
  <a class="logo" href="/">🛡 Qalqan AI</a>
  <a href="/" style="color:#64748b;font-size:14px">← Басты бет</a>
</div>
<div class="page">
  <h1>Орнату нұсқаулығы</h1>
  <p class="subtitle">Установка расширения Qalqan AI · Chrome &amp; Firefox</p>

  <div class="tab-bar">
    <div class="tab active" onclick="showTab('chrome',this)">Chrome</div>
    <div class="tab" onclick="showTab('firefox',this)">Firefox</div>
  </div>

  <!-- CHROME -->
  <div class="panel active" id="tab-chrome">
    <div class="note">Chrome 88+ (Windows, macOS, Linux). Manifest V3.</div>
    <div class="step">
      <div class="step-num">1</div>
      <div class="step-body">
        <h3>ZIP файлды жүктеу</h3>
        <p>GitHub-тан соңғы нұсқаны жүктеңіз</p>
        <a class="dl-btn" href="https://github.com/Kennurken/qalqan-ai/releases/latest" target="_blank">Жүктеу (GitHub Releases)</a>
        <p>немесе <a href="https://github.com/Kennurken/qalqan-ai/archive/refs/heads/master.zip">master.zip</a> жүктеп, <code>extension/dist/</code> қалтасын пайдаланыңыз</p>
      </div>
    </div>
    <div class="step">
      <div class="step-num">2</div>
      <div class="step-body">
        <h3>Developer Mode қосу</h3>
        <p>Chrome-да <code>chrome://extensions</code> беттін ашыңыз → оң жоғарғы бұрышта <b>Developer mode</b> ауыстырып-қосыңыз</p>
      </div>
    </div>
    <div class="step">
      <div class="step-num">3</div>
      <div class="step-body">
        <h3>Load unpacked</h3>
        <p><b>Load unpacked</b> түймесін басыңыз → жүктелген ZIP-тен шыққан <code>dist/</code> қалтасын таңдаңыз</p>
      </div>
    </div>
    <div class="step">
      <div class="step-num">4</div>
      <div class="step-body">
        <h3>Дайын!</h3>
        <p>Toolbar-да Qalqan AI белгісі пайда болады. Кез-келген сайтқа өтіңіз — автоматты тексеру іске қосылады.</p>
      </div>
    </div>
  </div>

  <!-- FIREFOX -->
  <div class="panel" id="tab-firefox">
    <div class="warn">Firefox 128+ қажет. Тұрақты нұсқа: 2026 шілдесінде Mozilla Add-ons-қа жіберіледі.</div>
    <div class="step">
      <div class="step-num">1</div>
      <div class="step-body">
        <h3>Firefox ZIP жүктеу</h3>
        <p>Firefox-қа арналған пакетті жүктеңіз:</p>
        <a class="dl-btn" href="https://github.com/Kennurken/qalqan-ai/raw/master/qalqan-ai-firefox-v5.1.0.zip">qalqan-ai-firefox-v5.1.0.zip</a>
      </div>
    </div>
    <div class="step">
      <div class="step-num">2</div>
      <div class="step-body">
        <h3>about:debugging ашу</h3>
        <p>Firefox мекенжай жолына <code>about:debugging</code> теріңіз</p>
      </div>
    </div>
    <div class="step">
      <div class="step-num">3</div>
      <div class="step-body">
        <h3>Load Temporary Add-on</h3>
        <p><b>This Firefox</b> → <b>Load Temporary Add-on</b> → жүктелген ZIP файлын таңдаңыз</p>
      </div>
    </div>
    <div class="step">
      <div class="step-num">4</div>
      <div class="step-body">
        <h3>Дайын!</h3>
        <p>Расширение жұмыс істейді. Firefox қайта іске қосылғанда қайта жүктеу керек (уақытша режим).</p>
      </div>
    </div>
  </div>
</div>

<script>
function showTab(name, el) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('tab-' + name).classList.add('active');
}
</script>
</body></html>"""


# ── Telegram Mini App (Web App) ───────────────────────────────────────────────
MINIAPP_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
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
</style>
</head>
<body>
<div class="hd"><span class="logo">🛡️</span><h1>Qalqan AI</h1></div>

<div class="tabs">
  <div class="tab on" data-p="check">🔍 Тексеру</div>
  <div class="tab" data-p="ask">🤖 AI-кеңес</div>
  <div class="tab" data-p="map">🗺️ Карта</div>
</div>

<div class="panel on" id="p-check">
  <input id="url" placeholder="kaspi-bonus.kz немесе https://..." autocapitalize="off" autocomplete="off">
  <button class="btn" id="btn-check">Тексеру</button>
  <div class="hint">Сілтемені қой — фишинг, клон, гемблингті тексеремін</div>
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
  <div class="kzmap" id="kzmap"></div>
</div>

<script>
const tg = window.Telegram?.WebApp;
if (tg) { tg.ready(); tg.expand(); }
const API = location.origin;
const $ = s => document.querySelector(s);
const vcolor = v => v==='DANGEROUS'?'var(--red)':v==='SUSPICIOUS'?'var(--amber)':'var(--green)';
const vlabel = v => v==='DANGEROUS'?'🔴 ҚАУІПТІ':v==='SUSPICIOUS'?'🟡 КҮДІКТІ':'🟢 ҚАУІПСІЗ';

document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{
  document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));
  document.querySelectorAll('.panel').forEach(x=>x.classList.remove('on'));
  t.classList.add('on'); $('#p-'+t.dataset.p).classList.add('on');
  if(t.dataset.p==='map') loadMap();
});

async function check(){
  const url=$('#url').value.trim(); if(!url) return;
  const box=$('#res-check'); box.className='res show'; box.innerHTML='<div class="spin">Тексерілуде...</div>';
  try{
    const r=await fetch(API+'/check',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url,lang:'kk'})});
    const d=await r.json();
    const v=d.verdict, sc=d.threat_score||0;
    box.innerHTML=`<div class="verdict" style="color:${vcolor(v)}">${vlabel(v)}</div>
      <div class="score">${sc}/100 · ${d.source||''}</div>
      <div class="bar"><div style="width:${sc}%;background:${vcolor(v)}"></div></div>
      <div class="detail">${d.detail_kk||d.detail||''}</div>`;
    if(tg) tg.HapticFeedback?.notificationOccurred(v==='DANGEROUS'?'error':v==='SAFE'?'success':'warning');
  }catch(e){ box.innerHTML='<div class="spin">Қате. Кейінірек қайталаңыз.</div>'; }
}
$('#btn-check').onclick=check;
$('#url').addEventListener('keydown',e=>{if(e.key==='Enter')check();});

async function ask(){
  const t=$('#situation').value.trim(); if(t.length<10) return;
  const box=$('#res-ask'); box.className='res show'; box.innerHTML='<div class="spin">AI талдап жатыр...</div>';
  try{
    const r=await fetch(API+'/advisor',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t,lang:'ru'})});
    const d=await r.json();
    const v=d.verdict, sc=d.threat_score||0;
    let h=`<div class="verdict" style="color:${vcolor(v)}">${vlabel(v)}</div>
      <div class="score">${sc}/100 · ${d.scam_type||''}</div>
      <div class="bar"><div style="width:${sc}%;background:${vcolor(v)}"></div></div>
      <div class="detail">${d.reasoning||d.detail_ru||''}</div>`;
    if((d.advice||[]).length) h+='<div class="meta">✅ '+d.advice.slice(0,4).map(a=>a).join('<br>✅ ')+'</div>';
    box.innerHTML=h;
  }catch(e){ box.innerHTML='<div class="spin">Қате. Кейінірек қайталаңыз.</div>'; }
}
$('#btn-ask').onclick=ask;

let mapLoaded=false;
async function loadMap(){
  if(mapLoaded) return; mapLoaded=true;
  try{
    const d=await (await fetch(API+'/dashboard/data?demo=1')).json();
    const k=d.kpis||{};
    $('#kpis').innerHTML=
      `<div class="kpi"><div class="v" style="color:var(--cyan)">${(k.total_checks||0).toLocaleString()}</div><div class="l">Тексерілді</div></div>`+
      `<div class="kpi"><div class="v" style="color:var(--red)">${(k.threats_blocked||0).toLocaleString()}</div><div class="l">Қауіп</div></div>`;
    const reg=d.regions||{}; const mx=Math.max(1,...Object.values(reg).map(r=>r.threats||0));
    const top=Object.entries(reg).sort((a,b)=>(b[1].threats||0)-(a[1].threats||0)).slice(0,12);
    $('#kzmap').innerHTML=top.map(([nm,r])=>{
      const f=Math.min(1,(r.threats||0)/mx);
      const c=`rgb(${Math.round(13+(255-13)*f)},${Math.round(20+(59-20)*f)},${Math.round(36+(92-36)*f)})`;
      return `<div class="kzt" style="background:${c};color:${f>.45?'#fff':'#e7ebf3'}">${nm}<b>${r.threats||0}</b></div>`;
    }).join('');
  }catch(e){ $('#kzmap').innerHTML='<div class="spin">Қате</div>'; }
}
</script>
</body></html>"""


GRAPH_HTML = """<!DOCTYPE html>
<html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
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
</style></head><body>
<div class="top">
  <div><h1>🕸️ Граф госзакупок — аффилированность и сговор</h1>
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
  <div class="card"><h3 style="font-size:14px;margin-bottom:12px">🚩 Найденные схемы</h3><div id="findings"></div></div>
</div>
<div class="foot">Qalqan AI · граф строится из данных закупок (заказчик↔поставщик↔учредитель↔адрес↔чиновник)</div>
<script>
const COL={customer:'#7aa2f7',supplier:'#bb9af7',founder:'#e0af68',address:'#9ece6a',official:'#f7768e'};
fetch('/goszakup/graph/demo').then(r=>r.json()).then(render).catch(()=>{document.getElementById('findings').textContent='Ошибка загрузки';});
function render(g){
  document.getElementById('src').textContent = (g._source==='demo'?'демо-сценарий':'данные');
  const W=900,H=600,nodes=g.nodes,edges=g.edges;
  nodes.forEach((n,i)=>{const a=i/nodes.length*6.283; n.x=W/2+Math.cos(a)*200; n.y=H/2+Math.sin(a)*170; n.vx=0;n.vy=0;});
  const by=Object.fromEntries(nodes.map(n=>[n.id,n]));
  for(let it=0;it<320;it++){
    for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++){
      const a=nodes[i],b=nodes[j];let dx=a.x-b.x,dy=a.y-b.y,d=Math.hypot(dx,dy)||1,f=2600/(d*d);
      a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;}
    edges.forEach(e=>{const a=by[e.source],b=by[e.target];if(!a||!b)return;let dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1,f=(d-95)*0.02;a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;});
    nodes.forEach(n=>{n.vx+=(W/2-n.x)*0.002;n.vy+=(H/2-n.y)*0.002;n.x+=Math.max(-8,Math.min(8,n.vx));n.y+=Math.max(-8,Math.min(8,n.vy));n.vx*=0.84;n.vy*=0.84;n.x=Math.max(40,Math.min(W-40,n.x));n.y=Math.max(34,Math.min(H-24,n.y));});
  }
  let s='';
  edges.forEach(e=>{const a=by[e.source],b=by[e.target];if(!a||!b)return;const c=e.risk?'#f7768e':'#334155';
    s+=`<line x1="${a.x.toFixed(1)}" y1="${a.y.toFixed(1)}" x2="${b.x.toFixed(1)}" y2="${b.y.toFixed(1)}" stroke="${c}" stroke-width="${e.risk?2.6:1}" ${e.risk?'stroke-dasharray="5 3"':''}/>`;});
  nodes.forEach(n=>{const c=COL[n.type]||'#888',r=(n.type==='customer'||n.type==='supplier')?13:8;
    s+=`<circle cx="${n.x.toFixed(1)}" cy="${n.y.toFixed(1)}" r="${r}" fill="${c}" stroke="${n.risk?'#f7768e':'#0a0e16'}" stroke-width="${n.risk?3:1.5}"/>`;
    s+=`<text x="${n.x.toFixed(1)}" y="${(n.y-r-5).toFixed(1)}" fill="#e7ebf3" font-size="10" text-anchor="middle">${(n.label||'').slice(0,22)}</text>`;});
  document.getElementById('graph').innerHTML=s;
  let f=`<div class="risk">Риск: <b>${g.risk_score}/100</b> · <span class="${g.verdict}">${g.verdict}</span></div>`;
  f+=(g.findings||[]).map(x=>`<div class="finding"><span class="sc">+${x.score}</span><span>${x.ru}</span></div>`).join('');
  document.getElementById('findings').innerHTML=f;
}
</script></body></html>"""


# ── Mobile PWA app shell (installable, offline-capable) ──────────────────────
MOBILE_HTML = """<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="utf-8">
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
</style></head>
<body>
<header>
  <div class="logo">🛡 Qalqan AI</div>
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

<script>
const $=s=>document.querySelector(s);
const API=location.origin;
let offlineDomains=new Set();

// tabs
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('nav button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('on'));
  $('#p-'+b.dataset.t).classList.add('on');
  if(b.dataset.t==='map')loadMap();
  if(b.dataset.t==='hist')renderHist();
});

// online/offline
function netState(){const on=navigator.onLine;const el=$('#net');el.classList.toggle('off',!on);$('#nett').textContent=on?'онлайн':'офлайн';}
addEventListener('online',netState);addEventListener('offline',netState);netState();

// history
function getHist(){try{return JSON.parse(localStorage.getItem('qh')||'[]')}catch(e){return[]}}
function pushHist(u,v,s){const h=getHist();h.unshift({u,v,s,t:Date.now()});localStorage.setItem('qh',JSON.stringify(h.slice(0,30)));}
function vcolor(v){return v==='DANGEROUS'?'#f7768e':v==='SUSPICIOUS'?'#e0af68':'#9ece6a'}
function renderHist(){const h=getHist();$('#hist').innerHTML=h.length?h.map(x=>`<div class="hist"><span class="u">${x.u}</span><span style="display:flex;gap:7px;align-items:center"><b style="color:${vcolor(x.v)}">${x.s}</b><span class="dot2" style="background:${vcolor(x.v)}"></span></span></div>`).join(''):'<div class="muted">Тексерулер әзірге жоқ</div>';}

function showRes(el,v,score,detail,flags){
  el.className='res show '+v;
  let h=`<div class="verdict">${v==='DANGEROUS'?'🛑':v==='SUSPICIOUS'?'⚠️':'✅'} ${v}</div><div class="score">Қауіп: ${score}/100</div><div class="detail">${detail||''}</div>`;
  if(flags&&flags.length)h+='<div class="flags">'+flags.slice(0,5).map(f=>`<div class="flag">• ${f}</div>`).join('')+'</div>';
  el.innerHTML=h;
}

// URL check
$('#btn-check').onclick=async()=>{
  const url=$('#url').value.trim(); if(!url)return;
  const btn=$('#btn-check'),el=$('#r-check'); btn.disabled=true; btn.innerHTML='<span class="spin"></span>';
  try{
    if(!navigator.onLine){
      const d=(url.replace(/^https?:\\/\\//,'').split('/')[0]||'').toLowerCase();
      const bad=[...offlineDomains].some(x=>d===x||d.endsWith('.'+x));
      showRes(el,bad?'DANGEROUS':'SAFE',bad?90:0,bad?'Офлайн базада қауіпті деп тіркелген':'Офлайн базада жоқ (интернетсіз тексеру шектеулі)');
    }else{
      const isPhone=/^[\\d\\s+()-]{9,18}$/.test(url) && url.replace(/\\D/g,'').length>=10;
      const ep=isPhone?'/phone':'/check';
      const body=isPhone?{phone:url,lang:'kk'}:{url,lang:'kk'};
      const r=await fetch(API+ep,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      const d=await r.json();
      showRes(el,d.verdict,d.threat_score,d.detail||d.detail_kk,(d.indicators||[]));
      pushHist(isPhone?(d.formatted||url):url,d.verdict,d.threat_score);
    }
  }catch(e){showRes(el,'SUSPICIOUS',50,'Қате: '+e.message);}
  btn.disabled=false; btn.textContent='Тексеру';
};

// AI advisor
$('#btn-ai').onclick=async()=>{
  const text=$('#sit').value.trim(); if(text.length<10){return;}
  const btn=$('#btn-ai'),el=$('#r-ai'); btn.disabled=true; btn.innerHTML='<span class="spin"></span>';
  try{
    const r=await fetch(API+'/advisor',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text,lang:'kk'})});
    const d=await r.json();
    const flags=(d.red_flags||d.indicators||[]).map(f=>typeof f==='string'?f:(f.kk||f.ru||f.text||''));
    showRes(el,d.verdict||'SUSPICIOUS',d.threat_score||d.score||50,d.advice||d.reasoning||d.detail||'',flags);
  }catch(e){showRes(el,'SUSPICIOUS',50,'Қате: '+e.message);}
  btn.disabled=false; btn.textContent='Талдау';
};

// map
let mapLoaded=false;
async function loadMap(){
  if(mapLoaded)return; mapLoaded=true;
  try{
    const d=await (await fetch(API+'/dashboard/data?demo=1')).json();
    const reg=Object.entries(d.regions||{}).sort((a,b)=>b[1].threats-a[1].threats).slice(0,12);
    const mx=Math.max(1,...reg.map(r=>r[1].threats));
    $('#regions').innerHTML=reg.map(([n,r])=>`<div class="region"><span class="nm">${n}</span><span class="tk"><span class="fl" style="width:${Math.round(100*r.threats/mx)}%"></span></span><span class="vv">${r.threats}</span></div>`).join('');
  }catch(e){$('#regions').innerHTML='<div class="muted">Картаны жүктеу қатесі</div>';}
}

// offline-db cache
fetch(API+'/offline-db').then(r=>r.json()).then(d=>{
  const s=new Set();
  Object.values(d).forEach(v=>{if(Array.isArray(v))v.forEach(x=>typeof x==='string'&&s.add(x.toLowerCase()));});
  offlineDomains=s; localStorage.setItem('qodb',JSON.stringify([...s].slice(0,5000)));
}).catch(()=>{try{offlineDomains=new Set(JSON.parse(localStorage.getItem('qodb')||'[]'))}catch(e){}});

// install prompt
let deferred;
addEventListener('beforeinstallprompt',e=>{e.preventDefault();deferred=e;$('#install').style.display='block';});
$('#install').onclick=async()=>{if(!deferred)return;deferred.prompt();await deferred.userChoice;deferred=null;$('#install').style.display='none';};

// service worker
if('serviceWorker' in navigator)navigator.serviceWorker.register('/sw.js').catch(()=>{});
</script>
</body></html>"""


SW_JS = """const CACHE='qalqan-pwa-v1';
const SHELL=['/m','/manifest.webmanifest'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(Promise.all([
  caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))),
  self.clients.claim()
]));});
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  const u=new URL(e.request.url);
  if(u.pathname==='/m'||u.pathname==='/manifest.webmanifest'){
    e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(resp=>{const cp=resp.clone();caches.open(CACHE).then(c=>c.put(e.request,cp));return resp;})));
    return;
  }
  if(u.pathname==='/offline-db'){
    e.respondWith(fetch(e.request).then(resp=>{const cp=resp.clone();caches.open(CACHE).then(c=>c.put(e.request,cp));return resp;}).catch(()=>caches.match(e.request)));
  }
});
"""


# ── Partner (B2G) API docs page ──────────────────────────────────────────────
PARTNERS_HTML = """<!DOCTYPE html>
<html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Qalqan AI — Партнёрский API (B2G)</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0e16;--panel:#111827;--bd:#1e293b;--tx:#e7ebf3;--mut:#8194ad;--cyan:#7aa2f7;--green:#9ece6a}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:24px;max-width:860px;margin:0 auto;line-height:1.6}
a{color:var(--cyan);text-decoration:none}
h1{font-size:26px;font-weight:800;margin-bottom:4px}
.sub{color:var(--mut);margin-bottom:24px}
h2{font-size:17px;margin:26px 0 10px;border-left:3px solid var(--cyan);padding-left:10px}
.card{background:var(--panel);border:1px solid var(--bd);border-radius:12px;padding:16px;margin-bottom:14px}
table{width:100%;border-collapse:collapse;font-size:14px}
th,td{text-align:left;padding:9px 8px;border-bottom:1px solid var(--bd)}
th{color:var(--mut);font-size:12px;text-transform:uppercase}
code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
code{background:#0d1424;padding:2px 6px;border-radius:5px;color:var(--cyan);font-size:13px}
pre{background:#0d1424;border:1px solid var(--bd);border-radius:10px;padding:14px;overflow-x:auto;font-size:13px;color:#cbd5e1;margin:8px 0}
.method{color:var(--green);font-weight:700}
.tag{display:inline-block;font-size:11px;font-weight:700;color:#06121a;background:var(--cyan);padding:3px 9px;border-radius:999px}
.foot{color:var(--mut);font-size:12px;margin-top:30px;text-align:center}
</style></head><body>
<h1>🛡 Qalqan AI — Партнёрский API <span class="tag">B2G</span></h1>
<div class="sub">Для банков, Антифрод-центра Нацбанка, KZ-CERT, АФМ. Проверка угроз в реальном времени.</div>

<h2>Авторизация</h2>
<div class="card">Все запросы — с заголовком <code>X-API-Key: &lt;ваш ключ&gt;</code>.<br>
Демо-ключ (ограниченный): <code>qalqan-demo-2026</code>. Боевой ключ — по запросу.</div>

<h2>Эндпоинты</h2>
<div class="card"><table>
<tr><th>Метод</th><th>Путь</th><th>Назначение</th></tr>
<tr><td><span class="method">POST</span></td><td><code>/v1/check</code></td><td>Проверка одного URL</td></tr>
<tr><td><span class="method">POST</span></td><td><code>/v1/batch</code></td><td>Пакетная проверка URL</td></tr>
<tr><td><span class="method">GET</span></td><td><code>/v1/feed</code></td><td>Полный KZ threat-feed</td></tr>
<tr><td><span class="method">GET</span></td><td><code>/v1/usage</code></td><td>Счётчик запросов вашего ключа</td></tr>
</table></div>

<h2>Пример — проверка URL</h2>
<pre>curl -X POST https://qalqan-ai-nu.vercel.app/v1/check \\
  -H "X-API-Key: qalqan-demo-2026" \\
  -H "Content-Type: application/json" \\
  -d '{"url":"kaspi-bonus123.kz","lang":"ru"}'</pre>
<pre>{
  "partner": "Demo (rate-limited)",
  "request_id": "a1b2c3d4e5f6...",
  "result": { "verdict": "DANGEROUS", "threat_score": 95, ... }
}</pre>

<h2>Лимиты</h2>
<div class="card">Демо-ключ: <b>30 запросов/мин</b>. Партнёрский ключ: <b>600/мин</b> (настраивается).<br>
Ответ <code>429</code> при превышении.</div>

<h2>Получить боевой ключ</h2>
<div class="card">Напишите на <a href="mailto:kmarukob76@gmail.com">kmarukob76@gmail.com</a> с указанием организации.
Ключ выдаётся под конкретного партнёра, лимиты и логирование — индивидуально.</div>

<div class="foot">Qalqan AI · Республиканский конкурс ДЭР 2026 · <a href="/">главная</a> · <a href="/dashboard">панель</a></div>
</body></html>"""


# ── Branded 404 page ─────────────────────────────────────────────────────────
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
</style></head>
<body>
<div class="bg"></div>
<div>
<svg class="shield" viewBox="0 0 24 24" fill="none"><path d="M12 2 4 5v6c0 5 3.4 8.6 8 10 4.6-1.4 8-5 8-10V5z" stroke="url(#g)" stroke-width="1.4" fill="rgba(122,162,247,.1)"/><defs><linearGradient id="g" x1="4" y1="2" x2="20" y2="22"><stop stop-color="#7aa2f7"/><stop offset="1" stop-color="#6ee7d3"/></linearGradient></defs></svg>
<div class="code">404</div>
<h1>Бет табылмады</h1>
<p>Бұл сілтеме жоқ немесе жылжытылған. Бастапқы бетке оралыңыз.</p>
<a class="btn" href="/">← Басты бетке</a>
<div class="links"><a href="/dashboard?demo=1">Панель</a>·<a href="/m">Мобилка</a>·<a href="https://t.me/QalqanAI_bot">Бот</a></div>
</div>
</body></html>"""
