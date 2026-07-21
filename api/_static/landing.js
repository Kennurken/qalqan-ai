document.documentElement.classList.add('js');
const $=s=>document.querySelector(s);
const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const io=new IntersectionObserver((es)=>{es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
document.querySelectorAll('.reveal').forEach((el,i)=>{el.style.transitionDelay=(Math.min(i%6,5)*60)+'ms';io.observe(el)});
function countUp(el){
  const to=+el.dataset.to||0, suf=el.dataset.suffix||'', dec=+el.dataset.dec||0;
  const fmt=v=>dec?v.toLocaleString('ru-RU',{minimumFractionDigits:dec,maximumFractionDigits:dec}):Math.round(v).toLocaleString('ru-RU');
  if(reduce||!to){el.textContent=fmt(to)+suf;return}
  const dur=1200, t0=performance.now();
  (function tick(t){const p=Math.min((t-t0)/dur,1);const e=1-Math.pow(1-p,3);
    el.textContent=fmt(to*e)+suf;
    if(p<1)requestAnimationFrame(tick)})(t0);
}
const statIO=new IntersectionObserver((es)=>{es.forEach(e=>{if(e.isIntersecting){countUp(e.target);statIO.unobserve(e.target)}})},{threshold:.5});
document.querySelectorAll('.stat .n[data-to], .prob .pn [data-to]').forEach(el=>statIO.observe(el));
if(!reduce){
  document.querySelectorAll('.tilt').forEach(card=>{
    card.addEventListener('mousemove',e=>{
      const r=card.getBoundingClientRect();
      const px=(e.clientX-r.left)/r.width, py=(e.clientY-r.top)/r.height;
      card.style.transform=`perspective(900px) rotateX(${(py-.5)*-5}deg) rotateY(${(px-.5)*5}deg) translateY(-4px)`;
      card.style.setProperty('--mx',px*100+'%');card.style.setProperty('--my',py*100+'%');
    });
    card.addEventListener('mouseleave',()=>{card.style.transform=''});
  });
}
/* i18n — kk/ru/en. AI/verdict comes back in currentLang (sent to /check). */
const I18N={
 kk:{nav_feat:'Функциялар',nav_arch:'Архитектура',nav_demo:'Демо',nav_tech:'Технологиялар',nav_install:'Орнату',n_map:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Карта',chip_leak:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> Құпиясөз утечкасы',chip_map:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Қауіп картасы',proof:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> 97% дәлдік · 0 жалған дабыл · ашық бенчмаркте (F1 0.98)',
     badge:'v5.1 · Қазақстан үшін · Open source',h1a:'Алаяқтықтан',h1b:'AI қорғанысы',
     lead:'Фишинг, телефон алаяқтығы, қаржылық пирамида, гемблинг және госзакуп фроды — бәрін бет жүктелмей тұрып анықтаймыз. Тегін.',
     checkPh:'kaspi-bonus.kz немесе https://...',checkBtn:'Тексеру',
     st_checked:'Тексерілді',st_blocked:'Бұғатталды',st_offline:'Офлайн база',st_levels:'Деңгей',err:'Қате',errd:'Кейінірек қайталаңыз',
     s_prob_e:'Неге керек',s_prob_t:'Қазақстандағы цифрлық алаяқтық',s_prob_s:'2025 жылғы 10 айдағы ресми статистика — масштаб орасан.',
     s_feat_e:'Функционал',s_feat_t:'Не қорғайды',s_feat_s:'7-деңгейлі pipeline — 1 мс кэш-тексеруден AI анализіне дейін.',
     s_arch_e:'Архитектура',s_arch_t:'7-деңгейлі анықтау',s_arch_s:'Әр сұраныс жеті қабаттан өтеді — жылдамнан тереңге.',
     s_demo_e:'Демо',s_demo_t:'Бәрі тірі — ашып көріңіз',s_demo_s:'Жұмыс істеп тұрған платформалар мен панельдер.',
     s_tech_e:'Технологиялар',s_tech_t:'Стек',s_faq_e:'Сұрақ-жауап',s_faq_t:'Жиі қойылатын сұрақтар',s_faq_s:'Нақты жауаптар — артық сөзсіз.',
     q1:'Тегін бе?',q2:'Менің деректерім қауіпсіз бе?',q3:'Қалай жұмыс істейді?',q4:'Қандай қауіптерді анықтайды?',q5:'Қай тілдерде?',q6:'Интернетсіз жұмыс істей ме?',q7:'Банктер/реттеушілер қалай қосыла алады?',
     f1t:'Фишинг сайттары',f2t:'Телефон алаяқтығы',f3t:'Қаржылық пирамидалар',f4t:'Нелегал гемблинг',f5t:'Госзакуп фроды',
     f1d:'Kaspi, eGov, Halyk Bank клондарын анықтайды — homoglyph (кириллица әріптерін) және typosquat шабуылдарын қоса. Бет жүктелуіне дейін бұғаттайды.',
     f2d:'Дауыстық хабарламаны Whisper арқылы транскрипциялап, ҚР скам-паттерндерін табады. #1 қауіп — енді одан қорғаныс бар.',
     f3d:'АФМ реестрі бойынша атау тексеру + Finiko, MMM, HYIP базасы.',f4d:'80+ ҚР-да тыйым салынған сайт. 1xBet, Mostbet — браузерде ашылмайды.',
     f5d:'Тапсырыс беруші↔жеткізуші↔құрылтайшы граф: аффилированность, сговор, картель.',
     d1t:'Реттеуші панелі',d2t:'Госзакуп графы',d3t:'Мобиль қосымша',d4t:'Telegram бот',d5t:'Тірі статистика',
     d1d:'Облыстар бойынша қауіп картасы, динамика, топ домендер.',d2d:'Аффилированность, сговор, картель — байланыс графы.',d3d:'Офлайн жұмыс істейді, телефонға орнатылады (PWA).',d4d:'Дауыс / SMS / сілтеме тексеру, KZ-CERT-ке хабарлау.',d5d:'Нақты деректер: тексерулер, вердиктер, трендтер.',d6d:'Ашық дерекқор (CC-BY) — басқа жүйелер пайдалана алады.',
     arrow:'Ашу →',tg_t:'Telegram-да тексер',tg_d:'Кез келген сілтемені, нөмірді, дауыстық хабарламаны жіберіп, бірден жауап ал.'},
 ru:{nav_feat:'Функции',nav_arch:'Архитектура',nav_demo:'Демо',nav_tech:'Технологии',nav_install:'Установить',n_map:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Карта',chip_leak:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> Пароль утёк?',chip_map:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Карта угроз',proof:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> 97% точность · 0 ложных срабатываний · открытый бенчмарк (F1 0.98)',
     badge:'v5.1 · Для Казахстана · Open source',h1a:'Защита от',h1b:'мошенников · AI',
     lead:'Фишинг, телефонный скам, финансовые пирамиды, гемблинг и госзакуп-фрод — ловим до загрузки страницы. Бесплатно.',
     checkPh:'kaspi-bonus.kz или https://...',checkBtn:'Проверить',
     st_checked:'Проверено',st_blocked:'Заблокировано',st_offline:'Офлайн-база',st_levels:'Уровней',err:'Ошибка',errd:'Повторите позже',
     s_prob_e:'Зачем нужно',s_prob_t:'Цифровое мошенничество в Казахстане',s_prob_s:'Официальная статистика за 10 месяцев 2025 — масштаб огромен.',
     s_feat_e:'Функционал',s_feat_t:'От чего защищает',s_feat_s:'7-уровневый pipeline — от 1 мс кэша до AI-анализа.',
     s_arch_e:'Архитектура',s_arch_t:'7-уровневое обнаружение',s_arch_s:'Каждый запрос проходит 7 уровней — от быстрого к глубокому.',
     s_demo_e:'Демо',s_demo_t:'Всё вживую — откройте',s_demo_s:'Работающие платформы и панели.',
     s_tech_e:'Технологии',s_tech_t:'Стек',s_faq_e:'Вопрос-ответ',s_faq_t:'Частые вопросы',s_faq_s:'Точные ответы — без воды.',
     q1:'Это бесплатно?',q2:'Мои данные в безопасности?',q3:'Как это работает?',q4:'Какие угрозы детектит?',q5:'На каких языках?',q6:'Работает без интернета?',q7:'Как подключаются банки/регуляторы?',
     f1t:'Фишинговые сайты',f2t:'Телефонное мошенничество',f3t:'Финансовые пирамиды',f4t:'Нелегальный гемблинг',f5t:'Фрод в госзакупках',
     f1d:'Детектит клоны Kaspi, eGov, Halyk Bank — включая homoglyph (кириллица) и typosquat. Блокирует до загрузки страницы.',
     f2d:'Транскрибирует голосовое через Whisper и находит KZ скам-паттерны. Угроза №1 — теперь есть защита.',
     f3d:'Проверка названия по реестру АФМ + база Finiko, MMM, HYIP.',f4d:'80+ запрещённых в РК сайтов. 1xBet, Mostbet — не откроются в браузере.',
     f5d:'Граф заказчик↔поставщик↔учредитель: аффилированность, сговор, картель.',
     d1t:'Панель регулятора',d2t:'Граф госзакупок',d3t:'Мобильное приложение',d4t:'Telegram бот',d5t:'Живая статистика',
     d1d:'Карта угроз по областям, динамика, топ-домены.',d2d:'Аффилированность, сговор, картель — граф связей.',d3d:'Работает офлайн, ставится на телефон (PWA).',d4d:'Голос / SMS / ссылка, сообщение в KZ-CERT.',d5d:'Реальные данные: проверки, вердикты, тренды.',d6d:'Открытая база (CC-BY) — могут использовать другие системы.',
     arrow:'Открыть →',tg_t:'Проверь в Telegram',tg_d:'Отправь любую ссылку, номер или голосовое — получи ответ сразу.'},
 en:{nav_feat:'Features',nav_arch:'Architecture',nav_demo:'Demo',nav_tech:'Tech',nav_install:'Install',n_map:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Map',chip_leak:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="0.5"/></svg> Password leak check',chip_map:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg> Threat map',proof:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> 97% accuracy · 0 false positives · open benchmark (F1 0.98)',
     badge:'v5.1 · For Kazakhstan · Open source',h1a:'AI shield',h1b:'against scams',
     lead:'Phishing, phone scams, financial pyramids, gambling and procurement fraud — caught before the page loads. Free.',
     checkPh:'kaspi-bonus.kz or https://...',checkBtn:'Check',
     st_checked:'Checked',st_blocked:'Blocked',st_offline:'Offline DB',st_levels:'Tiers',err:'Error',errd:'Try again later',
     s_prob_e:'Why it matters',s_prob_t:'Digital fraud in Kazakhstan',s_prob_s:'Official stats for 10 months of 2025 — the scale is huge.',
     s_feat_e:'Features',s_feat_t:'What it protects',s_feat_s:'7-tier pipeline — from 1ms cache to AI analysis.',
     s_arch_e:'Architecture',s_arch_t:'7-tier detection',s_arch_s:'Every request passes 7 tiers — fast to deep.',
     s_demo_e:'Demo',s_demo_t:'All live — open it',s_demo_s:'Working platforms and dashboards.',
     s_tech_e:'Technology',s_tech_t:'Stack',s_faq_e:'FAQ',s_faq_t:'Frequently asked',s_faq_s:'Precise answers — no fluff.',
     q1:'Is it free?',q2:'Is my data safe?',q3:'How does it work?',q4:'What threats does it detect?',q5:'Which languages?',q6:'Does it work offline?',q7:'How can banks/regulators integrate?',
     f1t:'Phishing sites',f2t:'Phone scams',f3t:'Financial pyramids',f4t:'Illegal gambling',f5t:'Procurement fraud',
     f1d:'Detects Kaspi, eGov, Halyk Bank clones — incl. homoglyph (Cyrillic) and typosquat. Blocks before the page loads.',
     f2d:'Transcribes voice via Whisper and finds KZ scam patterns. The #1 threat — now defended.',
     f3d:'Name lookup against the AFM registry + Finiko, MMM, HYIP database.',f4d:'80+ banned-in-KZ sites. 1xBet, Mostbet are blocked in the browser.',
     f5d:'Customer↔supplier↔founder graph: affiliation, collusion, cartel.',
     d1t:'Regulator dashboard',d2t:'Procurement graph',d3t:'Mobile app',d4t:'Telegram bot',d5t:'Live stats',
     d1d:'Regional threat map, trends, top domains.',d2d:'Affiliation, collusion, cartel — relationship graph.',d3d:'Works offline, installs on your phone (PWA).',d4d:'Voice / SMS / link check, report to KZ-CERT.',d5d:'Real data: checks, verdicts, trends.',d6d:'Open dataset (CC-BY) — usable by other systems.',
     arrow:'Open →',tg_t:'Check in Telegram',tg_d:'Send any link, number or voice message — get an answer instantly.'}
};
/* Default for the KZ audience: honor a saved choice, else browser lang only if it's
   kk/ru, otherwise fall back to ru (universally understood here) — never surprise a
   Kazakh jury with an English page just because the demo laptop's locale is en. */
let _nav=(navigator.language||'').slice(0,2).toLowerCase();
let currentLang=localStorage.getItem('qlang')||(['kk','ru'].includes(_nav)?_nav:'ru');
if(!I18N[currentLang])currentLang='ru';
function applyLang(l){
  currentLang=I18N[l]?l:'kk'; localStorage.setItem('qlang',currentLang);
  const D=I18N[currentLang];
  document.querySelectorAll('[data-i18n]').forEach(el=>{const v=D[el.dataset.i18n];if(v!=null)el.innerHTML=v;});
  document.querySelectorAll('[data-i18n-ph]').forEach(el=>{const v=D[el.dataset.i18nPh];if(v!=null)el.placeholder=v;});
  document.documentElement.lang=currentLang;
  document.querySelectorAll('#langSw button').forEach(b=>b.classList.toggle('on',b.dataset.lang===currentLang));
}
document.querySelectorAll('#langSw button').forEach(b=>b.addEventListener('click',()=>applyLang(b.dataset.lang)));
applyLang(currentLang);

const box=$('#resultBox'),verdict=$('#resultVerdict'),detail=$('#resultDetail'),btn=$('#checkBtn'),input=$('#urlInput');
// Context-menu / deep-link entry: /?check=<url> pre-fills and runs the checker.
try{
  const _q=new URLSearchParams(location.search).get('check');
  if(_q){ input.value=_q.slice(0,2048); setTimeout(()=>btn.click(),600);
          window.scrollTo({top:0}); }
}catch(e){}
async function runCheck(){
  const url=input.value.trim(); if(!url)return;
  btn.disabled=true; const old=btn.textContent; btn.textContent='...';
  try{
    const res=await fetch('/check',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url,lang:currentLang})});
    // NEVER fail-open: 429/403/500 must not render as an empty "<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg> 0/100" verdict
    if(res.status===429){
      box.className='result show SUSPICIOUS';
      verdict.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>  '+(currentLang==='kk'?'Тым көп сұраныс — 1 минуттан кейін қайталаңыз':currentLang==='en'?'Too many requests — retry in a minute':'Слишком много запросов — повторите через минуту');
      detail.textContent='';
      btn.disabled=false; btn.textContent=old; return;
    }
    if(!res.ok) throw new Error('http '+res.status);
    const d=await res.json();
    if(!d.verdict) throw new Error('bad payload');
    const V=(d.verdict||'').toUpperCase();
    // Localized verdict word (was always English) + neutral state for non-URLs.
    const VL={DANGEROUS:{kk:'Қауіпті',ru:'Опасно',en:'Dangerous'},SUSPICIOUS:{kk:'Күдікті',ru:'Подозрительно',en:'Suspicious'},SAFE:{kk:'Қауіпсіз',ru:'Безопасно',en:'Safe'},UNKNOWN:{kk:'Сілтеме емес',ru:'Не ссылка',en:'Not a link'}};
    const label=(VL[V]||{})[currentLang]||V;
    box.className='result show '+(V==='UNKNOWN'?'':V);
    const ic=V==='DANGEROUS'?'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.86 2h8.28L22 7.86v8.28L16.14 22H7.86L2 16.14V7.86z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>':V==='SUSPICIOUS'?'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>':V==='UNKNOWN'?'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>':'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';
    verdict.innerHTML=ic+'  '+label+(V==='UNKNOWN'?'':' · '+(d.threat_score||0)+'/100');
    detail.textContent=d.detail||d['detail_'+currentLang]||d.detail_kk||'';
  }catch(e){box.className='result show SUSPICIOUS';verdict.innerHTML='<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>  '+I18N[currentLang].err;detail.textContent=I18N[currentLang].errd;}
  btn.disabled=false; btn.textContent=old;
}
btn.addEventListener('click',runCheck);
input.addEventListener('keydown',e=>{if(e.key==='Enter')runCheck()});
// /trends is where total_checks + verdict_distribution actually live (/stats has neither)
fetch('/trends').then(r=>r.json()).then(t=>{
  const set=(id,v)=>{const el=document.getElementById(id);if(el&&v!=null){el.dataset.to=v;countUp(el)}};
  const dist=t.verdict_distribution||{};
  const checks=t.total_checks||0;
  set('statChecked',checks);
  set('statBlocked',(dist.DANGEROUS||0)+(dist.SUSPICIOUS||0));
  // Live pilot ticker: most-reported domain from real crowd data (only when we have activity)
  const rep=(t.top_reported_domains||[]);
  if(checks>0){
    const L={kk:'Соңғы бұғатталған қауіп: ',ru:'Недавно заблокировано: ',en:'Recently blocked: '}[currentLang]||'<svg class="qi" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7" fill="#f7768e"/></svg> ';
    const dom=rep.length?rep[0].domain:null;
    const w=document.getElementById('livewrap'), tx=document.getElementById('livetxt');
    if(w&&tx){ tx.textContent = dom ? (L+dom) : ({kk:'Пилот белсенді — нақты уақыттағы қорғаныс',ru:'Пилот активен — защита в реальном времени',en:'Pilot live — real-time protection'}[currentLang]||''); w.style.display='inline-flex'; }
  }
}).catch(()=>{});

