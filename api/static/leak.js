const QI={octagon:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.86 2h8.28L22 7.86v8.28L16.14 22H7.86L2 16.14V7.86z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>',alert:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',checkc:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',check:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',copy:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="8" width="14" height="14" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>'};
const $=s=>document.querySelector(s);
$('#eye').onclick=()=>{const p=$('#pw');p.type=p.type==='password'?'text':'password';};

async function sha1hex(str){
  const buf=await crypto.subtle.digest('SHA-1',new TextEncoder().encode(str));
  return [...new Uint8Array(buf)].map(b=>b.toString(16).padStart(2,'0')).join('').toUpperCase();
}

async function checkLeak(){
  const pw=$('#pw').value;
  const res=$('#res');
  if(!pw){ return; }
  const btn=$('#go'); btn.disabled=true; btn.textContent='Проверяем...';
  try{
    const hash=await sha1hex(pw);
    const prefix=hash.slice(0,5), suffix=hash.slice(5);
    const r=await fetch('https://api.pwnedpasswords.com/range/'+prefix,{headers:{'Add-Padding':'true'}});
    if(!r.ok) throw new Error('hibp '+r.status);
    const lines=(await r.text()).split('\n');
    let count=0;
    for(const ln of lines){
      const [suf,cnt]=ln.trim().split(':');
      if(suf===suffix){ count=parseInt(cnt,10)||0; break; }
    }
    if(count>0){
      res.className='res show bad';
      res.innerHTML=`<div class="big"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 18v-6a5 5 0 1 1 10 0v6"/><path d="M5 21a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2z"/><path d="M12 2v2"/><path d="m4.9 4.9 1.4 1.4"/><path d="m19.1 4.9-1.4 1.4"/></svg> Пароль скомпрометирован!</div>
        Этот пароль встречается в утечках <span class="cnt">${count.toLocaleString('ru-RU')}</span> раз.
        <ul>
          <li>Смени его ВЕЗДЕ, где используешь — прямо сейчас</li>
          <li>Включи двухфакторную защиту (2FA) в банках и почте</li>
          <li>Используй разные пароли для разных сервисов</li>
        </ul>`;
    }else{
      res.className='res show ok';
      res.innerHTML=`<div class="big"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> В известных утечках не найден</div>
        Это не гарантия абсолютной безопасности, но в 900+ млн утёкших паролей его нет.
        Совет: длина 12+ символов и уникальность для каждого сервиса важнее сложности.`;
    }
  }catch(e){
    res.className='res show bad';
    res.innerHTML='<div class="big"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Сервис недоступен</div>Попробуйте позже — проверка идёт напрямую в HaveIBeenPwned.';
  }
  btn.disabled=false; btn.textContent='Проверить утечку';
}
$('#go').onclick=checkLeak;
$('#pw').addEventListener('keydown',e=>{if(e.key==='Enter')checkLeak();});

// ── Tabs ──
document.querySelectorAll('.tabb').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('.tabb').forEach(x=>x.classList.toggle('on',x===b));
  document.getElementById('card-pw').style.display=b.dataset.t==='pw'?'block':'none';
  document.getElementById('card-em').style.display=b.dataset.t==='em'?'block':'none';
});
// ── Email breach check (XposedOrNot via backend proxy) ──
async function checkEmail(){
  const em=document.getElementById('em').value.trim();
  const R=document.getElementById('resem');
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em)){R.className='res show';R.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Введите корректный email.';return}
  R.className='res show';R.innerHTML='Проверяем базы утечек...';
  try{
    const r=await fetch('/leak/email?email='+encodeURIComponent(em));
    if(r.status===429){R.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> Слишком часто — подождите минуту.';return}
    if(!r.ok){R.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Сервис утечек недоступен, попробуйте позже.';return}
    const d=await r.json();
    if(!d.breached){R.innerHTML='<b style="color:var(--green,#9ece6a)"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> Не найден в известных утечках.</b><br>Это не гарантия — используйте уникальные пароли и 2FA.';}
    else{
      const esc=t=>{const x=document.createElement('div');x.textContent=t;return x.innerHTML};
      R.innerHTML='<b style="color:var(--red,#f7768e)"><svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 18v-6a5 5 0 1 1 10 0v6"/><path d="M5 21a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2z"/><path d="M12 2v2"/><path d="m4.9 4.9 1.4 1.4"/><path d="m19.1 4.9-1.4 1.4"/></svg> Найден в '+d.count+' утечках:</b><br>'+
        d.breaches.map(b=>'• '+esc(b)).join('<br>')+
        '<br><br><b>Что делать:</b> смените пароли на этих сервисах, включите 2FA, не переиспользуйте пароли.';
    }
  }catch(e){R.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> Ошибка сети.'}
}
document.getElementById('goem').onclick=checkEmail;
document.getElementById('em').addEventListener('keydown',e=>{if(e.key==='Enter')checkEmail()});

// ── Password generator (client-side only) ──
function genPw(){
  const L=+document.getElementById('genlen').value;
  const sym=document.getElementById('gensym').checked;
  const abc='abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'+(sym?'!@#$%^&*-_=+?':'');
  const buf=new Uint32Array(L);crypto.getRandomValues(buf);
  document.getElementById('genout').value=[...buf].map(n=>abc[n%abc.length]).join('');
}
document.getElementById('gengo').onclick=genPw;
document.getElementById('gencopy').onclick=async()=>{
  const v=document.getElementById('genout').value;if(!v)return;
  try{await navigator.clipboard.writeText(v);document.getElementById('gencopy').innerHTML=QI.check;
      setTimeout(()=>document.getElementById('gencopy').innerHTML=QI.copy,1200);}catch(e){}
};
