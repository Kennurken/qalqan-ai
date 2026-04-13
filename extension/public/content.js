// клауд Елдоса N1 — Qalqan AI v3.0
// Content Script: тек блоктау + bypass функциясы
// API-ға өзі сұраныс жібермейді — background.js-тен команда күтеді

let isBlocked = false;

// Background-тан BLOCK_PAGE командасын тыңдау
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "BLOCK_PAGE" && !isBlocked) {
    // Bypass тізімін тексеру
    chrome.storage.session.get("bypass_list", (result) => {
      const bypassList = result.bypass_list || [];
      if (bypassList.includes(window.location.href)) {
        return; // Bypass — блоктамау
      }
      blockPage(message.data);
    });
  }
});

function blockPage(data) {
  isBlocked = true;
  const score = data.threat_score || "?";
  const reason = data.detail || data.detail_kk || "Бұл сайт қауіпті деп танылды.";
  const source = data.source || "unknown";
  const threatType = data.threat_type || "unknown";

  // Қауіп түрі атаулары
  const typeNames = {
    phishing: "Фишинг",
    malware: "Зиянды бағдарлама",
    pyramid: "Қаржылық пирамида",
    scam: "Алаяқтық",
    gambling: "Құмар ойын",
    fake_shop: "Жалған дүкен",
    social_engineering: "Әлеуметтік инженерия",
    unknown: "Белгісіз қауіп"
  };

  // Дерек көзі атаулары
  const sourceNames = {
    phishtank: "PhishTank Database",
    google_safe_browsing: "Google Safe Browsing",
    urlhaus: "URLhaus (abuse.ch)",
    openphish: "OpenPhish Feed",
    pyramid_list: "Qalqan Pyramid Database",
    local_blacklist: "Local Blacklist",
    ai: "Qalqan AI Analysis",
    ai_vision: "Qalqan AI Vision"
  };

  const typeName = typeNames[threatType] || typeNames.unknown;
  const sourceName = sourceNames[source] || source;

  document.documentElement.innerHTML = `
    <div style="
      background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
      color: #f1f5f9;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      text-align: center;
      padding: 20px;
      margin: 0;
    ">
      <div style="max-width: 520px; width: 100%;">
        <!-- Логотип -->
        <div style="margin-bottom: 8px;">
          <div style="
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 16px;
            padding: 12px 24px;
          ">
            <span style="font-size: 40px;">🛡️</span>
            <div>
              <div style="font-size: 28px; font-weight: 800; color: #ef4444;">QALQAN AI</div>
              <div style="font-size: 11px; color: #94a3b8; letter-spacing: 2px;">CYBER SHIELD v3.0</div>
            </div>
          </div>
        </div>

        <!-- Негізгі ескерту -->
        <div style="
          background: rgba(30, 41, 59, 0.6);
          backdrop-filter: blur(16px);
          border: 2px solid #ef4444;
          border-radius: 20px;
          padding: 28px;
          margin: 20px 0;
        ">
          <p style="font-size: 22px; font-weight: 800; color: #ef4444; margin: 0 0 16px;">
            ⛔ Бұл сайт бұғатталды!
          </p>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; text-align: left; margin-bottom: 16px;">
            <div style="background: rgba(239,68,68,0.1); padding: 12px; border-radius: 10px;">
              <div style="font-size: 11px; color: #94a3b8; margin-bottom: 4px;">Қауіп деңгейі</div>
              <div style="font-size: 24px; font-weight: 800; color: #ef4444;">${score}/100</div>
            </div>
            <div style="background: rgba(239,68,68,0.1); padding: 12px; border-radius: 10px;">
              <div style="font-size: 11px; color: #94a3b8; margin-bottom: 4px;">Қауіп түрі</div>
              <div style="font-size: 16px; font-weight: 700; color: #f87171;">${typeName}</div>
            </div>
          </div>

          <div style="text-align: left; background: rgba(0,0,0,0.2); padding: 14px; border-radius: 10px; margin-bottom: 12px;">
            <div style="font-size: 11px; color: #94a3b8; margin-bottom: 6px;">📋 Себебі:</div>
            <div style="font-size: 14px; color: #e2e8f0; line-height: 1.5;">${reason}</div>
          </div>

          <div style="font-size: 11px; color: #64748b;">
            🔍 Дерек көзі: ${sourceName}
          </div>
        </div>

        <!-- Батырмалар -->
        <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
          <button onclick="window.history.back()" style="
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 700;
            font-size: 15px;
            transition: all 0.2s;
          ">
            ← Қауіпсіз жерге қайту
          </button>
          <button id="qalqan-bypass-btn" style="
            background: transparent;
            color: #64748b;
            border: 1px solid #334155;
            padding: 14px 20px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s;
          ">
            Сайтқа кіру (жауапкершілік өзіңізде)
          </button>
        </div>

        <p style="font-size: 11px; color: #475569; margin-top: 24px;">
          Қателік бар деп ойлайсыз ба? Кеңейтімдегі Апелляция батырмасын басыңыз.
        </p>
      </div>
    </div>
  `;

  // Bypass батырмасы
  const bypassBtn = document.getElementById("qalqan-bypass-btn");
  if (bypassBtn) {
    bypassBtn.addEventListener("click", () => {
      chrome.runtime.sendMessage({ action: "BYPASS", url: window.location.href });
      isBlocked = false;
      window.location.reload();
    });
  }
}
