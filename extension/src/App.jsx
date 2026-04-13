// клауд Елдоса N1 — Qalqan AI v3.0
// Бас компонент: main → stats → settings views

import { useState, useEffect } from "react";
import { useCheckUrl } from "./hooks/useCheckUrl";
import { APP_VERSION } from "./config";

import CheckButton from "./components/CheckButton";
import ResultCard from "./components/ResultCard";
import TextCheck from "./components/TextCheck";
import ScreenshotCheck from "./components/ScreenshotCheck";
import AppealForm from "./components/AppealForm";
import StatsPanel from "./components/StatsPanel";
import SettingsPanel from "./components/SettingsPanel";
import ReportButton from "./components/ReportButton";
import HistoryPanel from "./components/HistoryPanel";

import kkStrings from "./i18n/kk.json";
import ruStrings from "./i18n/ru.json";
import enStrings from "./i18n/en.json";

const strings = { kk: kkStrings, ru: ruStrings, en: enStrings };

export default function App() {
  const [view, setView] = useState("main");
  const [lang, setLang] = useState("kk");
  const { result, loading, error, checkCurrentTab, checkText, checkScreen, sendAppeal, reset } = useCheckUrl();

  // Тілді жүктеу
  useEffect(() => {
    chrome.storage.local.get("qalqan_lang", (r) => {
      if (r.qalqan_lang) setLang(r.qalqan_lang);
    });
  }, []);

  const changeLang = (newLang) => {
    setLang(newLang);
    chrome.storage.local.set({ qalqan_lang: newLang });
  };

  const t = (key) => strings[lang]?.[key] || strings.en[key] || key;

  return (
    <div style={{
      width: "380px",
      padding: "16px",
      background: "linear-gradient(180deg, #020617 0%, #0f172a 100%)",
      color: "#f8fafc",
      fontFamily: "'Segoe UI', system-ui, -apple-system, sans-serif",
      minHeight: "200px"
    }}>
      {/* Header — барлық views-те көрінеді */}
      {view === "main" && (
        <>
          <Header t={t} lang={lang} onStats={() => setView("stats")} onHistory={() => setView("history")} onSettings={() => setView("settings")} />

          {/* Негізгі тексеру батырмасы */}
          {!result && !error && (
            <>
              <CheckButton loading={loading} onClick={() => checkCurrentTab(lang)} t={t} />
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px" }}>
                <TextCheck onCheck={(text) => checkText(text, lang)} loading={loading} t={t} />
                <ScreenshotCheck onCheck={() => checkScreen(lang)} loading={loading} t={t} />
              </div>
              <ReportButton t={t} />
            </>
          )}

          {/* Нәтиже */}
          {result && (
            <>
              <ResultCard result={result} t={t} />
              <AppealForm result={result} onSendAppeal={sendAppeal} t={t} />
              <ReportButton t={t} />
              <button
                onClick={reset}
                style={{
                  width: "100%", padding: "8px", marginTop: "8px",
                  background: "transparent", color: "#64748b",
                  border: "1px solid #334155", borderRadius: "8px",
                  cursor: "pointer", fontSize: "12px"
                }}
              >
                🔄 Қайта тексеру
              </button>
            </>
          )}

          {/* Қате */}
          {error && !result && (
            <div style={{
              background: "rgba(239,68,68,0.1)", borderRadius: "10px",
              padding: "12px", border: "1px solid #ef444444"
            }}>
              <p style={{ color: "#f87171", margin: 0, fontSize: "13px" }}>⚠️ {error}</p>
              <button onClick={reset} style={{
                marginTop: "8px", padding: "6px 12px",
                background: "#334155", color: "#94a3b8",
                border: "none", borderRadius: "6px", cursor: "pointer", fontSize: "12px"
              }}>
                Қайталау
              </button>
            </div>
          )}
        </>
      )}

      {view === "stats" && <StatsPanel t={t} onBack={() => setView("main")} />}
      {view === "settings" && <SettingsPanel lang={lang} onLangChange={changeLang} t={t} onBack={() => setView("main")} />}
      {view === "history" && <HistoryPanel t={t} onBack={() => setView("main")} />}
    </div>
  );
}

function Header({ t, lang, onStats, onHistory, onSettings }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
      <div>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <div style={{ width: "4px", height: "24px", background: "#3b82f6", borderRadius: "4px" }} />
          <span style={{ fontSize: "20px", fontWeight: 800 }}>🛡️ {t("appName")}</span>
        </div>
        <div style={{ fontSize: "10px", color: "#94a3b8", marginLeft: "12px", letterSpacing: "1px" }}>
          {t("subtitle")} • v{APP_VERSION}
        </div>
      </div>
      <div style={{ display: "flex", gap: "4px" }}>
        <button onClick={onStats} title={t("stats")} style={iconBtnStyle}>📊</button>
        <button onClick={() => onHistory && onHistory()} title="History" style={iconBtnStyle}>📜</button>
        <button onClick={onSettings} title={t("settings")} style={iconBtnStyle}>⚙️</button>
      </div>
    </div>
  );
}

const iconBtnStyle = {
  background: "rgba(30,41,59,0.6)", border: "1px solid #334155",
  borderRadius: "8px", padding: "6px 8px", cursor: "pointer",
  fontSize: "14px", color: "#94a3b8"
};
