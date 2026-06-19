// Qalqan AI v5.0
// Content Script: блоктау (XSS-safe — тек textContent/createElement)
// API-ға сұраныс жібермейді — background.js-тен команда күтеді

let isBlocked = false;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "BLOCK_PAGE" && !isBlocked) {
    blockPage(message.data);
    sendResponse({ status: "blocked" });
    return true;
  }

  if (message.action === "GET_LINKS") {
    const links = [...new Set(
      Array.from(document.querySelectorAll("a[href]"))
        .map(a => { try { return new URL(a.href).href; } catch { return null; } })
        .filter(h => h && (h.startsWith("http://") || h.startsWith("https://")))
        .filter(h => !h.startsWith(window.location.origin))
    )].slice(0, 20);
    sendResponse({ links, total: document.querySelectorAll("a[href]").length });
    return true;
  }
});

function esc(str) {
  return String(str ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#x27;");
}

// ═══════════════ i18n ═══════════════
const _I18N = {
  kk: {
    brand: "QALQAN AI — КИБЕР ҚАЛҚАН",
    blocked: "БҰЛ САЙТ БҰҒАТТАЛДЫ",
    subtitle: "Qalqan AI қауіп анықтады және сізді қорғады",
    threatScore: "Қауіп деңгейі",
    threatType: "Қауіп түрі",
    detectedThreat: "Анықталған қауіп",
    dataSource: "Дерек көзі",
    back: "← Қауіпсіз жерге қайту",
    appeal: "Қателік деп ойласаңыз — кеңейтімдегі «Апелляция» батырмасын басыңыз",
    domainAge: "Домен жасы", days: "күн",
    ssl: { valid: "✅ SSL жарамды", expired: "❌ SSL мерзімі өткен", self_signed: "⚠️ Өзі қол қойған", no_ssl: "🔓 SSL жоқ", expiring_soon: "⚠️ SSL жақында аяқталады" }
  },
  ru: {
    brand: "QALQAN AI — КИБЕР ЩИТ",
    blocked: "САЙТ ЗАБЛОКИРОВАН",
    subtitle: "Qalqan AI обнаружил угрозу и защитил вас",
    threatScore: "Уровень угрозы",
    threatType: "Тип угрозы",
    detectedThreat: "Обнаруженная угроза",
    dataSource: "Источник данных",
    back: "← Вернуться в безопасное место",
    appeal: "Считаете это ошибкой? Нажмите «Апелляция» в расширении",
    domainAge: "Возраст домена", days: "дн.",
    ssl: { valid: "✅ SSL действителен", expired: "❌ SSL просрочен", self_signed: "⚠️ Самоподписанный", no_ssl: "🔓 Нет SSL", expiring_soon: "⚠️ SSL скоро истекает" }
  },
  en: {
    brand: "QALQAN AI — CYBER SHIELD",
    blocked: "SITE BLOCKED",
    subtitle: "Qalqan AI detected a threat and protected you",
    threatScore: "Threat Level",
    threatType: "Threat Type",
    detectedThreat: "Detected Threat",
    dataSource: "Data Source",
    back: "← Return to Safety",
    appeal: "Think this is an error? Click 'Appeal' in the extension",
    domainAge: "Domain age", days: "days",
    ssl: { valid: "✅ SSL valid", expired: "❌ SSL expired", self_signed: "⚠️ Self-signed", no_ssl: "🔓 No SSL", expiring_soon: "⚠️ SSL expiring soon" }
  }
};

const _TYPES = {
  kk: { phishing: "Фишинг", malware: "Зиянды бағдарлама", pyramid: "Қаржылық пирамида", scam: "Алаяқтық", gambling: "Лицензиясыз құмар ойын", fake_shop: "Жалған дүкен", social_engineering: "Әлеуметтік инженерия", suspicious_infrastructure: "Күдікті инфрақұрылым", safe: "Қауіпсіз", unknown: "Белгісіз қауіп" },
  ru: { phishing: "Фишинг", malware: "Вредоносное ПО", pyramid: "Финансовая пирамида", scam: "Мошенничество", gambling: "Нелицензированный гемблинг", fake_shop: "Поддельный магазин", social_engineering: "Социальная инженерия", suspicious_infrastructure: "Подозрительная инфраструктура", safe: "Безопасно", unknown: "Неизвестная угроза" },
  en: { phishing: "Phishing", malware: "Malware", pyramid: "Financial Pyramid", scam: "Scam", gambling: "Unlicensed Gambling", fake_shop: "Fake Shop", social_engineering: "Social Engineering", suspicious_infrastructure: "Suspicious Infrastructure", safe: "Safe", unknown: "Unknown Threat" }
};

const _SOURCES = {
  phishtank: "PhishTank", google_safe_browsing: "Google Safe Browsing", urlhaus: "URLhaus",
  openphish: "OpenPhish", virustotal: "VirusTotal", pyramid_list: "Qalqan Pyramid DB",
  gambling_list: "Qalqan Gambling DB", kz_intel_gambling: "KZ Gambling Intel",
  phishing_list: "Phishing DB", local_blacklist: "Blacklist",
  domain_intel: "Domain Intelligence", groq_ai: "Groq AI (Llama 70B)",
  gemini_ai: "Gemini AI Analysis", groq_vision: "Qalqan Vision AI",
  gemini_vision: "Qalqan Vision AI", kz_intel: "KZ Intel",
  kz_impersonation: "KZ Brand Protection", offline_pyramid: "Offline: Pyramid DB",
  offline_gambling: "Offline: Gambling DB", offline_phishing: "Offline: Phishing DB",
  offline_scam: "Offline: Scam DB", url_features: "URL Feature Analysis",
  quick_check: "Qalqan Quick Check", kz_impersonation: "KZ Brand Protection"
};

// ═══════════════ Main ═══════════════
function blockPage(data) {
  isBlocked = true;
  chrome.storage.local.get("qalqan_lang", (r) => {
    _render(data, r.qalqan_lang || "kk");
  });
}

function _render(data, lang) {
  const t = _I18N[lang] || _I18N.kk;
  const types = _TYPES[lang] || _TYPES.kk;

  const score    = Number(data.threat_score || 0);
  const reason   = esc(data[`detail_${lang}`] || data.detail || data.detail_kk || "");
  const srcKey   = data.source || "unknown";
  const ttKey    = data.threat_type || "unknown";
  const typeName = esc(types[ttKey] || types.unknown);
  const srcName  = esc(_SOURCES[srcKey] || srcKey);

  // Extract and display the blocked domain
  let blockedDomain = "";
  try { blockedDomain = new URL(window.location.href).hostname.replace("www.", ""); } catch {}
  const domainDisplay = blockedDomain ? esc(blockedDomain) : "";

  // Color palette based on score severity
  const isMax    = score >= 90;
  const scoreRgb = isMax ? "255,45,85" : score >= 70 ? "239,68,68" : "245,158,11";
  const scoreHex = isMax ? "#ff2d55"   : score >= 70 ? "#ef4444"   : "#f59e0b";

  // Domain extras
  const dd = data.domain_details || {};
  const indicators = (data.indicators || []).slice(0, 6);

  // Build extra info (domain age, ssl)
  let extraLines = [];
  if (dd.domain_age_days !== undefined) {
    const age = dd.domain_age_days;
    const ac = age < 30 ? "#f87171" : age < 90 ? "#fbbf24" : "#64748b";
    extraLines.push(`<span style="color:${ac};display:inline-flex;align-items:center;gap:4px;"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> ${esc(t.domainAge)}: ${age} ${esc(t.days)}</span>`);
  }
  if (dd.ssl && t.ssl[dd.ssl.status]) {
    const sslOk = dd.ssl.status === "valid";
    const sslIcon = sslOk
      ? `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`
      : `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#f87171" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>`;
    extraLines.push(`<span style="color:${sslOk ? "#22c55e" : "#f87171"};display:inline-flex;align-items:center;gap:4px;">${sslIcon} ${t.ssl[dd.ssl.status]}</span>`);
  }

  // CSS
  const css = `
    *{margin:0;padding:0;box-sizing:border-box;}
    html,body{width:100%;height:100%;background:#020617;overflow:hidden;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;}

    /* ── Layered background ── */
    #qbg{
      position:fixed;inset:0;z-index:0;
      background:
        radial-gradient(ellipse 90% 60% at 50% -5%, rgba(${scoreRgb},0.18) 0%, transparent 60%),
        radial-gradient(ellipse 55% 70% at 85% 90%, rgba(99,102,241,0.09) 0%, transparent 55%),
        radial-gradient(ellipse 45% 50% at 5%  70%, rgba(59,130,246,0.07) 0%, transparent 50%),
        linear-gradient(160deg,#020617 0%,#0f172a 45%,#160c2e 100%);
    }
    #qgrid{
      position:fixed;inset:0;z-index:1;pointer-events:none;
      background-image:
        linear-gradient(rgba(${scoreRgb},0.035) 1px,transparent 1px),
        linear-gradient(90deg,rgba(${scoreRgb},0.035) 1px,transparent 1px);
      background-size:44px 44px;
    }
    /* Glowing orbs */
    #qorb1{position:fixed;width:420px;height:420px;border-radius:50%;top:-120px;left:-80px;z-index:0;
      background:radial-gradient(circle,rgba(${scoreRgb},0.07),transparent 70%);pointer-events:none;}
    #qorb2{position:fixed;width:340px;height:340px;border-radius:50%;bottom:-80px;right:-60px;z-index:0;
      background:radial-gradient(circle,rgba(99,102,241,0.06),transparent 70%);pointer-events:none;}

    /* ── Center container ── */
    #qcenter{
      position:fixed;inset:0;z-index:10;
      display:flex;align-items:center;justify-content:center;
      padding:16px;
    }

    /* ── Main card ── */
    #qcard{
      width:100%;max-width:540px;max-height:calc(100vh - 32px);overflow-y:auto;
      scrollbar-width:none;
      background:rgba(13,20,38,0.88);
      backdrop-filter:blur(28px);-webkit-backdrop-filter:blur(28px);
      border:1px solid rgba(${scoreRgb},0.28);
      border-radius:24px;
      padding:36px 32px 28px;
      position:relative;overflow:hidden;
      box-shadow:0 0 90px rgba(${scoreRgb},0.14),0 32px 80px rgba(0,0,0,0.7);
      animation:qSlideIn 0.55s cubic-bezier(0.21,0.47,0.32,0.98) both;
    }
    #qcard::-webkit-scrollbar{display:none;}

    /* Top glow line */
    #qcard::before{
      content:'';position:absolute;top:0;left:0;right:0;height:2px;
      background:linear-gradient(90deg,transparent 5%,rgba(${scoreRgb},0.85) 50%,transparent 95%);
    }
    /* Inner radial sheen */
    #qcard::after{
      content:'';position:absolute;inset:0;pointer-events:none;
      background:radial-gradient(ellipse 70% 35% at 50% 0%,rgba(${scoreRgb},0.07),transparent);
    }

    /* ── Shield header ── */
    #qheader{display:flex;flex-direction:column;align-items:center;text-align:center;margin-bottom:28px;gap:0;}

    #qshield-wrap{position:relative;width:84px;height:84px;margin-bottom:18px;flex-shrink:0;}
    #qshield-ring{
      position:absolute;inset:-5px;border-radius:50%;
      background:conic-gradient(from 0deg,transparent 65%,rgba(${scoreRgb},0.45) 80%,${scoreHex} 88%,rgba(${scoreRgb},0.45) 96%,transparent 100%);
      animation:qSpin 4s linear infinite;
    }
    #qshield-icon{
      width:84px;height:84px;border-radius:50%;
      background:rgba(${scoreRgb},0.1);
      border:1px solid rgba(${scoreRgb},0.3);
      display:flex;align-items:center;justify-content:center;
      color:${scoreHex};
      position:relative;z-index:1;
      animation:qPulse 2.5s ease-in-out infinite;
    }

    #qbrand{font-size:10px;font-weight:700;letter-spacing:3px;color:${scoreHex};opacity:0.7;margin-bottom:8px;text-transform:uppercase;}
    #qtitle{font-size:clamp(20px,4vw,26px);font-weight:900;color:#f1f5f9;letter-spacing:-0.3px;line-height:1.1;}
    #qsubtitle{font-size:13px;color:#475569;margin-top:6px;line-height:1.4;}
    #qdomain{font-size:12px;font-family:'SF Mono','Fira Code','Courier New',monospace;color:rgba(${scoreRgb},0.75);
      background:rgba(${scoreRgb},0.07);border:1px solid rgba(${scoreRgb},0.15);
      border-radius:6px;padding:5px 12px;margin-top:8px;word-break:break-all;max-width:100%;
      display:inline-flex;align-items:center;gap:6px;}

    /* ── Metrics row ── */
    #qmetrics{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px;}
    .qm{
      background:rgba(${scoreRgb},0.06);
      border:1px solid rgba(${scoreRgb},0.12);
      border-radius:14px;padding:14px 16px;
    }
    .qm-label{font-size:10px;font-weight:600;letter-spacing:1.2px;text-transform:uppercase;color:#475569;margin-bottom:6px;font-family:'SF Mono','Fira Code',monospace;}
    .qm-score{display:flex;align-items:baseline;gap:4px;}
    .qm-num{font-size:32px;font-weight:900;color:${scoreHex};line-height:1;}
    .qm-denom{font-size:16px;font-weight:600;color:#475569;}
    .qm-type{font-size:14px;font-weight:700;color:#f87171;line-height:1.3;margin-top:4px;}

    /* Score arc */
    .qarc-wrap{margin-top:6px;width:100%;}
    .qarc-track{width:100%;height:5px;background:rgba(255,255,255,0.06);border-radius:4px;overflow:hidden;}
    .qarc-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,rgba(${scoreRgb},0.5),${scoreHex});
      width:0%;transition:width 1.2s cubic-bezier(0.34,1.56,0.64,1);}

    /* ── Reason box ── */
    #qreason{
      background:rgba(0,0,0,0.22);
      border:1px solid rgba(255,255,255,0.05);
      border-radius:14px;padding:16px;margin-bottom:14px;
    }
    .qr-label{font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#64748b;margin-bottom:8px;font-family:'SF Mono','Fira Code',monospace;display:flex;align-items:center;gap:6px;}
    .qr-text{font-size:13px;color:#94a3b8;line-height:1.65;}
    .qr-extras{font-size:12px;color:#475569;margin-top:8px;display:flex;flex-direction:column;gap:3px;}
    .qtags{display:flex;flex-wrap:wrap;gap:5px;margin-top:10px;}
    .qtag{
      font-size:10px;font-weight:600;padding:3px 9px;border-radius:20px;letter-spacing:0.3px;
      background:rgba(${scoreRgb},0.1);color:${scoreHex};border:1px solid rgba(${scoreRgb},0.22);
    }

    /* ── Source line ── */
    #qsource{font-size:11px;color:#475569;text-align:center;margin-bottom:16px;
      background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.04);
      border-radius:8px;padding:7px 12px;font-family:'SF Mono','Fira Code',monospace;
      display:flex;align-items:center;justify-content:center;gap:6px;}

    /* ── Back button — only action ── */
    #qback{
      width:100%;
      background:rgba(0,212,255,0.08);
      color:#00d4ff;
      border:1.5px solid rgba(0,212,255,0.5);
      padding:15px 28px;
      border-radius:12px;
      cursor:pointer;font-weight:700;font-size:14px;
      font-family:'SF Mono','Fira Code','Consolas',monospace;
      letter-spacing:1.5px;text-transform:uppercase;
      box-shadow:0 0 20px rgba(0,212,255,0.12);
      transition:all 0.2s;
      position:relative;overflow:hidden;
    }
    #qback::before{
      content:'';position:absolute;top:0;left:-100%;width:60%;height:100%;
      background:linear-gradient(90deg,transparent,rgba(0,212,255,0.1),transparent);
      transition:left 0.4s;
    }
    #qback:hover{
      background:rgba(0,212,255,0.14);
      box-shadow:0 0 32px rgba(0,212,255,0.25),inset 0 0 20px rgba(0,212,255,0.04);
      border-color:#00d4ff;
    }
    #qback:hover::before{left:200%;}
    #qback:active{transform:scale(0.98);}

    /* ── Appeal ── */
    #qappeal{font-size:11px;color:#334155;text-align:center;margin-top:14px;line-height:1.55;}

    /* ── Animations ── */
    @keyframes qSlideIn{
      from{opacity:0;transform:translateY(36px) scale(0.95);}
      to{opacity:1;transform:translateY(0) scale(1);}
    }
    @keyframes qPulse{
      0%,100%{box-shadow:0 0 0 0 rgba(${scoreRgb},0.5);}
      50%{box-shadow:0 0 0 14px rgba(${scoreRgb},0);}
    }
    @keyframes qSpin{
      from{transform:rotate(0deg);}
      to{transform:rotate(360deg);}
    }

    @media(max-width:500px){
      #qcard{padding:24px 16px 20px;}
      #qtitle{font-size:18px;}
      .qm-num{font-size:26px;}
    }
  `;

  // Build indicator tags HTML (escaped)
  const tagHTML = indicators.map(i => `<span class="qtag">${esc(i)}</span>`).join("");
  const extraHTML = extraLines.map(l => `<div>${l}</div>`).join("");

  // Rebuild page cleanly
  document.documentElement.innerHTML = "<head></head><body></body>";

  // Style
  const styleEl = document.createElement("style");
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  // DOM tree (no unsafe innerHTML for user content — only esc() strings)
  document.body.innerHTML = `
    <div id="qbg"></div>
    <div id="qgrid"></div>
    <div id="qorb1"></div>
    <div id="qorb2"></div>
    <div id="qcenter">
      <div id="qcard">
        <div id="qheader">
          <div id="qshield-wrap">
            <div id="qshield-ring"></div>
            <div id="qshield-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                <line x1="9" y1="9" x2="15" y2="15" stroke-width="2"/><line x1="15" y1="9" x2="9" y2="15" stroke-width="2"/>
              </svg>
            </div>
          </div>
          <div id="qbrand">${esc(t.brand)}</div>
          <div id="qtitle">${esc(t.blocked)}</div>
          <div id="qsubtitle">${esc(t.subtitle)}</div>
          ${domainDisplay ? `<div id="qdomain">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0">
              <circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
            </svg>
            ${domainDisplay}
          </div>` : ""}
        </div>

        <div id="qmetrics">
          <div class="qm">
            <div class="qm-label">${esc(t.threatScore)}</div>
            <div class="qm-score">
              <span class="qm-num">${score}</span>
              <span class="qm-denom">/100</span>
            </div>
            <div class="qarc-wrap">
              <div class="qarc-track">
                <div class="qarc-fill" id="qarc-fill"></div>
              </div>
            </div>
          </div>
          <div class="qm">
            <div class="qm-label">${esc(t.threatType)}</div>
            <div class="qm-type">${typeName}</div>
          </div>
        </div>

        <div id="qreason">
          <div class="qr-label">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            ${esc(t.detectedThreat)}
          </div>
          <div class="qr-text">${reason}</div>
          ${extraHTML ? `<div class="qr-extras">${extraHTML}</div>` : ""}
          ${tagHTML ? `<div class="qtags">${tagHTML}</div>` : ""}
        </div>

        <div id="qsource">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
          ${esc(t.dataSource)}: ${srcName}
        </div>

        <button id="qback">${esc(t.back)}</button>

        ${ttKey === "gambling" ? `<div style="margin-top:14px;padding:10px 14px;background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);border-radius:8px;text-align:center;">
          <div style="font-size:11px;color:#22c55e;font-weight:600;margin-bottom:4px;display:flex;align-items:center;gap:5px;justify-content:center;">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.45 2 2 0 0 1 3.6 1h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.56a16 16 0 0 0 6 6l.88-.88a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            ${lang === "kk" ? "Лудомания — емделетін ауру" : lang === "ru" ? "Лудомания — это болезнь, которую лечат" : "Gambling addiction is treatable"}
          </div>
          <div style="font-size:11px;color:#94a3b8;">${lang === "kk" ? "Тегін психологиялық көмек:" : lang === "ru" ? "Бесплатная психологическая помощь:" : "Free helpline (Kazakhstan):"} <strong style="color:#f8fafc;">8-800-080-88-87</strong></div>
        </div>` : ""}

        <p id="qappeal">${esc(t.appeal)}</p>
        <p style="font-size:10px;color:#334155;text-align:center;margin-top:8px;font-family:'SF Mono','Fira Code',monospace;letter-spacing:0.5px;">ESC → ${esc(t.back)}</p>
      </div>
    </div>
  `;

  // Wire back button
  document.getElementById("qback").addEventListener("click", () => window.history.back());

  // ESC key also goes back
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") window.history.back();
  });

  // Animate score arc after render
  requestAnimationFrame(() => {
    const arc = document.getElementById("qarc-fill");
    if (arc) {
      requestAnimationFrame(() => { arc.style.width = `${score}%`; });
    }
  });
}

