// клауд Елдоса N1 — Qalqan AI v5.0
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

async function safeFetch(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) {
    if (res.status === 429) throw new Error("Сұраныс лимиті асып кетті. 1 минут күтіңіз.");
    throw new Error(`Сервер қатесі: ${res.status}`);
  }
  return res.json();
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

      const data = await safeFetch(`${API_URL}/check`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: tabs[0].url, lang })
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
      const data = await safeFetch(`${API_URL}/check-text`, {
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
      const dataUrl = await new Promise((resolve, reject) => {
        chrome.tabs.captureVisibleTab(null, { format: "jpeg", quality: 80 }, (url) => {
          if (url) resolve(url);
          else reject(new Error("Скриншот алу мүмкін болмады"));
        });
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
