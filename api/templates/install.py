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
<div style="max-width:760px;margin:26px auto 0;padding:0 4px">
  <h2 style="font-size:19px;font-weight:800;margin-bottom:12px">Что умеет расширение v5.2</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;font-size:13.5px;line-height:1.55">
    <div style="border:1px solid var(--bd,#1e293b);border-radius:12px;padding:13px"><b>Блок до загрузки</b><br>Опасный сайт перехватывается прежде, чем страница откроется. Офлайн-база 390+ доменов работает без интернета.</div>
    <div style="border:1px solid var(--bd,#1e293b);border-radius:12px;padding:13px"><b>Бейджи в поиске</b><br>Google, Яндекс, Bing, DuckDuckGo: метка безопасности у каждого результата до клика.</div>
    <div style="border:1px solid var(--bd,#1e293b);border-radius:12px;padding:13px"><b>Защита в мессенджерах</b><br>Telegram Web и WhatsApp Web: опасные ссылки в чатах помечаются прямо в переписке.</div>
    <div style="border:1px solid var(--bd,#1e293b);border-radius:12px;padding:13px"><b>Страж паролей</b><br>Поле пароля на подозрительном сайте — красное предупреждение до того, как вы начали печатать.</div>
    <div style="border:1px solid var(--bd,#1e293b);border-radius:12px;padding:13px"><b>Проверка по клику</b><br>Правый клик на любой ссылке → «Qalqan AI: проверить» — вердикт за секунды.</div>
    <div style="border:1px solid var(--bd,#1e293b);border-radius:12px;padding:13px"><b>Анализ страницы</b><br>Формы кражи данных, фейк-розыгрыши, фингерпринтинг — детект прямо в DOM.</div>
  </div>
</div>
</body></html>"""
