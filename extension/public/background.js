// Qalqan AI v5.1
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

// --- Offline DB auto-update ---

function mergeOfflineDb(data) {
  if (!data) return;
  let added = 0;
  (data.pyramids || []).forEach(d => { if (!OFFLINE_PYRAMIDS.has(d)) { OFFLINE_PYRAMIDS.add(d); added++; } });
  (data.whitelist || []).forEach(d => { if (!OFFLINE_WHITELIST.has(d)) { OFFLINE_WHITELIST.add(d); added++; } });
  (data.blacklist || []).forEach(d => { if (!OFFLINE_SCAM.has(d)) { OFFLINE_SCAM.add(d); added++; } });
  if (added > 0) console.log(`[Qalqan] offline-db merged +${added} domains`);
}

async function fetchAndUpdateOfflineDb() {
  try {
    const r = await fetch(`${API_URL}/offline-db`);
    if (!r.ok) return;
    const data = await r.json();
    mergeOfflineDb(data);
    await chrome.storage.local.set({ qalqan_offline_db: { data, ts: Date.now() } });
    console.log("[Qalqan] offline-db updated from API");
  } catch (e) {
    console.warn("[Qalqan] offline-db fetch failed:", e.message);
  }
}

async function loadCachedOfflineDb() {
  const s = await chrome.storage.local.get("qalqan_offline_db");
  const cache = s.qalqan_offline_db;
  if (!cache) return;
  const age = Date.now() - (cache.ts || 0);
  mergeOfflineDb(cache.data);
  // Refetch if cache is older than 24h
  if (age > 86400000) fetchAndUpdateOfflineDb();
}

// --- Lifecycle ---
chrome.runtime.onInstalled.addListener((details) => {
  console.log(`Qalqan AI v5.1 installed (${details.reason})`);
  // Right-click any link → check it through Qalqan (opens the landing pre-filled)
  try {
    chrome.contextMenus.create({
      id: "qalqan-check-link",
      title: "🛡 Qalqan AI: сілтемені тексеру",
      contexts: ["link"],
    });
  } catch (e) { /* already exists on update */ }
  if (details.reason === "install") {
    chrome.storage.local.set({
      qalqan_stats: { checked: 0, blocked: 0, suspicious: 0, safe: 0, since: new Date().toISOString() },
      qalqan_lang: "kk"
    });
    chrome.notifications.create("qalqan_welcome", {
      type: "basic",
      iconUrl: "icons/icon48.png",
      title: "🛡️ QALQAN AI орнатылды!",
      message: "Сайттарды автоматты тексеру қосылды. Фишинг, пирамида, алаяқтықтан қорғаныс іске қосылды.",
      priority: 1
    });
    fetchAndUpdateOfflineDb();
  }
  if (details.reason === "update") {
    console.log(`Qalqan AI updated to v5.1 from ${details.previousVersion}`);
    fetchAndUpdateOfflineDb();
  }
  chrome.alarms.create("qalqan_db_update", { periodInMinutes: 720 }); // 12h per passport spec
});

// On SW startup: load cached DB into memory
loadCachedOfflineDb();

// --- Memory cleanup: таб жабылғанда ---
chrome.tabs.onRemoved.addListener((tabId) => {
  recentChecks.delete(tabId);
  chrome.storage.local.remove(`result_${tabId}`);
});

// --- Periodic cleanup via alarm (survives SW restart, unlike setInterval) ---
chrome.alarms.create("qalqan_cleanup", { periodInMinutes: 60 });

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "qalqan_db_update") fetchAndUpdateOfflineDb();
  if (alarm.name === "qalqan_cleanup") {
    const now = Date.now();
    for (const [key, data] of recentChecks.entries()) {
      if (now - data.timestamp > 3600000) recentChecks.delete(key);
    }
    if (_domainCache.size > 300) {
      const cutoff = Date.now() - DOMAIN_CACHE_TTL;
      for (const [k, v] of _domainCache.entries()) { if (v.ts < cutoff) _domainCache.delete(k); }
    }
  }
});

