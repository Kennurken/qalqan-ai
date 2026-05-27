// Qalqan AI v5.0
// Background Service Worker: auto-check + badge + notifications + offline + history
// Memory-safe: cleanup on tab close + periodic purge

importScripts("offline-db.js");

const API_URL = "https://qalqan-ai-nu.vercel.app";
const DEBOUNCE_MS = 800;   // Reduced: 3000→800ms
const FAST_DEBOUNCE_MS = 200;  // For the instant pre-check on navigation start
const recentChecks = new Map();

// Domain-level result cache (30-min TTL) — avoids repeated API calls for same site
const _domainCache = new Map();
const DOMAIN_CACHE_TTL = 30 * 60 * 1000;

function getDomainCache(domain) {
  const entry = _domainCache.get(domain);
  if (!entry) return null;
  if (Date.now() - entry.ts > DOMAIN_CACHE_TTL) { _domainCache.delete(domain); return null; }
  return entry.result;
}

function setDomainCache(domain, result) {
  _domainCache.set(domain, { result, ts: Date.now() });
  if (_domainCache.size > 500) {
    const cutoff = Date.now() - DOMAIN_CACHE_TTL;
    for (const [k, v] of _domainCache.entries()) { if (v.ts < cutoff) _domainCache.delete(k); }
  }
}

function updateBadge(tabId, data) {
  if (data.verdict === "DANGEROUS") {
    chrome.action.setBadgeText({ text: "!", tabId });
    chrome.action.setBadgeBackgroundColor({ color: "#EF4444" });
  } else if (data.threat_score >= 40) {
    chrome.action.setBadgeText({ text: "?", tabId });
    chrome.action.setBadgeBackgroundColor({ color: "#F59E0B" });
  } else {
    chrome.action.setBadgeText({ text: "", tabId });
  }
}

