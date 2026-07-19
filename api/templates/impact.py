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

<script src="/static/impact.js?v=__V__" defer></script>
</body>
</html>"""