// --- Fast pattern check (no API) — blocks known threats before page renders ---
// Pattern-only quick check — domain lists are already in offlineCheck() via offline-db.js.
// This catches regex patterns not representable as exact domain entries.
function quickRiskCheck(url) {
  try {
    const host = new URL(url).hostname.toLowerCase().replace(/^www\./, "");

    // Known gambling brands across ANY TLD — catches mirrors not in offline-db
    // e.g. 1xbet.africa, melbet.ng, mostbet.eu — the brand name IS the signal
    if (/(?:^|\.)(?:1xbet|1xstavka|melbet|linebet|betwinner|megapari|betandreas|22bet|4rabet|ggbet|betboom|winline|fonbet|olimpbet|mostbet|pin-?up)(?:\.|$)/i.test(host)) {
      return { verdict: "DANGEROUS", threat_score: 90, threat_type: "gambling", source: "quick_check",
               detail: "Known gambling operator", detail_kk: "Белгілі құмар ойын операторы",
               detail_ru: "Известный оператор азартных игр", detail_en: "Known gambling operator",
               indicators: ["gambling_brand"] };
    }

    // Gambling keyword patterns — catches subdomain variants and unlisted TLDs
    // e.g. "casinoX.co", "slots-online.ru" not in offline-db exact list.
    // Bare "bet" removed — too many false positives on legit domains; the specific
    // bookmaker brands (1xbet/melbet/…) are already covered by the brand regex above.
    if (/(\b|[-.])(casino|slots?|poker|gambling|букмекер|ставки)(\b|[-.])/i.test(host)) {
      return { verdict: "DANGEROUS", threat_score: 85, threat_type: "gambling", source: "quick_check",
               detail: "Gambling site pattern", detail_kk: "Құмар ойын сайты паттерні",
               detail_ru: "Паттерн сайта азартных игр", detail_en: "Gambling site pattern",
               indicators: ["gambling_pattern"] };
    }

    // Free TLD + KZ brand = phishing (regex — faster than array iteration)
    const FREE_TLD_RE = /\.(tk|ml|ga|cf|gq|xyz|top|pw|cc|icu|buzz|su|ws)$/;
    const KZ_BRAND_RE = /kaspi|egov|halyk|kcell|beeline|tengri|kolesa|homecredit|jysan|bereke|sberbank|qazaq/;
    if (FREE_TLD_RE.test(host) && KZ_BRAND_RE.test(host)) {
      return { verdict: "DANGEROUS", threat_score: 92, threat_type: "phishing", source: "quick_check",
               detail: "KZ brand phishing on free TLD", detail_kk: "Тегін домендегі KZ брендін еліктеу",
               detail_ru: "Фишинг KZ-бренда на бесплатном домене", detail_en: "KZ brand phishing on free TLD",
               indicators: ["free_tld", "kz_brand_impersonation"] };
    }

    // IP address URL — never legitimate for financial/gov services
    if (/^\d{1,3}(\.\d{1,3}){3}(:\d+)?$/.test(host)) {
      return { verdict: "SUSPICIOUS", threat_score: 65, threat_type: "suspicious_infrastructure", source: "quick_check",
               detail: "IP address URL", detail_kk: "IP мекенжайлы URL",
               detail_ru: "URL с IP-адресом", detail_en: "IP address URL", indicators: ["ip_address"] };
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
        await sendBlockCommand(tabId, cached, url);
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
      await sendBlockCommand(tabId, offResult, url);
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
      await sendBlockCommand(tabId, quick, url);
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
        await sendBlockCommand(tabId, offResult, url);
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
    const sensitivity = sensitivityData.qalqan_sensitivity || "high";
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
      await sendBlockCommand(tabId, data, url);
    }
  } catch (error) {
    console.error("Qalqan check error:", error.message);
  }
}

// --- Block command ---
// Primary: redirect tab to local blocked.html — pre-render safe, immune to site JS.
// Fallback: content-script DOM replacement (for edge cases where tab update fails).
async function sendBlockCommand(tabId, data, blockedUrl = "") {
  try {
    const payload = encodeURIComponent(JSON.stringify({
      url:        blockedUrl,
      score:      data.threat_score  || 0,
      type:       data.threat_type   || "unknown",
      source:     data.source        || "unknown",
      detail_kk:  data.detail_kk || data.detail || "",
      detail_ru:  data.detail_ru || data.detail || "",
      detail_en:  data.detail_en || data.detail || "",
      indicators: data.indicators    || [],
    }));
    await chrome.tabs.update(tabId, {
      url: chrome.runtime.getURL("blocked.html") + "#" + payload,
    });
    return;
  } catch (e) {
    console.warn("Qalqan: tab redirect failed, falling back:", e?.message);
  }

  // Fallback: inject content script and send BLOCK_PAGE message
  const MAX_RETRIES = 3;
  const RETRY_DELAY = 600;
  for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
    try {
      await chrome.tabs.sendMessage(tabId, { action: "BLOCK_PAGE", data });
      return;
    } catch {
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
  console.error(`Qalqan: failed to block tab ${tabId}`);
}

// --- Message listener ---
chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.action === "GET_RESULT") {
    const key = `result_${sender.tab?.id}`;
    chrome.storage.local.get(key, (result) => sendResponse(result[key] || null));
    return true;
  }
  if (message.action === "DOM_SUSPICIOUS") {
    const tabId = sender.tab?.id;
    if (!tabId) return;
    const stored = await new Promise(res => chrome.storage.local.get(`result_${tabId}`, r => res(r)));
    const existing = stored[`result_${tabId}`];
    const reason = message.reason;

    if (reason === "credential_form_kz_brand") {
      if (!existing || existing.verdict === "SAFE" || existing.verdict === "SUSPICIOUS") {
        // Elevate to SUSPICIOUS — let user know there's a credential form with KZ brand
        const elevated = {
          verdict: "SUSPICIOUS",
          threat_score: Math.max(existing?.threat_score || 0, 55),
          threat_type: "phishing",
          source: "dom_analysis",
          detail_kk: `Беттe ${message.brand} атауы бар кіру форма анықталды`,
          detail_ru: `На странице обнаружена форма входа с именем ${message.brand}`,
          detail_en: `Login form with ${message.brand} brand detected on page`,
          indicators: ["dom_credential_form", `brand_${message.brand}`],
        };
        if (existing?.verdict === "SUSPICIOUS" && existing?.threat_score >= 60) {
          // Was already suspicious with moderate score — escalate
          elevated.verdict = "DANGEROUS";
          elevated.threat_score = Math.min((existing.threat_score || 60) + 20, 92);
        }
        chrome.storage.local.set({ [`result_${tabId}`]: elevated });
        updateBadge(tabId, elevated);
        if (elevated.verdict === "DANGEROUS") await sendBlockCommand(tabId, elevated, sender.tab?.url || "");
      }
    }

    if (reason === "prize_scam_text") {
      if (!existing || existing.verdict === "SAFE") {
        const flagged = {
          verdict: "SUSPICIOUS",
          threat_score: Math.max(existing?.threat_score || 0, 45),
          threat_type: "scam",
          source: "dom_analysis",
          detail_kk: "Беттe жалған ұтыс мәтіні анықталды",
          detail_ru: "На странице обнаружен текст ложного розыгрыша",
          detail_en: "Fake prize/lottery text detected on page",
          indicators: ["dom_prize_text"],
        };
        chrome.storage.local.set({ [`result_${tabId}`]: flagged });
        updateBadge(tabId, flagged);
      }
    }
    sendResponse({ status: "noted" });
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

  if (message.action === "ANNOTATE_SEARCH") {
    annotateSearch(message.urls || []).then(results => sendResponse({ results }));
    return true; // async response
  }
});

