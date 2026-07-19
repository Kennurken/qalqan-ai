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

<script src="/static/screen.js?v=__V__" defer></script>
</body>
</html>"""
