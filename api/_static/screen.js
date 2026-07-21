const QT={
 kk:{h1:'Скриншотты тексеру',sub:'Күдікті SMS, «банктен» хабарлама, «инвестиция» жарнамасы келді ме? Скриншот жасап жүктеңіз — AI мәтінді оқып, алаяқтық па екенін айтады.',drop_t:'Скриншотты басыңыз немесе сүйреңіз',drop_h:'JPG/PNG 3 МБ-қа дейін · хат-хабар, SMS, сайт, хабарландыру',go:'Тексеру',big:'Файл 3 МБ-тан үлкен — скриншотты қысқартыңыз.',reading:'AI скриншотты оқуда...',wait:'Талдау (20 сек-қа дейін)...',toofast:'Тым жиі — минутына ең көбі 5 скриншот.',err:'Талдау қатесі. Кейінірек көріңіз.'},
 ru:{h1:'Проверка скриншота',sub:'Пришло подозрительное SMS, сообщение «из банка», объявление об «инвестициях»? Сделай скриншот и загрузи — AI прочитает текст и скажет, мошенничество ли это.',drop_t:'Нажми или перетащи скриншот',drop_h:'JPG/PNG до 3 МБ · переписка, SMS, сайт, объявление',go:'Проверить',big:'Файл больше 3 МБ — сожмите или обрежьте скриншот.',reading:'AI читает скриншот...',wait:'Анализ (до 20 сек)...',toofast:'Слишком часто — максимум 5 скриншотов в минуту.',err:'Ошибка анализа. Попробуйте позже.'}};
const T=k=>QTL.t(QT,k);
const QI={octagon:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.86 2h8.28L22 7.86v8.28L16.14 22H7.86L2 16.14V7.86z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>',alert:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',checkc:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',check:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',copy:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="8" width="14" height="14" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>'};
const $=s=>document.querySelector(s);
let b64=null;
const drop=$('#drop'),file=$('#file');
drop.onclick=()=>file.click();
drop.addEventListener('dragover',e=>{e.preventDefault();drop.classList.add('over')});
drop.addEventListener('dragleave',()=>drop.classList.remove('over'));
drop.addEventListener('drop',e=>{e.preventDefault();drop.classList.remove('over');if(e.dataTransfer.files[0])load(e.dataTransfer.files[0])});
file.addEventListener('change',()=>{if(file.files[0])load(file.files[0])});
function load(f){
  if(f.size>3.2*1024*1024){alert(T('big'));return}
  const rd=new FileReader();
  rd.onload=()=>{
    const s=String(rd.result);
    b64=s.substring(s.indexOf(',')+1);
    $('#preview').src=s;$('#preview').style.display='block';
    $('#go').style.display='block';
    $('#res').style.display='none';
  };
  rd.readAsDataURL(f);
}
$('#go').onclick=async()=>{
  if(!b64)return;
  const btn=$('#go');btn.disabled=true;btn.textContent=T('reading');
  const R=$('#res');R.className='res';R.style.display='block';R.textContent=T('wait');
  try{
    const lang=localStorage.getItem('qlang')||'ru';
    const r=await fetch('/analyze-screen',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image_base64:b64,lang:lang==='kk'?'kk':lang==='en'?'en':'ru'})});
    if(r.status===429){R.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> '+T('toofast')+'';btn.disabled=false;btn.textContent=T('go');return}
    const d=await r.json();
    const v=(d.verdict||'').toUpperCase();
    const em=v==='DANGEROUS'?QI.octagon:v==='SUSPICIOUS'?QI.alert:QI.checkc;
    R.className='res '+(v==='DANGEROUS'?'d':v==='SUSPICIOUS'?'s':'ok');
    const esc=t=>{const x=document.createElement('div');x.textContent=t;return x.innerHTML};
    const _vl={DANGEROUS:{kk:'Қауіпті',ru:'Опасно',en:'Dangerous'},SUSPICIOUS:{kk:'Күдікті',ru:'Подозрительно',en:'Suspicious'},SAFE:{kk:'Қауіпсіз',ru:'Безопасно',en:'Safe'}};
    const vlabel=(_vl[v]||{})[QTL.L]||v;
    R.innerHTML=`${em} <b>${esc(vlabel)} · ${esc(String(d.threat_score??'?'))}/100</b><br><br>${esc(d.detail||d['detail_'+QTL.L]||d.detail_ru||'')}`;
  }catch(e){R.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg> '+T('err')+''}
  btn.disabled=false;btn.textContent=T('go');
};

QTL.mount(QT,()=>{const b=$('#go');if(b&&!b.disabled)b.textContent=T('go');});
