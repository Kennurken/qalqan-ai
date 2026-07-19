const $=s=>document.querySelector(s);
async function scan(dom){
  dom=(dom||$('#dom').value).trim().replace(/^https?:\/\//,'').replace(/\/.*$/,''); if(!dom) return;
  $('#dom').value=dom;
  const btn=$('#go'); btn.disabled=true; btn.textContent='...';
  $('#card').className='card'; $('#status').innerHTML='<div class="spin">Анализируем '+dom+' (SSL, домен, репутация)...</div>';
  try{
    const r=await fetch('/scan/'+encodeURIComponent(dom));
    if(!r.ok) throw new Error('http '+r.status);
    const d=await r.json();
    if(d.error){ $('#status').innerHTML='<div class="spin"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> '+d.error+'</div>'; btn.disabled=false; btn.textContent='Оценить'; return; }
    $('#badge').textContent=d.grade; $('#badge').style.background=d.grade_color;
    $('#dm').textContent=d.domain;
    const vlabel=d.verdict==='DANGEROUS'?'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#f7768e"/></svg> Опасный':d.verdict==='SUSPICIOUS'?'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#e0af68"/></svg> Подозрительный':'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#9ece6a"/></svg> Чистый';
    $('#vv').textContent=vlabel+' · риск '+d.risk_score+'/100';
    $('#pc').innerHTML='<span style="color:var(--green)"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg> '+d.passed+'</span> из '+d.total_checks+' проверок пройдено';
    $('#factors').innerHTML=(d.factors||[]).map(f=>{
      const ic=f.status==='pass'?'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>':f.status==='warn'?'▲':'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>';
      return `<div class="f ${f.status}"><span class="i">${ic}</span><span>${f.ru}</span></div>`;
    }).join('');
    $('#card').className='card show'; $('#status').innerHTML='';
  }catch(e){ $('#status').innerHTML='<div class="spin">Ошибка анализа. Попробуйте позже.</div>'; }
  btn.disabled=false; btn.textContent='Оценить';
}
$('#go').onclick=()=>scan();
$('#dom').addEventListener('keydown',e=>{if(e.key==='Enter')scan();});
document.querySelectorAll('.ex b').forEach(b=>b.onclick=()=>scan(b.dataset.d));