/* scroll progress */
const prog=document.getElementById('progress');
addEventListener('scroll',()=>{const h=document.documentElement;const m=h.scrollHeight-h.clientHeight;prog.style.width=(m>0?h.scrollTop/m*100:0)+'%';},{passive:true});

/* theme toggle (respects prefers-color-scheme; persists) */
const SUN='<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4 12H2M22 12h-2M5 5l1.4 1.4M17.6 17.6 19 19M19 5l-1.4 1.4M6.4 17.6 5 19"/></svg>';
const MOON='<svg viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
const tb=document.getElementById('themeBtn'), tcMeta=document.querySelector('meta[name=theme-color]');
function applyTheme(t){document.documentElement.dataset.theme=t;tb.innerHTML=t==='light'?MOON:SUN;if(tcMeta)tcMeta.setAttribute('content',t==='light'?'#f5f7fc':'#0a0e16');}
applyTheme(localStorage.getItem('qtheme')||(window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark'));
tb.addEventListener('click',()=>{const n=document.documentElement.dataset.theme==='light'?'dark':'light';localStorage.setItem('qtheme',n);applyTheme(n);});

/* magnetic buttons */
if(!reduce){document.querySelectorAll('.mag').forEach(b=>{
  b.addEventListener('mousemove',e=>{const r=b.getBoundingClientRect();b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.22}px,${(e.clientY-r.top-r.height/2)*.32}px)`;});
  b.addEventListener('mouseleave',()=>b.style.transform='');
});}

/* pipeline packet lights up steps as it flows */
if(!reduce){
  const steps=[...document.querySelectorAll('#pipeline .pstep')], pk=document.getElementById('packet');
  if(pk&&steps.length)setInterval(()=>{const x=pk.getBoundingClientRect().left+5;steps.forEach(s=>{const r=s.getBoundingClientRect();s.classList.toggle('lit',x>=r.left&&x<=r.right);});},90);
}

/* PWA install banner */
let dp; const ib=document.getElementById('ibanner');
addEventListener('beforeinstallprompt',e=>{e.preventDefault();dp=e;if(!localStorage.getItem('qib'))setTimeout(()=>ib.classList.add('show'),2800);});
document.getElementById('ibYes').addEventListener('click',async()=>{ib.classList.remove('show');if(dp){dp.prompt();await dp.userChoice;dp=null;}});
document.getElementById('ibNo').addEventListener('click',()=>{ib.classList.remove('show');localStorage.setItem('qib','1');});

;/* ---- next block ---- */;

// ── QR check on web: decode an uploaded/captured QR image → run the URL checker.
//    BarcodeDetector (Chrome/Android native) → jsQR CDN fallback (Safari/Firefox).
(function(){
const F=document.getElementById('qrFile');
document.getElementById('qrBtn').onclick=()=>F.click();
function note(t){const rb=document.getElementById('resultBox'),rv=document.getElementById('resultVerdict');rb.className='result show';rv.textContent=t;document.getElementById('resultDetail').textContent='';}
async function toBitmap(file){return await createImageBitmap(file)}
async function decodeNative(bmp){
  if(!('BarcodeDetector' in window))return null;
  try{const det=new BarcodeDetector({formats:['qr_code']});const codes=await det.detect(bmp);return codes.length?codes[0].rawValue:null}catch(e){return null}
}
function loadJsQR(){return new Promise((res,rej)=>{
  if(window.jsQR)return res();
  const sc=document.createElement('script');sc.src='https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js';
  sc.onload=res;sc.onerror=rej;document.head.appendChild(sc);})}
async function decodeFallback(bmp){
  await loadJsQR();
  const c=document.createElement('canvas');const MAX=1200;
  const sc=Math.min(1,MAX/Math.max(bmp.width,bmp.height));
  c.width=bmp.width*sc;c.height=bmp.height*sc;
  const ctx=c.getContext('2d');ctx.drawImage(bmp,0,0,c.width,c.height);
  const img=ctx.getImageData(0,0,c.width,c.height);
  const r=window.jsQR(img.data,c.width,c.height);
  return r?r.data:null;
}
F.addEventListener('change',async()=>{
  const file=F.files&&F.files[0];F.value='';if(!file)return;
  note('Читаем QR-код...');
  try{
    const bmp=await toBitmap(file);
    let data=await decodeNative(bmp);
    if(!data)data=await decodeFallback(bmp);
    if(!data){note('QR-код не найден на фото. Снимите ближе и ровнее.');return}
    const inp=document.getElementById('urlInput');
    inp.value=data.trim();
    note('QR: '+data.trim().slice(0,80));
    document.getElementById('checkBtn').click();
  }catch(e){note('Не удалось обработать фото.')}
});
})();

;/* ---- next block ---- */;

const QI={octagon:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.86 2h8.28L22 7.86v8.28L16.14 22H7.86L2 16.14V7.86z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>',alert:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',checkc:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',check:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',copy:'<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="8" width="14" height="14" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>'};
(function(){
const P=document.getElementById('advPanel'),B=document.getElementById('advBtn'),M=document.getElementById('advMsgs');
const L={kk:{t:'Qalqan AI-кеңесші',h:'Жағдайды сипатта: қоңырау, SMS, «инвестиция» — алаяқтық па, айтамын.',ph:'Маған «банктен» қоңырау шалып жатыр...',think:'Талдап жатырмын...',err:'Қате. Кейінірек көріңіз.',rl:'Тым жиі — минут күтіңіз.',flags:'Қауіп белгілері',adv:'Не істеу керек'},
ru:{t:'AI-советник Qalqan',h:'Опиши ситуацию: звонок, SMS, «инвестиции» — скажу, скам ли это.',ph:'Мне звонят из «банка»...',think:'Анализирую...',err:'Ошибка. Попробуйте позже.',rl:'Слишком часто — подождите минуту.',flags:'Признаки угрозы',adv:'Что делать'},
en:{t:'Qalqan AI advisor',h:'Describe the situation: a call, SMS, an "investment" — I will tell you if it is a scam.',ph:'The "bank" is calling me...',think:'Analyzing...',err:'Error. Try later.',rl:'Too often — wait a minute.',flags:'Red flags',adv:'What to do'}};
function dict(){return L[typeof currentLang!=='undefined'?currentLang:'ru']||L.ru}
function applyAdvLang(){const D=dict();document.getElementById('advTitle').textContent=D.t;document.getElementById('advHint').textContent=D.h;document.getElementById('advTxt').placeholder=D.ph}
B.onclick=()=>{P.classList.toggle('open');applyAdvLang();if(P.classList.contains('open'))document.getElementById('advTxt').focus()};
document.getElementById('advClose').onclick=()=>P.classList.remove('open');
function add(cls,html){const d=document.createElement('div');d.className='advM '+cls;d.innerHTML=html;M.appendChild(d);M.scrollTop=M.scrollHeight;return d}
const esc=t=>{const d=document.createElement('div');d.textContent=t;return d.innerHTML};
let busy=false;
async function send(){
  if(busy)return;const T=document.getElementById('advTxt'),txt=T.value.trim();if(!txt)return;
  const D=dict();T.value='';add('u',esc(txt));const w=add('a',D.think);busy=true;
  try{
    const lang=typeof currentLang!=='undefined'?currentLang:'ru';
    const r=await fetch('/advisor',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:txt,lang})});
    if(r.status===429){w.textContent=D.rl;busy=false;return}
    const d=await r.json();
    const v=(d.verdict||'').toUpperCase();
    const em=v==='DANGEROUS'?QI.octagon:v==='SUSPICIOUS'?QI.alert:QI.checkc;
    w.className='advM a '+(v==='DANGEROUS'?'danger':v==='SUSPICIOUS'?'warn':'');
    const _vl={DANGEROUS:{kk:'Қауіпті',ru:'Опасно',en:'Dangerous'},SUSPICIOUS:{kk:'Күдікті',ru:'Подозрительно',en:'Suspicious'},SAFE:{kk:'Қауіпсіз',ru:'Безопасно',en:'Safe'}};
    const vlabel=(_vl[v]||{})[lang]||v;
    let h=`<b>${em} ${esc(vlabel)} · ${d.threat_score??''}/100</b>`;
    if(d.reasoning)h+=`<br>${esc(d.reasoning)}`;
    if(Array.isArray(d.red_flags)&&d.red_flags.length)h+=`<br><br><b>${D.flags}:</b><br>${d.red_flags.slice(0,5).map(f=>'• '+esc(f)).join('<br>')}`;
    if(Array.isArray(d.advice)&&d.advice.length)h+=`<br><br><b>${D.adv}:</b><br>${d.advice.slice(0,4).map(f=>'• '+esc(f)).join('<br>')}`;
    w.innerHTML=h;
  }catch(e){w.textContent=dict().err}
  busy=false;
}
document.getElementById('advSend').onclick=send;
document.getElementById('advTxt').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send()}});
})();
