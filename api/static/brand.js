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
