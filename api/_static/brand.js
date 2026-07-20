const QT={
 kk:{h1:'Брендті фишингтен қорғау',b2b:'БАНКТЕР · МЕМОРГАНДАР · БИЗНЕС ҮШІН',sub:'Брендіңіздің доменін енгізіңіз — алаяқтар клиенттеріңізден ұрлау үшін тіркейтін домен-егіздерді көрсетеміз.',ph:'kaspi.kz',go:'Сканерлеу',ex:'Мысалдар:',live:'Тіркелгендерді live-тексеру',watch:'Күнделікті мониторингке',cert:'7 күндегі SSL-серттер (CT-логтар)',crit:'Критикалық',high:'Жоғары',med:'Орташа',gen:'Шабуыл нұсқаларын жасаудамыз...',invalid:'Дұрыс домен енгізіңіз, мыс. kaspi.kz',neterr:'Қате. Кейінірек көріңіз.',rdap:'Домен реестрлеріне RDAP-сұраулар (15 сек-қа дейін)...',toofast:'Тым жиі — минут күтіңіз.',regd:'тіркелген',exists:'БАР',age:'жасы',days:'күн',ok_none:'тексерілген нұсқаның ешқайсысы тіркелмеген. Шабуыл инфрақұрылымы табылмады.',regcnt:'Тіркелгені',of:'/',watch_on:'Мониторингте',watch_fail:'Қолжетімсіз',ct_read:'CT-логтарды оқудамыз (20 сек-қа дейін)...',ct_req:'crt.sh — ашық сертификат логтарына сұрау...',ct_busy:'CT-көзі (crt.sh) қазір жүктелген — минуттан кейін қайталаңыз.',ct_none_a:'күнде бренд атауымен бөтен домендерде жаңа SSL-сертификат байқалмады.',ct_cnt:'Брендтен тыс жаңа сертификаттар',issued:'берілген'},
 ru:{h1:'Защита бренда от фишинга',b2b:'ДЛЯ БАНКОВ · ГОСОРГАНОВ · БИЗНЕСА',sub:'Введите домен вашего бренда — покажем домены-двойники, которые регистрируют мошенники, чтобы красть у ваших клиентов.',ph:'kaspi.kz',go:'Сканировать',ex:'Примеры:',live:'Live-проверка регистраций',watch:'На ежедневный мониторинг',cert:'SSL-серты за 7 дней (CT-логи)',crit:'Критичных',high:'Высоких',med:'Средних',gen:'Генерируем варианты атаки...',invalid:'Введите корректный домен, напр. kaspi.kz',neterr:'Ошибка. Попробуйте позже.',rdap:'RDAP-запросы к доменным реестрам (до 15 сек)...',toofast:'Слишком часто — подождите минуту.',regd:'зарегистрирован',exists:'СУЩЕСТВУЕТ',age:'возраст',days:'дн.',ok_none:'проверенных вариантов — ни один не зарегистрирован. Атакующей инфраструктуры не обнаружено.',regcnt:'Зарегистрировано',of:'из',watch_on:'На мониторинге',watch_fail:'Недоступно',ct_read:'Читаем CT-логи (до 20 сек)...',ct_req:'Запрос к crt.sh — публичным логам сертификатов...',ct_busy:'CT-источник (crt.sh) сейчас перегружен — повторите через минуту.',ct_none_a:'дней новых SSL-сертификатов с именем бренда на чужих доменах не замечено.',ct_cnt:'Свежих сертификатов вне бренда',issued:'выдан'}};
