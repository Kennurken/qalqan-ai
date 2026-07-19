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

<script src="/static/scan.js?v=__V__" defer></script>
<div class="foot">Qalqan AI · Website security grade · <a href="/brand">Защита бренда</a> · <a href="/">Главная</a></div>
</body>
</html>"""
