LEAK_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<script>document.documentElement.dataset.theme=localStorage.getItem("qtheme")||"dark";</script>
<meta charset="utf-8">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237aa2f7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qalqan AI — Проверка утечки пароля</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:oklch(16% .02 255);--card:oklch(21.5% .025 260);--card2:oklch(19% .028 258);--cyan:oklch(72% .12 265);--red:oklch(70% .15 15);--amber:oklch(78% .11 78);--green:oklch(80% .13 130);--tx:oklch(93% .01 250);--mut:oklch(63% .02 250);--bd:oklch(30% .03 258);--panel:var(--card);--s1:4px;--s2:8px;--s3:12px;--s4:16px;--s5:24px;--s6:36px}
[data-theme="light"]{--bg:oklch(96.5% .006 250);--card:oklch(99.2% .003 250);--card2:oklch(94.5% .008 250);--cyan:oklch(50% .15 262);--red:oklch(54% .17 18);--amber:oklch(58% .12 78);--green:oklch(52% .12 140);--tx:oklch(26% .02 255);--mut:oklch(48% .02 250);--bd:oklch(87% .012 250)}
[data-theme="light"] body{background:var(--bg)}
.qtgl{background:var(--card2);border:1px solid var(--bd);border-radius:9px;color:var(--mut);cursor:pointer;padding:7px 9px;line-height:0;transition:color .2s,border-color .2s}
.qtgl:hover{color:var(--tx);border-color:var(--cyan)}
.qtgl .sun{display:none}.qtgl .moon{display:block}
[data-theme="light"] .qtgl .sun{display:block}[data-theme="light"] .qtgl .moon{display:none}
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
  <div class="top"><h1><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> <span data-qtl="h1">Пароль утёк?</span></h1><button class="qtgl" id="qtgl" aria-label="Тема / Theme"><svg class="moon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg><svg class="sun" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg></button> <a href="/">← Qalqan AI</a></div>
  <div class="sub" data-qtl="sub">Проверь пароль по базе <b>HaveIBeenPwned</b> — 900+ млн паролей из реальных утечек.</div>

  <div class="tabs">
    <button class="tabb on" data-t="pw" data-qtl="tab_pw"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> Пароль</button>
    <button class="tabb" data-t="em" data-qtl="tab_em"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg> Email</button>
  </div>

  <div class="card" id="card-pw">
    <div class="inrow">
      <input id="pw" type="password" data-qtl-ph="ph_pw" aria-label="Пароль для проверки" placeholder="Введите пароль для проверки" autocomplete="off">
      <button class="eye" id="eye" aria-label="Показать пароль"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/></svg></button>
    </div>
    <button class="btn" id="go" data-qtl="go">Проверить утечку</button>
    <div class="priv">
      <span style="font-size:16px"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></span>
      <span><b>Пароль не покидает ваше устройство.</b> Считается SHA-1 хэш прямо в браузере, наружу уходят только первые 5 символов хэша (k-анонимность). Ни мы, ни HIBP не видим пароль и даже его полный хэш.</span>
    </div>
    <div class="res" id="res" role="status" aria-live="polite"></div>
    <div class="how">Как это работает: пароль → <code>SHA-1</code> в браузере → префикс <code>5 симв.</code> → HIBP возвращает ~800 хэшей с этим префиксом → сравнение происходит локально у вас.</div>
  </div>

    <div class="card" id="card-em" style="display:none">
    <div class="inrow">
      <input id="em" type="email" aria-label="Email для проверки" placeholder="you@example.com" autocomplete="off">
    </div>
    <button class="btn" id="goem" data-qtl="goem">Проверить email</button>
    <div class="priv">
      <span style="font-size:16px"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></span>
      <span><b>Email не сохраняется.</b> Запрос уходит в открытую базу утечек XposedOrNot; Qalqan не логирует и не хранит адрес.</span>
    </div>
    <div class="res" id="resem" role="status" aria-live="polite"></div>
  </div>

  <div class="card" style="margin-top:14px">
    <div style="font-weight:700;font-size:14px;margin-bottom:10px"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg> Генератор надёжных паролей</div>
    <div class="inrow">
      <input id="genout" type="text" readonly data-qtl-ph="gen_ph" aria-label="Сгенерированный пароль" placeholder="Нажми «Сгенерировать»" style="font-family:ui-monospace,monospace">
      <button class="eye" id="gencopy" aria-label="Скопировать"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="8" width="14" height="14" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg></button>
    </div>
    <div style="display:flex;gap:10px;margin-top:10px;align-items:center;font-size:12.5px;color:var(--mut)">
      <label><input type="checkbox" id="gensym" checked> символы</label>
      <label>длина <select id="genlen" aria-label="Длина пароля"><option>16</option><option>20</option><option selected>24</option><option>32</option></select></label>
    </div>
    <button class="btn" id="gengo" data-qtl="gen_go" style="margin-top:12px">Сгенерировать</button>
    <div class="priv" style="margin-top:10px"><span style="font-size:16px"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></span><span>Генерируется в браузере (crypto.getRandomValues), никуда не отправляется.</span></div>
  </div>

<div class="foot">Qalqan AI · Данные: <a href="https://haveibeenpwned.com/Passwords" rel="noopener" target="_blank">HaveIBeenPwned</a> (k-anonymity API) · </div>
</div>

<script src="/static/qtl.js?v=__V__" defer></script>
<script src="/static/leak.js?v=__V__" defer></script>
<script>document.getElementById("qtgl").onclick=function(){var d=document.documentElement,t=d.dataset.theme==="dark"?"light":"dark";d.dataset.theme=t;localStorage.setItem("qtheme",t)};</script>
</body>
</html>"""
