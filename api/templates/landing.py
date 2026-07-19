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
<script src="/static/landing.js?v=__V__" defer></script>
</body>
</html>"""
