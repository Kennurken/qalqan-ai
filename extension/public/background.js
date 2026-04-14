// клауд Елдоса N1 — Qalqan AI v5.0
// Background Service Worker: auto-check + badge + notifications + offline + history
// Memory-safe: cleanup on tab close + periodic purge

importScripts("offline-db.js");

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
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status !== "complete") return;
  if (!tab.url || !tab.url.startsWith("http")) return;
  if (tab.url.startsWith("chrome://") || tab.url.startsWith("chrome-extension://")) return;

  // Respect auto-check setting
  const settings = await chrome.storage.local.get("qalqan_autocheck");
  if (settings.qalqan_autocheck === false) return;

  const recent = recentChecks.get(tabId);
  if (recent && recent.url === tab.url && Date.now() - recent.timestamp < DEBOUNCE_MS) return;
  recentChecks.set(tabId, { url: tab.url, timestamp: Date.now() });

  checkUrl(tab.url, tabId);
});

// --- URL normalization ---
function normalizeUrl(url) {
  if (!url) return url;
  url = url.trim();
  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    url = "https://" + url;
  }
  return url;
}

// --- URL check ---
async function checkUrl(url, tabId) {
  try {
    url = normalizeUrl(url);
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
    saveHistory(url, data);

    const isDangerous = data.verdict === "DANGEROUS";
    const isSuspicious = data.threat_score >= 40 && data.threat_score < 70;

    if (isDangerous) {
      chrome.action.setBadgeText({ text: "!", tabId });
      chrome.action.setBadgeBackgroundColor({ color: "#EF4444" });

      // Respect notifications setting
      const notifSettings = await chrome.storage.local.get("qalqan_notifications");
      if (notifSettings.qalqan_notifications !== false) {
        chrome.notifications.create(`threat_${tabId}_${Date.now()}`, {
          type: "basic",
          iconUrl: "icons/icon128.png",
          title: "QALQAN AI: Қауіп анықталды!",
          message: (data.detail || "Бұл сайт қауіпті деп танылды.").slice(0, 200),
          priority: 2
        });
      }

      await sendBlockCommand(tabId, data);
    } else if (isSuspicious) {
      chrome.action.setBadgeText({ text: "?", tabId });
      chrome.action.setBadgeBackgroundColor({ color: "#F59E0B" });
    } else {
      chrome.action.setBadgeText({ text: "", tabId });
    }
  } catch (error) {
    // Offline fallback
    if (typeof offlineCheck === "function") {
      const offResult = offlineCheck(url);
      if (offResult) {
        chrome.storage.local.set({ [`result_${tabId}`]: offResult });
        if (offResult.verdict === "DANGEROUS") {
          chrome.action.setBadgeText({ text: "!", tabId });
          chrome.action.setBadgeBackgroundColor({ color: "#EF4444" });
          sendBlockCommand(tabId, offResult);
        }
        saveHistory(url, offResult);
        return;
      }
    }
    console.error("Qalqan check error:", error.message);
  }
}

// --- Block command (with retry) ---
async function sendBlockCommand(tabId, data) {
  const MAX_RETRIES = 3;
  const RETRY_DELAY = 600;

  for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
    try {
      await chrome.tabs.sendMessage(tabId, { action: "BLOCK_PAGE", data });
      console.log(`Qalqan: block command sent to tab ${tabId} (attempt ${attempt + 1})`);
      return;
    } catch {
      // Content script not ready — inject it and retry
      if (attempt === 0) {
        try {
          await chrome.scripting.executeScript({ target: { tabId }, files: ["content.js"] });
        } catch (e) {
          console.error("Qalqan: cannot inject content script:", e.message);
          return;
        }
      }
      await new Promise(r => setTimeout(r, RETRY_DELAY));
    }
  }
  console.error(`Qalqan: failed to send block command to tab ${tabId} after ${MAX_RETRIES} attempts`);
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
  if (message.action === "FINGERPRINT_DETECTED") {
    chrome.notifications.create(`fp_${Date.now()}`, {
      type: "basic",
      iconUrl: "icons/icon128.png",
      title: "QALQAN AI: Fingerprint!",
      message: `${message.types.join(", ")} detected on this site`,
      priority: 1
    });
    sendResponse({ status: "noted" });
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

async function saveHistory(url, data) {
  try {
    const domain = new URL(url).hostname.replace("www.", "");
    const r = await chrome.storage.local.get("qalqan_history");
    const history = r.qalqan_history || [];
    history.push({
      url, domain,
      verdict: data.verdict,
      score: data.threat_score || 0,
      source: data.source || "unknown",
      time: new Date().toLocaleString()
    });
    // Keep last 200
    if (history.length > 200) history.splice(0, history.length - 200);
    chrome.storage.local.set({ qalqan_history: history });
  } catch {}
}

async function getLanguage() {
  const result = await chrome.storage.local.get("qalqan_lang");
  return result.qalqan_lang || "kk";
}

console.log("Qalqan AI v4.0 — Background Service Worker started");
