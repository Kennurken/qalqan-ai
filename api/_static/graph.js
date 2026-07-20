const COL={customer:'#7aa2f7',supplier:'#bb9af7',founder:'#e0af68',address:'#9ece6a',official:'#f7768e'};
fetch('/goszakup/graph/demo').then(r=>r.json()).then(render).catch(()=>{document.getElementById('findings').textContent='Ошибка загрузки';});
function render(g){
  document.getElementById('src').textContent = (g._source==='demo'?'демо-сценарий':'данные');
  const W=900,H=600,nodes=g.nodes,edges=g.edges;
  nodes.forEach((n,i)=>{const a=i/nodes.length*6.283; n.x=W/2+Math.cos(a)*200; n.y=H/2+Math.sin(a)*170; n.vx=0;n.vy=0;});
  const by=Object.fromEntries(nodes.map(n=>[n.id,n]));
  for(let it=0;it<320;it++){
    for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++){
      const a=nodes[i],b=nodes[j];let dx=a.x-b.x,dy=a.y-b.y,d=Math.hypot(dx,dy)||1,f=2600/(d*d);
      a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;}
    edges.forEach(e=>{const a=by[e.source],b=by[e.target];if(!a||!b)return;let dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1,f=(d-95)*0.02;a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;});
    nodes.forEach(n=>{n.vx+=(W/2-n.x)*0.002;n.vy+=(H/2-n.y)*0.002;n.x+=Math.max(-8,Math.min(8,n.vx));n.y+=Math.max(-8,Math.min(8,n.vy));n.vx*=0.84;n.vy*=0.84;n.x=Math.max(40,Math.min(W-40,n.x));n.y=Math.max(34,Math.min(H-24,n.y));});
  }
  let s='';
  edges.forEach(e=>{const a=by[e.source],b=by[e.target];if(!a||!b)return;const c=e.risk?'#f7768e':'#334155';
    s+=`<line x1="${a.x.toFixed(1)}" y1="${a.y.toFixed(1)}" x2="${b.x.toFixed(1)}" y2="${b.y.toFixed(1)}" stroke="${c}" stroke-width="${e.risk?2.6:1}" ${e.risk?'stroke-dasharray="5 3"':''}/>`;});
  nodes.forEach(n=>{const c=COL[n.type]||'#888',r=(n.type==='customer'||n.type==='supplier')?13:8;
    s+=`<circle cx="${n.x.toFixed(1)}" cy="${n.y.toFixed(1)}" r="${r}" fill="${c}" stroke="${n.risk?'#f7768e':'#0a0e16'}" stroke-width="${n.risk?3:1.5}"/>`;
    s+=`<text x="${n.x.toFixed(1)}" y="${(n.y-r-5).toFixed(1)}" fill="#e7ebf3" font-size="10" text-anchor="middle">${(n.label||'').slice(0,22)}</text>`;});
  document.getElementById('graph').innerHTML=s;
  let f=`<div class="risk">Риск: <b>${g.risk_score}/100</b> · <span class="${g.verdict}">${g.verdict}</span></div>`;
  f+=(g.findings||[]).map(x=>`<div class="finding"><span class="sc">+${x.score}</span><span>${x.ru}</span></div>`).join('');
  document.getElementById('findings').innerHTML=f;
}
