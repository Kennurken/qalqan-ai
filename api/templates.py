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
<meta name="theme-color" content="#0a0e1a">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Qalqan AI","applicationCategory":"SecurityApplication","operatingSystem":"Web, Chrome, Firefox, Android, iOS","offers":{"@type":"Offer","price":"0","priceCurrency":"KZT"},"inLanguage":["kk","ru","en"],"url":"https://qalqan-ai-nu.vercel.app","description":"AI cybersecurity for Kazakhstan: phishing, phone scam, financial pyramids, gambling and procurement-fraud detection."}
</script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--cyan:#00d4ff;--cyan2:#00b8d9;--green:#22c55e;--red:#ef4444;--amber:#f59e0b;--bg:#0a0e1a;--bg2:#0f1629;--card:#131d35;--border:#1e2d4a;--text:#e2e8f0;--muted:#64748b}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;overflow-x:hidden}
a{color:var(--cyan);text-decoration:none}
/* SCANLINE */
body::before{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,212,255,.015) 2px,rgba(0,212,255,.015) 4px);pointer-events:none;z-index:0}
/* NAV */
nav{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(10,14,26,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:0 24px;height:56px;display:flex;align-items:center;justify-content:space-between}
.nav-logo{display:flex;align-items:center;gap:10px;font-weight:700;font-size:18px;color:var(--cyan)}
.nav-logo svg{width:28px;height:28px}
.nav-links{display:flex;gap:20px;font-size:14px}
.nav-links a{color:var(--muted);transition:color .2s}
.nav-links a:hover{color:var(--cyan)}
.nav-cta{background:var(--cyan);color:#0a0e1a;padding:7px 16px;border-radius:6px;font-weight:600;font-size:13px;transition:opacity .2s}
.nav-cta:hover{opacity:.85}
/* HERO */
.hero{position:relative;min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:100px 24px 60px}
.hero-glow{position:absolute;top:20%;left:50%;transform:translateX(-50%);width:600px;height:600px;background:radial-gradient(ellipse,rgba(0,212,255,.12) 0%,transparent 70%);pointer-events:none}
.hero-badge{display:inline-flex;align-items:center;gap:6px;background:rgba(0,212,255,.1);border:1px solid rgba(0,212,255,.25);border-radius:20px;padding:5px 14px;font-size:12px;color:var(--cyan);margin-bottom:24px;letter-spacing:.5px}
.hero-badge span{width:6px;height:6px;border-radius:50%;background:var(--cyan);animation:pulse 2s infinite}
h1{font-size:clamp(36px,6vw,72px);font-weight:800;line-height:1.1;margin-bottom:20px;background:linear-gradient(135deg,#fff 30%,var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-sub{font-size:clamp(16px,2vw,20px);color:var(--muted);max-width:600px;margin:0 auto 40px;line-height:1.6}
/* CHECKER */
.checker{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:28px;max-width:600px;margin:0 auto;position:relative}
.checker-title{font-size:13px;color:var(--muted);margin-bottom:14px;text-align:left;text-transform:uppercase;letter-spacing:1px}
.checker-row{display:flex;gap:10px}
.checker-input{flex:1;background:#0a0e1a;border:1px solid var(--border);border-radius:8px;padding:12px 16px;color:var(--text);font-size:15px;outline:none;transition:border-color .2s}
.checker-input:focus{border-color:var(--cyan)}
.checker-input::placeholder{color:var(--muted)}
.checker-btn{background:var(--cyan);color:#0a0e1a;border:none;border-radius:8px;padding:12px 22px;font-weight:700;font-size:14px;cursor:pointer;transition:opacity .2s;white-space:nowrap}
.checker-btn:hover{opacity:.85}
.checker-btn:disabled{opacity:.5;cursor:not-allowed}
.result-box{margin-top:16px;padding:16px;border-radius:10px;border:1px solid;display:none;text-align:left;animation:fadeUp .2s ease}
.result-box.safe{border-color:rgba(34,197,94,.3);background:rgba(34,197,94,.06)}
.result-box.danger{border-color:rgba(239,68,68,.3);background:rgba(239,68,68,.06)}
.result-box.suspicious{border-color:rgba(245,158,11,.3);background:rgba(245,158,11,.06)}
.result-verdict{font-size:18px;font-weight:700;margin-bottom:4px}
.result-detail{font-size:13px;color:var(--muted);line-height:1.5}
/* STATS */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;max-width:900px;margin:60px auto 0;padding:0 24px}
.stat-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px;text-align:center}
.stat-num{font-size:32px;font-weight:800;color:var(--cyan);font-variant-numeric:tabular-nums}
.stat-label{font-size:12px;color:var(--muted);margin-top:4px;text-transform:uppercase;letter-spacing:.5px}
/* FEATURES */
.section{padding:80px 24px;max-width:1100px;margin:0 auto}
.section-label{font-size:12px;color:var(--cyan);text-transform:uppercase;letter-spacing:2px;margin-bottom:12px}
.section-title{font-size:clamp(24px,4vw,40px);font-weight:700;margin-bottom:16px}
.section-sub{color:var(--muted);font-size:16px;max-width:500px;line-height:1.6}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:48px}
.feat-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:24px;transition:border-color .2s,transform .2s}
.feat-card:hover{border-color:rgba(0,212,255,.35);transform:translateY(-2px)}
.feat-icon{width:40px;height:40px;border-radius:10px;background:rgba(0,212,255,.1);display:flex;align-items:center;justify-content:center;margin-bottom:16px}
.feat-icon svg{width:20px;height:20px;stroke:var(--cyan);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.feat-title{font-size:15px;font-weight:600;margin-bottom:8px}
.feat-desc{font-size:13px;color:var(--muted);line-height:1.6}
.demo-link{display:block;text-decoration:none;color:inherit}
.demo-link .feat-title{color:var(--cyan)}
.demo-arrow{font-size:12px;color:var(--cyan);margin-top:12px;font-weight:600}
/* PIPELINE */
.pipeline{background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:60px 24px}
.pipeline-inner{max-width:900px;margin:0 auto}
.pipeline-steps{display:flex;flex-wrap:wrap;gap:0;margin-top:40px}
.pipe-step{flex:1;min-width:120px;position:relative;padding:20px 16px;text-align:center}
.pipe-step:not(:last-child)::after{content:'→';position:absolute;right:-8px;top:50%;transform:translateY(-50%);color:var(--cyan);font-size:18px}
.pipe-num{width:32px;height:32px;border-radius:50%;border:2px solid var(--cyan);color:var(--cyan);font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center;margin:0 auto 10px}
.pipe-name{font-size:12px;color:var(--muted);font-weight:500}
/* TELEGRAM */
.tg-section{padding:80px 24px;text-align:center}
.tg-card{max-width:500px;margin:0 auto;background:var(--card);border:1px solid var(--border);border-radius:20px;padding:40px}
.tg-icon{width:60px;height:60px;background:rgba(0,212,255,.1);border-radius:16px;display:flex;align-items:center;justify-content:center;margin:0 auto 20px}
.tg-icon svg{width:30px;height:30px;fill:var(--cyan)}
.tg-title{font-size:22px;font-weight:700;margin-bottom:10px}
.tg-sub{color:var(--muted);font-size:14px;line-height:1.6;margin-bottom:24px}
.tg-btn{display:inline-flex;align-items:center;gap:8px;background:var(--cyan);color:#0a0e1a;padding:13px 28px;border-radius:10px;font-weight:700;font-size:15px;transition:opacity .2s}
.tg-btn:hover{opacity:.85;color:#0a0e1a}
/* TECH STACK */
.stack-grid{display:flex;flex-wrap:wrap;gap:10px;margin-top:32px}
.stack-tag{background:var(--card);border:1px solid var(--border);border-radius:6px;padding:6px 14px;font-size:13px;color:var(--muted);font-family:monospace}
/* FOOTER */
footer{background:var(--bg2);border-top:1px solid var(--border);padding:40px 24px;text-align:center}
.footer-logo{font-size:20px;font-weight:700;color:var(--cyan);margin-bottom:8px}
.footer-sub{font-size:13px;color:var(--muted);margin-bottom:16px}
.footer-links{display:flex;justify-content:center;gap:20px;font-size:13px;flex-wrap:wrap}
/* ANIMATIONS */
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
@keyframes fadeUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
/* RESPONSIVE */
@media(max-width:600px){
  .nav-links{display:none}
  .checker-row{flex-direction:column}
  .pipe-step:not(:last-child)::after{display:none}
}
</style>
</head>
<body>

<!-- NAV -->
<nav>
  <div class="nav-logo">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      <polyline points="9 12 11 14 15 10"/>
    </svg>
    Qalqan AI
  </div>
  <div class="nav-links">
    <a href="#features">Функции</a>
    <a href="#pipeline">Pipeline</a>
    <a href="#telegram">Telegram</a>
    <a href="#tech">Технологии</a>
  </div>
  <a class="nav-cta" href="/install">Орнату</a>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-glow"></div>
  <div style="position:relative;z-index:1">
    <div class="hero-badge"><span></span>v5.1.0 · Қазақстан үшін</div>
    <h1>Фишингтен<br>AI Қорғанысы</h1>
    <p class="hero-sub">Qalqan AI — Chrome кеңейтімі, ол барған сайын автоматты тексереді. Фишинг, пирамидалар, гемблинг — бет жүктелмей бұрын бұғаттайды.</p>

    <!-- LIVE CHECKER -->
    <div class="checker">
      <div class="checker-title">Сайтты тексеру / Проверить сайт</div>
      <div class="checker-row">
        <input class="checker-input" id="urlInput" type="text" placeholder="kaspi-bonus123.kz немесе https://..." autocomplete="off">
        <button class="checker-btn" id="checkBtn" onclick="checkUrl()">Тексеру</button>
      </div>
      <div class="result-box" id="resultBox">
        <div class="result-verdict" id="resultVerdict"></div>
        <div class="result-detail" id="resultDetail"></div>
      </div>
    </div>

    <!-- STATS -->
    <div class="stats" id="statsRow">
      <div class="stat-card"><div class="stat-num" id="statChecked">—</div><div class="stat-label">Тексерілді</div></div>
      <div class="stat-card"><div class="stat-num" id="statBlocked">—</div><div class="stat-label">Бұғатталды</div></div>
      <div class="stat-card"><div class="stat-num" id="statDomains">390+</div><div class="stat-label">Офлайн база</div></div>
      <div class="stat-card"><div class="stat-num">6</div><div class="stat-label">Анықтау деңгейі</div></div>
    </div>
  </div>
</section>

<!-- FEATURES -->
<section class="section" id="features">
  <div class="section-label">Функционал</div>
  <div class="section-title">Не қорғайды?</div>
  <p class="section-sub">6 деңгейлі pipeline — 1 мс кеш-тексеруден AI анализіне дейін</p>

  <div class="features-grid">
    <div class="feat-card">
      <div class="feat-icon"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg></div>
      <div class="feat-title">Фишинг сайттары</div>
      <div class="feat-desc">Kaspi, eGov, Halyk Bank клондарын анықтайды. Беттің жүктелуіне дейін бұғаттайды.</div>
    </div>
    <div class="feat-card">
      <div class="feat-icon"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>
      <div class="feat-title">Қаржылық пирамидалар</div>
      <div class="feat-desc">166+ белгілі пирамида схемасы базасы. Finiko, МММ, HYIP сайттарын автоматты анықтайды.</div>
    </div>
    <div class="feat-card">
      <div class="feat-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg></div>
      <div class="feat-title">Нелегал гемблинг</div>
      <div class="feat-desc">80+ ҚР-да тыйым салынған сайт. 1xbet, Mostbet, Pin-Up — браузерде ашылмайды.</div>
    </div>
    <div class="feat-card">
      <div class="feat-icon"><svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div>
      <div class="feat-title">Скриншот анализі</div>
      <div class="feat-desc">Vision AI арқылы бет скриншотын тексереді. Жасырын алаяқтық элементтерін анықтайды.</div>
    </div>
    <div class="feat-card">
      <div class="feat-icon"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div>
      <div class="feat-title">SMS / Хабарлама тексеру</div>
      <div class="feat-desc">Алынған SMS немесе хабарламадағы алаяқтық сілтемелерді AI арқылы анализдейді.</div>
    </div>
    <div class="feat-card">
      <div class="feat-icon"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
      <div class="feat-title">Goszakup тендер тексеру</div>
      <div class="feat-desc">goszakup.gov.kz тендерлерінде алаяқтық белгілерін 10 ереже бойынша анықтайды.</div>
    </div>
  </div>
</section>

<!-- PIPELINE -->
<section class="pipeline" id="pipeline">
  <div class="pipeline-inner">
    <div class="section-label">Архитектура</div>
    <div class="section-title">6-деңгейлі анықтау</div>
    <div class="pipeline-steps">
      <div class="pipe-step"><div class="pipe-num">1</div><div class="pipe-name">Ақ тізім</div></div>
      <div class="pipe-step"><div class="pipe-num">2</div><div class="pipe-name">Redis кэш</div></div>
      <div class="pipe-step"><div class="pipe-num">3</div><div class="pipe-name">Офлайн DB</div></div>
      <div class="pipe-step"><div class="pipe-num">4</div><div class="pipe-name">KZ Intel</div></div>
      <div class="pipe-step"><div class="pipe-num">5</div><div class="pipe-name">Сыртқы DB + домен</div></div>
      <div class="pipe-step"><div class="pipe-num">6</div><div class="pipe-name">Groq / Gemini AI</div></div>
    </div>
  </div>
</section>

<!-- DEMO / PLATFORMS -->
<section class="section" id="demo">
  <div class="section-label">Демо</div>
  <div class="section-title">Бәрі тірі — ашып көріңіз</div>
  <p class="section-sub">Жұмыс істеп тұрған платформалар мен панельдер</p>
  <div class="features-grid">
    <a class="feat-card demo-link" href="/dashboard?demo=1">
      <div class="feat-title">📊 Реттеуші панелі</div>
      <div class="feat-desc">Облыстар бойынша қауіп картасы, динамика, топ қауіпті домендер.</div>
      <div class="demo-arrow">Ашу →</div>
    </a>
    <a class="feat-card demo-link" href="/goszakup/graph">
      <div class="feat-title">🕸️ Госзакуп фрод графы</div>
      <div class="feat-desc">Аффилированность, сговор, картель — байланыс графы.</div>
      <div class="demo-arrow">Ашу →</div>
    </a>
    <a class="feat-card demo-link" href="/m">
      <div class="feat-title">📱 Мобиль қосымша</div>
      <div class="feat-desc">Офлайн жұмыс істейді, телефон экранына орнатылады (PWA).</div>
      <div class="demo-arrow">Ашу →</div>
    </a>
    <a class="feat-card demo-link" href="https://t.me/QalqanAI_bot" target="_blank" rel="noopener">
      <div class="feat-title">🤖 Telegram бот</div>
      <div class="feat-desc">Дауыс / SMS / сілтеме тексеру, KZ-CERT-ке хабарлау.</div>
      <div class="demo-arrow">Ашу →</div>
    </a>
    <a class="feat-card demo-link" href="/stats">
      <div class="feat-title">📈 Тірі статистика</div>
      <div class="feat-desc">Нақты деректер: тексерулер, вердиктер, трендтер.</div>
      <div class="demo-arrow">Ашу →</div>
    </a>
    <a class="feat-card demo-link" href="/feed/kz">
      <div class="feat-title">🌐 KZ Threat Feed</div>
      <div class="feat-desc">Ашық дерекқор (CC-BY) — басқа жүйелер пайдалана алады.</div>
      <div class="demo-arrow">Ашу →</div>
    </a>
  </div>
</section>

<!-- TELEGRAM -->
<section class="tg-section" id="telegram">
  <div class="tg-card">
    <div class="tg-icon">
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12L7.26 13.561l-2.94-.916c-.64-.203-.654-.64.135-.954l11.566-4.461c.537-.194 1.006.131.873.991z"/>
      </svg>
    </div>
    <div class="tg-title">Telegram Bot</div>
    <div class="tg-sub">Telegram арқылы кез-келген сілтемені тексер. Пәрмендер: /check, /report, /stats</div>
    <a class="tg-btn" href="https://t.me/QalqanAI_bot" target="_blank">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="#0a0e1a"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12L7.26 13.561l-2.94-.916c-.64-.203-.654-.64.135-.954l11.566-4.461c.537-.194 1.006.131.873.991z"/></svg>
      @QalqanAI_bot ашу
    </a>
  </div>
</section>

<!-- TECH STACK -->
<section class="section" id="tech">
  <div class="section-label">Технологиялар</div>
  <div class="section-title">Технологиялық стек</div>
  <div class="stack-grid">
    <span class="stack-tag">Python 3.11</span>
    <span class="stack-tag">FastAPI</span>
    <span class="stack-tag">React 19</span>
    <span class="stack-tag">Chrome MV3</span>
    <span class="stack-tag">Groq llama-3.3-70b</span>
    <span class="stack-tag">Gemini 2.5-flash</span>
    <span class="stack-tag">30+ URL lexical features</span>
    <span class="stack-tag">Upstash Redis</span>
    <span class="stack-tag">Supabase / PostgreSQL</span>
    <span class="stack-tag">Vercel Serverless</span>
    <span class="stack-tag">PhishTank API</span>
    <span class="stack-tag">Google Safe Browsing</span>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-logo">🛡 Qalqan AI</div>
  <div class="footer-sub">Қазақстандық пайдаланушыларды цифрлық қауіптерден қорғау · v5.1.0</div>
  <div class="footer-links">
    <a href="https://github.com/Kennurken/qalqan-ai" target="_blank">GitHub</a>
    <a href="/m">📱 Мобиль қосымша</a>
    <a href="/docs">API Docs</a>
    <a href="/stats">Statistics</a>
    <a href="/dashboard">Панель регулятора</a>
    <a href="/goszakup/graph">Граф госзакупок</a>
    <a href="/partners">API для партнёров</a>
    <a href="/health">Health</a>
  </div>
  <div style="margin-top:16px;font-size:12px;color:var(--muted)">
    Разработчик: Қыдырбек Елдос Нүркенұлы · Кызылординский университет имени Коркыт ата<br>
    ДЭР по Кызылординской области · 2026
  </div>
</footer>

<script>
async function checkUrl() {
  const input = document.getElementById('urlInput');
  const btn = document.getElementById('checkBtn');
  const box = document.getElementById('resultBox');
  const verdict = document.getElementById('resultVerdict');
  const detail = document.getElementById('resultDetail');

  let url = input.value.trim();
  if (!url) return;
  if (!url.startsWith('http')) url = 'https://' + url;

  btn.disabled = true;
  btn.textContent = '...';
  box.style.display = 'none';

  try {
    const res = await fetch('/check', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({url, lang:'ru'})
    });
    const data = await res.json();

    box.className = 'result-box';
    const v = data.verdict || 'UNKNOWN';
    const score = data.threat_score || 0;

    if (v === 'SAFE') {
      box.classList.add('safe');
      verdict.textContent = '✓ БЕЗОПАСНО (' + score + '/100)';
      verdict.style.color = '#22c55e';
    } else if (v === 'DANGEROUS') {
      box.classList.add('danger');
      verdict.textContent = '✗ ОПАСНО (' + score + '/100)';
      verdict.style.color = '#ef4444';
    } else {
      box.classList.add('suspicious');
      verdict.textContent = '⚠ ПОДОЗРИТЕЛЬНО (' + score + '/100)';
      verdict.style.color = '#f59e0b';
    }

    detail.textContent = data.detail_ru || data.detail || data.detail_kk || '';
    box.style.display = 'block';
  } catch(e) {
    box.className = 'result-box suspicious';
    box.style.display = 'block';
    verdict.textContent = 'Ошибка соединения';
    verdict.style.color = '#f59e0b';
    detail.textContent = e.message;
  }

  btn.disabled = false;
  btn.textContent = 'Тексеру';
}

document.getElementById('urlInput').addEventListener('keydown', e => {
  if (e.key === 'Enter') checkUrl();
});

// Load stats
async function loadStats() {
  try {
    const res = await fetch('/stats');
    const data = await res.json();
    const t = data.today || {};
    const el = id => document.getElementById(id);
    if (t.total_checks) el('statChecked').textContent = t.total_checks.toLocaleString();
    if (t.dangerous_blocked) el('statBlocked').textContent = t.dangerous_blocked.toLocaleString();
  } catch {}
}
loadStats();
</script>
</body>
</html>"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Панель регулятора</title>
<style>
:root{--bg:#0a0e1a;--panel:#111827;--panel2:#0d1424;--cyan:#00d4ff;--red:#ff3b5c;--amber:#ffb020;--green:#22c55e;--tx:#e6edf6;--mut:#7d8aa0;--bd:#1e293b}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:24px;max-width:1280px;margin:0 auto}
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
.maplegend .grad{height:10px;width:120px;border-radius:5px;background:linear-gradient(90deg,#0d1424,#ff3b5c)}
@media(max-width:820px){.grid{grid-template-columns:1fr}.kzmap{grid-template-rows:repeat(5,40px)}}
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

<div class="kpis" id="kpis"></div>

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
      <div class="legend"><span><span class="dot" style="background:#00d4ff"></span>Всего проверок</span><span><span class="dot" style="background:#ff3b5c"></span>Угрозы (опасн.+подозр.)</span></div>
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
    `<path d="${path(series.map(s=>s.total))}" fill="none" stroke="#00d4ff" stroke-width="2.5"/>`+
    `<path d="${path(series.map(s=>s.threats))}" fill="none" stroke="#ff3b5c" stroke-width="2.5"/>`+
    `<text x="${pad}" y="14" fill="#7d8aa0" font-size="11">${fmt(mx)}</text>`;
}

function renderDonut(vd){
  const order=[['DANGEROUS','#ff3b5c'],['SUSPICIOUS','#ffb020'],['SAFE','#22c55e']];
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
    const col=frac>0.45?'#fff':'#e6edf6';
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
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0e1a;color:#e2e8f0;font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh}
.navbar{background:rgba(10,14,26,.95);border-bottom:1px solid #1e2d4a;padding:16px 24px;display:flex;align-items:center;justify-content:space-between}
.logo{color:#00d4ff;font-weight:700;font-size:18px;text-decoration:none}
a{color:#00d4ff}
.page{max-width:800px;margin:0 auto;padding:48px 24px}
h1{font-size:32px;font-weight:800;margin-bottom:8px}
.subtitle{color:#64748b;margin-bottom:48px}
.tab-bar{display:flex;gap:4px;margin-bottom:32px;background:#0f1629;border-radius:10px;padding:4px}
.tab{flex:1;text-align:center;padding:10px;border-radius:7px;cursor:pointer;font-size:14px;font-weight:600;color:#64748b;transition:all .2s}
.tab.active{background:#131d35;color:#00d4ff}
.panel{display:none}
.panel.active{display:block}
.step{display:flex;gap:16px;margin-bottom:24px;align-items:flex-start}
.step-num{width:36px;height:36px;border-radius:50%;background:rgba(0,212,255,.1);border:2px solid rgba(0,212,255,.3);color:#00d4ff;font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px}
.step-body h3{font-size:15px;font-weight:600;margin-bottom:6px}
.step-body p{font-size:14px;color:#94a3b8;line-height:1.6}
code{background:#131d35;border:1px solid #1e2d4a;border-radius:4px;padding:2px 7px;font-family:monospace;font-size:13px;color:#00d4ff}
.dl-btn{display:inline-flex;align-items:center;gap:8px;background:#00d4ff;color:#0a0e1a;padding:13px 28px;border-radius:10px;font-weight:700;font-size:15px;text-decoration:none;margin:12px 0}
.dl-btn:hover{opacity:.85}
.warn{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:8px;padding:12px 16px;font-size:13px;color:#f59e0b;margin:16px 0}
.note{background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.15);border-radius:8px;padding:12px 16px;font-size:13px;color:#94a3b8;margin:16px 0}
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
<style>
:root{--bg:#0a0e1a;--card:#111827;--card2:#0d1424;--cyan:#00d4ff;--red:#ff3b5c;--amber:#ffb020;--green:#22c55e;--tx:#e6edf6;--mut:#7d8aa0;--bd:#1e293b}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:14px;min-height:100vh}
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
      return `<div class="kzt" style="background:${c};color:${f>.45?'#fff':'#e6edf6'}">${nm}<b>${r.threats||0}</b></div>`;
    }).join('');
  }catch(e){ $('#kzmap').innerHTML='<div class="spin">Қате</div>'; }
}
</script>
</body></html>"""


GRAPH_HTML = """<!DOCTYPE html>
<html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Граф госзакупок</title>
<style>
:root{--bg:#0a0e1a;--panel:#111827;--bd:#1e293b;--tx:#e6edf6;--mut:#7d8aa0;--cyan:#00d4ff;--red:#ef4444}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:20px;max-width:1280px;margin:0 auto}
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
.DANGEROUS{color:var(--red);font-weight:800}.SUSPICIOUS{color:#f59e0b;font-weight:800}.SAFE{color:#22c55e;font-weight:800}
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
      <span><span class="dot" style="background:#00d4ff"></span>Заказчик</span>
      <span><span class="dot" style="background:#a855f7"></span>Поставщик</span>
      <span><span class="dot" style="background:#f59e0b"></span>Учредитель</span>
      <span><span class="dot" style="background:#22c55e"></span>Адрес</span>
      <span><span class="dot" style="background:#ef4444"></span>Чиновник</span>
      <span><span class="dot" style="background:#ef4444"></span>— красная связь = подозрение</span>
    </div>
  </div>
  <div class="card"><h3 style="font-size:14px;margin-bottom:12px">🚩 Найденные схемы</h3><div id="findings"></div></div>
</div>
<div class="foot">Qalqan AI · граф строится из данных закупок (заказчик↔поставщик↔учредитель↔адрес↔чиновник)</div>
<script>
const COL={customer:'#00d4ff',supplier:'#a855f7',founder:'#f59e0b',address:'#22c55e',official:'#ef4444'};
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
  edges.forEach(e=>{const a=by[e.source],b=by[e.target];if(!a||!b)return;const c=e.risk?'#ef4444':'#334155';
    s+=`<line x1="${a.x.toFixed(1)}" y1="${a.y.toFixed(1)}" x2="${b.x.toFixed(1)}" y2="${b.y.toFixed(1)}" stroke="${c}" stroke-width="${e.risk?2.6:1}" ${e.risk?'stroke-dasharray="5 3"':''}/>`;});
  nodes.forEach(n=>{const c=COL[n.type]||'#888',r=(n.type==='customer'||n.type==='supplier')?13:8;
    s+=`<circle cx="${n.x.toFixed(1)}" cy="${n.y.toFixed(1)}" r="${r}" fill="${c}" stroke="${n.risk?'#ef4444':'#0a0e1a'}" stroke-width="${n.risk?3:1.5}"/>`;
    s+=`<text x="${n.x.toFixed(1)}" y="${(n.y-r-5).toFixed(1)}" fill="#e6edf6" font-size="10" text-anchor="middle">${(n.label||'').slice(0,22)}</text>`;});
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
<meta name="theme-color" content="#0a0e1a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="manifest" href="/manifest.webmanifest">
<style>
:root{--bg:#0a0e1a;--panel:#111827;--bd:#1e293b;--tx:#e6edf6;--mut:#8194ad;--cyan:#00d4ff;--red:#ef4444;--amber:#f59e0b;--green:#22c55e}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding-bottom:calc(72px + env(safe-area-inset-bottom))}
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
function vcolor(v){return v==='DANGEROUS'?'#ef4444':v==='SUSPICIOUS'?'#f59e0b':'#22c55e'}
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
<style>
:root{--bg:#0a0e1a;--panel:#111827;--bd:#1e293b;--tx:#e6edf6;--mut:#8194ad;--cyan:#00d4ff;--green:#22c55e}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:24px;max-width:860px;margin:0 auto;line-height:1.6}
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
