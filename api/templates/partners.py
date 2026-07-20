PARTNERS_HTML = r"""<!DOCTYPE html>
<html lang="ru"><head>
<script>document.documentElement.dataset.theme=localStorage.getItem("qtheme")||"dark";</script>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Qalqan AI — Партнёрский API (B2G)</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:oklch(16% .02 255);--card:oklch(21.5% .025 260);--card2:oklch(19% .028 258);--cyan:oklch(72% .12 265);--red:oklch(70% .15 15);--amber:oklch(78% .11 78);--green:oklch(80% .13 130);--tx:oklch(93% .01 250);--mut:oklch(63% .02 250);--bd:oklch(30% .03 258);--panel:var(--card);--s1:4px;--s2:8px;--s3:12px;--s4:16px;--s5:24px;--s6:36px}
[data-theme="light"]{--bg:oklch(96.5% .006 250);--card:oklch(99.2% .003 250);--card2:oklch(94.5% .008 250);--cyan:oklch(50% .15 262);--red:oklch(54% .17 18);--amber:oklch(58% .12 78);--green:oklch(52% .12 140);--tx:oklch(26% .02 255);--mut:oklch(48% .02 250);--bd:oklch(87% .012 250)}
[data-theme="light"] body{background:var(--bg)}
.qtgl{background:var(--card2);border:1px solid var(--bd);border-radius:9px;color:var(--mut);cursor:pointer;padding:7px 9px;line-height:0;transition:color .2s,border-color .2s}
.qtgl:hover{color:var(--tx);border-color:var(--cyan)}
.qtgl .sun{display:none}.qtgl .moon{display:block}
[data-theme="light"] .qtgl .sun{display:block}[data-theme="light"] .qtgl .moon{display:none}
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
<pre>curl -X POST https://qalqan-ai-nu.vercel.app/v1/check \
  -H "X-API-Key: qalqan-demo-2026" \
  -H "Content-Type: application/json" \
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

<h2>Trial-ключ за 30 секунд (self-service)</h2>
<div class="card">
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px">
    <input id="korg" placeholder="Организация" aria-label="Организация" style="flex:1;min-width:180px;background:var(--card2,#0d1424);border:1px solid var(--bd);border-radius:9px;color:var(--tx);padding:10px 12px;font-family:inherit">
    <input id="kemail" type="email" placeholder="email@company.kz" aria-label="Email" style="flex:1;min-width:180px;background:var(--card2,#0d1424);border:1px solid var(--bd);border-radius:9px;color:var(--tx);padding:10px 12px;font-family:inherit">
  </div>
  <button id="kgo" style="background:var(--cyan);border:none;border-radius:9px;color:#04121a;font-weight:700;padding:11px 18px;cursor:pointer;font-family:inherit">Получить trial-ключ</button>
  <div id="kout" style="margin-top:12px;font-size:13px;line-height:1.6"></div>
  <div style="font-size:11.5px;color:var(--mut);margin-top:8px">Trial: 30 запросов/мин, показывается один раз, храним только хеш. 2 ключа в день с одного IP.</div>
</div>

<h2>Получить боевой ключ</h2>
<div class="card">Напишите на <a href="mailto:kmarukob76@gmail.com">kmarukob76@gmail.com</a> с указанием организации.
Ключ выдаётся под конкретного партнёра, лимиты и логирование — индивидуально.</div>

<div class="foot">Qalqan AI · Республиканский конкурс ДЭР 2026 · <button class="qtgl" id="qtgl" aria-label="Тема / Theme"><svg class="moon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg><svg class="sun" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg></button> <a href="/">главная</a> · <a href="/dashboard">панель</a></div>
<script>document.getElementById("qtgl").onclick=function(){var d=document.documentElement,t=d.dataset.theme==="dark"?"light":"dark";d.dataset.theme=t;localStorage.setItem("qtheme",t)};</script>
<script src="/static/partners.js?v=__V__" defer></script>
</body></html>"""