// --- Lifecycle ---
chrome.runtime.onInstalled.addListener((details) => {
  console.log(`Qalqan AI v5.0 installed (${details.reason})`);
  if (details.reason === "install") {
    chrome.storage.local.set({
      qalqan_stats: { checked: 0, blocked: 0, suspicious: 0, safe: 0, since: new Date().toISOString() },
      qalqan_lang: "kk"
    });
    // Welcome notification
    chrome.notifications.create("qalqan_welcome", {
      type: "basic",
      iconUrl: "icons/icon48.png",
      title: "🛡️ QALQAN AI орнатылды!",
      message: "Сайттарды автоматты тексеру қосылды. Фишинг, пирамида, алаяқтықтан қорғаныс іске қосылды.",
      priority: 1
    });
  }
  if (details.reason === "update") {
    console.log(`Qalqan AI updated to v5.0 from ${details.previousVersion}`);
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

// --- Fast pattern check (no API) — blocks known threats before page renders ---
function quickRiskCheck(url) {
  try {
    const host = new URL(url).hostname.toLowerCase().replace(/^www\./, "");
    const path = new URL(url).pathname.toLowerCase();

    // Gambling (inline — critical for speed)
    const GAMBLE = ["1xbet","mostbet","pin-up","vavada","1win","melbet","pokerdom",
                    "vulkan","hellcase","rollbit","parimatch","stake","rox","betmaster"];
    if (GAMBLE.some(g => host.includes(g))) {
      return { verdict: "DANGEROUS", threat_score: 90, threat_type: "gambling", source: "quick_check",
               detail: "Unlicensed gambling site blocked", detail_kk: "Лицензиясыз құмар ойын сайты бұғатталды",
               detail_ru: "Заблокирован нелицензированный сайт азартных игр", detail_en: "Unlicensed gambling site blocked", indicators: [] };
    }

    // Free TLD + KZ brand = phishing
    const FREE_TLDS = [".tk",".ml",".ga",".cf",".gq",".xyz",".top",".pw",".cc",".icu",".buzz"];
    const KZ_BRANDS = ["kaspi","egov","halyk","kcell","beeline","tengri","kolesa","homecredit","jysan","bereke"];
    const hasFree = FREE_TLDS.some(t => host.endsWith(t));
    const hasBrand = KZ_BRANDS.some(b => host.includes(b));
    if (hasFree && hasBrand) {
      return { verdict: "DANGEROUS", threat_score: 92, threat_type: "phishing", source: "quick_check",
               detail: "KZ brand phishing on free TLD", detail_kk: "Тегін домендегі KZ брендін еліктеу",
               detail_ru: "Фишинг KZ-бренда на бесплатном домене", detail_en: "KZ brand phishing on free TLD", indicators: ["free_tld","kz_brand_impersonation"] };
    }

    // Known pyramid keywords in domain
    const PYRAMID_KEYS = ["crowd1","finiko","onecoin","forsage","bitconnect","qubittech","antares.trade"];
    if (PYRAMID_KEYS.some(p => host.includes(p))) {
      return { verdict: "DANGEROUS", threat_score: 95, threat_type: "pyramid", source: "quick_check",
               detail: "Known pyramid scheme", detail_kk: "Белгілі қаржылық пирамида",
               detail_ru: "Известная финансовая пирамида", detail_en: "Known pyramid scheme", indicators: ["pyramid_scheme"] };
    }

    // IP address URL
    if (/^\d{1,3}(\.\d{1,3}){3}(:\d+)?$/.test(host)) {
      return { verdict: "SUSPICIOUS", threat_score: 65, threat_type: "suspicious_infrastructure", source: "quick_check",
               detail: "IP address URL", detail_kk: "IP мекенжайлы URL", detail_ru: "URL с IP-адресом", detail_en: "IP address URL", indicators: ["ip_address"] };
    }

    return null;
  } catch { return null; }
}

// --- Auto-check on tab update — TWO PHASE ---
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (!tab.url || !tab.url.startsWith("http")) return;
  if (tab.url.startsWith("chrome://") || tab.url.startsWith("chrome-extension://")) return;

  const settings = await chrome.storage.local.get("qalqan_autocheck");
  if (settings.qalqan_autocheck === false) return;

  // ── PHASE 1: Fires on "loading" (navigation start, before page renders) ──
  // Runs offline DB + quick pattern check only — no API, no I/O, <5ms
  if (changeInfo.status === "loading") {
    const url = tab.url;
    const fastRecent = recentChecks.get(`fast_${tabId}`);
    if (fastRecent && fastRecent.url === url && Date.now() - fastRecent.timestamp < FAST_DEBOUNCE_MS) return;
    recentChecks.set(`fast_${tabId}`, { url, timestamp: Date.now() });

    // User whitelist check
    const wlData = await chrome.storage.local.get("qalqan_user_whitelist");
    const userWl = wlData.qalqan_user_whitelist || [];
    try {
      const domain = new URL(url).hostname.replace("www.", "").toLowerCase();
      if (userWl.includes(domain) || userWl.some(d => domain.endsWith("." + d))) return;

      // Domain cache hit
      const cached = getDomainCache(domain);
      if (cached && cached.verdict === "DANGEROUS") {
        await sendBlockCommand(tabId, cached);
        return;
      }
      if (cached) return;  // Safe/suspicious — let phase 2 handle
    } catch {}

    // Offline DB
    const offResult = typeof offlineCheck === "function" ? offlineCheck(url) : null;
    if (offResult && offResult.verdict === "DANGEROUS") {
      chrome.storage.local.set({ [`result_${tabId}`]: offResult });
      updateBadge(tabId, offResult);
      updateStats(offResult.verdict);
      saveHistory(url, offResult);
      try { const d = new URL(url).hostname.replace("www.","").toLowerCase(); setDomainCache(d, offResult); } catch {}
      await sendBlockCommand(tabId, offResult);
      return;
    }

    // Quick pattern check (inline JS, <1ms)
    const quick = quickRiskCheck(url);
    if (quick && quick.verdict === "DANGEROUS") {
      chrome.storage.local.set({ [`result_${tabId}`]: quick });
      updateBadge(tabId, quick);
      updateStats(quick.verdict);
      saveHistory(url, quick);
      try { const d = new URL(url).hostname.replace("www.","").toLowerCase(); setDomainCache(d, quick); } catch {}
      await sendBlockCommand(tabId, quick);
      // Don't return — phase 2 will still run full API to get proper result & update
    }
    return;
  }

  // ── PHASE 2: Fires on "complete" (full API check) ──
  if (changeInfo.status !== "complete") return;

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
    const domain = new URL(url).hostname.replace("www.", "").toLowerCase();

    // 1. User whitelist — instant, no API call
    const wlData = await chrome.storage.local.get("qalqan_user_whitelist");
    const userWhitelist = wlData.qalqan_user_whitelist || [];
    if (userWhitelist.includes(domain) || userWhitelist.some(d => domain.endsWith("." + d))) {
      const safeResult = { verdict: "SAFE", threat_score: 0, source: "user_whitelist", cached: false };
      chrome.storage.local.set({ [`result_${tabId}`]: safeResult });
      updateBadge(tabId, safeResult);
      return;
    }

    // 2. Domain cache (30-min TTL) — avoid redundant API calls
    const cachedResult = getDomainCache(domain);
    if (cachedResult) {
      const r = { ...cachedResult, cached: true };
      chrome.storage.local.set({ [`result_${tabId}`]: r });
      updateBadge(tabId, r);
      return;
    }

    // 3. Offline check — instant for known dangerous/safe sites
    const offResult = typeof offlineCheck === "function" ? offlineCheck(url) : null;
    if (offResult) {
      chrome.storage.local.set({ [`result_${tabId}`]: offResult });
      updateBadge(tabId, offResult);
      updateStats(offResult.verdict);
      saveHistory(url, offResult);
      setDomainCache(domain, offResult);

      if (offResult.verdict === "SAFE") return;  // Trusted offline — skip API

      if (offResult.verdict === "DANGEROUS") {
        const notifSettings = await chrome.storage.local.get("qalqan_notifications");
        if (notifSettings.qalqan_notifications !== false) {
          chrome.notifications.create(`threat_${tabId}_${Date.now()}`, {
            type: "basic", iconUrl: "icons/icon128.png",
            title: "QALQAN AI: Қауіп анықталды!",
            message: (offResult.detail_kk || offResult.detail || "Бұл сайт қауіпті деп танылды.").slice(0, 200),
            priority: 2
          });
        }
        await sendBlockCommand(tabId, offResult);
        return;  // Offline DB is conclusive for DANGEROUS
      }
      // SUSPICIOUS offline: still make API call for richer analysis
    }

    // 4. Privacy mode check — skip API if enabled
    const privacyData = await chrome.storage.local.get("qalqan_privacy_mode");
    if (privacyData.qalqan_privacy_mode) {
      console.log("Qalqan: privacy mode ON — skipping API call");
      return;
    }

    // 5. API call
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
    setDomainCache(domain, data);
    updateBadge(tabId, data);

    // Read sensitivity threshold (high=60, medium=70, low=80; default=70)
    const sensitivityData = await chrome.storage.local.get("qalqan_sensitivity");
    const sensitivity = sensitivityData.qalqan_sensitivity || "medium";
    const BLOCK_THRESHOLD = { high: 60, medium: 70, low: 80 }[sensitivity] ?? 70;

    const shouldBlock = data.verdict === "DANGEROUS" || data.threat_score >= BLOCK_THRESHOLD;

    if (shouldBlock) {
      const notifSettings = await chrome.storage.local.get("qalqan_notifications");
      if (notifSettings.qalqan_notifications !== false) {
        chrome.notifications.create(`threat_${tabId}_${Date.now()}`, {
          type: "basic", iconUrl: "icons/icon128.png",
          title: "QALQAN AI: Қауіп анықталды!",
          message: (data.detail_kk || data.detail || "Бұл сайт қауіпті деп танылды.").slice(0, 200),
          priority: 2
        });
      }
      await sendBlockCommand(tabId, data);
    }
  } catch (error) {
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
      threat_type: data.threat_type || "unknown",
      source: data.source || "unknown",
      time: new Date().toLocaleString()
    });
    // Keep last 200
    if (history.length > 200) history.splice(0, history.length - 200);
    chrome.storage.local.set({ qalqan_history: history });

    // Auto-whitelist: domain checked SAFE 3+ times → add to user whitelist
    if (data.verdict === "SAFE" && data.source !== "user_whitelist" && data.source !== "offline_whitelist") {
      const safeCount = history.filter(h => h.domain === domain && h.verdict === "SAFE").length;
      if (safeCount >= 3) {
        const wlData = await chrome.storage.local.get("qalqan_user_whitelist");
        const wl = wlData.qalqan_user_whitelist || [];
        if (!wl.includes(domain)) {
          wl.push(domain);
          chrome.storage.local.set({ qalqan_user_whitelist: wl });
          console.log(`Qalqan: auto-whitelisted ${domain} (${safeCount}x safe)`);
        }
      }
    }
  } catch {}
}

async function getLanguage() {
  const result = await chrome.storage.local.get("qalqan_lang");
  return result.qalqan_lang || "kk";
}

console.log("Qalqan AI v5.0 — Background Service Worker started");