// --- Search-results annotation: offline-first, batch the rest via API ---
async function annotateSearch(urls) {
  const results = [];
  const unknown = [];
  for (const url of urls.slice(0, 30)) {
    // Domain cache (30-min) first — free, instant
    let domain = "";
    try { domain = new URL(url).hostname.replace("www.", "").toLowerCase(); } catch {}
    const cached = domain && getDomainCache(domain);
    if (cached) { results.push({ url, verdict: cached.verdict, threat_score: cached.threat_score }); continue; }
    // Offline DB — instant, no network
    const off = typeof offlineCheck === "function" ? offlineCheck(url) : null;
    if (off) {
      results.push({ url, verdict: off.verdict, threat_score: off.threat_score });
      if (domain) setDomainCache(domain, off);
    } else {
      unknown.push(url);
    }
  }
  // Batch the unknowns (cap 15 per /batch call; take the first 15 to stay cheap)
  if (unknown.length) {
    try {
      const controller = new AbortController();
      const to = setTimeout(() => controller.abort(), 12000);
      const r = await fetch(`${API_URL}/batch`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ urls: unknown.slice(0, 15), lang: "kk" }),
        signal: controller.signal,
      });
      clearTimeout(to);
      if (r.ok) {
        const d = await r.json();
        for (const res of (d.results || [])) {
          results.push({ url: res.url, verdict: res.verdict, threat_score: res.threat_score });
          try { const dm = new URL(res.url).hostname.replace("www.", "").toLowerCase(); setDomainCache(dm, res); } catch {}
        }
      }
    } catch (e) { /* offline / rate-limited — annotate what we have */ }
  }
  return results;
}

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

    // Auto-whitelist: HTTPS-only domains checked SAFE 5+ times → suggest (not silently add)
    if (data.verdict === "SAFE" && url.startsWith("https://")
        && data.source !== "user_whitelist" && data.source !== "offline_whitelist") {
      const safeCount = history.filter(h => h.domain === domain && h.verdict === "SAFE").length;
      if (safeCount === 5) {
        chrome.notifications.create(`autowl_${domain}`, {
          type: "basic", iconUrl: "icons/icon48.png",
          title: "Qalqan AI: Сенімді сайт",
          message: `${domain} 5 рет SAFE деп танылды. Ақ тізімге қосу үшін Параметрлерге өтіңіз.`,
          priority: 0
        });
      }
    }
  } catch {}
}

async function getLanguage() {
  const result = await chrome.storage.local.get("qalqan_lang");
  return result.qalqan_lang || "kk";
}

console.log("Qalqan AI v5.1 — Background Service Worker started");


chrome.contextMenus.onClicked.addListener((info) => {
  if (info.menuItemId === "qalqan-check-link" && info.linkUrl) {
    chrome.tabs.create({
      url: "https://qalqan-ai-nu.vercel.app/?check=" + encodeURIComponent(info.linkUrl),
    });
  }
});
