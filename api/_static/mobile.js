const $=s=>document.querySelector(s);
const API=location.origin;
let offlineDomains=new Set();

// tabs
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('nav button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('on'));
  $('#p-'+b.dataset.t).classList.add('on');
  if(b.dataset.t==='map')loadMap();
  if(b.dataset.t==='hist')renderHist();
});

// online/offline
function netState(){const on=navigator.onLine;const el=$('#net');el.classList.toggle('off',!on);$('#nett').textContent=on?'онлайн':'офлайн';}
addEventListener('online',netState);addEventListener('offline',netState);netState();

// history
function getHist(){try{return JSON.parse(localStorage.getItem('qh')||'[]')}catch(e){return[]}}
function pushHist(u,v,s){const h=getHist();h.unshift({u,v,s,t:Date.now()});localStorage.setItem('qh',JSON.stringify(h.slice(0,30)));}
function vcolor(v){return v==='DANGEROUS'?'#f7768e':v==='SUSPICIOUS'?'#e0af68':'#9ece6a'}
function renderHist(){const h=getHist();$('#hist').innerHTML=h.length?h.map(x=>`<div class="hist"><span class="u">${x.u}</span><span style="display:flex;gap:7px;align-items:center"><b style="color:${vcolor(x.v)}">${x.s}</b><span class="dot2" style="background:${vcolor(x.v)}"></span></span></div>`).join(''):'<div class="muted">Тексерулер әзірге жоқ</div>';}

function showRes(el,v,score,detail,flags){
  el.className='res show '+v;
  let h=`<div class="verdict">${v==='DANGEROUS'?'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.86 2h8.28L22 7.86v8.28L16.14 22H7.86L2 16.14V7.86z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>':v==='SUSPICIOUS'?'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>':'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'} ${v}</div><div class="score">Қауіп: ${score}/100</div><div class="detail">${detail||''}</div>`;
  if(flags&&flags.length)h+='<div class="flags">'+flags.slice(0,5).map(f=>`<div class="flag">• ${f}</div>`).join('')+'</div>';
  el.innerHTML=h;
}

// URL check
$('#btn-check').onclick=async()=>{
  const url=$('#url').value.trim(); if(!url)return;
  const btn=$('#btn-check'),el=$('#r-check'); btn.disabled=true; btn.innerHTML='<span class="spin"></span>';
  try{
    if(!navigator.onLine){
      const d=(url.replace(/^https?:\/\//,'').split('/')[0]||'').toLowerCase();
      const bad=[...offlineDomains].some(x=>d===x||d.endsWith('.'+x));
      showRes(el,bad?'DANGEROUS':'SAFE',bad?90:0,bad?'Офлайн базада қауіпті деп тіркелген':'Офлайн базада жоқ (интернетсіз тексеру шектеулі)');
    }else{
      const isPhone=/^[\d\s+()-]{9,18}$/.test(url) && url.replace(/\D/g,'').length>=10;
      const ep=isPhone?'/phone':'/check';
      const body=isPhone?{phone:url,lang:'kk'}:{url,lang:'kk'};
      const r=await fetch(API+ep,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      const d=await r.json();
      showRes(el,d.verdict,d.threat_score,d.detail||d.detail_kk,(d.indicators||[]));
      pushHist(isPhone?(d.formatted||url):url,d.verdict,d.threat_score);
    }
  }catch(e){showRes(el,'SUSPICIOUS',50,'Қате: '+e.message);}
  btn.disabled=false; btn.textContent='Тексеру';
};

// AI advisor
$('#btn-ai').onclick=async()=>{
  const text=$('#sit').value.trim(); if(text.length<10){return;}
  const btn=$('#btn-ai'),el=$('#r-ai'); btn.disabled=true; btn.innerHTML='<span class="spin"></span>';
  try{
    const r=await fetch(API+'/advisor',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text,lang:'kk'})});
    const d=await r.json();
    const flags=(d.red_flags||d.indicators||[]).map(f=>typeof f==='string'?f:(f.kk||f.ru||f.text||''));
    showRes(el,d.verdict||'SUSPICIOUS',d.threat_score||d.score||50,d.advice||d.reasoning||d.detail||'',flags);
  }catch(e){showRes(el,'SUSPICIOUS',50,'Қате: '+e.message);}
  btn.disabled=false; btn.textContent='Талдау';
};

// map
let mapLoaded=false;
async function loadMap(){
  if(mapLoaded)return; mapLoaded=true;
  try{
    const d=await (await fetch(API+'/dashboard/data')).json();
    const demoTag = d._source==='demo' ? ' <small style="color:#e0af68">(демо)</small>' : '';
    const reg=Object.entries(d.regions||{}).sort((a,b)=>b[1].threats-a[1].threats).slice(0,12);
    const mx=Math.max(1,...reg.map(r=>r[1].threats));
    $('#regions').innerHTML=demoTag+reg.map(([n,r])=>`<div class="region"><span class="nm">${n}</span><span class="tk"><span class="fl" style="width:${Math.round(100*r.threats/mx)}%"></span></span><span class="vv">${r.threats}</span></div>`).join('');
  }catch(e){$('#regions').innerHTML='<div class="muted">Картаны жүктеу қатесі</div>';}
}

// offline-db cache
fetch(API+'/offline-db').then(r=>r.json()).then(d=>{
  const s=new Set();
  Object.values(d).forEach(v=>{if(Array.isArray(v))v.forEach(x=>typeof x==='string'&&s.add(x.toLowerCase()));});
  offlineDomains=s; localStorage.setItem('qodb',JSON.stringify([...s].slice(0,5000)));
}).catch(()=>{try{offlineDomains=new Set(JSON.parse(localStorage.getItem('qodb')||'[]'))}catch(e){}});

// install prompt
let deferred;
addEventListener('beforeinstallprompt',e=>{e.preventDefault();deferred=e;$('#install').style.display='block';});
$('#install').onclick=async()=>{if(!deferred)return;deferred.prompt();await deferred.userChoice;deferred=null;$('#install').style.display='none';};

// service worker
if('serviceWorker' in navigator)navigator.serviceWorker.register('/sw.js').catch(()=>{});
