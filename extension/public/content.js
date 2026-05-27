// Qalqan AI v5.0
// Content Script: блоктау (XSS-safe — тек textContent/createElement)
// API-ға сұраныс жібермейді — background.js-тен команда күтеді

let isBlocked = false;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "BLOCK_PAGE" && !isBlocked) {
    chrome.storage.session.get("bypass_list", (result) => {
      const bypassList = result.bypass_list || [];
      if (bypassList.includes(window.location.href)) {
        sendResponse({ status: "bypassed" });
        return;
      }
      blockPage(message.data);
      sendResponse({ status: "blocked" });
    });
    return true; // keep channel open for async response
  }

  if (message.action === "GET_LINKS") {
    // Collect unique external links from page (max 20)
    const links = [...new Set(
      Array.from(document.querySelectorAll("a[href]"))
        .map(a => { try { return new URL(a.href).href; } catch { return null; } })
        .filter(h => h && (h.startsWith("http://") || h.startsWith("https://")))
        .filter(h => !h.startsWith(window.location.origin))  // external only
    )].slice(0, 20);
    sendResponse({ links, total: document.querySelectorAll("a[href]").length });
    return true;
  }
});

function esc(str) {
  // Sanitize — тек текст, HTML/JS injection жоқ
  return String(str ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#x27;").replace(/\//g, "&#x2F;");
}

const _BLOCK_I18N = {
  kk: {
    title: "БҰЛ САЙТ БҰҒАТТАЛДЫ",
    threatLevel: "Қауіп деңгейі", threatType: "Қауіп түрі",
    reason: "Себебі:", source: "Дерек көзі:",
    domainAge: "Домен жасы", days: "күн",
    back: "← Қауіпсіз жерге қайту",
    bypass: "Сайтқа кіру",
    bypassWarn: "Жауапкершілік өзіңізде",
    bypassCountdown: (n) => `${n}с...`,
    appeal: "Қателік бар деп ойлайсыз ба? Кеңейтімдегі Апелляция батырмасын басыңыз.",
    sslStatus: { valid: "✅ SSL жарамды", expired: "❌ SSL мерзімі өткен", self_signed: "⚠️ Өзі қол қойған SSL", no_ssl: "🔓 SSL жоқ", expiring_soon: "⚠️ SSL жақында аяқталады" }
  },
  ru: {
    title: "САЙТ ЗАБЛОКИРОВАН",
    threatLevel: "Уровень угрозы", threatType: "Тип угрозы",
    reason: "Причина:", source: "Источник:",
    domainAge: "Возраст домена", days: "дн.",
    back: "← Вернуться в безопасное место",
    bypass: "Перейти на сайт",
    bypassWarn: "На свой страх и риск",
    bypassCountdown: (n) => `${n}с...`,
    appeal: "Считаете это ошибкой? Нажмите кнопку Апелляция в расширении.",
    sslStatus: { valid: "✅ SSL действителен", expired: "❌ SSL просрочен", self_signed: "⚠️ Самоподписанный SSL", no_ssl: "🔓 Нет SSL", expiring_soon: "⚠️ SSL скоро истекает" }
  },
  en: {
    title: "SITE BLOCKED",
    threatLevel: "Threat Level", threatType: "Threat Type",
    reason: "Reason:", source: "Source:",
    domainAge: "Domain age", days: "days",
    back: "← Go back to safety",
    bypass: "Proceed to site",
    bypassWarn: "At your own risk",
    bypassCountdown: (n) => `${n}s...`,
    appeal: "Think this is a mistake? Click Appeal in the extension.",
    sslStatus: { valid: "✅ SSL valid", expired: "❌ SSL expired", self_signed: "⚠️ Self-signed SSL", no_ssl: "🔓 No SSL", expiring_soon: "⚠️ SSL expiring soon" }
  }
};

const _TYPE_NAMES = {
  kk: { phishing: "Фишинг", malware: "Зиянды БҚ", pyramid: "Қаржылық пирамида", scam: "Алаяқтық", gambling: "Құмар ойын", fake_shop: "Жалған дүкен", social_engineering: "Әлеуметтік инженерия", suspicious_infrastructure: "Күдікті инфрақұрылым", casino: "Казино", case_battle: "Кейс-батл", unknown: "Белгісіз қауіп" },
  ru: { phishing: "Фишинг", malware: "Вредоносное ПО", pyramid: "Финансовая пирамида", scam: "Мошенничество", gambling: "Азартные игры", fake_shop: "Поддельный магазин", social_engineering: "Социальная инженерия", suspicious_infrastructure: "Подозрительная инфраструктура", casino: "Казино", case_battle: "Кейс-батл", unknown: "Неизвестная угроза" },
  en: { phishing: "Phishing", malware: "Malware", pyramid: "Financial Pyramid", scam: "Scam", gambling: "Gambling", fake_shop: "Fake Shop", social_engineering: "Social Engineering", suspicious_infrastructure: "Suspicious Infrastructure", casino: "Casino", case_battle: "Case Battle", unknown: "Unknown Threat" }
};

const _SOURCE_NAMES = {
  phishtank: "PhishTank", google_safe_browsing: "Google Safe Browsing",
  urlhaus: "URLhaus", openphish: "OpenPhish", virustotal: "VirusTotal",
  pyramid_list: "Qalqan Pyramid DB", gambling_list: "Gambling DB", phishing_list: "Phishing DB",
  local_blacklist: "Blacklist", domain_intel: "Domain Intelligence",
  groq_ai: "Qalqan AI", gemini_ai: "Qalqan AI", groq_vision: "Qalqan Vision AI",
  gemini_vision: "Qalqan Vision AI", kz_intel: "KZ Intelligence",
  offline_pyramid: "Offline: Pyramid DB", offline_gambling: "Offline: Gambling DB",
  offline_casebattle: "Offline: Case Battle DB", offline_phishing: "Offline: Phishing DB",
  offline_scam: "Offline: Scam DB", offline_tld: "Offline: TLD Check",
  url_features: "URL Analysis", kz_impersonation: "KZ Brand Protection"
};

function blockPage(data) {
  isBlocked = true;
  // Read language setting then render
  chrome.storage.local.get("qalqan_lang", (r) => {
    const lang = r.qalqan_lang || "kk";
    _renderBlockPage(data, lang);
  });
}

function _renderBlockPage(data, lang) {
  const i18n = _BLOCK_I18N[lang] || _BLOCK_I18N.kk;
  const typeNames = _TYPE_NAMES[lang] || _TYPE_NAMES.kk;

  const score = esc(data.threat_score || "?");
  const reason = esc(data[`detail_${lang}`] || data.detail || data.detail_kk || "");
  const source = esc(data.source || "unknown");
  const threatType = esc(data.threat_type || "unknown");
  const typeName = esc(typeNames[threatType] || typeNames.unknown);
  const sourceName = esc(_SOURCE_NAMES[source] || source);

  // Domain info extras
  const domainDetails = data.domain_details || {};
  const indicators = (data.indicators || []).slice(0, 5);
  let extraInfo = "";

  if (domainDetails.domain_age_days !== undefined) {
    const ageDays = domainDetails.domain_age_days;
    const ageColor = ageDays < 30 ? "#f87171" : ageDays < 90 ? "#fbbf24" : "#94a3b8";
    extraInfo += `<div style="font-size:12px;color:${ageColor};margin-top:8px;">📅 ${esc(i18n.domainAge)}: ${esc(ageDays)} ${esc(i18n.days)}</div>`;
  }

  if (domainDetails.ssl) {
    const ssl = domainDetails.ssl;
    const sslText = i18n.sslStatus[ssl.status] || "";
    let sslExtra = "";
    if (ssl.status === "valid" && ssl.days_left) sslExtra = ` (${esc(ssl.days_left)}d)`;
    if (ssl.status === "expired" && ssl.days_expired) sslExtra = ` (${esc(ssl.days_expired)}d ago)`;
    if (ssl.issuer) sslExtra += ` — ${esc(ssl.issuer)}`;
    if (sslText) extraInfo += `<div style="font-size:12px;color:#94a3b8;margin-top:4px;">${sslText}${sslExtra}</div>`;
  }

  if (indicators.length > 0) {
    extraInfo += `<div style="margin-top:8px;display:flex;gap:4px;flex-wrap:wrap;">${indicators.map(i => `<span style="font-size:10px;background:rgba(239,68,68,0.15);padding:2px 6px;border-radius:4px;color:#fca5a5;">${esc(i)}</span>`).join("")}</div>`;
  }

  const root = document.createElement("div");
  root.style.cssText = "background:linear-gradient(135deg,#0f172a,#1e1b4b);color:#f1f5f9;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Segoe UI',system-ui,sans-serif;text-align:center;padding:20px;margin:0;";

  root.innerHTML = `
    <div style="max-width:520px;width:100%;">
      <div style="margin-bottom:8px;">
        <div style="display:inline-flex;align-items:center;gap:12px;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:16px;padding:12px 24px;">
          <span style="font-size:40px;">🛡️</span>
          <div>
            <div style="font-size:28px;font-weight:800;color:#ef4444;">QALQAN AI</div>
            <div style="font-size:11px;color:#94a3b8;letter-spacing:2px;">CYBER SHIELD v5.0</div>
          </div>
        </div>
      </div>
      <div style="background:rgba(30,41,59,0.6);backdrop-filter:blur(16px);border:2px solid #ef4444;border-radius:20px;padding:28px;margin:20px 0;">
        <p style="font-size:22px;font-weight:800;color:#ef4444;margin:0 0 16px;">⛔ ${esc(i18n.title)}</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;text-align:left;margin-bottom:16px;">
          <div style="background:rgba(239,68,68,0.1);padding:12px;border-radius:10px;">
            <div style="font-size:11px;color:#94a3b8;">${esc(i18n.threatLevel)}</div>
            <div style="font-size:24px;font-weight:800;color:#ef4444;">${score}/100</div>
          </div>
          <div style="background:rgba(239,68,68,0.1);padding:12px;border-radius:10px;">
            <div style="font-size:11px;color:#94a3b8;">${esc(i18n.threatType)}</div>
            <div style="font-size:16px;font-weight:700;color:#f87171;">${typeName}</div>
          </div>
        </div>
        <div style="text-align:left;background:rgba(0,0,0,0.2);padding:14px;border-radius:10px;margin-bottom:12px;">
          <div style="font-size:11px;color:#94a3b8;margin-bottom:6px;">📋 ${esc(i18n.reason)}</div>
          <div style="font-size:14px;color:#e2e8f0;line-height:1.5;">${reason}</div>
          ${extraInfo}
        </div>
        <div style="font-size:11px;color:#64748b;">🔍 ${esc(i18n.source)} ${sourceName}</div>
      </div>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
        <button id="qalqan-back-btn" style="background:linear-gradient(135deg,#3b82f6,#2563eb);color:white;border:none;padding:14px 28px;border-radius:12px;cursor:pointer;font-weight:700;font-size:15px;">${esc(i18n.back)}</button>
        <button id="qalqan-bypass-btn" disabled style="background:rgba(30,41,59,0.6);color:#64748b;border:1px solid #334155;padding:14px 20px;border-radius:12px;cursor:not-allowed;font-size:13px;" data-countdown="5">⏳ ${esc(i18n.bypass)} (5s...)</button>
      </div>
      <p style="font-size:11px;color:#475569;margin-top:24px;">${esc(i18n.appeal)}</p>
    </div>`;

  document.documentElement.replaceChildren(root);

  document.getElementById("qalqan-back-btn").addEventListener("click", () => window.history.back());

  // Bypass countdown — 5 second delay to prevent accidents
  const bypassBtn = document.getElementById("qalqan-bypass-btn");
  let countdown = 5;
  const timer = setInterval(() => {
    countdown--;
    if (countdown <= 0) {
      clearInterval(timer);
      bypassBtn.disabled = false;
      bypassBtn.style.cursor = "pointer";
      bypassBtn.style.color = "#94a3b8";
      bypassBtn.textContent = `${i18n.bypass} — ${i18n.bypassWarn}`;
    } else {
      bypassBtn.textContent = `⏳ ${i18n.bypass} (${countdown}s...)`;
    }
  }, 1000);

  bypassBtn.addEventListener("click", () => {
    if (bypassBtn.disabled) return;
    chrome.runtime.sendMessage({ action: "BYPASS", url: window.location.href });
    isBlocked = false;
    window.location.reload();
  });
}
