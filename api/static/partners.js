// Self-service trial API key issuance.
document.getElementById('kgo').onclick = async () => {
  const org = document.getElementById('korg').value.trim();
  const email = document.getElementById('kemail').value.trim();
  const out = document.getElementById('kout');
  const esc = t => { const d = document.createElement('div'); d.textContent = t; return d.innerHTML; };
  if (org.length < 2 || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
    out.innerHTML = 'Укажите организацию и корректный email.'; return;
  }
  const b = document.getElementById('kgo'); b.disabled = true; b.textContent = 'Выпускаем...';
  try {
    const r = await fetch('/v1/request-key', { method: 'POST',
      headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ org, email }) });
    const d = await r.json();
    if (!r.ok) { out.innerHTML = esc(d.error || 'Ошибка, попробуйте позже.'); }
    else {
      out.innerHTML =
        '<b style="color:var(--green,#9ece6a)">Ключ выпущен (сохраните сейчас — второй раз не покажем):</b><br>' +
        '<code id="kval" style="user-select:all;word-break:break-all">' + esc(d.api_key) + '</code> ' +
        '<button id="kcopy" style="background:transparent;border:1px solid var(--bd);border-radius:7px;color:var(--tx);cursor:pointer;padding:3px 10px;font-family:inherit">копировать</button>' +
        '<br>Тариф: trial · ' + esc(String(d.limit_per_min)) + ' запр/мин · заголовок <code>X-API-Key</code>';
      document.getElementById('kcopy').onclick = async () => {
        try { await navigator.clipboard.writeText(d.api_key);
              document.getElementById('kcopy').textContent = 'скопировано'; } catch (e) {}
      };
    }
  } catch (e) { out.innerHTML = 'Сеть недоступна.'; }
  b.disabled = false; b.textContent = 'Получить trial-ключ';
};
