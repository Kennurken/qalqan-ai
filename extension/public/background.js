// клауд Елдоса N1 — Qalqan AI v3.0
// Background Service Worker: автоматты URL тексеру + badge + notifications
// Бұл жалғыз тексеруші — content.js тек блоктау үшін

const API_URL = "https://qalqan-ai-nu.vercel.app";
const DEBOUNCE_MS = 3000;
const recentChecks = new Map();

// --- Табты жаңартқанда автоматты тексеру ---
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status !== "complete") return;
  if (!tab.url || !tab.url.startsWith("http")) return;

  // Chrome internal pages-ті өткізіп жіберу
  if (tab.url.startsWith("chrome://") || tab.url.startsWith("chrome-extension://")) return;

  // Debounce: бір URL-ді қайта тексермеу
  const recent = recentChecks.get(tabId);
  if (recent && recent.url === tab.url && Date.now() - recent.timestamp < DEBOUNCE_MS) return;
  recentChecks.set(tabId, { url: tab.url, timestamp: Date.now() });

  checkUrl(tab.url, tabId);
});

// --- URL тексеру ---
async function checkUrl(url, tabId) {
  try {
    const lang = await getLanguage();
    const response = await fetch(`${API_URL}/check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, lang })
    });

    if (!response.ok) return;
    const data = await response.json();

    // Нәтижені storage-ға сақтау (popup оқиды)
    chrome.storage.local.set({ [`result_${tabId}`]: data });

    // Статистиканы жаңарту
    updateStats(data.verdict);

    const isDangerous = data.verdict === "DANGEROUS" || data.verdict === "ҚАУІПТІ";
    const isSuspicious = data.threat_score >= 40 && data.threat_score < 70;

    if (isDangerous) {
      // Қызыл badge
      chrome.action.setBadgeText({ text: "!", tabId });
      chrome.action.setBadgeBackgroundColor({ color: "#EF4444" });

      // Desktop notification
      chrome.notifications.create(`threat_${tabId}_${Date.now()}`, {
        type: "basic",
        iconUrl: "icons/icon128.png",
        title: "QALQAN AI: Қауіп анықталды!",
        message: data.detail || data.detail_kk || "Бұл сайт қауіпті деп танылды.",
        priority: 2
      });

      // Content script-ке блоктау командасын жіберу
      sendBlockCommand(tabId, data);

    } else if (isSuspicious) {
      // Сары badge
      chrome.action.setBadgeText({ text: "?", tabId });
      chrome.action.setBadgeBackgroundColor({ color: "#F59E0B" });

    } else {
      // Жасыл / бос
      chrome.action.setBadgeText({ text: "", tabId });
    }
  } catch (error) {
    console.error("Qalqan AI тексеру қатесі:", error);
  }
}

// --- Content script-ке блок командасы ---
function sendBlockCommand(tabId, data) {
  chrome.tabs.sendMessage(tabId, { action: "BLOCK_PAGE", data }).catch(() => {
    // Content script әлі дайын емес — inject ету
    chrome.scripting.executeScript({
      target: { tabId },
      files: ["content.js"]
    }).then(() => {
      // Қайта жіберу
      setTimeout(() => {
        chrome.tabs.sendMessage(tabId, { action: "BLOCK_PAGE", data }).catch(() => {});
      }, 300);
    }).catch(() => {});
  });
}

// --- Bypass хабарламасын тыңдау ---
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "BYPASS") {
    // Сессия whitelist-ке қосу
    chrome.storage.session.get("bypass_list", (result) => {
      const list = result.bypass_list || [];
      list.push(message.url);
      chrome.storage.session.set({ bypass_list: list });
    });
    sendResponse({ status: "ok" });
  }

  if (message.action === "GET_RESULT") {
    // Popup сұрайды — кэштелген нәтижені қайтару
    chrome.storage.local.get(`result_${sender.tab?.id}`, (result) => {
      sendResponse(result[`result_${sender.tab?.id}`] || null);
    });
    return true; // async response
  }

  if (message.action === "MANUAL_CHECK") {
    // Popup-тан қолмен тексеру
    checkUrl(message.url, sender.tab?.id || 0);
    sendResponse({ status: "checking" });
  }
});

// --- Статистика ---
async function updateStats(verdict) {
  const result = await chrome.storage.local.get("qalqan_stats");
  const s = result.qalqan_stats || { checked: 0, blocked: 0, suspicious: 0, safe: 0, since: new Date().toISOString() };
  s.checked++;
  if (verdict === "DANGEROUS" || verdict === "ҚАУІПТІ") s.blocked++;
  else if (verdict === "SUSPICIOUS") s.suspicious++;
  else s.safe++;
  chrome.storage.local.set({ qalqan_stats: s });
}

// --- Тіл алу ---
async function getLanguage() {
  const result = await chrome.storage.local.get("qalqan_lang");
  return result.qalqan_lang || "kk";
}

console.log("Qalqan AI v3.0 — Background Service Worker іске қосылды");
