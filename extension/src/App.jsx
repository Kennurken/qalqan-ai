// Qalqan AI v5.1
// Бас компонент: main → stats → history → scanner → trends → settings → whitelist → goszakup views

import { useState, useEffect } from "react";
import { useCheckUrl } from "./hooks/useCheckUrl";
import { APP_VERSION, API_URL } from "./config";

import CheckButton from "./components/CheckButton";
import ResultCard from "./components/ResultCard";
import TextCheck from "./components/TextCheck";
import ScreenshotCheck from "./components/ScreenshotCheck";
import AppealForm from "./components/AppealForm";
import StatsPanel from "./components/StatsPanel";
import SettingsPanel from "./components/SettingsPanel";
import ReportButton from "./components/ReportButton";
import HistoryPanel from "./components/HistoryPanel";
import WhitelistPanel from "./components/WhitelistPanel";
import LinkScannerPanel from "./components/LinkScannerPanel";
import TrendsPanel from "./components/TrendsPanel";
import GoszakupPanel from "./components/GoszakupPanel";

import kkStrings from "./i18n/kk.json";
import ruStrings from "./i18n/ru.json";
import enStrings from "./i18n/en.json";

const strings = { kk: kkStrings, ru: ruStrings, en: enStrings };

export default function App() {
  const [view, setView] = useState("main");
  const [lang, setLang] = useState("kk");
  const { result, loading, error, checkCurrentTab, checkText, checkScreen, sendAppeal, reset, setResult } = useCheckUrl();

  // Тілді жүктеу + cached result auto-load
  useEffect(() => {
    chrome.storage.local.get("qalqan_lang", (r) => {
      if (r.qalqan_lang) setLang(r.qalqan_lang);
    });

    // Auto-load cached result for current tab (no click needed)
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (!tabs?.length || !tabs[0]?.id) return;
      const tabId = tabs[0].id;
      chrome.storage.local.get(`result_${tabId}`, (r) => {
        const cached = r[`result_${tabId}`];
        if (cached && cached.verdict) {
          setResult(cached);
        }
      });
    });
  }, []);

  // Keyboard shortcut: Escape → main, Enter → check (when on main + idle)
  useEffect(() => {
    const handler = (e) => {
      if (e.key === "Escape" && view !== "main") {
        setView("main");
      }
    };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [view]);

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
          <Header t={t} lang={lang} onStats={() => setView("stats")} onHistory={() => setView("history")} onScanner={() => setView("scanner")} onTrends={() => setView("trends")} onSettings={() => setView("settings")} onGoszakup={() => setView("goszakup")} />

          {/* Негізгі тексеру батырмасы */}
          {!result && !error && (
            <>
              <CheckButton loading={loading} onClick={() => checkCurrentTab(lang)} t={t} />
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px" }}>
                <TextCheck onCheck={(text) => checkText(text, lang)} loading={loading} t={t} />
                <ScreenshotCheck onCheck={() => checkScreen(lang)} loading={loading} t={t} />
              </div>
              <ReportButton t={t} />
              {/* KZ Threat Report download */}
              <button
                onClick={() => chrome.tabs.create({ url: `${API_URL}/report/generate` })}
                style={{
                  width: "100%", padding: "7px", marginTop: "6px",
                  background: "rgba(16,185,129,0.08)", color: "#10b981",
                  border: "1px solid rgba(16,185,129,0.3)", borderRadius: "6px",
                  fontSize: "11px", cursor: "pointer", fontWeight: "500",
                  letterSpacing: "0.3px",
                }}
              >
                [ PDF ]  KZ Cyber Threat Report 2026
              </button>
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
                🔄 {t("recheck")}
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
      {view === "settings" && <SettingsPanel lang={lang} onLangChange={changeLang} t={t} onBack={() => setView("main")} onWhitelist={() => setView("whitelist")} />}
      {view === "history" && <HistoryPanel t={t} onBack={() => setView("main")} />}
      {view === "whitelist" && <WhitelistPanel t={t} onBack={() => setView("main")} />}
      {view === "scanner" && <LinkScannerPanel t={t} onBack={() => setView("main")} />}
      {view === "trends" && <TrendsPanel t={t} onBack={() => setView("main")} />}
      {view === "goszakup" && <GoszakupPanel t={t} onBack={() => setView("main")} />}
    </div>
  );
}

function Header({ t, lang, onStats, onHistory, onScanner, onTrends, onSettings, onGoszakup }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
      <div>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <div style={{ width: "4px", height: "24px", background: "#3b82f6", borderRadius: "4px" }} />
          <span style={{ fontSize: "20px", fontWeight: 800 }}>[ Q ] {t("appName")}</span>
        </div>
        <div style={{ fontSize: "10px", color: "#94a3b8", marginLeft: "12px", letterSpacing: "1px" }}>
          {t("subtitle")} • v{APP_VERSION}
        </div>
      </div>
      <div style={{ display: "flex", gap: "4px" }}>
        <button onClick={onStats} title={t("stats")} style={iconBtnStyle}>📊</button>
        <button onClick={() => onHistory && onHistory()} title={t("history")} style={iconBtnStyle}>🕐</button>
        <button onClick={onScanner} title={t("linkScanner")} style={iconBtnStyle}>🔗</button>
        <button onClick={onGoszakup} title="Госзакупки fraud check" style={{...iconBtnStyle, color: "#10b981"}}>🏛️</button>
        <button onClick={onTrends} title={t("trends")} style={iconBtnStyle}>📈</button>
        <button onClick={onSettings} title={t("settings")} style={iconBtnStyle}>⚙️</button>
      </div>
    </div>
  );
}

const iconBtnStyle = {
  background: "rgba(30,41,59,0.6)", border: "1px solid #334155",
  borderRadius: "8px", padding: "6px 8px", cursor: "pointer",
  fontSize: "16px", color: "#94a3b8"
};