const T=k=>QTL.t(QT,k);
const $=s=>document.querySelector(s);
async function scan(dom){
  dom=(dom||$('#dom').value).trim(); if(!dom) return;
  $('#dom').value=dom;
  const btn=$('#go'); btn.disabled=true; btn.textContent='...';
  $('#summary').className='summary'; $('#grid').className='grid'; $('#advice').className='advice';
  $('#status').innerHTML='<div class="spin">'+T('gen')+'</div>';
  try{
    const r=await fetch('/brand/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({domain:dom})});
    const d=await r.json();
    if(d.error){ $('#status').innerHTML='<div class="spin"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Введите корректный домен, напр. kaspi.kz</div>'; btn.disabled=false; btn.textContent=T('go'); return; }
    const c=d.risk_counts||{};
    $('#summary').innerHTML=
      `<div class="pill c"><svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#f7768e"/></svg> ${T("crit")}: ${c.critical||0}</div>`+
      `<div class="pill h"><svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#e08f68"/></svg> ${T("high")}: ${c.high||0}</div>`+
      `<div class="pill m"><svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#7aa2f7"/></svg> ${T("med")}: ${c.medium||0}</div>`;
    $('#summary').className='summary show';
    $('#grid').innerHTML=(d.variants||[]).map(v=>
      `<div class="row"><span class="dot ${v.risk}"></span><div><div class="dm">${v.domain}</div><div class="nt">${v.note}</div></div></div>`).join('');
    $('#grid').className='grid show';
    $('#advice').innerHTML=`<b>Что делать:</b> ${d.advice_ru||''}<div class="disc">${d.disclaimer_ru||''}</div>`;
    $('#advice').className='advice show';
    $('#status').innerHTML='';
    $('#liveblock').style.display='block'; $('#liveres').innerHTML='';
  }catch(e){ $('#status').innerHTML='<div class="spin">'+T('neterr')+'</div>'; }
  btn.disabled=false; btn.textContent=T('go');
}
$('#go').onclick=()=>scan();
$('#dom').addEventListener('keydown',e=>{if(e.key==='Enter')scan();});
document.querySelectorAll('.ex b').forEach(b=>b.onclick=()=>scan(b.dataset.d));

// ── Live RDAP scan: which look-alikes are ACTUALLY registered right now ──
$('#livego').onclick=async()=>{
  const dom=$('#dom').value.trim(); if(!dom) return;
  const b=$('#livego'); b.disabled=true; b.textContent=T('rdap').slice(0,22)+'...';
  $('#liveres').innerHTML='<div class="spin">RDAP-запросы к доменным реестрам (до 15 сек)...</div><div class="skl" style="height:44px;margin-top:10px"></div><div class="skl" style="height:44px;margin-top:8px"></div>';
  try{
    const r=await fetch('/brand/live-scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({domain:dom})});
    if(r.status===429){ $('#liveres').innerHTML='<div class="spin"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> '+T('toofast')+'</div>'; b.disabled=false; b.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg> Live-проверка регистраций'; return; }
    const d=await r.json();
    if(d.error){ $('#liveres').innerHTML='<div class="spin"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> '+T('invalid')+'</div>'; }
    else if(!d.registered_count){
      $('#liveres').innerHTML=`<div class="liveok"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> ${d.answered} ${T("ok_none")}</div>`;
    } else {
      $('#liveres').innerHTML=
        `<div class="livebad"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 18v-6a5 5 0 1 1 10 0v6"/><path d="M5 21a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2z"/><path d="M12 2v2"/><path d="m4.9 4.9 1.4 1.4"/><path d="m19.1 4.9-1.4 1.4"/></svg> ${T("regcnt")} ${d.registered_count} ${T("of")} ${d.answered}:</div>`+
        d.registered.map(v=>`<div class="row"><span class="dot critical"></span><div><div class="dm">${v.domain}</div><div class="nt">${v.note}${v.age_days!=null?` · ${T('age')} ${v.age_days} ${T('days')}`:''} · <b style="color:var(--red)">${'`'.trim?T('exists'):''}</b></div></div></div>`).join('')+
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
    b.textContent=d.ok?T('watch_on'):T('watch_fail');
  }catch(e){ b.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Ошибка'; b.disabled=false; }
};

// ── Certificate-transparency sweep: fresh certs with the brand keyword ──
$('#certgo').onclick=async()=>{
  const dom=$('#dom').value.trim(); if(!dom) return;
  const b=$('#certgo'); b.disabled=true; b.textContent=T('ct_read');
  $('#liveres').innerHTML='<div class="spin">Запрос к crt.sh — публичным логам сертификатов...</div><div class="skl" style="height:44px;margin-top:10px"></div>';
  try{
    const r=await fetch('/brand/certs',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({domain:dom})});
    if(r.status===429){ $('#liveres').innerHTML='<div class="spin">'+T('toofast')+'</div>'; }
    else{
      const d=await r.json();
      if(d.status==='unavailable'){ $('#liveres').innerHTML='<div class="spin">'+T('ct_busy')+'</div>'; }
      else if(d.error){ $('#liveres').innerHTML='<div class="spin">'+T('invalid')+'</div>'; }
      else if(!d.count){ $('#liveres').innerHTML='<div class="liveok">'+d.window_days+' '+T('ct_none_a')+'</div>'; }
      else{
        const esc=t=>{const x=document.createElement('div');x.textContent=t;return x.innerHTML};
        $('#liveres').innerHTML=
          '<div class="livebad">'+T('ct_cnt')+' («'+esc(d.brand.split('.')[0])+'»): '+d.count+'</div>'+
          d.certs.map(c=>'<div class="row"><span class="dot high"></span><div><div class="dm">'+esc(c.domain)+'</div><div class="nt">выдан '+esc(c.issued)+' · '+esc(c.issuer)+'</div></div></div>').join('')+
          '<div class="disc" style="margin-top:8px">'+esc(d.note_ru||'')+'</div>';
      }
    }
  }catch(e){ $('#liveres').innerHTML='<div class="spin">Ошибка сети.</div>'; }
  b.disabled=false; b.textContent=T('cert');
};

QTL.mount(QT,()=>{
  const g=$('#go'); if(g&&!g.disabled)g.textContent=T('go');
  const l=$('#livego'); if(l&&!l.disabled)l.textContent=T('live');
  const c=$('#certgo'); if(c&&!c.disabled)c.textContent=T('cert');
});
