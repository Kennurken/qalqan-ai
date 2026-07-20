const tg = window.Telegram?.WebApp;
if (tg) { tg.ready(); tg.expand(); }
const API = location.origin;
const $ = s => document.querySelector(s);
const vcolor = v => v==='DANGEROUS'?'var(--red)':v==='SUSPICIOUS'?'var(--amber)':'var(--green)';
const vlabel = v => v==='DANGEROUS'?'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#f7768e"/></svg> ҚАУІПТІ':v==='SUSPICIOUS'?'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#e0af68"/></svg> КҮДІКТІ':'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#9ece6a"/></svg> ҚАУІПСІЗ';

document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{
  document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));
  document.querySelectorAll('.panel').forEach(x=>x.classList.remove('on'));
  t.classList.add('on'); $('#p-'+t.dataset.p).classList.add('on');
  if(t.dataset.p==='map') loadMap();
});

async function check(){
  const url=$('#url').value.trim(); if(!url) return;
  const box=$('#res-check'); box.className='res show'; box.innerHTML='<div class="spin">Тексерілуде...</div>';
  try{
    const r=await fetch(API+'/check',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url,lang:'kk'})});
    const d=await r.json();
    const v=d.verdict, sc=d.threat_score||0;
    box.innerHTML=`<div class="verdict" style="color:${vcolor(v)}">${vlabel(v)}</div>
      <div class="score">${sc}/100 · ${d.source||''}</div>
      <div class="bar"><div style="width:${sc}%;background:${vcolor(v)}"></div></div>
      <div class="detail">${d.detail_kk||d.detail||''}</div>`;
    if(tg) tg.HapticFeedback?.notificationOccurred(v==='DANGEROUS'?'error':v==='SAFE'?'success':'warning');
  }catch(e){ box.innerHTML='<div class="spin">Қате. Кейінірек қайталаңыз.</div>'; }
}
$('#btn-check').onclick=check;
$('#url').addEventListener('keydown',e=>{if(e.key==='Enter')check();});

// ── QR scanner (Telegram WebApp 6.4+) — fake Kaspi-QR is a common KZ scam ──
// Scan → URL lands in the input → the normal /check pipeline runs.
if (tg && tg.isVersionAtLeast && tg.isVersionAtLeast('6.4') && tg.showScanQrPopup) {
  $('#btn-qr').style.display='block';
  $('#btn-qr').onclick = () => {
    try {
      tg.showScanQrPopup({ text: 'QR-кодты камераға көрсетіңіз' });
    } catch(e) {}
  };
  tg.onEvent('qrTextReceived', (ev) => {
    try { tg.closeScanQrPopup(); } catch(e) {}
    const data = (ev && ev.data || '').trim();
    if (!data) return;
    // Non-URL QR payloads (wifi:, tel:, plain text) → show as-is, no check
    const m = data.match(/https?:\/\/[^\s]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}[^\s]*/);
    if (!m) {
      const box=$('#res-check'); box.className='res show';
      box.innerHTML=`<div class="verdict" style="color:var(--amber)">ℹ QR ішінде сілтеме жоқ</div>
        <div class="detail" style="word-break:break-all">${data.replace(/&/g,'&amp;').replace(/</g,'&lt;')}</div>`;
      return;
    }
    $('#url').value = m[0];
    check();
    if (tg.HapticFeedback) tg.HapticFeedback.impactOccurred('medium');
  });
}

async function ask(){
  const t=$('#situation').value.trim(); if(t.length<10) return;
  const box=$('#res-ask'); box.className='res show'; box.innerHTML='<div class="spin">AI талдап жатыр...</div>';
  try{
    const ulang=(tg&&tg.initDataUnsafe&&tg.initDataUnsafe.user&&tg.initDataUnsafe.user.language_code)||'ru';
    const r=await fetch(API+'/advisor',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t,lang:['kk','ru','en'].includes(ulang)?ulang:'ru'})});
    const d=await r.json();
    const v=d.verdict, sc=d.threat_score||0;
    let h=`<div class="verdict" style="color:${vcolor(v)}">${vlabel(v)}</div>
      <div class="score">${sc}/100 · ${d.scam_type||''}</div>
      <div class="bar"><div style="width:${sc}%;background:${vcolor(v)}"></div></div>
      <div class="detail">${d.reasoning||d.detail_ru||''}</div>`;
    if((d.advice||[]).length) h+='<div class="meta"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> '+d.advice.slice(0,4).map(a=>a).join('<br><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> ')+'</div>';
    box.innerHTML=h;
  }catch(e){ box.innerHTML='<div class="spin">Қате. Кейінірек қайталаңыз.</div>'; }
}
$('#btn-ask').onclick=ask;

let mapLoaded=false;
async function loadMap(){
  if(mapLoaded) return; mapLoaded=true;
  try{
    // Load geometry + data in parallel (geometry cached 24h by the CDN).
    // No forced demo: server returns real data when it exists, falls back to a
    // demo dataset and labels it via _source — show an honest badge either way.
    const [geoTxt, d] = await Promise.all([
      fetch(API+'/kz-regions.js').then(r=>r.text()),
      fetch(API+'/dashboard/data').then(r=>r.json()),
    ]);
    let KZ_GEO; try{ KZ_GEO = (new Function(geoTxt+';return KZ_GEO;'))(); }catch(e){ KZ_GEO=null; }
    const k=d.kpis||{};
    const demoBadge = d._source==='demo' ? ' <span style="font-size:9px;color:var(--amber);border:1px solid var(--amber);border-radius:6px;padding:1px 5px;vertical-align:middle">ДЕМО</span>' : '';
    $('#kpis').innerHTML=
      `<div class="kpi"><div class="v" style="color:var(--cyan)">${(k.total_checks||0).toLocaleString()}</div><div class="l">Тексерілді${demoBadge}</div></div>`+
      `<div class="kpi"><div class="v" style="color:var(--red)">${(k.threats_blocked||0).toLocaleString()}</div><div class="l">Қауіп</div></div>`;
    const reg=d.regions||{}; const mx=Math.max(1,...Object.values(reg).map(r=>r.threats||0));
    if(KZ_GEO){
      // Real choropleth — 20 регионов (2023 COD-AB)
      let out='';
      for(const [nm,path] of Object.entries(KZ_GEO.paths)){
        const r=reg[nm]||{threats:0};
        const f=Math.min(1,(r.threats||0)/mx);
        const c=`rgb(${Math.round(13+(255-13)*f)},${Math.round(20+(59-20)*f)},${Math.round(36+(92-36)*f)})`;
        out+=`<path d="${path}" fill="${c}" stroke="#1e293b" stroke-width="1.5"/>`;
      }
      $('#kzsvg').innerHTML=out;
    }
    const top=Object.entries(reg).sort((a,b)=>(b[1].threats||0)-(a[1].threats||0)).slice(0,8);
    $('#kzmap').innerHTML=top.map(([nm,r])=>{
      const f=Math.min(1,(r.threats||0)/mx);
      const c=`rgb(${Math.round(13+(255-13)*f)},${Math.round(20+(59-20)*f)},${Math.round(36+(92-36)*f)})`;
      return `<div class="kzt" style="background:${c};color:${f>.45?'#fff':'#e7ebf3'}">${nm}<b>${r.threats||0}</b></div>`;
    }).join('');
  }catch(e){ $('#kzmap').innerHTML='<div class="spin">Қате</div>'; }
}
