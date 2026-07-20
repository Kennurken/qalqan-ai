const QT={
 kk:{h1:'URL-дерді жаппай тексеру',sub:'Банктер, реттеушілер және қауіпсіздік қызметтері үшін: сілтемелер тізімін қойыңыз (әр жолға біреу) немесе CSV жүктеңіз — әр URL толық 7-деңгейлі pipeline-нан өтеді.',upload:'CSV/TXT жүктеу',go:'Тізімді тексеру',dl:'CSV-есепті жүктеп алу',th_v:'Вердикт',th_s:'Балл',th_src:'Дереккөз',empty:'Кемінде бір URL қойыңыз',checking:'Тексерудеміз...',danger:'Қауіпті',susp:'Күдікті',clean:'Таза',total:'Барлығы'},
 ru:{h1:'Массовая проверка URL',sub:'Для банков, регуляторов и служб безопасности: вставьте список ссылок (по одной на строку) или загрузите CSV — каждый URL пройдёт полный 7-уровневый pipeline.',upload:'Загрузить CSV/TXT',go:'Проверить список',dl:'Скачать отчёт CSV',th_v:'Вердикт',th_s:'Балл',th_src:'Источник',empty:'Вставьте хотя бы один URL',checking:'Проверяем...',danger:'Опасных',susp:'Подозрительных',clean:'Чистых',total:'Всего'}};
const T=k=>QTL.t(QT,k);
const $=s=>document.querySelector(s);
let results=[];
$('#upload').onclick=()=>$('#file').click();
$('#file').addEventListener('change',()=>{
  const f=$('#file').files[0]; if(!f) return;
  const rd=new FileReader();
  rd.onload=()=>{
    // CSV: take the first column of each line; TXT: line as-is
    const lines=String(rd.result).split(/\r?\n/).map(l=>l.split(/[,;\t]/)[0].trim()).filter(Boolean);
    $('#urls').value=lines.join('\n');
  };
  rd.readAsText(f);
});
function parseUrls(){
  return [...new Set($('#urls').value.split(/\r?\n/).map(s=>s.trim()).filter(s=>s&&!s.startsWith('#')&&s.includes('.')))].slice(0,150);
}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function run(){
  const urls=parseUrls();
  if(!urls.length){alert(T('empty'));return}
  const btn=$('#go');btn.disabled=true;btn.textContent=T('checking');
  results=[];$('#tbody').innerHTML='';$('#tblwrap').style.display='block';
  $('#prog').style.display='block';$('#sum').style.display='none';$('#dlrow').style.display='none';
  const esc=t=>{const d=document.createElement('div');d.textContent=t;return d.innerHTML};
  for(let i=0;i<urls.length;i+=15){
    const chunk=urls.slice(i,i+15);
    try{
      const r=await fetch('/batch',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({urls:chunk,lang:'ru'})});
      if(r.status===429){ // rate-limited: wait and retry this chunk once
        await sleep(35000);i-=15;continue;
      }
      const d=await r.json();
      for(const res of (d.results||[])){
        results.push(res);
        const v=(res.verdict||'?').toUpperCase();
        $('#tbody').insertAdjacentHTML('beforeend',
          `<tr><td>${esc(res.url||'')}</td><td class="v-${v}">${v}</td><td>${res.threat_score??''}</td><td>${esc(res.source||res.top_source||'')}</td></tr>`);
      }
    }catch(e){ chunk.forEach(u=>{results.push({url:u,verdict:'ERROR',threat_score:'',source:'network'});}); }
    $('#progbar').style.width=Math.min(100,Math.round(100*(i+15)/urls.length))+'%';
    if(i+15<urls.length) await sleep(4000);  // stay under the per-minute rate limit
  }
  $('#progbar').style.width='100%';
  const d=results.filter(r=>r.verdict==='DANGEROUS').length,
        s2=results.filter(r=>r.verdict==='SUSPICIOUS').length,
        ok=results.filter(r=>r.verdict==='SAFE').length;
  $('#sum').innerHTML=`<div class="pill d"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.86 2h8.28L22 7.86v8.28L16.14 22H7.86L2 16.14V7.86z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg> ${T("danger")}: ${d}</div><div class="pill s"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> ${T("susp")}: ${s2}</div><div class="pill ok"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> ${T("clean")}: ${ok}</div><div class="pill">${T("total")}: ${results.length}</div>`;
  $('#sum').style.display='flex';$('#dlrow').style.display='flex';
  btn.disabled=false;btn.textContent=T('go');
}
$('#go').onclick=run;
$('#dl').onclick=()=>{
  const head='url,verdict,score,source\n';
  const body=results.map(r=>`"${String(r.url||'').replace(/"/g,'""')}",${r.verdict||''},${r.threat_score??''},${r.source||r.top_source||''}`).join('\n');
  const blob=new Blob([head+body],{type:'text/csv'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='qalqan-batch-report.csv';a.click();
};

QTL.mount(QT,()=>{const b=$('#go');if(b&&!b.disabled)b.textContent=T('go');});
