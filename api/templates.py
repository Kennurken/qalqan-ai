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
<meta property="og:description" content="Бесплатно: блокирует фишинг, пирамиды, гемблинг, телефонный скам и госзакуп-фрод. Расширение + мобилка + Telegram-бот + дашборд регулятора. 7-уровневый AI.">
<meta property="og:url" content="https://qalqan-ai-nu.vercel.app">
<meta property="og:type" content="website">
<meta property="og:image" content="https://raw.githubusercontent.com/Kennurken/qalqan-ai/master/extension/public/icons/icon128.png">
<meta property="og:locale" content="kk_KZ">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Qalqan AI — AI Cybersecurity for Kazakhstan">
<meta name="twitter:description" content="Blocks phishing, scams, gambling, phone fraud & procurement fraud. Extension + mobile + bot + regulator dashboard. 7-tier AI. kk/ru/en.">
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
body{background:var(--bg);color:var(--text);overflow-x:clip;font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.6;overflow-x:hidden;-webkit-font-smoothing:antialiased;letter-spacing:-.011em}
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
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 4px}
.chip{font-size:12.5px;font-weight:600;color:var(--text2);border:1px solid var(--line);border-radius:999px;padding:7px 13px;transition:all .2s var(--ease)}
.proof{margin:14px 0 2px;font-size:13px;font-weight:600;color:var(--accent);opacity:.92}
.livewrap{display:inline-flex;align-items:center;gap:8px;margin-top:14px;font-size:12.5px;color:var(--text2);background:rgba(247,118,142,.06);border:1px solid rgba(247,118,142,.18);border-radius:999px;padding:6px 14px}
.livedot{width:7px;height:7px;border-radius:50%;background:#f7768e;box-shadow:0 0 0 0 rgba(247,118,142,.6);animation:livep 2s infinite}
@keyframes livep{0%{box-shadow:0 0 0 0 rgba(247,118,142,.5)}70%{box-shadow:0 0 0 7px rgba(247,118,142,0)}100%{box-shadow:0 0 0 0 rgba(247,118,142,0)}}
.chip:hover{color:var(--text);border-color:var(--accent)}
.hero{padding:170px 0 80px;text-align:center;position:relative}
.badge{display:inline-flex;align-items:center;gap:7px;font-size:12.5px;color:var(--text2);background:var(--surface);border:1px solid var(--border);padding:6px 14px;border-radius:999px;margin-bottom:26px}
.badge .dot{width:7px;height:7px;border-radius:50%;background:var(--ok);box-shadow:0 0 0 3px rgba(158,206,106,.18)}
h1{font-size:clamp(40px,7vw,76px);font-weight:800;line-height:1.04;letter-spacing:-.035em;margin-bottom:22px}
h1 .grad{color:var(--accent)}
@keyframes shimmer{to{background-position:220% center}}
.lead{font-size:clamp(16px,2.2vw,20px);color:var(--text2);max-width:620px;margin:0 auto 38px;line-height:1.6}
.checker{max-width:560px;margin:0 auto;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:10px;display:flex;gap:9px;box-shadow:0 24px 60px -20px rgba(0,0,0,.6);transition:border-color .3s var(--ease)}
.checker:focus-within{border-color:var(--border2)}
.checker input{flex:1;min-width:0;background:transparent;border:none;outline:none;color:var(--text);font-size:15.5px;padding:13px 16px;font-family:inherit}
.checker input::placeholder{color:var(--muted)}
.checker button{background:linear-gradient(135deg,var(--accent),#5b87e8);color:#06101f;border:none;font-weight:700;font-size:14.5px;padding:0 24px;border-radius:12px;cursor:pointer;font-family:inherit;transition:transform .25s var(--ease),box-shadow .25s var(--ease)}
.checker button:hover{transform:translateY(-1px);box-shadow:0 10px 28px rgba(122,162,247,.35)}
.checker button:disabled{opacity:.6;cursor:default;transform:none}
@media(max-width:430px){nav .logo{font-size:15px}nav{gap:8px}.checker{gap:6px;padding:8px}.checker button{padding:0 14px;font-size:13.5px}.checker input{padding:11px 10px;font-size:14px}.checker #qrBtn{padding:0 10px}}

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
.pipe{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:8px;position:relative}
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
@media(max-width:560px){.lang button{padding:8px 7px;font-size:11px}}
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
.checker #qrBtn{border:1px solid var(--bd,#1e293b);background:transparent;color:inherit;border-radius:12px;padding:0 14px;font-size:18px;cursor:pointer}
.checker #qrBtn:hover{border-color:#7aa2f7}
.qi{width:1em;height:1em;vertical-align:-0.14em;display:inline-block}
:focus-visible{outline:2px solid #7aa2f7;outline-offset:2px;border-radius:4px}
::selection{background:rgba(122,162,247,.32)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
*{scrollbar-width:thin;scrollbar-color:#2a3550 transparent}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-thumb{background:#2a3550;border-radius:5px}::-webkit-scrollbar-track{background:transparent}
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
      <a href="/dashboard" data-i18n="n_map"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Карта</a>
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
      <button id="qrBtn" type="button" title="Проверить QR-код" aria-label="QR тексеру"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg></button>
      <button id="checkBtn" data-i18n="checkBtn">Тексеру</button>
      <input id="qrFile" type="file" accept="image/*" capture="environment" style="display:none">
    </div>
    <div class="result" id="resultBox"><div class="rv" id="resultVerdict"></div><div class="rd" id="resultDetail"></div></div>
    <div class="proof reveal" data-i18n="proof"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> 97% дәлдік · 0 жалған дабыл · ашық бенчмаркте (F1 0.98)</div>
    <div class="chips reveal">
      <a class="chip" href="/leak" data-i18n="chip_leak"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> Пароль утёк?</a>
      <a class="chip" href="/dashboard" data-i18n="chip_map"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Карта угроз</a>
      <a class="chip" href="/scan"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 1 0 0-14h-1"/><path d="M9 14h2"/><path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z"/><path d="M12 6V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3"/></svg> Оценка сайта</a>
      <a class="chip" href="/brand"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> Защита бренда</a>
      <a class="chip" href="/screen"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg> Скриншот-тест</a>
      <a class="chip" href="/help"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m4.93 19.07 4.24-4.24"/></svg> Обманули?</a>
      <a class="chip" href="/impact"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01"/><path d="M18 12h.01"/></svg> Эконом-эффект</a>
      <a class="chip" href="https://t.me/QalqanAI_bot"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="8" width="16" height="12" rx="2"/><path d="M12 8V4"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg> Telegram-бот</a>
    </div>
    <div class="stats reveal">
      <div class="stat"><div class="n" id="statChecked" data-to="0">—</div><div class="l" data-i18n="st_checked">Тексерілді</div></div>
      <div class="stat"><div class="n" id="statBlocked" data-to="0">—</div><div class="l" data-i18n="st_blocked">Бұғатталды</div></div>
      <div class="stat"><div class="n" id="statDomains" data-to="390" data-suffix="+">390+</div><div class="l" data-i18n="st_offline">Офлайн база</div></div>
      <div class="stat"><div class="n" data-to="7">7</div><div class="l" data-i18n="st_levels">Деңгей</div></div>
    </div>
    <div class="livewrap reveal" id="livewrap" style="display:none">
      <span class="livedot"></span><span class="livetxt" id="livetxt"></span>
    </div>
  </div>
</header>
<section class="sec" id="problem">
  <div class="wrap">
    <div class="eyebrow reveal" data-i18n="s_prob_e">Неге керек</div>
    <h2 class="stitle reveal" data-i18n="s_prob_t">Қазақстандағы цифрлық алаяқтық</h2>
    <p class="ssub reveal" data-i18n="s_prob_s">2025 жылғы 10 айдағы ресми статистика — масштаб орасан.</p>
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
    <div class="eyebrow reveal" data-i18n="s_feat_e">Функционал</div>
    <h2 class="stitle reveal" data-i18n="s_feat_t">Не қорғайды</h2>
    <p class="ssub reveal" data-i18n="s_feat_s">7-деңгейлі pipeline — 1 мс кэш-тексеруден AI анализіне дейін.</p>
    <div class="bento">
      <div class="card span3 tilt reveal">
        <div class="ic"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg></div>
        <h3 data-i18n="f1t">Фишинг сайттары</h3><p data-i18n="f1d">Kaspi, eGov, Halyk Bank клондарын анықтайды — homoglyph (кириллица әріптерін) және typosquat шабуылдарын қоса. Бет жүктелуіне дейін бұғаттайды.</p>
      </div>
      <div class="card span3 tilt reveal">
        <div class="ic"><svg viewBox="0 0 24 24"><path d="M3 18a9 9 0 0 1 18 0"/><path d="M12 3v3M5 9 7 11M19 9l-2 2"/><circle cx="12" cy="18" r="1.5"/></svg></div>
        <h3 data-i18n="f2t">Телефон алаяқтығы</h3><p data-i18n="f2d">Дауыстық хабарламаны Whisper арқылы транскрипциялап, ҚР скам-паттерндерін табады. #1 қауіп — енді одан қорғаныс бар.</p>
      </div>
      <div class="card span2 tilt reveal">
        <div class="ic"><svg viewBox="0 0 24 24"><polygon points="12 2 15 9 22 9.3 16.5 14 18.5 21 12 17 5.5 21 7.5 14 2 9.3 9 9"/></svg></div>
        <h3 data-i18n="f3t">Қаржылық пирамидалар</h3><p data-i18n="f3d">АФМ реестрі бойынша атау тексеру + Finiko, MMM, HYIP базасы.</p>
      </div>
      <div class="card span2 tilt reveal">
        <div class="ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M5 5l14 14"/></svg></div>
        <h3 data-i18n="f4t">Нелегал гемблинг</h3><p data-i18n="f4d">80+ ҚР-да тыйым салынған сайт. 1xBet, Mostbet — браузерде ашылмайды.</p>
      </div>
      <div class="card span2 tilt reveal">
        <div class="ic"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h4"/></svg></div>
        <h3 data-i18n="f5t">Госзакуп фроды</h3><p data-i18n="f5d">Заказчик↔поставщик↔учредитель граф: аффилированность, сговор, картель.</p>
      </div>
    </div>
  </div>
</section>
<section class="sec" id="pipeline">
  <div class="wrap">
    <div class="eyebrow reveal" data-i18n="s_arch_e">Архитектура</div>
    <h2 class="stitle reveal" data-i18n="s_arch_t">7-деңгейлі анықтау</h2>
    <p class="ssub reveal" data-i18n="s_arch_s">Әр сұраныс жеті қабаттан өтеді — жылдамнан тереңге.</p>
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
    <div class="eyebrow reveal" data-i18n="s_demo_e">Демо</div>
    <h2 class="stitle reveal" data-i18n="s_demo_t">Бәрі тірі — ашып көріңіз</h2>
    <p class="ssub reveal" data-i18n="s_demo_s">Жұмыс істеп тұрған платформалар мен панельдер.</p>
    <div class="bento">
      <a class="card span2 tilt reveal" href="/dashboard?demo=1">
        <div class="ic"><svg viewBox="0 0 24 24"><path d="M3 3v18h18"/><path d="M7 14l3-4 3 2 4-6"/></svg></div>
        <h3 data-i18n="d1t">Реттеуші панелі</h3><p data-i18n="d1d">Облыстар бойынша қауіп картасы, динамика, топ домендер.</p><span class="arrow" data-i18n="arrow">Ашу →</span>
      </a>
      <a class="card span2 tilt reveal" href="/goszakup/graph">
        <div class="ic"><svg viewBox="0 0 24 24"><circle cx="5" cy="6" r="2.5"/><circle cx="19" cy="7" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M7 7l3 9M17 9l-3 7"/></svg></div>
        <h3 data-i18n="d2t">Госзакуп графы</h3><p data-i18n="d2d">Аффилированность, сговор, картель — байланыс графы.</p><span class="arrow" data-i18n="arrow">Ашу →</span>
      </a>
      <a class="card span2 tilt reveal" href="/m">
        <div class="ic"><svg viewBox="0 0 24 24"><rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/></svg></div>
        <h3 data-i18n="d3t">Мобиль қосымша</h3><p data-i18n="d3d">Офлайн жұмыс істейді, телефонға орнатылады (PWA).</p><span class="arrow" data-i18n="arrow">Ашу →</span>
      </a>
      <a class="card span2 tilt reveal" href="https://t.me/QalqanAI_bot" target="_blank" rel="noopener">
        <div class="ic"><svg viewBox="0 0 24 24"><path d="M21 5 3 12l5 2 2 5 3-4 4 3z"/></svg></div>
        <h3 data-i18n="d4t">Telegram бот</h3><p data-i18n="d4d">Дауыс / SMS / сілтеме тексеру, KZ-CERT-ке хабарлау.</p><span class="arrow" data-i18n="arrow">Ашу →</span>
      </a>
      <a class="card span2 tilt reveal" href="/stats">
        <div class="ic"><svg viewBox="0 0 24 24"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg></div>
        <h3 data-i18n="d5t">Тірі статистика</h3><p data-i18n="d5d">Нақты деректер: тексерулер, вердиктер, трендтер.</p><span class="arrow" data-i18n="arrow">Ашу →</span>
      </a>
      <a class="card span2 tilt reveal" href="/feed/kz">
        <div class="ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18"/></svg></div>
        <h3>KZ Threat Feed</h3><p data-i18n="d6d">Ашық дерекқор (CC-BY) — басқа жүйелер пайдалана алады.</p><span class="arrow" data-i18n="arrow">Ашу →</span>
      </a>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="tg reveal">
      <h3 data-i18n="tg_t">Telegram-да тексер</h3>
      <p data-i18n="tg_d">Кез келген сілтемені, нөмірді, дауыстық хабарламаны жіберіп, бірден жауап ал.</p>
      <a class="tg-btn" href="https://t.me/QalqanAI_bot" target="_blank" rel="noopener">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="#0a0e16"><path d="M21 5 3 12l5 2 2 5 3-4 4 3z"/></svg>@QalqanAI_bot ашу
      </a>
    </div>
  </div>
</section>
<section class="sec" id="tech">
  <div class="wrap">
    <div class="eyebrow reveal" data-i18n="s_tech_e">Технологиялар</div>
    <h2 class="stitle reveal" data-i18n="s_tech_t">Стек</h2>
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
    <div class="eyebrow reveal" data-i18n="s_faq_e">Сұрақ-жауап</div>
    <h2 class="stitle reveal" data-i18n="s_faq_t">Жиі қойылатын сұрақтар</h2>
    <p class="ssub reveal" data-i18n="s_faq_s">Нақты жауаптар — артық сөзсіз.</p>
    <div class="faq reveal">
      <details class="fq"><summary><span data-i18n="q1">Тегін бе?</span><i></i></summary><div class="fa">Иә, азаматтарға толық тегін — жасырын ақы жоқ. Монетизация: банк пен реттеушіге арналған B2G API (<code>/v1</code>).</div></details>
      <details class="fq"><summary><span data-i18n="q2">Менің деректерім қауіпсіз бе?</span><i></i></summary><div class="fa">Сілтеме мен IP тек SHA-256 хэш түрінде сақталады — шикі дерек ешқашан жазылмайды. URL query-параметрлері логқа түспейді. Барлық агрегация анонимді.</div></details>
      <details class="fq"><summary><span data-i18n="q3">Қалай жұмыс істейді?</span><i></i></summary><div class="fa">7 деңгейлі pipeline: ақ тізім → Redis кэш → офлайн-база → KZ intel (бренд/пирамида/гемблинг) → сыртқы БД + домен анализі → қоғамдастық + ML → Groq/Gemini AI. Қауіпті сайт бет жүктелмей тұрып бұғатталады.</div></details>
      <details class="fq"><summary><span data-i18n="q4">Қандай қауіптерді анықтайды?</span><i></i></summary><div class="fa">Фишинг (homoglyph/typosquat қоса), телефон/SMS алаяқтығы, қаржы пирамидалары (АФМ реестрі), нелегал гемблинг, госзакуп фроды (граф), дауыс-скам (Whisper). Офлайн-база: 390+ домен, тірі threat-feed: 1800+ домен.</div></details>
      <details class="fq"><summary><span data-i18n="q5">Қай тілдерде?</span><i></i></summary><div class="fa">Қазақша, орысша, ағылшынша — детекция да, түсіндірме де үш тілде.</div></details>
      <details class="fq"><summary><span data-i18n="q6">Интернетсіз жұмыс істей ме?</span><i></i></summary><div class="fa">Иә. Мобиль қосымша (PWA) мен браузер кеңейтімі офлайн-базамен жұмыс істейді — желісіз де негізгі тексеру жүреді.</div></details>
      <details class="fq"><summary><span data-i18n="q7">Банктер/реттеушілер қалай қосыла алады?</span><i></i></summary><div class="fa">B2G API: <code>X-API-Key</code> арқылы <code>/v1/check</code>, <code>/v1/batch</code>, <code>/v1/phone</code>. <code>/v1/contribute</code> арқылы CERT/банктер ортақ қауіп-базасын толтырады (federated).</div></details>
    </div>
  </div>
</section>
<div class="ibanner" id="ibanner" role="dialog" aria-label="Қосымшаны орнату">
  <div><b>Qalqan AI — телефоныңа</b><span class="it">Офлайн жұмыс істейді · PWA</span></div>
  <button class="ib-yes" id="ibYes">Орнату</button>
  <button class="ib-no" id="ibNo" aria-label="Жабу"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg></button>
</div>
<footer>
  <div class="wrap">
    <div class="brand" style="justify-content:center">
      <svg viewBox="0 0 24 24" fill="none"><path d="M12 2 4 5v6c0 5 3.4 8.6 8 10 4.6-1.4 8-5 8-10V5z" stroke="url(#g2)" stroke-width="1.6" fill="rgba(122,162,247,.12)"/><defs><linearGradient id="g2" x1="4" y1="2" x2="20" y2="22"><stop stop-color="#7aa2f7"/><stop offset="1" stop-color="#6ee7d3"/></linearGradient></defs></svg>
      Qalqan AI
    </div>
    <div class="flinks">
      <a href="https://github.com/Kennurken/qalqan-ai" target="_blank" rel="noopener">GitHub</a>
      <a href="/m">Мобилка</a><a href="/scan">Оценка сайта</a><a href="/brand">Защита бренда</a><a href="/help"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m4.93 19.07 4.24-4.24"/></svg> Помощь</a><a href="/leak">Пароль-чек</a><a href="/docs">API</a><a href="/dashboard">Панель</a><a href="/feed/kz">Feed</a><a href="/health">Health</a>
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
 kk:{nav_feat:'Функциялар',nav_arch:'Архитектура',nav_demo:'Демо',nav_tech:'Технологиялар',nav_install:'Орнату',n_map:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Карта',chip_leak:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> Құпиясөз утечкасы',chip_map:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Қауіп картасы',proof:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> 97% дәлдік · 0 жалған дабыл · ашық бенчмаркте (F1 0.98)',
     badge:'v5.1 · Қазақстан үшін · Open source',h1a:'Алаяқтықтан',h1b:'AI қорғанысы',
     lead:'Фишинг, телефон алаяқтығы, қаржылық пирамида, гемблинг және госзакуп фроды — бәрін бет жүктелмей тұрып анықтаймыз. Тегін.',
     checkPh:'kaspi-bonus.kz немесе https://...',checkBtn:'Тексеру',
     st_checked:'Тексерілді',st_blocked:'Бұғатталды',st_offline:'Офлайн база',st_levels:'Деңгей',err:'Қате',errd:'Кейінірек қайталаңыз',
     s_prob_e:'Неге керек',s_prob_t:'Қазақстандағы цифрлық алаяқтық',s_prob_s:'2025 жылғы 10 айдағы ресми статистика — масштаб орасан.',
     s_feat_e:'Функционал',s_feat_t:'Не қорғайды',s_feat_s:'7-деңгейлі pipeline — 1 мс кэш-тексеруден AI анализіне дейін.',
     s_arch_e:'Архитектура',s_arch_t:'7-деңгейлі анықтау',s_arch_s:'Әр сұраныс жеті қабаттан өтеді — жылдамнан тереңге.',
     s_demo_e:'Демо',s_demo_t:'Бәрі тірі — ашып көріңіз',s_demo_s:'Жұмыс істеп тұрған платформалар мен панельдер.',
     s_tech_e:'Технологиялар',s_tech_t:'Стек',s_faq_e:'Сұрақ-жауап',s_faq_t:'Жиі қойылатын сұрақтар',s_faq_s:'Нақты жауаптар — артық сөзсіз.',
     q1:'Тегін бе?',q2:'Менің деректерім қауіпсіз бе?',q3:'Қалай жұмыс істейді?',q4:'Қандай қауіптерді анықтайды?',q5:'Қай тілдерде?',q6:'Интернетсіз жұмыс істей ме?',q7:'Банктер/реттеушілер қалай қосыла алады?',
     f1t:'Фишинг сайттары',f2t:'Телефон алаяқтығы',f3t:'Қаржылық пирамидалар',f4t:'Нелегал гемблинг',f5t:'Госзакуп фроды',
     f1d:'Kaspi, eGov, Halyk Bank клондарын анықтайды — homoglyph (кириллица әріптерін) және typosquat шабуылдарын қоса. Бет жүктелуіне дейін бұғаттайды.',
     f2d:'Дауыстық хабарламаны Whisper арқылы транскрипциялап, ҚР скам-паттерндерін табады. #1 қауіп — енді одан қорғаныс бар.',
     f3d:'АФМ реестрі бойынша атау тексеру + Finiko, MMM, HYIP базасы.',f4d:'80+ ҚР-да тыйым салынған сайт. 1xBet, Mostbet — браузерде ашылмайды.',
     f5d:'Тапсырыс беруші↔жеткізуші↔құрылтайшы граф: аффилированность, сговор, картель.',
     d1t:'Реттеуші панелі',d2t:'Госзакуп графы',d3t:'Мобиль қосымша',d4t:'Telegram бот',d5t:'Тірі статистика',
     d1d:'Облыстар бойынша қауіп картасы, динамика, топ домендер.',d2d:'Аффилированность, сговор, картель — байланыс графы.',d3d:'Офлайн жұмыс істейді, телефонға орнатылады (PWA).',d4d:'Дауыс / SMS / сілтеме тексеру, KZ-CERT-ке хабарлау.',d5d:'Нақты деректер: тексерулер, вердиктер, трендтер.',d6d:'Ашық дерекқор (CC-BY) — басқа жүйелер пайдалана алады.',
     arrow:'Ашу →',tg_t:'Telegram-да тексер',tg_d:'Кез келген сілтемені, нөмірді, дауыстық хабарламаны жіберіп, бірден жауап ал.'},
 ru:{nav_feat:'Функции',nav_arch:'Архитектура',nav_demo:'Демо',nav_tech:'Технологии',nav_install:'Установить',n_map:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Карта',chip_leak:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> Пароль утёк?',chip_map:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Карта угроз',proof:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> 97% точность · 0 ложных срабатываний · открытый бенчмарк (F1 0.98)',
     badge:'v5.1 · Для Казахстана · Open source',h1a:'Защита от',h1b:'мошенников · AI',
     lead:'Фишинг, телефонный скам, финансовые пирамиды, гемблинг и госзакуп-фрод — ловим до загрузки страницы. Бесплатно.',
     checkPh:'kaspi-bonus.kz или https://...',checkBtn:'Проверить',
     st_checked:'Проверено',st_blocked:'Заблокировано',st_offline:'Офлайн-база',st_levels:'Уровней',err:'Ошибка',errd:'Повторите позже',
     s_prob_e:'Зачем нужно',s_prob_t:'Цифровое мошенничество в Казахстане',s_prob_s:'Официальная статистика за 10 месяцев 2025 — масштаб огромен.',
     s_feat_e:'Функционал',s_feat_t:'От чего защищает',s_feat_s:'7-уровневый pipeline — от 1 мс кэша до AI-анализа.',
     s_arch_e:'Архитектура',s_arch_t:'7-уровневое обнаружение',s_arch_s:'Каждый запрос проходит 7 уровней — от быстрого к глубокому.',
     s_demo_e:'Демо',s_demo_t:'Всё вживую — откройте',s_demo_s:'Работающие платформы и панели.',
     s_tech_e:'Технологии',s_tech_t:'Стек',s_faq_e:'Вопрос-ответ',s_faq_t:'Частые вопросы',s_faq_s:'Точные ответы — без воды.',
     q1:'Это бесплатно?',q2:'Мои данные в безопасности?',q3:'Как это работает?',q4:'Какие угрозы детектит?',q5:'На каких языках?',q6:'Работает без интернета?',q7:'Как подключаются банки/регуляторы?',
     f1t:'Фишинговые сайты',f2t:'Телефонное мошенничество',f3t:'Финансовые пирамиды',f4t:'Нелегальный гемблинг',f5t:'Фрод в госзакупках',
     f1d:'Детектит клоны Kaspi, eGov, Halyk Bank — включая homoglyph (кириллица) и typosquat. Блокирует до загрузки страницы.',
     f2d:'Транскрибирует голосовое через Whisper и находит KZ скам-паттерны. Угроза №1 — теперь есть защита.',
     f3d:'Проверка названия по реестру АФМ + база Finiko, MMM, HYIP.',f4d:'80+ запрещённых в РК сайтов. 1xBet, Mostbet — не откроются в браузере.',
     f5d:'Граф заказчик↔поставщик↔учредитель: аффилированность, сговор, картель.',
     d1t:'Панель регулятора',d2t:'Граф госзакупок',d3t:'Мобильное приложение',d4t:'Telegram бот',d5t:'Живая статистика',
     d1d:'Карта угроз по областям, динамика, топ-домены.',d2d:'Аффилированность, сговор, картель — граф связей.',d3d:'Работает офлайн, ставится на телефон (PWA).',d4d:'Голос / SMS / ссылка, сообщение в KZ-CERT.',d5d:'Реальные данные: проверки, вердикты, тренды.',d6d:'Открытая база (CC-BY) — могут использовать другие системы.',
     arrow:'Открыть →',tg_t:'Проверь в Telegram',tg_d:'Отправь любую ссылку, номер или голосовое — получи ответ сразу.'},
 en:{nav_feat:'Features',nav_arch:'Architecture',nav_demo:'Demo',nav_tech:'Tech',nav_install:'Install',n_map:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Map',chip_leak:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> Password leak check',chip_map:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Threat map',proof:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> 97% accuracy · 0 false positives · open benchmark (F1 0.98)',
     badge:'v5.1 · For Kazakhstan · Open source',h1a:'AI shield',h1b:'against scams',
     lead:'Phishing, phone scams, financial pyramids, gambling and procurement fraud — caught before the page loads. Free.',
     checkPh:'kaspi-bonus.kz or https://...',checkBtn:'Check',
     st_checked:'Checked',st_blocked:'Blocked',st_offline:'Offline DB',st_levels:'Tiers',err:'Error',errd:'Try again later',
     s_prob_e:'Why it matters',s_prob_t:'Digital fraud in Kazakhstan',s_prob_s:'Official stats for 10 months of 2025 — the scale is huge.',
     s_feat_e:'Features',s_feat_t:'What it protects',s_feat_s:'7-tier pipeline — from 1ms cache to AI analysis.',
     s_arch_e:'Architecture',s_arch_t:'7-tier detection',s_arch_s:'Every request passes 7 tiers — fast to deep.',
     s_demo_e:'Demo',s_demo_t:'All live — open it',s_demo_s:'Working platforms and dashboards.',
     s_tech_e:'Technology',s_tech_t:'Stack',s_faq_e:'FAQ',s_faq_t:'Frequently asked',s_faq_s:'Precise answers — no fluff.',
     q1:'Is it free?',q2:'Is my data safe?',q3:'How does it work?',q4:'What threats does it detect?',q5:'Which languages?',q6:'Does it work offline?',q7:'How can banks/regulators integrate?',
     f1t:'Phishing sites',f2t:'Phone scams',f3t:'Financial pyramids',f4t:'Illegal gambling',f5t:'Procurement fraud',
     f1d:'Detects Kaspi, eGov, Halyk Bank clones — incl. homoglyph (Cyrillic) and typosquat. Blocks before the page loads.',
     f2d:'Transcribes voice via Whisper and finds KZ scam patterns. The #1 threat — now defended.',
     f3d:'Name lookup against the AFM registry + Finiko, MMM, HYIP database.',f4d:'80+ banned-in-KZ sites. 1xBet, Mostbet are blocked in the browser.',
     f5d:'Customer↔supplier↔founder graph: affiliation, collusion, cartel.',
     d1t:'Regulator dashboard',d2t:'Procurement graph',d3t:'Mobile app',d4t:'Telegram bot',d5t:'Live stats',
     d1d:'Regional threat map, trends, top domains.',d2d:'Affiliation, collusion, cartel — relationship graph.',d3d:'Works offline, installs on your phone (PWA).',d4d:'Voice / SMS / link check, report to KZ-CERT.',d5d:'Real data: checks, verdicts, trends.',d6d:'Open dataset (CC-BY) — usable by other systems.',
     arrow:'Open →',tg_t:'Check in Telegram',tg_d:'Send any link, number or voice message — get an answer instantly.'}
};
/* Default for the KZ audience: honor a saved choice, else browser lang only if it's
   kk/ru, otherwise fall back to ru (universally understood here) — never surprise a
   Kazakh jury with an English page just because the demo laptop's locale is en. */
let _nav=(navigator.language||'').slice(0,2).toLowerCase();
let currentLang=localStorage.getItem('qlang')||(['kk','ru'].includes(_nav)?_nav:'ru');
if(!I18N[currentLang])currentLang='ru';
function applyLang(l){
  currentLang=I18N[l]?l:'kk'; localStorage.setItem('qlang',currentLang);
  const D=I18N[currentLang];
  document.querySelectorAll('[data-i18n]').forEach(el=>{const v=D[el.dataset.i18n];if(v!=null)el.innerHTML=v;});
  document.querySelectorAll('[data-i18n-ph]').forEach(el=>{const v=D[el.dataset.i18nPh];if(v!=null)el.placeholder=v;});
  document.documentElement.lang=currentLang;
  document.querySelectorAll('#langSw button').forEach(b=>b.classList.toggle('on',b.dataset.lang===currentLang));
}
document.querySelectorAll('#langSw button').forEach(b=>b.addEventListener('click',()=>applyLang(b.dataset.lang)));
applyLang(currentLang);

const box=$('#resultBox'),verdict=$('#resultVerdict'),detail=$('#resultDetail'),btn=$('#checkBtn'),input=$('#urlInput');
// Context-menu / deep-link entry: /?check=<url> pre-fills and runs the checker.
try{
  const _q=new URLSearchParams(location.search).get('check');
  if(_q){ input.value=_q.slice(0,2048); setTimeout(()=>btn.click(),600);
          window.scrollTo({top:0}); }
}catch(e){}
async function runCheck(){
  const url=input.value.trim(); if(!url)return;
  btn.disabled=true; const old=btn.textContent; btn.textContent='...';
  try{
    const res=await fetch('/check',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url,lang:currentLang})});
    // NEVER fail-open: 429/403/500 must not render as an empty "<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg> 0/100" verdict
    if(res.status===429){
      box.className='result show SUSPICIOUS';
      verdict.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>  '+(currentLang==='kk'?'Тым көп сұраныс — 1 минуттан кейін қайталаңыз':currentLang==='en'?'Too many requests — retry in a minute':'Слишком много запросов — повторите через минуту');
      detail.textContent='';
      btn.disabled=false; btn.textContent=old; return;
    }
    if(!res.ok) throw new Error('http '+res.status);
    const d=await res.json();
    if(!d.verdict) throw new Error('bad payload');
    box.className='result show '+d.verdict;
    const ic=d.verdict==='DANGEROUS'?'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.86 2h8.28L22 7.86v8.28L16.14 22H7.86L2 16.14V7.86z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>':d.verdict==='SUSPICIOUS'?'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>':'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';
    verdict.textContent=ic+'  '+d.verdict+' · '+(d.threat_score||0)+'/100';
    detail.textContent=d.detail||d['detail_'+currentLang]||d.detail_kk||'';
  }catch(e){box.className='result show SUSPICIOUS';verdict.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>  '+I18N[currentLang].err;detail.textContent=I18N[currentLang].errd;}
  btn.disabled=false; btn.textContent=old;
}
btn.addEventListener('click',runCheck);
input.addEventListener('keydown',e=>{if(e.key==='Enter')runCheck()});
// /trends is where total_checks + verdict_distribution actually live (/stats has neither)
fetch('/trends').then(r=>r.json()).then(t=>{
  const set=(id,v)=>{const el=document.getElementById(id);if(el&&v!=null){el.dataset.to=v;countUp(el)}};
  const dist=t.verdict_distribution||{};
  const checks=t.total_checks||0;
  set('statChecked',checks);
  set('statBlocked',(dist.DANGEROUS||0)+(dist.SUSPICIOUS||0));
  // Live pilot ticker: most-reported domain from real crowd data (only when we have activity)
  const rep=(t.top_reported_domains||[]);
  if(checks>0){
    const L={kk:'Соңғы бұғатталған қауіп: ',ru:'Недавно заблокировано: ',en:'Recently blocked: '}[currentLang]||'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#f7768e"/></svg> ';
    const dom=rep.length?rep[0].domain:null;
    const w=document.getElementById('livewrap'), tx=document.getElementById('livetxt');
    if(w&&tx){ tx.textContent = dom ? (L+dom) : ({kk:'Пилот белсенді — нақты уақыттағы қорғаныс',ru:'Пилот активен — защита в реальном времени',en:'Pilot live — real-time protection'}[currentLang]||''); w.style.display='inline-flex'; }
  }
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

<script>
// ── QR check on web: decode an uploaded/captured QR image → run the URL checker.
//    BarcodeDetector (Chrome/Android native) → jsQR CDN fallback (Safari/Firefox).
(function(){
const F=document.getElementById('qrFile');
document.getElementById('qrBtn').onclick=()=>F.click();
function note(t){const rb=document.getElementById('resultBox'),rv=document.getElementById('resultVerdict');rb.className='result show';rv.textContent=t;document.getElementById('resultDetail').textContent='';}
async function toBitmap(file){return await createImageBitmap(file)}
async function decodeNative(bmp){
  if(!('BarcodeDetector' in window))return null;
  try{const det=new BarcodeDetector({formats:['qr_code']});const codes=await det.detect(bmp);return codes.length?codes[0].rawValue:null}catch(e){return null}
}
function loadJsQR(){return new Promise((res,rej)=>{
  if(window.jsQR)return res();
  const sc=document.createElement('script');sc.src='https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js';
  sc.onload=res;sc.onerror=rej;document.head.appendChild(sc);})}
async function decodeFallback(bmp){
  await loadJsQR();
  const c=document.createElement('canvas');const MAX=1200;
  const sc=Math.min(1,MAX/Math.max(bmp.width,bmp.height));
  c.width=bmp.width*sc;c.height=bmp.height*sc;
  const ctx=c.getContext('2d');ctx.drawImage(bmp,0,0,c.width,c.height);
  const img=ctx.getImageData(0,0,c.width,c.height);
  const r=window.jsQR(img.data,c.width,c.height);
  return r?r.data:null;
}
F.addEventListener('change',async()=>{
  const file=F.files&&F.files[0];F.value='';if(!file)return;
  note('Читаем QR-код...');
  try{
    const bmp=await toBitmap(file);
    let data=await decodeNative(bmp);
    if(!data)data=await decodeFallback(bmp);
    if(!data){note('QR-код не найден на фото. Снимите ближе и ровнее.');return}
    const inp=document.getElementById('urlInput');
    inp.value=data.trim();
    note('QR: '+data.trim().slice(0,80));
    document.getElementById('checkBtn').click();
  }catch(e){note('Не удалось обработать фото.')}
});
})();
</script>

<!-- AI scam-advisor chat widget -->
<style>
#advBtn{position:fixed;right:18px;bottom:18px;z-index:60;width:56px;height:56px;border-radius:50%;border:none;background:linear-gradient(135deg,#7aa2f7,#5a7fd6);color:#04121a;font-size:24px;cursor:pointer;box-shadow:0 6px 24px rgba(122,162,247,.45);transition:transform .15s}
#advBtn:hover{transform:scale(1.08)}
#advPanel{position:fixed;right:18px;bottom:84px;z-index:60;width:min(360px,calc(100vw - 36px));max-height:min(480px,70vh);background:var(--card,#111827);border:1px solid var(--bd,#1e293b);border-radius:16px;display:none;flex-direction:column;overflow:hidden;box-shadow:0 16px 48px rgba(0,0,0,.5)}
#advPanel.open{display:flex}
.advHead{padding:12px 14px;font-weight:700;font-size:14px;border-bottom:1px solid var(--bd,#1e293b);display:flex;justify-content:space-between;align-items:center}
.advHead button{background:none;border:none;color:var(--mut,#7d8aa0);font-size:18px;cursor:pointer}
#advMsgs{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
.advM{max-width:88%;padding:9px 12px;border-radius:12px;font-size:13px;line-height:1.5;white-space:pre-wrap;word-break:break-word}
.advM.u{align-self:flex-end;background:rgba(122,162,247,.16);border:1px solid rgba(122,162,247,.3)}
.advM.a{align-self:flex-start;background:rgba(125,138,160,.1);border:1px solid var(--bd,#1e293b)}
.advM.a.danger{border-color:rgba(247,118,142,.5);background:rgba(247,118,142,.08)}
.advM.a.warn{border-color:rgba(224,175,104,.5);background:rgba(224,175,104,.08)}
.advIn{display:flex;gap:8px;padding:10px;border-top:1px solid var(--bd,#1e293b)}
.advIn textarea{flex:1;background:var(--bg,#0a0e16);border:1px solid var(--bd,#1e293b);border-radius:10px;color:inherit;font-family:inherit;font-size:13px;padding:8px 10px;resize:none;height:40px}
.advIn button{border:none;border-radius:10px;background:#7aa2f7;color:#04121a;font-weight:700;padding:0 14px;cursor:pointer}
.advHint{font-size:11px;color:var(--mut,#7d8aa0);padding:0 12px 10px}
.qi{width:1em;height:1em;vertical-align:-0.14em;display:inline-block}
:focus-visible{outline:2px solid #7aa2f7;outline-offset:2px;border-radius:4px}
::selection{background:rgba(122,162,247,.32)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
*{scrollbar-width:thin;scrollbar-color:#2a3550 transparent}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-thumb{background:#2a3550;border-radius:5px}::-webkit-scrollbar-track{background:transparent}
</style>
<button id="advBtn" aria-label="AI-советник"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22z"/></svg></button>
<div id="advPanel">
  <div class="advHead"><span id="advTitle"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg> AI-советник Qalqan</span><button id="advClose"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg></button></div>
  <div id="advMsgs"></div>
  <div class="advHint" id="advHint">Опиши ситуацию: звонок, SMS, «инвестиции» — скажу, скам ли это.</div>
  <div class="advIn"><textarea id="advTxt" maxlength="1500" placeholder="Мне звонят из «банка»..."></textarea><button id="advSend"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/></svg></button></div>
</div>
<script>
const QI={octagon:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.86 2h8.28L22 7.86v8.28L16.14 22H7.86L2 16.14V7.86z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>',alert:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',checkc:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',check:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',copy:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="8" width="14" height="14" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>'};
(function(){
const P=document.getElementById('advPanel'),B=document.getElementById('advBtn'),M=document.getElementById('advMsgs');
const L={kk:{t:'Qalqan AI-кеңесші',h:'Жағдайды сипатта: қоңырау, SMS, «инвестиция» — алаяқтық па, айтамын.',ph:'Маған «банктен» қоңырау шалып жатыр...',think:'Талдап жатырмын...',err:'Қате. Кейінірек көріңіз.',rl:'Тым жиі — минут күтіңіз.',flags:'Қауіп белгілері',adv:'Не істеу керек'},
ru:{t:'AI-советник Qalqan',h:'Опиши ситуацию: звонок, SMS, «инвестиции» — скажу, скам ли это.',ph:'Мне звонят из «банка»...',think:'Анализирую...',err:'Ошибка. Попробуйте позже.',rl:'Слишком часто — подождите минуту.',flags:'Признаки угрозы',adv:'Что делать'},
en:{t:'Qalqan AI advisor',h:'Describe the situation: a call, SMS, an "investment" — I will tell you if it is a scam.',ph:'The "bank" is calling me...',think:'Analyzing...',err:'Error. Try later.',rl:'Too often — wait a minute.',flags:'Red flags',adv:'What to do'}};
function dict(){return L[typeof currentLang!=='undefined'?currentLang:'ru']||L.ru}
function applyAdvLang(){const D=dict();document.getElementById('advTitle').textContent=D.t;document.getElementById('advHint').textContent=D.h;document.getElementById('advTxt').placeholder=D.ph}
B.onclick=()=>{P.classList.toggle('open');applyAdvLang();if(P.classList.contains('open'))document.getElementById('advTxt').focus()};
document.getElementById('advClose').onclick=()=>P.classList.remove('open');
function add(cls,html){const d=document.createElement('div');d.className='advM '+cls;d.innerHTML=html;M.appendChild(d);M.scrollTop=M.scrollHeight;return d}
const esc=t=>{const d=document.createElement('div');d.textContent=t;return d.innerHTML};
let busy=false;
async function send(){
  if(busy)return;const T=document.getElementById('advTxt'),txt=T.value.trim();if(!txt)return;
  const D=dict();T.value='';add('u',esc(txt));const w=add('a',D.think);busy=true;
  try{
    const lang=typeof currentLang!=='undefined'?currentLang:'ru';
    const r=await fetch('/advisor',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:txt,lang})});
    if(r.status===429){w.textContent=D.rl;busy=false;return}
    const d=await r.json();
    const v=(d.verdict||'').toUpperCase();
    const em=v==='DANGEROUS'?QI.octagon:v==='SUSPICIOUS'?QI.alert:QI.checkc;
    w.className='advM a '+(v==='DANGEROUS'?'danger':v==='SUSPICIOUS'?'warn':'');
    let h=`<b>${em} ${esc(v)} · ${d.threat_score??''}/100</b>`;
    if(d.reasoning)h+=`<br>${esc(d.reasoning)}`;
    if(Array.isArray(d.red_flags)&&d.red_flags.length)h+=`<br><br><b>${D.flags}:</b><br>${d.red_flags.slice(0,5).map(f=>'• '+esc(f)).join('<br>')}`;
    if(Array.isArray(d.advice)&&d.advice.length)h+=`<br><br><b>${D.adv}:</b><br>${d.advice.slice(0,4).map(f=>'• '+esc(f)).join('<br>')}`;
    w.innerHTML=h;
  }catch(e){w.textContent=dict().err}
  busy=false;
}
document.getElementById('advSend').onclick=send;
document.getElementById('advTxt').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send()}});
})();
</script>
</body>
</html>"""

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

// ── Real KZ choropleth (geometry from /kz-regions.js → KZ_GEO, 20 regions 2023) ──
function heat(frac){
  const a=[13,20,36], b=[255,59,92];
  const c=a.map((v,i)=>Math.round(v+(b[i]-v)*frac));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}
function renderMap(regions){
  regions=regions||{};
  if(typeof KZ_GEO==='undefined'){ return; }
  const mx=Math.max(1,...Object.values(regions).map(r=>r.threats||0));
  const svg=$('kzsvg'), tip=$('maptip');
  let out='';
  for(const [name,d] of Object.entries(KZ_GEO.paths)){
    const r=regions[name]||{total:0,threats:0};
    const frac=Math.min(1,(r.threats||0)/mx);
    out+=`<path d="${d}" fill="${heat(frac)}" stroke="#1e293b" stroke-width="1.2" data-n="${name}" data-t="${r.threats||0}" data-c="${r.total||0}" style="cursor:pointer;transition:filter .15s"/>`;
  }
  // Region labels for the biggest oblasts + city markers
  for(const [name,c] of Object.entries(KZ_GEO.centroids)){
    const small = (name==='Алматы қ.'||name==='Астана'||name==='Шымкент');
    if(small) continue;
    out+=`<text x="${c[0]}" y="${c[1]}" text-anchor="middle" font-size="15" fill="#e7ebf3" opacity=".75" pointer-events="none" font-weight="600">${name}</text>`;
  }
  svg.innerHTML=out;
  svg.querySelectorAll('path').forEach(p=>{
    p.addEventListener('mousemove',e=>{
      p.style.filter='brightness(1.5)';
      tip.style.display='block';
      tip.innerHTML=`<b>${p.dataset.n}</b><br><svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#f7768e"/></svg> ${p.dataset.t} қауіп · <svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg> ${p.dataset.c} тексеру`;
      const box=svg.getBoundingClientRect();
      tip.style.left=Math.min(e.clientX-box.left+14, box.width-160)+'px';
      tip.style.top=(e.clientY-box.top+14)+'px';
    });
    p.addEventListener('mouseleave',()=>{ p.style.filter=''; tip.style.display='none'; });
  });
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
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E"><meta name="viewport" content="width=device-width,initial-scale=1">
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
.qi{width:1em;height:1em;vertical-align:-0.14em;display:inline-block}
:focus-visible{outline:2px solid #7aa2f7;outline-offset:2px;border-radius:4px}
::selection{background:rgba(122,162,247,.32)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
*{scrollbar-width:thin;scrollbar-color:#2a3550 transparent}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-thumb{background:#2a3550;border-radius:5px}::-webkit-scrollbar-track{background:transparent}
</style></head>
<body>
<div class="navbar">
  <a class="logo" href="/"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg> Qalqan AI</a>
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
  <a href="/help" style="flex:1;text-align:center;background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:12px;color:var(--tx);text-decoration:none;font-size:13px;font-weight:700"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m4.93 19.07 4.24-4.24"/></svg> Помощь</a>
</div>

<script>
const tg = window.Telegram?.WebApp;
if (tg) { tg.ready(); tg.expand(); }
const API = location.origin;
const $ = s => document.querySelector(s);
const vcolor = v => v==='DANGEROUS'?'var(--red)':v==='SUSPICIOUS'?'var(--amber)':'var(--green)';
const vlabel = v => v==='DANGEROUS'?'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#f7768e"/></svg> ҚАУІПТІ':v==='SUSPICIOUS'?'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#e0af68"/></svg> КҮДІКТІ':'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#9ece6a"/></svg> ҚАУІПСІЗ';

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

// ── QR scanner (Telegram WebApp 6.4+) — fake Kaspi-QR is a common KZ scam ──
// Scan → URL lands in the input → the normal /check pipeline runs.
if (tg && tg.isVersionAtLeast && tg.isVersionAtLeast('6.4') && tg.showScanQrPopup) {
  $('#btn-qr').style.display='block';
  $('#btn-qr').onclick = () => {
    try {
      tg.showScanQrPopup({ text: 'QR-кодты камераға көрсетіңіз' });
    } catch(e) {}
  };
  tg.onEvent('qrTextReceived', (ev) => {
    try { tg.closeScanQrPopup(); } catch(e) {}
    const data = (ev && ev.data || '').trim();
    if (!data) return;
    // Non-URL QR payloads (wifi:, tel:, plain text) → show as-is, no check
    const m = data.match(/https?:\\/\\/[^\\s]+|[a-zA-Z0-9-]+\\.[a-zA-Z]{2,}[^\\s]*/);
    if (!m) {
      const box=$('#res-check'); box.className='res show';
      box.innerHTML=`<div class="verdict" style="color:var(--amber)">ℹ QR ішінде сілтеме жоқ</div>
        <div class="detail" style="word-break:break-all">${data.replace(/&/g,'&amp;').replace(/</g,'&lt;')}</div>`;
      return;
    }
    $('#url').value = m[0];
    check();
    if (tg.HapticFeedback) tg.HapticFeedback.impactOccurred('medium');
  });
}

async function ask(){
  const t=$('#situation').value.trim(); if(t.length<10) return;
  const box=$('#res-ask'); box.className='res show'; box.innerHTML='<div class="spin">AI талдап жатыр...</div>';
  try{
    const ulang=(tg&&tg.initDataUnsafe&&tg.initDataUnsafe.user&&tg.initDataUnsafe.user.language_code)||'ru';
    const r=await fetch(API+'/advisor',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t,lang:['kk','ru','en'].includes(ulang)?ulang:'ru'})});
    const d=await r.json();
    const v=d.verdict, sc=d.threat_score||0;
    let h=`<div class="verdict" style="color:${vcolor(v)}">${vlabel(v)}</div>
      <div class="score">${sc}/100 · ${d.scam_type||''}</div>
      <div class="bar"><div style="width:${sc}%;background:${vcolor(v)}"></div></div>
      <div class="detail">${d.reasoning||d.detail_ru||''}</div>`;
    if((d.advice||[]).length) h+='<div class="meta"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> '+d.advice.slice(0,4).map(a=>a).join('<br><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> ')+'</div>';
    box.innerHTML=h;
  }catch(e){ box.innerHTML='<div class="spin">Қате. Кейінірек қайталаңыз.</div>'; }
}
$('#btn-ask').onclick=ask;

let mapLoaded=false;
async function loadMap(){
  if(mapLoaded) return; mapLoaded=true;
  try{
    // Load geometry + data in parallel (geometry cached 24h by the CDN).
    // No forced demo: server returns real data when it exists, falls back to a
    // demo dataset and labels it via _source — show an honest badge either way.
    const [geoTxt, d] = await Promise.all([
      fetch(API+'/kz-regions.js').then(r=>r.text()),
      fetch(API+'/dashboard/data').then(r=>r.json()),
    ]);
    let KZ_GEO; try{ KZ_GEO = (new Function(geoTxt+';return KZ_GEO;'))(); }catch(e){ KZ_GEO=null; }
    const k=d.kpis||{};
    const demoBadge = d._source==='demo' ? ' <span style="font-size:9px;color:var(--amber);border:1px solid var(--amber);border-radius:6px;padding:1px 5px;vertical-align:middle">ДЕМО</span>' : '';
    $('#kpis').innerHTML=
      `<div class="kpi"><div class="v" style="color:var(--cyan)">${(k.total_checks||0).toLocaleString()}</div><div class="l">Тексерілді${demoBadge}</div></div>`+
      `<div class="kpi"><div class="v" style="color:var(--red)">${(k.threats_blocked||0).toLocaleString()}</div><div class="l">Қауіп</div></div>`;
    const reg=d.regions||{}; const mx=Math.max(1,...Object.values(reg).map(r=>r.threats||0));
    if(KZ_GEO){
      // Real choropleth — 20 регионов (2023 COD-AB)
      let out='';
      for(const [nm,path] of Object.entries(KZ_GEO.paths)){
        const r=reg[nm]||{threats:0};
        const f=Math.min(1,(r.threats||0)/mx);
        const c=`rgb(${Math.round(13+(255-13)*f)},${Math.round(20+(59-20)*f)},${Math.round(36+(92-36)*f)})`;
        out+=`<path d="${path}" fill="${c}" stroke="#1e293b" stroke-width="1.5"/>`;
      }
      $('#kzsvg').innerHTML=out;
    }
    const top=Object.entries(reg).sort((a,b)=>(b[1].threats||0)-(a[1].threats||0)).slice(0,8);
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
  let h=`<div class="verdict">${v==='DANGEROUS'?'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.86 2h8.28L22 7.86v8.28L16.14 22H7.86L2 16.14V7.86z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>':v==='SUSPICIOUS'?'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>':'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'} ${v}</div><div class="score">Қауіп: ${score}/100</div><div class="detail">${detail||''}</div>`;
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
    const d=await (await fetch(API+'/dashboard/data')).json();
    const demoTag = d._source==='demo' ? ' <small style="color:#e0af68">(демо)</small>' : '';
    const reg=Object.entries(d.regions||{}).sort((a,b)=>b[1].threats-a[1].threats).slice(0,12);
    const mx=Math.max(1,...reg.map(r=>r[1].threats));
    $('#regions').innerHTML=demoTag+reg.map(([n,r])=>`<div class="region"><span class="nm">${n}</span><span class="tk"><span class="fl" style="width:${Math.round(100*r.threats/mx)}%"></span></span><span class="vv">${r.threats}</span></div>`).join('');
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
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E"><meta name="viewport" content="width=device-width,initial-scale=1">
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
.qi{width:1em;height:1em;vertical-align:-0.14em;display:inline-block}
:focus-visible{outline:2px solid #7aa2f7;outline-offset:2px;border-radius:4px}
::selection{background:rgba(122,162,247,.32)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
*{scrollbar-width:thin;scrollbar-color:#2a3550 transparent}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-thumb{background:#2a3550;border-radius:5px}::-webkit-scrollbar-track{background:transparent}
</style></head><body>
<h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg> Qalqan AI — Партнёрский API <span class="tag">B2G</span></h1>
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

<h2>Бейдж «Qalqan Verified» для вашего сайта</h2>
<div class="card">Встраиваемый SVG-бейдж с грейдом безопасности вашего домена (обновляется раз в сутки):<br><br>
<img src="/badge/kaspi.kz" alt="Qalqan badge" style="vertical-align:middle"><br><br>
<pre>&lt;a href="https://qalqan-ai-nu.vercel.app/scan"&gt;
  &lt;img src="https://qalqan-ai-nu.vercel.app/badge/ВАШ-ДОМЕН.kz" alt="Qalqan Security Grade"&gt;
&lt;/a&gt;</pre>
Зелёный A/A+ — сайт прошёл проверку; жёлтый/красный — есть проблемы (смотрите /scan).</div>

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

LEAK_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Проверка утечки пароля</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0e16;--card:#111827;--card2:#0d1424;--cyan:#7aa2f7;--red:#f7768e;--amber:#e0af68;--green:#9ece6a;--tx:#e7ebf3;--mut:#7d8aa0;--bd:#1e293b}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--tx);font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;min-height:100vh;padding:20px}
.wrap{max-width:560px;margin:0 auto}
.top{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px}
.top a{color:var(--mut);text-decoration:none;font-size:14px}
.top a:hover{color:var(--cyan)}
h1{font-size:22px;font-weight:800}
.sub{color:var(--mut);font-size:13px;margin:6px 0 22px;line-height:1.6}
.card{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:22px;margin-bottom:14px}
.inrow{display:flex;gap:8px}
input{flex:1;background:var(--card2);border:1px solid var(--bd);border-radius:12px;padding:14px;color:var(--tx);font-size:16px;outline:none;font-family:inherit}
input:focus{border-color:var(--cyan)}
.eye{background:var(--card2);border:1px solid var(--bd);border-radius:12px;padding:0 14px;color:var(--mut);cursor:pointer;font-size:16px}
.btn{width:100%;margin-top:12px;background:linear-gradient(90deg,#0891b2,var(--cyan));color:#04121a;border:none;border-radius:12px;padding:15px;font-size:15px;font-weight:800;cursor:pointer;font-family:inherit}
.btn:disabled{opacity:.6;cursor:wait}
.priv{display:flex;gap:10px;align-items:flex-start;background:rgba(158,206,106,.07);border:1px solid rgba(158,206,106,.25);border-radius:12px;padding:13px;font-size:12.5px;line-height:1.55;color:var(--mut);margin-top:14px}
.priv b{color:var(--green)}
.res{margin-top:16px;border-radius:14px;padding:18px;display:none;line-height:1.6}
.res.show{display:block}
.res.bad{background:rgba(247,118,142,.09);border:1px solid rgba(247,118,142,.35)}
.res.ok{background:rgba(158,206,106,.09);border:1px solid rgba(158,206,106,.35)}
.res .big{font-size:19px;font-weight:800;margin-bottom:6px}
.res .cnt{font-size:34px;font-weight:800;color:var(--red)}
.res ul{margin:10px 0 0 18px;font-size:13.5px;color:var(--tx)}
.res li{margin-bottom:5px}
.foot{text-align:center;color:var(--mut);font-size:12px;margin-top:22px}
.foot a{color:var(--cyan);text-decoration:none}
.how{font-size:12.5px;color:var(--mut);line-height:1.6;margin-top:14px}
.how code{background:var(--card2);border:1px solid var(--bd);border-radius:5px;padding:1px 6px;font-size:11.5px}
.tabs{display:flex;gap:8px;margin-bottom:14px}
.tabb{flex:1;background:var(--card2);border:1px solid var(--bd);border-radius:10px;color:var(--mut);font-family:inherit;font-size:13.5px;font-weight:700;padding:10px;cursor:pointer}
.tabb.on{background:var(--cyan);color:#04121a;border-color:var(--cyan)}
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
  <div class="top"><h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> Пароль утёк?</h1><a href="/">← Qalqan AI</a></div>
  <div class="sub">Құпиясөзіңіз деректер утечкаларында бар ма? · Проверь пароль по базе <b>HaveIBeenPwned</b> — 900+ млн паролей из реальных утечек.</div>

  <div class="tabs">
    <button class="tabb on" data-t="pw"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> Пароль</button>
    <button class="tabb" data-t="em"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg> Email</button>
  </div>

  <div class="card" id="card-pw">
    <div class="inrow">
      <input id="pw" type="password" aria-label="Пароль для проверки" placeholder="Введите пароль для проверки" autocomplete="off">
      <button class="eye" id="eye" aria-label="Показать пароль"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/></svg></button>
    </div>
    <button class="btn" id="go">Проверить утечку</button>
    <div class="priv">
      <span style="font-size:16px"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></span>
      <span><b>Пароль не покидает ваше устройство.</b> Считается SHA-1 хэш прямо в браузере, наружу уходят только первые 5 символов хэша (k-анонимность). Ни мы, ни HIBP не видим пароль и даже его полный хэш.</span>
    </div>
    <div class="res" id="res"></div>
    <div class="how">Как это работает: пароль → <code>SHA-1</code> в браузере → префикс <code>5 симв.</code> → HIBP возвращает ~800 хэшей с этим префиксом → сравнение происходит локально у вас.</div>
  </div>

    <div class="card" id="card-em" style="display:none">
    <div class="inrow">
      <input id="em" type="email" aria-label="Email для проверки" placeholder="you@example.com" autocomplete="off">
    </div>
    <button class="btn" id="goem">Проверить email</button>
    <div class="priv">
      <span style="font-size:16px"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></span>
      <span><b>Email не сохраняется.</b> Запрос уходит в открытую базу утечек XposedOrNot; Qalqan не логирует и не хранит адрес.</span>
    </div>
    <div class="res" id="resem"></div>
  </div>

  <div class="card" style="margin-top:14px">
    <div style="font-weight:700;font-size:14px;margin-bottom:10px"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg> Генератор надёжных паролей</div>
    <div class="inrow">
      <input id="genout" type="text" readonly aria-label="Сгенерированный пароль" placeholder="Нажми «Сгенерировать»" style="font-family:ui-monospace,monospace">
      <button class="eye" id="gencopy" aria-label="Скопировать"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="8" width="14" height="14" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg></button>
    </div>
    <div style="display:flex;gap:10px;margin-top:10px;align-items:center;font-size:12.5px;color:var(--mut)">
      <label><input type="checkbox" id="gensym" checked> символы</label>
      <label>длина <select id="genlen" aria-label="Длина пароля"><option>16</option><option>20</option><option selected>24</option><option>32</option></select></label>
    </div>
    <button class="btn" id="gengo" style="margin-top:12px">Сгенерировать</button>
    <div class="priv" style="margin-top:10px"><span style="font-size:16px"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></span><span>Генерируется в браузере (crypto.getRandomValues), никуда не отправляется.</span></div>
  </div>

<div class="foot">Qalqan AI · Данные: <a href="https://haveibeenpwned.com/Passwords" rel="noopener" target="_blank">HaveIBeenPwned</a> (k-anonymity API) · </div>
</div>

<script>
const QI={octagon:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.86 2h8.28L22 7.86v8.28L16.14 22H7.86L2 16.14V7.86z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>',alert:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',checkc:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',check:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',copy:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="8" width="14" height="14" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>'};
const $=s=>document.querySelector(s);
$('#eye').onclick=()=>{const p=$('#pw');p.type=p.type==='password'?'text':'password';};

async function sha1hex(str){
  const buf=await crypto.subtle.digest('SHA-1',new TextEncoder().encode(str));
  return [...new Uint8Array(buf)].map(b=>b.toString(16).padStart(2,'0')).join('').toUpperCase();
}

async function checkLeak(){
  const pw=$('#pw').value;
  const res=$('#res');
  if(!pw){ return; }
  const btn=$('#go'); btn.disabled=true; btn.textContent='Проверяем...';
  try{
    const hash=await sha1hex(pw);
    const prefix=hash.slice(0,5), suffix=hash.slice(5);
    const r=await fetch('https://api.pwnedpasswords.com/range/'+prefix,{headers:{'Add-Padding':'true'}});
    if(!r.ok) throw new Error('hibp '+r.status);
    const lines=(await r.text()).split('\\n');
    let count=0;
    for(const ln of lines){
      const [suf,cnt]=ln.trim().split(':');
      if(suf===suffix){ count=parseInt(cnt,10)||0; break; }
    }
    if(count>0){
      res.className='res show bad';
      res.innerHTML=`<div class="big"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 18v-6a5 5 0 1 1 10 0v6"/><path d="M5 21a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2z"/><path d="M12 2v2"/><path d="m4.9 4.9 1.4 1.4"/><path d="m19.1 4.9-1.4 1.4"/></svg> Пароль скомпрометирован!</div>
        Этот пароль встречается в утечках <span class="cnt">${count.toLocaleString('ru-RU')}</span> раз.
        <ul>
          <li>Смени его ВЕЗДЕ, где используешь — прямо сейчас</li>
          <li>Включи двухфакторную защиту (2FA) в банках и почте</li>
          <li>Используй разные пароли для разных сервисов</li>
        </ul>`;
    }else{
      res.className='res show ok';
      res.innerHTML=`<div class="big"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> В известных утечках не найден</div>
        Это не гарантия абсолютной безопасности, но в 900+ млн утёкших паролей его нет.
        Совет: длина 12+ символов и уникальность для каждого сервиса важнее сложности.`;
    }
  }catch(e){
    res.className='res show bad';
    res.innerHTML='<div class="big"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Сервис недоступен</div>Попробуйте позже — проверка идёт напрямую в HaveIBeenPwned.';
  }
  btn.disabled=false; btn.textContent='Проверить утечку';
}
$('#go').onclick=checkLeak;
$('#pw').addEventListener('keydown',e=>{if(e.key==='Enter')checkLeak();});

// ── Tabs ──
document.querySelectorAll('.tabb').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('.tabb').forEach(x=>x.classList.toggle('on',x===b));
  document.getElementById('card-pw').style.display=b.dataset.t==='pw'?'block':'none';
  document.getElementById('card-em').style.display=b.dataset.t==='em'?'block':'none';
});
// ── Email breach check (XposedOrNot via backend proxy) ──
async function checkEmail(){
  const em=document.getElementById('em').value.trim();
  const R=document.getElementById('resem');
  if(!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/.test(em)){R.className='res show';R.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Введите корректный email.';return}
  R.className='res show';R.innerHTML='Проверяем базы утечек...';
  try{
    const r=await fetch('/leak/email?email='+encodeURIComponent(em));
    if(r.status===429){R.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> Слишком часто — подождите минуту.';return}
    if(!r.ok){R.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Сервис утечек недоступен, попробуйте позже.';return}
    const d=await r.json();
    if(!d.breached){R.innerHTML='<b style="color:var(--green,#9ece6a)"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> Не найден в известных утечках.</b><br>Это не гарантия — используйте уникальные пароли и 2FA.';}
    else{
      const esc=t=>{const x=document.createElement('div');x.textContent=t;return x.innerHTML};
      R.innerHTML='<b style="color:var(--red,#f7768e)"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 18v-6a5 5 0 1 1 10 0v6"/><path d="M5 21a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2z"/><path d="M12 2v2"/><path d="m4.9 4.9 1.4 1.4"/><path d="m19.1 4.9-1.4 1.4"/></svg> Найден в '+d.count+' утечках:</b><br>'+
        d.breaches.map(b=>'• '+esc(b)).join('<br>')+
        '<br><br><b>Что делать:</b> смените пароли на этих сервисах, включите 2FA, не переиспользуйте пароли.';
    }
  }catch(e){R.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Ошибка сети.'}
}
document.getElementById('goem').onclick=checkEmail;
document.getElementById('em').addEventListener('keydown',e=>{if(e.key==='Enter')checkEmail()});

// ── Password generator (client-side only) ──
function genPw(){
  const L=+document.getElementById('genlen').value;
  const sym=document.getElementById('gensym').checked;
  const abc='abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'+(sym?'!@#$%^&*-_=+?':'');
  const buf=new Uint32Array(L);crypto.getRandomValues(buf);
  document.getElementById('genout').value=[...buf].map(n=>abc[n%abc.length]).join('');
}
document.getElementById('gengo').onclick=genPw;
document.getElementById('gencopy').onclick=async()=>{
  const v=document.getElementById('genout').value;if(!v)return;
  try{await navigator.clipboard.writeText(v);document.getElementById('gencopy').innerHTML=QI.check;
      setTimeout(()=>document.getElementById('gencopy').innerHTML=QI.copy,1200);}catch(e){}
};
</script>
</body>
</html>"""

HELP_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Обманули? Куда обращаться</title>
<meta name="description" content="Официальные контакты Казахстана при мошенничестве: Нацбанк 1477, Антифрод-центр, KZ-CERT, АФМ, полиция 102. Пошаговый план действий.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0e16;--card:#111827;--card2:#0d1424;--cyan:#7aa2f7;--red:#f7768e;--amber:#e0af68;--green:#9ece6a;--tx:#e7ebf3;--mut:#7d8aa0;--bd:#1e293b}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--tx);font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;min-height:100vh;padding:20px}
.wrap{max-width:640px;margin:0 auto}
.top{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}
.top a{color:var(--mut);text-decoration:none;font-size:14px}.top a:hover{color:var(--cyan)}
h1{font-size:24px;font-weight:800;line-height:1.2}
.sub{color:var(--mut);font-size:14px;margin:8px 0 22px;line-height:1.6}
.urgent{background:linear-gradient(135deg,rgba(247,118,142,.14),rgba(247,118,142,.05));border:1px solid rgba(247,118,142,.4);border-radius:16px;padding:18px;margin-bottom:22px}
.urgent .t{font-size:15px;font-weight:800;color:var(--red);margin-bottom:6px}
.urgent .n{font-size:30px;font-weight:800;color:var(--tx);letter-spacing:1px}
.urgent .d{font-size:13px;color:var(--mut);margin-top:4px}
.sec-t{font-size:13px;font-weight:800;text-transform:uppercase;letter-spacing:.5px;color:var(--mut);margin:24px 0 10px}
.steps{counter-reset:s;list-style:none}
.steps li{position:relative;padding:12px 12px 12px 46px;background:var(--card);border:1px solid var(--bd);border-radius:12px;margin-bottom:8px;font-size:14px;line-height:1.55}
.steps li::before{counter-increment:s;content:counter(s);position:absolute;left:12px;top:12px;width:24px;height:24px;border-radius:8px;background:var(--cyan);color:#04121a;font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center}
.steps b{color:var(--tx)}
.grid{display:grid;gap:10px}
.org{display:flex;gap:12px;align-items:flex-start;background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:15px;text-decoration:none;color:inherit;transition:border-color .2s}
.org:hover{border-color:var(--cyan)}
.org .ic{font-size:24px;flex-shrink:0;line-height:1.2}
.org .nm{font-weight:700;font-size:15px}
.org .ds{font-size:12.5px;color:var(--mut);margin-top:2px;line-height:1.5}
.org .ph{font-size:15px;font-weight:800;color:var(--cyan);margin-top:5px}
.foot{text-align:center;color:var(--mut);font-size:12px;margin-top:26px;line-height:1.7}
.foot a{color:var(--cyan);text-decoration:none}
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
  <div class="top"><h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m4.93 19.07 4.24-4.24"/></svg> Обманули? Действуй быстро</h1><a href="/">← Qalqan AI</a></div>
  <div class="sub">Алдап кетті ме? Тез әрекет ет — алғашқы сағаттар шешуші. · Первые часы решают: чем быстрее заблокируешь операцию, тем выше шанс вернуть деньги.</div>

  <div class="urgent">
    <div class="t"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/></svg> Деньги ушли только что — звони НЕМЕДЛЕННО</div>
    <div class="n"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg> 1477</div>
    <div class="d">Контакт-центр Нацбанка РК · круглосуточно · блокировка перевода через Антифрод-центр</div>
  </div>

  <div class="sec-t">Пошаговый план</div>
  <ol class="steps">
    <li><b>Позвони в свой банк</b> и на 1477 — потребуй заблокировать карту и оспорить операцию. Антифрод-центр может приостановить перевод и вернуть деньги.</li>
    <li><b>Не переходи по ссылкам и не диктуй SMS-коды</b> — настоящий банк никогда их не спрашивает. Положи трубку и перезвони на номер с обратной стороны карты.</li>
    <li><b>Подай заявление в полицию</b> — 102 или через eGov. Приложи скриншоты, номера, реквизиты получателя.</li>
    <li><b>Смени пароли</b> банка, почты, госуслуг. Включи 2FA. Проверь пароль на <a href="/leak" style="color:var(--cyan)">/leak</a>.</li>
    <li><b>Сообщи о сайте/номере</b> — помоги другим: <a href="/" style="color:var(--cyan)">проверь ссылку</a> или отправь боту <a href="https://t.me/QalqanAI_bot" style="color:var(--cyan)">@QalqanAI_bot</a>.</li>
  </ol>

  <div class="sec-t">Официальные службы Казахстана</div>
  <div class="grid">
    <a class="org" href="tel:1477">
      <span class="ic"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 18v-7"/><path d="M11.12 2.198a2 2 0 0 1 1.76.006l7.866 3.847c.476.233.31.949-.22.949H3.474c-.53 0-.695-.716-.22-.949z"/><path d="M14 18v-7"/><path d="M18 18v-7"/><path d="M3 22h18"/><path d="M6 18v-7"/></svg></span>
      <div><div class="nm">Нацбанк РК · Антифрод-центр</div>
      <div class="ds">Блокировка мошеннических переводов, возврат средств. Работает с банками и операторами 24/7.</div>
      <div class="ph">1477</div></div>
    </a>
    <a class="org" href="tel:102">
      <span class="ic"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 18v-6a5 5 0 1 1 10 0v6"/><path d="M5 21a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2z"/><path d="M12 2v2"/><path d="m4.9 4.9 1.4 1.4"/><path d="m19.1 4.9-1.4 1.4"/></svg></span>
      <div><div class="nm">Полиция · киберпреступления</div>
      <div class="ds">Заявление о мошенничестве. Единый номер экстренных служб.</div>
      <div class="ph">102</div></div>
    </a>
    <a class="org" href="https://www.cert.gov.kz/" target="_blank" rel="noopener">
      <span class="ic"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg></span>
      <div><div class="nm">KZ-CERT · Нацинтех</div>
      <div class="ds">Национальная служба реагирования на киберинциденты — фишинг, взломы, вредоносные сайты.</div>
      <div class="ph">cert.gov.kz →</div></div>
    </a>
    <a class="org" href="https://www.gov.kz/memleket/entities/ardfm" target="_blank" rel="noopener">
      <span class="ic"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg></span>
      <div><div class="nm">АРРФР / АФМ</div>
      <div class="ds">Финансовые пирамиды, нелегальные инвестиции, обманутые вкладчики. Реестр пирамид.</div>
      <div class="ph">gov.kz/ardfm →</div></div>
    </a>
    <a class="org" href="https://egov.kz/" target="_blank" rel="noopener">
      <span class="ic"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 18v-7"/><path d="M11.12 2.198a2 2 0 0 1 1.76.006l7.866 3.847c.476.233.31.949-.22.949H3.474c-.53 0-.695-.716-.22-.949z"/><path d="M14 18v-7"/><path d="M18 18v-7"/><path d="M3 22h18"/><path d="M6 18v-7"/></svg></span>
      <div><div class="nm">eGov · онлайн-заявление</div>
      <div class="ds">Подать обращение в органы онлайн, проверить статус дела.</div>
      <div class="ph">egov.kz →</div></div>
    </a>
    <a class="org" href="tel:1406">
      <span class="ic"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 8h.01"/><path d="M16 8h.01"/><path d="M8 16h.01"/><path d="M16 16h.01"/><path d="M12 12h.01"/></svg></span>
      <div><div class="nm">Помощь при лудомании</div>
      <div class="ds">Игровая зависимость — это болезнь, которую лечат. Бесплатная психологическая помощь.</div>
      <div class="ph">1406 · 8-800-080-88-87</div></div>
    </a>
  </div>

  <div class="foot">
    Qalqan AI · Бұл ресми қызметтер тізімі, кеңес емес · Список официальных служб, не является юр. консультацией<br>
    <a href="/leak"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> Пароль</a> · <a href="/"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg> Проверить сайт</a>
  </div>
</div>
</body>
</html>"""

BRAND_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Защита бренда от фишинга</title>
<meta name="description" content="Radar фишинговых доменов-двойников вашего бренда: гомоглифы, бесплатные TLD, приманки. Для банков, госорганов, бизнеса Казахстана.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0e16;--card:#111827;--card2:#0d1424;--cyan:#7aa2f7;--red:#f7768e;--amber:#e0af68;--green:#9ece6a;--tx:#e7ebf3;--mut:#7d8aa0;--bd:#1e293b}
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
  <div class="top"><h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> Защита бренда от фишинга</h1><a href="/">← Qalqan AI</a></div>
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

<script>
const $=s=>document.querySelector(s);
async function scan(dom){
  dom=(dom||$('#dom').value).trim(); if(!dom) return;
  $('#dom').value=dom;
  const btn=$('#go'); btn.disabled=true; btn.textContent='...';
  $('#summary').className='summary'; $('#grid').className='grid'; $('#advice').className='advice';
  $('#status').innerHTML='<div class="spin">Генерируем варианты атаки...</div>';
  try{
    const r=await fetch('/brand/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({domain:dom})});
    const d=await r.json();
    if(d.error){ $('#status').innerHTML='<div class="spin"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Введите корректный домен, напр. kaspi.kz</div>'; btn.disabled=false; btn.textContent='Сканировать'; return; }
    const c=d.risk_counts||{};
    $('#summary').innerHTML=
      `<div class="pill c"><svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#f7768e"/></svg> Критичных: ${c.critical||0}</div>`+
      `<div class="pill h"><svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#e08f68"/></svg> Высоких: ${c.high||0}</div>`+
      `<div class="pill m"><svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#7aa2f7"/></svg> Средних: ${c.medium||0}</div>`;
    $('#summary').className='summary show';
    $('#grid').innerHTML=(d.variants||[]).map(v=>
      `<div class="row"><span class="dot ${v.risk}"></span><div><div class="dm">${v.domain}</div><div class="nt">${v.note}</div></div></div>`).join('');
    $('#grid').className='grid show';
    $('#advice').innerHTML=`<b>Что делать:</b> ${d.advice_ru||''}<div class="disc">${d.disclaimer_ru||''}</div>`;
    $('#advice').className='advice show';
    $('#status').innerHTML='';
    $('#liveblock').style.display='block'; $('#liveres').innerHTML='';
  }catch(e){ $('#status').innerHTML='<div class="spin">Ошибка. Попробуйте позже.</div>'; }
  btn.disabled=false; btn.textContent='Сканировать';
}
$('#go').onclick=()=>scan();
$('#dom').addEventListener('keydown',e=>{if(e.key==='Enter')scan();});
document.querySelectorAll('.ex b').forEach(b=>b.onclick=()=>scan(b.dataset.d));

// ── Live RDAP scan: which look-alikes are ACTUALLY registered right now ──
$('#livego').onclick=async()=>{
  const dom=$('#dom').value.trim(); if(!dom) return;
  const b=$('#livego'); b.disabled=true; b.textContent='Проверяем реестры...';
  $('#liveres').innerHTML='<div class="spin">RDAP-запросы к доменным реестрам (до 15 сек)...</div>';
  try{
    const r=await fetch('/brand/live-scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({domain:dom})});
    if(r.status===429){ $('#liveres').innerHTML='<div class="spin"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> Слишком часто — подождите минуту.</div>'; b.disabled=false; b.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg> Live-проверка регистраций'; return; }
    const d=await r.json();
    if(d.error){ $('#liveres').innerHTML='<div class="spin"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Некорректный домен.</div>'; }
    else if(!d.registered_count){
      $('#liveres').innerHTML=`<div class="liveok"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> Из ${d.answered} проверенных вариантов — ни один не зарегистрирован. Атакующей инфраструктуры не обнаружено.</div>`;
    } else {
      $('#liveres').innerHTML=
        `<div class="livebad"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 18v-6a5 5 0 1 1 10 0v6"/><path d="M5 21a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2z"/><path d="M12 2v2"/><path d="m4.9 4.9 1.4 1.4"/><path d="m19.1 4.9-1.4 1.4"/></svg> Зарегистрировано ${d.registered_count} из ${d.answered} проверенных:</div>`+
        d.registered.map(v=>`<div class="row"><span class="dot critical"></span><div><div class="dm">${v.domain}</div><div class="nt">${v.note}${v.age_days!=null?` · возраст ${v.age_days} дн.`:''} · <b style="color:var(--red)">СУЩЕСТВУЕТ</b></div></div></div>`).join('')+
        `<div class="disc" style="margin-top:8px">${d.note_ru||''}</div>`;
    }
  }catch(e){ $('#liveres').innerHTML='<div class="spin">Ошибка сети.</div>'; }
  b.disabled=false; b.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg> Live-проверка регистраций';
};

// ── Subscribe to daily monitoring ──
$('#watchgo').onclick=async()=>{
  const dom=$('#dom').value.trim(); if(!dom) return;
  const b=$('#watchgo'); b.disabled=true;
  try{
    const r=await fetch('/brand/watch',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({domain:dom})});
    const d=await r.json();
    b.textContent=d.ok?'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> На мониторинге':'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Недоступно';
  }catch(e){ b.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Ошибка'; b.disabled=false; }
};
</script>
<div class="foot">Qalqan AI · Domain typosquatting radar · <a href="/partners">B2G API</a> · <a href="/">Проверить сайт</a></div>
</body>
</html>"""

SCAN_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Оценка безопасности сайта</title>
<meta name="description" content="Оценка безопасности любого сайта от A+ до F: HTTPS/SSL, возраст домена, репутация, гомоглифы, инфраструктура. Бесплатно.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0e16;--card:#111827;--card2:#0d1424;--cyan:#7aa2f7;--red:#f7768e;--amber:#e0af68;--green:#9ece6a;--tx:#e7ebf3;--mut:#7d8aa0;--bd:#1e293b}
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
  <div class="top"><h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 1 0 0-14h-1"/><path d="M9 14h2"/><path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z"/><path d="M12 6V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3"/></svg> Оценка безопасности сайта</h1><a href="/">← Qalqan AI</a></div>
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

<script>
const $=s=>document.querySelector(s);
async function scan(dom){
  dom=(dom||$('#dom').value).trim().replace(/^https?:\\/\\//,'').replace(/\\/.*$/,''); if(!dom) return;
  $('#dom').value=dom;
  const btn=$('#go'); btn.disabled=true; btn.textContent='...';
  $('#card').className='card'; $('#status').innerHTML='<div class="spin">Анализируем '+dom+' (SSL, домен, репутация)...</div>';
  try{
    const r=await fetch('/scan/'+encodeURIComponent(dom));
    if(!r.ok) throw new Error('http '+r.status);
    const d=await r.json();
    if(d.error){ $('#status').innerHTML='<div class="spin"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> '+d.error+'</div>'; btn.disabled=false; btn.textContent='Оценить'; return; }
    $('#badge').textContent=d.grade; $('#badge').style.background=d.grade_color;
    $('#dm').textContent=d.domain;
    const vlabel=d.verdict==='DANGEROUS'?'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#f7768e"/></svg> Опасный':d.verdict==='SUSPICIOUS'?'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#e0af68"/></svg> Подозрительный':'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#9ece6a"/></svg> Чистый';
    $('#vv').textContent=vlabel+' · риск '+d.risk_score+'/100';
    $('#pc').innerHTML='<span style="color:var(--green)"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg> '+d.passed+'</span> из '+d.total_checks+' проверок пройдено';
    $('#factors').innerHTML=(d.factors||[]).map(f=>{
      const ic=f.status==='pass'?'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>':f.status==='warn'?'▲':'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>';
      return `<div class="f ${f.status}"><span class="i">${ic}</span><span>${f.ru}</span></div>`;
    }).join('');
    $('#card').className='card show'; $('#status').innerHTML='';
  }catch(e){ $('#status').innerHTML='<div class="spin">Ошибка анализа. Попробуйте позже.</div>'; }
  btn.disabled=false; btn.textContent='Оценить';
}
$('#go').onclick=()=>scan();
$('#dom').addEventListener('keydown',e=>{if(e.key==='Enter')scan();});
document.querySelectorAll('.ex b').forEach(b=>b.onclick=()=>scan(b.dataset.d));
</script>
<div class="foot">Qalqan AI · Website security grade · <a href="/brand">Защита бренда</a> · <a href="/">Главная</a></div>
</body>
</html>"""

IMPACT_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Экономический эффект</title>
<meta name="description" content="Сколько денег экономит Qalqan AI для Казахстана. Интерактивный расчёт предотвращённого ущерба от киберскама.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0e16;--card:#111827;--card2:#0d1424;--cyan:#7aa2f7;--red:#f7768e;--amber:#e0af68;--green:#9ece6a;--tx:#e7ebf3;--mut:#7d8aa0;--bd:#1e293b}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--tx);font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;min-height:100vh;padding:20px}
.wrap{max-width:680px;margin:0 auto}
.top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.top a{color:var(--mut);text-decoration:none;font-size:14px}.top a:hover{color:var(--cyan)}
.lang{display:inline-flex;border:1px solid var(--bd);border-radius:9px;overflow:hidden}
.lang button{background:none;border:none;color:var(--mut);font-size:12px;font-weight:700;padding:10px 14px;cursor:pointer;font-family:inherit}
.lang button.on{background:var(--cyan);color:#04121a}
h1{font-size:24px;font-weight:800;line-height:1.2}
.sub{color:var(--mut);font-size:13.5px;margin:8px 0 20px;line-height:1.6}
.stat-src{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:22px}
.ss{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:14px}
.ss .n{font-size:22px;font-weight:800;color:var(--red)}
.ss .l{font-size:11.5px;color:var(--mut);margin-top:2px;line-height:1.4}
.calc{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:22px;margin-bottom:16px}
.calc label{display:block;font-size:13px;font-weight:600;margin-bottom:10px;color:var(--tx)}
.calc .val{color:var(--cyan);font-weight:800}
input[type=range]{width:100%;accent-color:var(--cyan);height:6px}
.big-out{text-align:center;padding:26px 18px;background:linear-gradient(135deg,rgba(158,206,106,.12),rgba(122,162,247,.06));border:1px solid rgba(158,206,106,.3);border-radius:18px;margin-top:18px}
.big-out .lbl{font-size:13px;color:var(--mut);text-transform:uppercase;letter-spacing:.5px}
.big-out .amt{font-size:clamp(30px,8vw,52px);font-weight:900;color:var(--green);line-height:1.1;margin:8px 0;font-variant-numeric:tabular-nums}
.big-out .per{font-size:13px;color:var(--mut)}
.rows{margin-top:14px}
.r{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid rgba(30,41,59,.6);font-size:13.5px}
.r:last-child{border:none}.r .rl{color:var(--mut)}.r .rv{font-weight:700}
.disc{color:var(--mut);font-size:11px;margin-top:14px;line-height:1.5}
.foot{text-align:center;color:var(--mut);font-size:12px;margin-top:24px}.foot a{color:var(--cyan);text-decoration:none}
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
  <div class="top">
    <h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01"/><path d="M18 12h.01"/></svg> <span id="h1"></span></h1>
    <div style="display:flex;gap:10px;align-items:center">
      <div class="lang"><button data-l="kk">ҚАЗ</button><button data-l="ru" class="on">РУС</button></div>
      <a href="/">← Qalqan AI</a>
    </div>
  </div>
  <div class="sub" id="sub">Сколько денег Qalqan AI может сберечь для граждан Казахстана. Расчёт основан на официальной статистике 2025 года.</div>

  <div class="stat-src">
    <div class="ss"><div class="n">16,4 млрд ₸</div><div class="l" id="s1">украдено за 10 мес. 2025 (×29 к 2024)</div></div>
    <div class="ss"><div class="n">26 300</div><div class="l" id="s2">случаев кибермошенничества (+86%)</div></div>
  </div>

  <div class="calc">
    <label id="lb1">Пользователей Qalqan AI: <span class="val" id="vUsers">100 000</span></label>
    <input type="range" id="users" min="10000" max="5000000" step="10000" value="100000">
    <label style="margin-top:18px" id="lb2">Эффективность блокировки: <span class="val" id="vEff">75%</span></label>
    <input type="range" id="eff" min="30" max="95" step="5" value="75">

    <div class="big-out">
      <div class="lbl" id="outLbl">Предотвращённый ущерб в год</div>
      <div class="amt" id="amount">—</div>
      <div class="per" id="perUser">—</div>
    </div>

    <div class="rows">
      <div class="r"><span class="rl" id="r1">Средний ущерб на случай</span><span class="rv" id="avgLoss">—</span></div>
      <div class="r"><span class="rl" id="r2">Ожидаемых жертв среди пользователей/год</span><span class="rv" id="victims">—</span></div>
      <div class="r"><span class="rl" id="r3">Из них защищено Qalqan AI</span><span class="rv" id="saved">—</span></div>
    </div>
    <div class="disc" id="disc">Оценка. Источник базовых цифр: официальная статистика МВД/Нацбанка РК за 2025 г. Расчёт: (население-риск × частота × средний ущерб × охват × эффективность).</div>
  </div>

  <div class="foot">Qalqan AI · Экономика кибербезопасности · <a href="/">Проверить сайт</a> · <a href="/help"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m4.93 19.07 4.24-4.24"/></svg> Обманули?</a></div>
</div>

<script>
// Base facts (KZ 2025): ~26 300 cases, 16.4bn ₸ over 10 months → annualized.
const CASES_YR = 26300 * 12/10;         // annualized cases ≈ 31 560
const LOSS_YR = 16.4e9 * 12/10;         // annualized ₸ loss ≈ 19.68bn
const AVG_LOSS = LOSS_YR / CASES_YR;    // ≈ 623 000 ₸ per case
const ADULTS_KZ = 13500000;             // ~adult population exposed
const CASE_RATE = CASES_YR / ADULTS_KZ; // annual victim probability

const I18N={
  ru:{h1:'Экономический эффект',sub:'Сколько денег Qalqan AI может сберечь для граждан Казахстана. Расчёт основан на официальной статистике 2025 года.',
    s1:'украдено за 10 мес. 2025 (×29 к 2024)',s2:'случаев кибермошенничества (+86%)',
    lb1:'Пользователей Qalqan AI: ',lb2:'Эффективность блокировки: ',outLbl:'Предотвращённый ущерб в год',
    r1:'Средний ущерб на случай',r2:'Ожидаемых жертв среди пользователей/год',r3:'Из них защищено Qalqan AI',
    perUser:u=>`≈ ${u} ₸ сбережено на пользователя в год`,
    disc:'Оценка. Источник базовых цифр: официальная статистика МВД/Нацбанка РК за 2025 г. Расчёт: (население-риск × частота × средний ущерб × охват × эффективность).'},
  kk:{h1:'Экономикалық әсер',sub:'Qalqan AI Қазақстан азаматтары үшін қанша ақша үнемдей алады. Есеп 2025 жылғы ресми статистикаға негізделген.',
    s1:'2025 жылдың 10 айында ұрланды (2024-ке ×29)',s2:'кибералаяқтық дерегі (+86%)',
    lb1:'Qalqan AI қолданушылары: ',lb2:'Блоктау тиімділігі: ',outLbl:'Жылына болдырмаған залал',
    r1:'Бір дерекке орташа залал',r2:'Қолданушылар арасында күтілетін құрбандар/жыл',r3:'Оның ішінде Qalqan AI қорғады',
    perUser:u=>`≈ жылына бір қолданушыға ${u} ₸ үнемделді`,
    disc:'Бағалау. Негізгі сандар көзі: ҚР ІІМ/Ұлттық банктің 2025 ж. ресми статистикасы. Есеп: (тәуекел-халық × жиілік × орташа залал × қамту × тиімділік).'}
};
let L=localStorage.getItem('qlang')||'ru'; if(L!=='kk'&&L!=='ru')L='ru';
const $=s=>document.querySelector(s);
const fmt=n=>Math.round(n).toLocaleString('ru-RU').replace(/,/g,' ');
function money(n){
  if(n>=1e9) return (n/1e9).toFixed(1).replace('.',',')+' млрд ₸';
  if(n>=1e6) return (n/1e6).toFixed(1).replace('.',',')+' млн ₸';
  return fmt(n)+' ₸';
}
function calc(){
  const users=+$('#users').value, eff=+$('#eff').value/100;
  const victims=users*CASE_RATE;
  const saved=victims*eff;
  const prevented=saved*AVG_LOSS;
  const perUser=prevented/users;
  $('#vUsers').textContent=fmt(users);
  $('#vEff').textContent=(eff*100)+'%';
  $('#amount').textContent=money(prevented);
  $('#perUser').textContent=I18N[L].perUser(fmt(perUser));
  $('#avgLoss').textContent=money(AVG_LOSS);
  $('#victims').textContent=fmt(victims);
  $('#saved').textContent=fmt(saved);
}
function applyLang(l){
  L=(l==='kk'||l==='ru')?l:'ru'; localStorage.setItem('qlang',L);
  const D=I18N[L];
  document.querySelectorAll('.lang button').forEach(b=>b.classList.toggle('on',b.dataset.l===L));
  $('#h1').textContent=D.h1; $('#sub').textContent=D.sub; $('#s1').textContent=D.s1; $('#s2').textContent=D.s2;
  $('#lb1').firstChild.textContent=D.lb1; $('#lb2').firstChild.textContent=D.lb2;
  $('#outLbl').textContent=D.outLbl; $('#r1').textContent=D.r1; $('#r2').textContent=D.r2; $('#r3').textContent=D.r3;
  $('#disc').textContent=D.disc; document.documentElement.lang=L;
  calc();
}
$('#users').addEventListener('input',calc);
$('#eff').addEventListener('input',calc);
document.querySelectorAll('.lang button').forEach(b=>b.addEventListener('click',()=>applyLang(b.dataset.l)));
applyLang(L);
</script>
</body>
</html>"""

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

<script>
const $=s=>document.querySelector(s);
let results=[];
$('#upload').onclick=()=>$('#file').click();
$('#file').addEventListener('change',()=>{
  const f=$('#file').files[0]; if(!f) return;
  const rd=new FileReader();
  rd.onload=()=>{
    // CSV: take the first column of each line; TXT: line as-is
    const lines=String(rd.result).split(/\\r?\\n/).map(l=>l.split(/[,;\\t]/)[0].trim()).filter(Boolean);
    $('#urls').value=lines.join('\\n');
  };
  rd.readAsText(f);
});
function parseUrls(){
  return [...new Set($('#urls').value.split(/\\r?\\n/).map(s=>s.trim()).filter(s=>s&&!s.startsWith('#')&&s.includes('.')))].slice(0,150);
}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function run(){
  const urls=parseUrls();
  if(!urls.length){alert('Вставьте хотя бы один URL');return}
  const btn=$('#go');btn.disabled=true;btn.textContent='Проверяем...';
  results=[];$('#tbody').innerHTML='';$('#tblwrap').style.display='block';
  $('#prog').style.display='block';$('#sum').style.display='none';$('#dlrow').style.display='none';
  const esc=t=>{const d=document.createElement('div');d.textContent=t;return d.innerHTML};
  for(let i=0;i<urls.length;i+=15){
    const chunk=urls.slice(i,i+15);
    try{
      const r=await fetch('/batch',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({urls:chunk,lang:'ru'})});
      if(r.status===429){ // rate-limited: wait and retry this chunk once
        await sleep(35000);i-=15;continue;
      }
      const d=await r.json();
      for(const res of (d.results||[])){
        results.push(res);
        const v=(res.verdict||'?').toUpperCase();
        $('#tbody').insertAdjacentHTML('beforeend',
          `<tr><td>${esc(res.url||'')}</td><td class="v-${v}">${v}</td><td>${res.threat_score??''}</td><td>${esc(res.source||res.top_source||'')}</td></tr>`);
      }
    }catch(e){ chunk.forEach(u=>{results.push({url:u,verdict:'ERROR',threat_score:'',source:'network'});}); }
    $('#progbar').style.width=Math.min(100,Math.round(100*(i+15)/urls.length))+'%';
    if(i+15<urls.length) await sleep(4000);  // stay under the per-minute rate limit
  }
  $('#progbar').style.width='100%';
  const d=results.filter(r=>r.verdict==='DANGEROUS').length,
        s2=results.filter(r=>r.verdict==='SUSPICIOUS').length,
        ok=results.filter(r=>r.verdict==='SAFE').length;
  $('#sum').innerHTML=`<div class="pill d"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.86 2h8.28L22 7.86v8.28L16.14 22H7.86L2 16.14V7.86z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg> Опасных: ${d}</div><div class="pill s"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Подозрительных: ${s2}</div><div class="pill ok"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> Чистых: ${ok}</div><div class="pill">Всего: ${results.length}</div>`;
  $('#sum').style.display='flex';$('#dlrow').style.display='flex';
  btn.disabled=false;btn.textContent='Проверить список';
}
$('#go').onclick=run;
$('#dl').onclick=()=>{
  const head='url,verdict,score,source\\n';
  const body=results.map(r=>`"${String(r.url||'').replace(/"/g,'""')}",${r.verdict||''},${r.threat_score??''},${r.source||r.top_source||''}`).join('\\n');
  const blob=new Blob([head+body],{type:'text/csv'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='qalqan-batch-report.csv';a.click();
};
</script>
</body>
</html>"""

SCREEN_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Проверка скриншота</title>
<meta name="description" content="Загрузи скриншот подозрительной переписки, SMS или сайта — AI прочитает и скажет, мошенничество ли это.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0e16;--card:#111827;--card2:#0d1424;--cyan:#7aa2f7;--red:#f7768e;--amber:#e0af68;--green:#9ece6a;--tx:#e7ebf3;--mut:#7d8aa0;--bd:#1e293b}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font-family:'Inter',-apple-system,sans-serif;min-height:100vh;padding:20px}
.wrap{max-width:640px;margin:0 auto}
.top{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
.top a{color:var(--mut);text-decoration:none;font-size:14px}.top a:hover{color:var(--cyan)}
h1{font-size:24px;font-weight:800}
.sub{color:var(--mut);font-size:13.5px;margin:8px 0 18px;line-height:1.6}
.card{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:20px}
.drop{border:2px dashed var(--bd);border-radius:14px;padding:34px 18px;text-align:center;cursor:pointer;transition:border-color .15s}
.drop:hover,.drop.over{border-color:var(--cyan)}
.drop .big{font-size:34px}
.drop .t{font-weight:700;margin-top:8px}
.drop .h{font-size:12.5px;color:var(--mut);margin-top:6px;line-height:1.5}
#file{display:none}
#preview{max-width:100%;max-height:260px;border-radius:10px;margin-top:14px;display:none}
.btn{width:100%;margin-top:14px;background:var(--cyan);border:none;border-radius:10px;color:#04121a;font-weight:800;font-size:14px;padding:13px;cursor:pointer;font-family:inherit;display:none}
.btn:disabled{opacity:.5}
.res{margin-top:16px;padding:16px;border-radius:12px;border:1px solid var(--bd);display:none;font-size:13.5px;line-height:1.65;white-space:pre-wrap}
.res.d{border-color:rgba(247,118,142,.5);background:rgba(247,118,142,.07)}
.res.s{border-color:rgba(224,175,104,.5);background:rgba(224,175,104,.07)}
.res.ok{border-color:rgba(158,206,106,.5);background:rgba(158,206,106,.07)}
.priv{font-size:11.5px;color:var(--mut);margin-top:12px;line-height:1.5}
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
  <div class="top"><h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg> Проверка скриншота</h1><a href="/">← Qalqan AI</a></div>
  <div class="sub">Пришло подозрительное SMS, сообщение «из банка», объявление об «инвестициях»? Сделай скриншот и загрузи — AI прочитает текст и скажет, мошенничество ли это. Каз/рус/англ.</div>

  <div class="card">
    <div class="drop" id="drop">
      <div class="big"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg></div>
      <div class="t">Нажми или перетащи скриншот</div>
      <div class="h">JPG/PNG до 3 МБ · переписка, SMS, сайт, объявление</div>
    </div>
    <input id="file" type="file" accept="image/*">
    <img id="preview" alt="preview">
    <button class="btn" id="go">Проверить</button>
    <div class="res" id="res"></div>
    <div class="priv"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg> Скриншот анализируется на лету и не сохраняется. Не загружай фото с личными данными без необходимости — закрась лишнее.</div>
  </div>

  <div class="foot">Qalqan AI · Groq Vision + Gemini · <a href="/">Проверить сайт</a> · <a href="/help"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m4.93 19.07 4.24-4.24"/></svg> Обманули?</a></div>
</div>

<script>
const QI={octagon:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.86 2h8.28L22 7.86v8.28L16.14 22H7.86L2 16.14V7.86z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>',alert:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',checkc:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',check:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',copy:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="8" width="14" height="14" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>'};
const $=s=>document.querySelector(s);
let b64=null;
const drop=$('#drop'),file=$('#file');
drop.onclick=()=>file.click();
drop.addEventListener('dragover',e=>{e.preventDefault();drop.classList.add('over')});
drop.addEventListener('dragleave',()=>drop.classList.remove('over'));
drop.addEventListener('drop',e=>{e.preventDefault();drop.classList.remove('over');if(e.dataTransfer.files[0])load(e.dataTransfer.files[0])});
file.addEventListener('change',()=>{if(file.files[0])load(file.files[0])});
function load(f){
  if(f.size>3.2*1024*1024){alert('Файл больше 3 МБ — сожмите или обрежьте скриншот.');return}
  const rd=new FileReader();
  rd.onload=()=>{
    const s=String(rd.result);
    b64=s.substring(s.indexOf(',')+1);
    $('#preview').src=s;$('#preview').style.display='block';
    $('#go').style.display='block';
    $('#res').style.display='none';
  };
  rd.readAsDataURL(f);
}
$('#go').onclick=async()=>{
  if(!b64)return;
  const btn=$('#go');btn.disabled=true;btn.textContent='AI читает скриншот...';
  const R=$('#res');R.className='res';R.style.display='block';R.textContent='Анализ (до 20 сек)...';
  try{
    const lang=localStorage.getItem('qlang')||'ru';
    const r=await fetch('/analyze-screen',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image_base64:b64,lang:lang==='kk'?'kk':lang==='en'?'en':'ru'})});
    if(r.status===429){R.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> Слишком часто — максимум 5 скриншотов в минуту.';btn.disabled=false;btn.textContent='Проверить';return}
    const d=await r.json();
    const v=(d.verdict||'').toUpperCase();
    const em=v==='DANGEROUS'?QI.octagon:v==='SUSPICIOUS'?QI.alert:QI.checkc;
    R.className='res '+(v==='DANGEROUS'?'d':v==='SUSPICIOUS'?'s':'ok');
    const esc=t=>{const x=document.createElement('div');x.textContent=t;return x.innerHTML};
    R.innerHTML=`${em} <b>${esc(v)} · ${esc(String(d.threat_score??'?'))}/100</b><br><br>${esc(d.detail||d.detail_ru||'')}`;
  }catch(e){R.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Ошибка анализа. Попробуйте позже.'}
  btn.disabled=false;btn.textContent='Проверить';
};
</script>
</body>
</html>"""
