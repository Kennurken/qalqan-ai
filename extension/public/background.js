// клауд Елдоса N1 — Qalqan AI v4.0
// Background Service Worker: auto-check + badge + notifications
// Memory-safe: cleanup on tab close + periodic purge

const API_URL = "https://qalqan-ai-nu.vercel.app";
const DEBOUNCE_MS = 3000;
const recentChecks = new Map();

// --- Lifecycle ---
chrome.runtime.onInstalled.addListener((details) => {
  console.log(`Qalqan AI v4.0 installed (${details.reason})`);
  if (details.reason === "install") {
    chrome.storage.local.set({
      qalqan_stats: { checked: 0, blocked: 0, suspicious: 0, safe: 0, since: new Date().toISOString() },
      qalqan_lang: "kk"
    });
  }
});

// --- Memory cleanup: таб жабылғанда ---
chrome.tabs.onRemoved.addListener((tabId) => {
  recentChecks.delete(tabId);
  chrome.storage.local.remove(`result_${tabId}`);
});

// --- Periodic cleanup: сағат сайын ескі жазбалар ---
setInterval(() => {
  const now = Date.now();
  for (const [tabId, data] of recentChecks.entries()) {
    if (now - data.timestamp > 3600000) recentChecks.delete(tabId);
  }
}, 3600000);

// --- Auto-check on tab update ---
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status !== "complete") return;
  if (!tab.url || !tab.url.startsWith("http")) return;
  if (tab.url.startsWith("chrome://") || tab.url.startsWith("chrome-extension://")) return;

  const recent = recentChecks.get(tabId);
  if (recent && recent.url === tab.url && Date.now() - recent.timestamp < DEBOUNCE_MS) return;
  recentChecks.set(tabId, { url: tab.url, timestamp: Date.now() });

  checkUrl(tab.url, tabId);
});

// --- URL check ---
async function checkUrl(url, tabId) {
  try {
    const lang = await getLanguage();
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);
    let response;
    try {
      response = await fetch(`${API_URL}/check`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, lang }),
        signal: controller.signal
      });
    } finally {
      clearTimeout(timeout);
    }

    if (!response.ok) {
      if (response.status === 429) console.warn("Qalqan: rate limited");
      return;
    }

    let data;
    try { data = await response.json(); }
    catch { console.error("Qalqan: invalid JSON response"); return; }

    chrome.storage.local.set({ [`result_${tabId}`]: data });
    updateStats(data.verdict);

    const isDangerous = data.verdict === "DANGEROUS";
    const isSuspicious = data.threat_score >= 40 && data.threat_score < 70;

    if (isDangerous) {
      chrome.action.setBadgeText({ text: "!", tabId });
      chrome.action.setBadgeBackgroundColor({ color: "#EF4444" });

      chrome.notifications.create(`threat_${tabId}_${Date.now()}`, {
        type: "basic",
        iconUrl: "icons/icon128.png",
        title: "QALQAN AI: Қауіп анықталды!",
        message: (data.detail || "Бұл сайт қауіпті деп танылды.").slice(0, 200),
        priority: 2
      });

      sendBlockCommand(tabId, data);
    } else if (isSuspicious) {
      chrome.action.setBadgeText({ text: "?", tabId });
      chrome.action.setBadgeBackgroundColor({ color: "#F59E0B" });
    } else {
      chrome.action.setBadgeText({ text: "", tabId });
    }
  } catch (error) {
    console.error("Qalqan check error:", error.message);
  }
}

// --- Block command ---
function sendBlockCommand(tabId, data) {
  chrome.tabs.sendMessage(tabId, { action: "BLOCK_PAGE", data }).catch(() => {
    chrome.scripting.executeScript({ target: { tabId }, files: ["content.js"] })
      .then(() => setTimeout(() => {
        chrome.tabs.sendMessage(tabId, { action: "BLOCK_PAGE", data }).catch(() => {});
      }, 500))
      .catch(() => {});
  });
}

// --- Message listener ---
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "BYPASS") {
    chrome.storage.session.get("bypass_list", (result) => {
      const list = result.bypass_list || [];
      list.push(message.url);
      chrome.storage.session.set({ bypass_list: list });
    });
    sendResponse({ status: "ok" });
  }
  if (message.action === "GET_RESULT") {
    const key = `result_${sender.tab?.id}`;
    chrome.storage.local.get(key, (result) => sendResponse(result[key] || null));
    return true;
  }
  if (message.action === "MANUAL_CHECK") {
    checkUrl(message.url, sender.tab?.id || 0);
    sendResponse({ status: "checking" });
  }
});

// --- Stats ---
async function updateStats(verdict) {
  const result = await chrome.storage.local.get("qalqan_stats");
  const s = result.qalqan_stats || { checked: 0, blocked: 0, suspicious: 0, safe: 0, since: new Date().toISOString() };
  s.checked++;
  if (verdict === "DANGEROUS") s.blocked++;
  else if (verdict === "SUSPICIOUS") s.suspicious++;
  else s.safe++;
  chrome.storage.local.set({ qalqan_stats: s });
}

async function getLanguage() {
  const result = await chrome.storage.local.get("qalqan_lang");
  return result.qalqan_lang || "kk";
}

console.log("Qalqan AI v4.0 — Background Service Worker started");
