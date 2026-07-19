const fmt = n => (n||0).toLocaleString('ru-RU');
const $ = id => document.getElementById(id);

function kpiCard(v,l,cls){return `<div class="kpi ${cls||''}"><div class="v">${v}</div><div class="l">${l}</div></div>`}

function renderBars(elId, obj, max){
  const entries = Object.entries(obj||{});
  const mx = max || Math.max(1, ...entries.map(e=>e[1]));
  $(elId).innerHTML = entries.map(([k,v])=>`
    <div class="bar-row"><div class="nm" title="${k}">${k}</div>
    <div class="bar-track"><div class="bar-fill" style="width:${Math.round(100*v/mx)}%"></div></div>
    <div class="vv">${fmt(v)}</div></div>`).join('') || '<div class="sub">нет данных</div>';
}

function renderLine(series){
  if(!series||!series.length){return}
  const W=640,H=220,pad=30, mx=Math.max(...series.map(s=>s.total),1);
  const X=i=>pad+i*(W-2*pad)/(series.length-1);
  const Y=v=>H-pad-(v/mx)*(H-2*pad);
  const path=arr=>arr.map((s,i)=>`${i?'L':'M'}${X(i).toFixed(1)},${Y(s).toFixed(1)}`).join(' ');
  const grid=[0,.25,.5,.75,1].map(f=>`<line x1="${pad}" y1="${H-pad-f*(H-2*pad)}" x2="${W-pad}" y2="${H-pad-f*(H-2*pad)}" stroke="#1e293b" stroke-width="1"/>`).join('');
  $('line').innerHTML = grid +
    `<path d="${path(series.map(s=>s.total))}" fill="none" stroke="#7aa2f7" stroke-width="2.5"/>`+
    `<path d="${path(series.map(s=>s.threats))}" fill="none" stroke="#f7768e" stroke-width="2.5"/>`+
    `<text x="${pad}" y="14" fill="#7d8aa0" font-size="11">${fmt(mx)}</text>`;
}

function renderDonut(vd){
  const order=[['DANGEROUS','#f7768e'],['SUSPICIOUS','#e0af68'],['SAFE','#9ece6a']];
  const total=Object.values(vd||{}).reduce((a,b)=>a+b,0)||1;
  let a0=-Math.PI/2, svg='', leg='';
  for(const [k,c] of order){
    const val=vd[k]||0; const frac=val/total; const a1=a0+frac*2*Math.PI;
    const r=80,cx=100,cy=100, lg=frac>.5?1:0;
    const x0=cx+r*Math.cos(a0),y0=cy+r*Math.sin(a0),x1=cx+r*Math.cos(a1),y1=cy+r*Math.sin(a1);
    if(val>0)svg+=`<path d="M${cx},${cy} L${x0.toFixed(1)},${y0.toFixed(1)} A${r},${r} 0 ${lg} 1 ${x1.toFixed(1)},${y1.toFixed(1)} Z" fill="${c}"/>`;
    leg+=`<div class="bar-row"><span><span class="dot" style="background:${c}"></span>${k}</span><div style="flex:1"></div><b>${fmt(val)}</b> <span class="sub">(${Math.round(frac*100)}%)</span></div>`;
    a0=a1;
  }
  svg+='<circle cx="100" cy="100" r="46" fill="#111827"/>';
  $('donut').innerHTML=svg; $('donut-leg').innerHTML=leg;
}

// ── Real KZ choropleth (geometry from /kz-regions.js → KZ_GEO, 20 regions 2023) ──
function heat(frac){
  const a=[13,20,36], b=[255,59,92];
  const c=a.map((v,i)=>Math.round(v+(b[i]-v)*frac));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}
function renderMap(regions){
  regions=regions||{};
  if(typeof KZ_GEO==='undefined'){ return; }
  const mx=Math.max(1,...Object.values(regions).map(r=>r.threats||0));
  const svg=$('kzsvg'), tip=$('maptip');
  let out='';
  for(const [name,d] of Object.entries(KZ_GEO.paths)){
    const r=regions[name]||{total:0,threats:0};
    const frac=Math.min(1,(r.threats||0)/mx);
    out+=`<path d="${d}" fill="${heat(frac)}" stroke="#1e293b" stroke-width="1.2" data-n="${name}" data-t="${r.threats||0}" data-c="${r.total||0}" style="cursor:pointer;transition:filter .15s"/>`;
  }
  // Region labels for the biggest oblasts + city markers
  for(const [name,c] of Object.entries(KZ_GEO.centroids)){
    const small = (name==='Алматы қ.'||name==='Астана'||name==='Шымкент');
    if(small) continue;
    out+=`<text x="${c[0]}" y="${c[1]}" text-anchor="middle" font-size="15" fill="#e7ebf3" opacity=".75" pointer-events="none" font-weight="600">${name}</text>`;
  }
  svg.innerHTML=out;
  svg.querySelectorAll('path').forEach(p=>{
    p.addEventListener('mousemove',e=>{
      p.style.filter='brightness(1.5)';
      tip.style.display='block';
      tip.innerHTML=`<b>${p.dataset.n}</b><br><svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#f7768e"/></svg> ${p.dataset.t} қауіп · <svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg> ${p.dataset.c} тексеру`;
      const box=svg.getBoundingClientRect();
      tip.style.left=Math.min(e.clientX-box.left+14, box.width-160)+'px';
      tip.style.top=(e.clientY-box.top+14)+'px';
    });
    p.addEventListener('mouseleave',()=>{ p.style.filter=''; tip.style.display='none'; });
  });
}

fetch('/dashboard/data'+location.search).then(r=>r.json()).then(d=>{
  const src=$('src'); const live=d._source==='live';
  src.textContent = live?'● LIVE':'● DEMO'; src.className='badge '+(live?'live':'demo');
  const k=d.kpis||{};
  $('kpis').innerHTML =
    kpiCard(fmt(k.total_checks),'Всего проверок','cyan')+
    kpiCard(fmt(k.threats_blocked),'Заблокировано угроз','red')+
    kpiCard(fmt(k.suspicious),'Подозрительных','amber')+
    kpiCard((k.block_rate_pct||0)+'%','Доля угроз')+
    kpiCard(fmt(k.total_reports),'Жалоб граждан')+
    kpiCard(k.avg_score||0,'Средний риск-балл');
  renderLine(d.time_series);
  renderMap(d.regions);
  renderDonut(d.verdict_distribution);
  renderBars('types', d.threat_types);
  renderBars('tiers', d.tier_effectiveness);
  $('domains').innerHTML = (d.top_dangerous_domains||[]).map(x=>
    `<tr><td class="dom">${x.domain}</td><td class="n">${fmt(x.count)}</td></tr>`).join('')||'<tr><td class="sub">нет данных</td></tr>';
}).catch(e=>{ $('kpis').innerHTML='<div class="sub">Ошибка загрузки данных</div>'; });