// ═══════════════ Passive DOM Security Scan ═══════════════
// Runs after page load — detects suspicious page patterns without API calls
const _KZ_BRANDS_DOM = ['kaspi', 'halyk', 'egov', 'salyk', 'kcell', 'beeline',
                         'jysan', 'bereke', 'kolesa', 'tengri', 'homebank'];
const _PRIZE_KW_DOM  = ['вы выиграли', 'сіз ұтып', 'you won', 'ұтып алдыңыз',
                         'получите приз', 'бонус активирован', 'ваш приз'];

function _passiveDomScan() {
  if (isBlocked) return; // already blocked — no need
  try {
    const title = (document.title || '').toLowerCase();
    const bodyText = (document.body?.innerText || '').slice(0, 3000).toLowerCase();

    const hasPasswordInput = !!document.querySelector('input[type="password"]');
    const matchedBrand = _KZ_BRANDS_DOM.find(b => title.includes(b) || bodyText.includes(b));

    // Credential harvesting: password form + KZ brand on non-official domain
    if (hasPasswordInput && matchedBrand) {
      try {
        chrome.runtime.sendMessage({
          action: 'DOM_SUSPICIOUS',
          reason: 'credential_form_kz_brand',
          brand: matchedBrand,
          title: document.title.slice(0, 80),
        });
      } catch {}
    }

    // Fake prize / lottery scam text
    const hasPrize = _PRIZE_KW_DOM.some(k => bodyText.includes(k));
    if (hasPrize) {
      try {
        chrome.runtime.sendMessage({
          action: 'DOM_SUSPICIOUS',
          reason: 'prize_scam_text',
        });
      } catch {}
    }
  } catch {}
}

// Run after DOM ready
if (document.readyState === 'complete' || document.readyState === 'interactive') {
  setTimeout(_passiveDomScan, 1500); // slight delay for dynamic content
} else {
  window.addEventListener('load', () => setTimeout(_passiveDomScan, 1500), { once: true });
}
