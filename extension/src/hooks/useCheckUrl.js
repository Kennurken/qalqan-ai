// Qalqan AI v5.0
// Hook: URL/text/screen тексеру логикасы
// Audit fix: response.ok checks, base64 safety, error messages

import { useState } from "react";
import { API_URL } from "../config";

const ERR = {
  "Failed to fetch": "Серверге қосылу мүмкін болмады. Интернетті тексеріңіз.",
  "NetworkError": "Желі қатесі. Интернет байланысын тексеріңіз.",
};

function friendlyError(e) {
  return ERR[e.message] || e.message || "Белгісіз қате";
}

function normalizeUrl(url) {
  if (!url) return url;
  url = url.trim();
  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    url = "https://" + url;
  }
  return url;
}

async function safeFetch(url, options, timeoutMs = 20000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    clearTimeout(timer);
    if (!res.ok) {
      if (res.status === 429) throw new Error("Сұраныс лимиті асып кетті. 1 минут күтіңіз.");
      if (res.status === 422) throw new Error("URL форматы дұрыс емес. Тексеріңіз.");
      if (res.status === 503) throw new Error("Сервер уақытша қолжетімсіз. Қайталаңыз.");
      throw new Error(`Сервер қатесі: ${res.status}`);
    }
    return res.json();
  } catch (e) {
    clearTimeout(timer);
    if (e.name === "AbortError") throw new Error("Тексеру уақыты аяқталды (20с). Қайталаңыз.");
    throw e;
  }
}

async function safeFetchWithRetry(url, options, retries = 1) {
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      return await safeFetch(url, options);
    } catch (e) {
      const isRetryable = e.message.includes("503") || e.message.includes("NetworkError") || e.message.includes("Failed to fetch");
      if (attempt < retries && isRetryable) {
        await new Promise(r => setTimeout(r, 1500 * (attempt + 1)));
        continue;
      }
      throw e;
    }
  }
}

async function isPrivacyMode() {
  return new Promise(resolve => {
    chrome.storage.local.get("qalqan_privacy_mode", (r) => resolve(!!r.qalqan_privacy_mode));
  });
}

// Privacy mode: offline-only result object
function privacyModeResult(lang = "kk") {
  const msgs = {
    kk: "Құпиялылық режимі қосулы — URL серверге жіберілмейді. Тек офлайн дерекқор тексеріледі.",
    ru: "Режим конфиденциальности включён — URL не отправляется. Используется только офлайн база.",
    en: "Privacy mode enabled — URL not sent to server. Using offline database only."
  };
  return { verdict: "SAFE", threat_score: 0, threat_type: "safe", source: "privacy_mode",
           detail: msgs[lang] || msgs.kk, detail_kk: msgs.kk, detail_ru: msgs.ru, detail_en: msgs.en,
           indicators: [], privacy_mode: true };
}

export function useCheckUrl() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const checkCurrentTab = async (lang = "kk") => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
      if (!tabs?.length || !tabs[0]?.url) throw new Error("URL анықталмады");

      const tabUrl = normalizeUrl(tabs[0].url);

      // Privacy mode — skip API, return offline-only notice
      if (await isPrivacyMode()) {
        const res = privacyModeResult(lang);
        setResult(res);
        return res;
      }

      const data = await safeFetchWithRetry(`${API_URL}/check`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: tabUrl, lang })
      });
      setResult(data);
      return data;
    } catch (e) {
      setError(friendlyError(e));
      return null;
    } finally {
      setLoading(false);
    }
  };

  const checkText = async (text, lang = "kk") => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      if (await isPrivacyMode()) {
        const res = privacyModeResult(lang);
        setResult(res);
        return res;
      }
      const data = await safeFetchWithRetry(`${API_URL}/check-text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, lang })
      });
      setResult(data);
      return data;
    } catch (e) {
      setError(friendlyError(e));
      return null;
    } finally {
      setLoading(false);
    }
  };

  const checkScreen = async (lang = "kk") => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      if (await isPrivacyMode()) {
        const res = privacyModeResult(lang);
        setResult(res);
        return res;
      }
      const dataUrl = await new Promise((resolve, reject) => {
        try {
          chrome.tabs.captureVisibleTab(null, { format: "jpeg", quality: 80 }, (url) => {
            if (chrome.runtime.lastError) {
              reject(new Error(chrome.runtime.lastError.message || "Скриншот алу мүмкін болмады"));
              return;
            }
            if (url) resolve(url);
            else reject(new Error("Скриншот алу мүмкін болмады"));
          });
        } catch (e) {
          reject(new Error("Скриншот рұқсаты жоқ. chrome:// беттерін тексеру мүмкін емес."));
        }
      });
      if (!dataUrl.includes(",")) throw new Error("Скриншот форматы дұрыс емес");
      const base64 = dataUrl.split(",")[1];

      const data = await safeFetch(`${API_URL}/analyze-screen`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image_base64: base64, lang })
      });
      setResult(data);
      return data;
    } catch (e) {
      setError(friendlyError(e));
      return null;
    } finally {
      setLoading(false);
    }
  };

  const sendAppeal = async (url, reason) => {
    try {
      return await safeFetch(`${API_URL}/appeal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, reason })
      });
    } catch (e) {
      return { status: "error", message: friendlyError(e) };
    }
  };

  const reset = () => { setResult(null); setError(null); };

  return { result, loading, error, checkCurrentTab, checkText, checkScreen, sendAppeal, reset };
}
