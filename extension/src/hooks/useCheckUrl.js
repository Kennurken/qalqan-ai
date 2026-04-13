// клауд Елдоса N1 — Qalqan AI v3.0
// Hook: URL/text/screen тексеру логикасы

import { useState } from "react";
import { API_URL } from "../config";

export function useCheckUrl() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const checkCurrentTab = async (lang = "kk") => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (!tab?.url) throw new Error("URL анықталмады");

      const res = await fetch(`${API_URL}/check`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: tab.url, lang })
      });
      const data = await res.json();
      setResult(data);
      return data;
    } catch (e) {
      setError(e.message);
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
      const res = await fetch(`${API_URL}/check-text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, lang })
      });
      const data = await res.json();
      setResult(data);
      return data;
    } catch (e) {
      setError(e.message);
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
      const base64 = dataUrl.split(",")[1];
      const res = await fetch(`${API_URL}/analyze-screen`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image_base64: base64, lang })
      });
      const data = await res.json();
      setResult(data);
      return data;
    } catch (e) {
      setError(e.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const sendAppeal = async (url, reason) => {
    try {
      const res = await fetch(`${API_URL}/appeal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, reason })
      });
      return await res.json();
    } catch (e) {
      return { status: "error", message: e.message };
    }
  };

  const reset = () => {
    setResult(null);
    setError(null);
  };

  return { result, loading, error, checkCurrentTab, checkText, checkScreen, sendAppeal, reset };
}
