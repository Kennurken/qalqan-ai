// Base facts (KZ 2025): ~26 300 cases, 16.4bn ₸ over 10 months → annualized.
const CASES_YR = 26300 * 12/10;         // annualized cases ≈ 31 560
const LOSS_YR = 16.4e9 * 12/10;         // annualized ₸ loss ≈ 19.68bn
const AVG_LOSS = LOSS_YR / CASES_YR;    // ≈ 623 000 ₸ per case
const ADULTS_KZ = 13500000;             // ~adult population exposed
const CASE_RATE = CASES_YR / ADULTS_KZ; // annual victim probability

const I18N={
  ru:{h1:'Экономический эффект',sub:'Сколько денег Qalqan AI может сберечь для граждан Казахстана. Расчёт основан на официальной статистике 2025 года.',
    s1:'украдено за 10 мес. 2025 (×29 к 2024)',s2:'случаев кибермошенничества (+86%)',
    lb1:'Пользователей Qalqan AI: ',lb2:'Эффективность блокировки: ',outLbl:'Предотвращённый ущерб в год',
    r1:'Средний ущерб на случай',r2:'Ожидаемых жертв среди пользователей/год',r3:'Из них защищено Qalqan AI',
    perUser:u=>`≈ ${u} ₸ сбережено на пользователя в год`,
    disc:'Оценка. Источник базовых цифр: официальная статистика МВД/Нацбанка РК за 2025 г. Расчёт: (население-риск × частота × средний ущерб × охват × эффективность).'},
  kk:{h1:'Экономикалық әсер',sub:'Qalqan AI Қазақстан азаматтары үшін қанша ақша үнемдей алады. Есеп 2025 жылғы ресми статистикаға негізделген.',
    s1:'2025 жылдың 10 айында ұрланды (2024-ке ×29)',s2:'кибералаяқтық дерегі (+86%)',
    lb1:'Qalqan AI қолданушылары: ',lb2:'Блоктау тиімділігі: ',outLbl:'Жылына болдырмаған залал',
    r1:'Бір дерекке орташа залал',r2:'Қолданушылар арасында күтілетін құрбандар/жыл',r3:'Оның ішінде Qalqan AI қорғады',
    perUser:u=>`≈ жылына бір қолданушыға ${u} ₸ үнемделді`,
    disc:'Бағалау. Негізгі сандар көзі: ҚР ІІМ/Ұлттық банктің 2025 ж. ресми статистикасы. Есеп: (тәуекел-халық × жиілік × орташа залал × қамту × тиімділік).'}
};
let L=localStorage.getItem('qlang')||'ru'; if(L!=='kk'&&L!=='ru')L='ru';
const $=s=>document.querySelector(s);
const fmt=n=>Math.round(n).toLocaleString('ru-RU').replace(/,/g,' ');
function money(n){
  if(n>=1e9) return (n/1e9).toFixed(1).replace('.',',')+' млрд ₸';
  if(n>=1e6) return (n/1e6).toFixed(1).replace('.',',')+' млн ₸';
  return fmt(n)+' ₸';
}
function calc(){
  const users=+$('#users').value, eff=+$('#eff').value/100;
  const victims=users*CASE_RATE;
  const saved=victims*eff;
  const prevented=saved*AVG_LOSS;
  const perUser=prevented/users;
  $('#vUsers').textContent=fmt(users);
  $('#vEff').textContent=(eff*100)+'%';
  $('#amount').textContent=money(prevented);
  $('#perUser').textContent=I18N[L].perUser(fmt(perUser));
  $('#avgLoss').textContent=money(AVG_LOSS);
  $('#victims').textContent=fmt(victims);
  $('#saved').textContent=fmt(saved);
}
function applyLang(l){
  L=(l==='kk'||l==='ru')?l:'ru'; localStorage.setItem('qlang',L);
  const D=I18N[L];
  document.querySelectorAll('.lang button').forEach(b=>b.classList.toggle('on',b.dataset.l===L));
  $('#h1').textContent=D.h1; $('#sub').textContent=D.sub; $('#s1').textContent=D.s1; $('#s2').textContent=D.s2;
  $('#lb1').firstChild.textContent=D.lb1; $('#lb2').firstChild.textContent=D.lb2;
  $('#outLbl').textContent=D.outLbl; $('#r1').textContent=D.r1; $('#r2').textContent=D.r2; $('#r3').textContent=D.r3;
  $('#disc').textContent=D.disc; document.documentElement.lang=L;
  calc();
}
$('#users').addEventListener('input',calc);
$('#eff').addEventListener('input',calc);
document.querySelectorAll('.lang button').forEach(b=>b.addEventListener('click',()=>applyLang(b.dataset.l)));
applyLang(L);
