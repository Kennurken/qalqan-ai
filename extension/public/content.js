// клауд Елдоса N1 — Qalqan AI v4.0
// Content Script: блоктау (XSS-safe — тек textContent/createElement)
// API-ға сұраныс жібермейді — background.js-тен команда күтеді

let isBlocked = false;

chrome.runtime.onMessage.addListener((message) => {
  if (message.action === "BLOCK_PAGE" && !isBlocked) {
    chrome.storage.session.get("bypass_list", (result) => {
      const bypassList = result.bypass_list || [];
      if (bypassList.includes(window.location.href)) return;
      blockPage(message.data);
    });
  }
});

function esc(str) {
  // Sanitize — тек текст, HTML/JS injection жоқ
  return String(str ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#x27;").replace(/\//g, "&#x2F;");
}

function blockPage(data) {
  isBlocked = true;
  const score = esc(data.threat_score || "?");
  const reason = esc(data.detail || data.detail_kk || "Бұл сайт қауіпті деп танылды.");
  const source = esc(data.source || "unknown");
  const threatType = esc(data.threat_type || "unknown");

  const typeNames = {
    phishing: "Фишинг", malware: "Зиянды БҚ", pyramid: "Қаржылық пирамида",
    scam: "Алаяқтық", gambling: "Құмар ойын", fake_shop: "Жалған дүкен",
    social_engineering: "Әлеуметтік инженерия", suspicious_infrastructure: "Күдікті инфрақұрылым",
    unknown: "Белгісіз қауіп"
  };
  const sourceNames = {
    phishtank: "PhishTank", google_safe_browsing: "Google Safe Browsing",
    urlhaus: "URLhaus", openphish: "OpenPhish", pyramid_list: "Qalqan Pyramid DB",
    domain_intel: "Domain Intelligence", groq_ai: "Qalqan AI", gemini_ai: "Qalqan AI",
    gemini_vision: "Qalqan Vision", local_blacklist: "Blacklist"
  };

  const typeName = esc(typeNames[threatType] || typeNames.unknown);
  const sourceName = esc(sourceNames[source] || source);

  // Domain info көрсету
  const domainDetails = data.domain_details || {};
  let extraInfo = "";
  if (domainDetails.domain_age_days !== undefined) {
    extraInfo += `<div style="font-size:12px;color:#fbbf24;margin-top:8px;">📅 Домен жасы: ${esc(domainDetails.domain_age_days)} күн</div>`;
  }
  if (domainDetails.ssl) {
    const sslStatus = {valid:"✅ SSL жарамды", expired:"❌ SSL мерзімі өткен", self_signed:"⚠️ Өзі қол қойған SSL", no_ssl:"🔓 SSL жоқ"};
    extraInfo += `<div style="font-size:12px;color:#94a3b8;margin-top:4px;">${sslStatus[domainDetails.ssl.status] || ""}</div>`;
  }

  // Бүкіл бетті қауіпсіз тәсілмен ауыстыру
  const root = document.createElement("div");
  root.style.cssText = "background:linear-gradient(135deg,#0f172a,#1e1b4b);color:#f1f5f9;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Segoe UI',system-ui,sans-serif;text-align:center;padding:20px;margin:0;";

  root.innerHTML = `
    <div style="max-width:520px;width:100%;">
      <div style="margin-bottom:8px;">
        <div style="display:inline-flex;align-items:center;gap:12px;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:16px;padding:12px 24px;">
          <span style="font-size:40px;">🛡️</span>
          <div>
            <div style="font-size:28px;font-weight:800;color:#ef4444;">QALQAN AI</div>
            <div style="font-size:11px;color:#94a3b8;letter-spacing:2px;">CYBER SHIELD v4.0</div>
          </div>
        </div>
      </div>
      <div style="background:rgba(30,41,59,0.6);backdrop-filter:blur(16px);border:2px solid #ef4444;border-radius:20px;padding:28px;margin:20px 0;">
        <p style="font-size:22px;font-weight:800;color:#ef4444;margin:0 0 16px;">⛔ Бұл сайт бұғатталды!</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;text-align:left;margin-bottom:16px;">
          <div style="background:rgba(239,68,68,0.1);padding:12px;border-radius:10px;">
            <div style="font-size:11px;color:#94a3b8;">Қауіп деңгейі</div>
            <div style="font-size:24px;font-weight:800;color:#ef4444;">${score}/100</div>
          </div>
          <div style="background:rgba(239,68,68,0.1);padding:12px;border-radius:10px;">
            <div style="font-size:11px;color:#94a3b8;">Қауіп түрі</div>
            <div style="font-size:16px;font-weight:700;color:#f87171;">${typeName}</div>
          </div>
        </div>
        <div style="text-align:left;background:rgba(0,0,0,0.2);padding:14px;border-radius:10px;margin-bottom:12px;">
          <div style="font-size:11px;color:#94a3b8;margin-bottom:6px;">📋 Себебі:</div>
          <div style="font-size:14px;color:#e2e8f0;line-height:1.5;">${reason}</div>
          ${extraInfo}
        </div>
        <div style="font-size:11px;color:#64748b;">🔍 Дерек көзі: ${sourceName}</div>
      </div>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
        <button id="qalqan-back-btn" style="background:linear-gradient(135deg,#3b82f6,#2563eb);color:white;border:none;padding:14px 28px;border-radius:12px;cursor:pointer;font-weight:700;font-size:15px;">← Қауіпсіз жерге қайту</button>
        <button id="qalqan-bypass-btn" style="background:transparent;color:#64748b;border:1px solid #334155;padding:14px 20px;border-radius:12px;cursor:pointer;font-size:13px;">Сайтқа кіру (жауапкершілік өзіңізде)</button>
      </div>
      <p style="font-size:11px;color:#475569;margin-top:24px;">Қателік бар деп ойлайсыз ба? Кеңейтімдегі Апелляция батырмасын басыңыз.</p>
    </div>`;

  document.documentElement.replaceChildren(root);

  document.getElementById("qalqan-back-btn").addEventListener("click", () => window.history.back());
  document.getElementById("qalqan-bypass-btn").addEventListener("click", () => {
    chrome.runtime.sendMessage({ action: "BYPASS", url: window.location.href });
    isBlocked = false;
    window.location.reload();
  });
}
