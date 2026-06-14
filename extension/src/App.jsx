// Qalqan AI v5.1 — REDESIGN
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

// ── Design tokens ──────────────────────────────────────────────────────────
export const C = {
  bg:       "#080c16",
  surface:  "rgba(13, 20, 38, 0.95)",
  border:   "rgba(51, 65, 85, 0.5)",
  accent:   "#00d4ff",
  safe:     "#22c55e",
  danger:   "#ff3b5c",
  warning:  "#fbbf24",
  text:     "#e2e8f0",
  muted:    "#64748b",
  mono:     "'SF Mono','Fira Code','Cascadia Code','Consolas',monospace",
  sans:     "Inter,system-ui,-apple-system,sans-serif",
};

const GLOBAL_CSS = `
  @keyframes spin { to { transform: rotate(360deg); } }
  @keyframes pulse-danger {
    0%,100% { box-shadow: 0 0 0 0 rgba(255,59,92,0); }
    50%      { box-shadow: 0 0 16px 4px rgba(255,59,92,0.35); }
  }
  @keyframes scan {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(400%); }
  }
  @keyframes fadeUp {
    from { opacity:0; transform:translateY(6px); }
    to   { opacity:1; transform:translateY(0); }
  }
  @keyframes neon-flicker {
    0%,19%,21%,23%,25%,54%,56%,100% { opacity: 1; }
    20%,24%,55% { opacity: 0.6; }
  }
  @keyframes shimmer {
    0%   { background-position: -400px 0; }
    100% { background-position: 400px 0; }
  }
  * { box-sizing: border-box; }
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: rgba(51,65,85,0.6); border-radius: 4px; }
  body { margin: 0; }
  .skeleton {
    background: linear-gradient(90deg, rgba(30,41,59,0.6) 25%, rgba(51,65,85,0.4) 50%, rgba(30,41,59,0.6) 75%);
    background-size: 800px 100%;
    animation: shimmer 1.5s infinite linear;
    border-radius: 6px;
  }
`;

function SkeletonLoader() {
  return (
    <div style={{ animation: "fadeUp 0.2s ease", padding: "4px 0" }}>
      {/* Score card skeleton */}
      <div style={{ background: "rgba(13,20,38,0.8)", border: "1px solid rgba(51,65,85,0.4)", borderRadius: "12px", padding: "16px", marginBottom: "8px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
          <div className="skeleton" style={{ width: "80px", height: "14px" }} />
          <div className="skeleton" style={{ width: "50px", height: "22px", borderRadius: "20px" }} />
        </div>
        <div className="skeleton" style={{ width: "100%", height: "42px", marginBottom: "10px" }} />
        <div className="skeleton" style={{ width: "70%", height: "12px", marginBottom: "6px" }} />
        <div className="skeleton" style={{ width: "55%", height: "12px" }} />
      </div>
      {/* Factors skeleton */}
      <div style={{ background: "rgba(13,20,38,0.6)", border: "1px solid rgba(51,65,85,0.3)", borderRadius: "10px", padding: "12px", marginBottom: "8px" }}>
        {[85, 60, 45].map((w, i) => (
          <div key={i} style={{ marginBottom: i < 2 ? "8px" : 0 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
              <div className="skeleton" style={{ width: `${w}%`, height: "10px" }} />
              <div className="skeleton" style={{ width: "28px", height: "10px" }} />
            </div>
            <div className="skeleton" style={{ width: "100%", height: "4px", borderRadius: "2px" }} />
          </div>
        ))}
      </div>
      {/* Status text */}
      <div style={{ textAlign: "center", padding: "6px 0" }}>
        <div style={{ fontSize: "11px", color: "rgba(0,212,255,0.5)", fontFamily: "'SF Mono',monospace", letterSpacing: "1px" }}>
          SCANNING...
        </div>
      </div>
    </div>
  );
}

// ── SVG icon library ───────────────────────────────────────────────────────
const Icon = {
  stats: (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
    </svg>
  ),
  history: (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
    </svg>
  ),
  link: (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
    </svg>
  ),
  gov: (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="3" y1="22" x2="21" y2="22"/><line x1="6" y1="18" x2="6" y2="11"/><line x1="10" y1="18" x2="10" y2="11"/><line x1="14" y1="18" x2="14" y2="11"/><line x1="18" y1="18" x2="18" y2="11"/><polygon points="12 2 20 7 4 7"/>
    </svg>
  ),
  trends: (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>
    </svg>
  ),
  settings: (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
    </svg>
  ),
  shield: (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
  ),
  refresh: (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
    </svg>
  ),
  pdf: (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
    </svg>
  ),
};

export default function App() {
  const [view, setView] = useState("main");
  const [lang, setLang] = useState("kk");
  const [onboarded, setOnboarded] = useState(true);
  const { result, loading, error, checkCurrentTab, checkText, checkScreen, sendAppeal, reset, setResult } = useCheckUrl();

  useEffect(() => {
    chrome.storage.local.get(["qalqan_lang", "qalqan_onboarded"], (r) => {
      if (r.qalqan_lang) setLang(r.qalqan_lang);
      if (!r.qalqan_onboarded) setOnboarded(false);
      else setOnboarded(true);
    });
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (!tabs?.length || !tabs[0]?.id) return;
      chrome.storage.local.get(`result_${tabs[0].id}`, (r) => {
        const cached = r[`result_${tabs[0].id}`];
        if (cached?.verdict) setResult(cached);
      });
    });
  }, []);

  useEffect(() => {
    const handler = (e) => { if (e.key === "Escape" && view !== "main") setView("main"); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [view]);

  const changeLang = (l) => { setLang(l); chrome.storage.local.set({ qalqan_lang: l }); };
  const t = (key) => strings[lang]?.[key] || strings.en[key] || key;

  return (
    <>
      <style>{GLOBAL_CSS}</style>
      <div style={{
        width: "380px",
        minHeight: "200px",
        background: C.bg,
        color: C.text,
        fontFamily: C.sans,
        position: "relative",
        overflow: "hidden",
      }}>
        {/* Subtle grid texture */}
        <div style={{
          position: "absolute", inset: 0, pointerEvents: "none", zIndex: 0,
          backgroundImage: "linear-gradient(rgba(0,212,255,0.025) 1px,transparent 1px),linear-gradient(90deg,rgba(0,212,255,0.025) 1px,transparent 1px)",
          backgroundSize: "24px 24px",
        }} />

        {/* Top accent line */}
        <div style={{
          position: "absolute", top: 0, left: 0, right: 0, height: "2px",
          background: `linear-gradient(90deg, transparent, ${C.accent}, transparent)`,
          zIndex: 2,
        }} />

        <div style={{ position: "relative", zIndex: 1, padding: "16px" }}>
          {!onboarded && (
            <OnboardingScreen lang={lang} onLangChange={(l) => { setLang(l); chrome.storage.local.set({ qalqan_lang: l }); }} t={(k) => strings[lang]?.[k] || strings.en[k] || k} onDone={() => { chrome.storage.local.set({ qalqan_onboarded: true }); setOnboarded(true); }} />
          )}
          {onboarded && view === "main" && (
            <>
              <Header t={t} onStats={() => setView("stats")} onHistory={() => setView("history")}
                onScanner={() => setView("scanner")} onTrends={() => setView("trends")}
                onSettings={() => setView("settings")} onGoszakup={() => setView("goszakup")} />

              {loading && !result && <SkeletonLoader />}

              {!result && !error && !loading && (
                <div style={{ animation: "fadeUp 0.2s ease" }}>
                  <CheckButton loading={loading} onClick={() => checkCurrentTab(lang)} t={t} />
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px", marginBottom: "8px" }}>
                    <TextCheck onCheck={(text) => checkText(text, lang)} loading={loading} t={t} />
                    <ScreenshotCheck onCheck={() => checkScreen(lang)} loading={loading} t={t} />
                  </div>
                  <ReportButton t={t} />
                  <button
                    onClick={() => chrome.tabs.create({ url: `${API_URL}/report/generate` })}
                    style={{
                      width: "100%", padding: "8px", marginTop: "8px",
                      background: "transparent", color: C.safe,
                      border: `1px solid rgba(34,197,94,0.25)`, borderRadius: "8px",
                      fontSize: "11px", cursor: "pointer", fontWeight: 500,
                      letterSpacing: "0.5px", fontFamily: C.mono,
                      display: "flex", alignItems: "center", justifyContent: "center", gap: "6px",
                      transition: "all 0.2s",
                    }}
                    onMouseEnter={e => { e.currentTarget.style.borderColor = "rgba(34,197,94,0.5)"; e.currentTarget.style.background = "rgba(34,197,94,0.06)"; }}
                    onMouseLeave={e => { e.currentTarget.style.borderColor = "rgba(34,197,94,0.25)"; e.currentTarget.style.background = "transparent"; }}
                  >
                    {Icon.pdf} KZ Cyber Threat Report 2026
                  </button>
                </div>
              )}

              {result && (
                <div style={{ animation: "fadeUp 0.25s ease" }}>
                  <ResultCard result={result} t={t} />
                  <AppealForm result={result} onSendAppeal={sendAppeal} t={t} />
                  <ReportButton t={t} />
                  <button onClick={reset} style={{
                    width: "100%", padding: "8px", marginTop: "8px",
                    background: "transparent", color: C.muted,
                    border: `1px solid ${C.border}`, borderRadius: "8px",
                    cursor: "pointer", fontSize: "12px", fontFamily: C.sans,
                    display: "flex", alignItems: "center", justifyContent: "center", gap: "6px",
                    transition: "all 0.2s",
                  }}
                  onMouseEnter={e => { e.currentTarget.style.borderColor = "rgba(100,116,139,0.8)"; e.currentTarget.style.color = C.text; }}
                  onMouseLeave={e => { e.currentTarget.style.borderColor = C.border; e.currentTarget.style.color = C.muted; }}
                  >
                    {Icon.refresh} {t("recheck")}
                  </button>
                </div>
              )}

              {error && !result && (
                <div style={{
                  background: "rgba(255,59,92,0.06)", borderRadius: "10px",
                  padding: "14px", border: `1px solid rgba(255,59,92,0.25)`,
                  animation: "fadeUp 0.2s ease",
                }}>
                  <p style={{ color: "#ff8096", margin: "0 0 10px", fontSize: "13px" }}>{error}</p>
                  <button onClick={reset} style={{
                    padding: "6px 14px", background: "rgba(255,59,92,0.1)",
                    color: "#ff8096", border: `1px solid rgba(255,59,92,0.3)`,
                    borderRadius: "6px", cursor: "pointer", fontSize: "12px",
                  }}>
                    {t("recheck") || "Retry"}
                  </button>
                </div>
              )}
            </>
          )}

          {view === "stats"     && <StatsPanel t={t} onBack={() => setView("main")} />}
          {view === "settings"  && <SettingsPanel lang={lang} onLangChange={changeLang} t={t} onBack={() => setView("main")} onWhitelist={() => setView("whitelist")} />}
          {view === "history"   && <HistoryPanel t={t} onBack={() => setView("main")} />}
          {view === "whitelist" && <WhitelistPanel t={t} onBack={() => setView("main")} />}
          {view === "scanner"   && <LinkScannerPanel t={t} onBack={() => setView("main")} />}
          {view === "trends"    && <TrendsPanel t={t} onBack={() => setView("main")} />}
          {view === "goszakup"  && <GoszakupPanel t={t} onBack={() => setView("main")} />}
        </div>
      </div>
    </>
  );
}

// ── Header ─────────────────────────────────────────────────────────────────
function Header({ t, onStats, onHistory, onScanner, onTrends, onSettings, onGoszakup }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "14px" }}>
      {/* Logo */}
      <div>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          {/* Shield logo mark */}
          <div style={{
            width: "28px", height: "28px", borderRadius: "7px",
            background: "linear-gradient(135deg, rgba(0,212,255,0.15), rgba(0,212,255,0.05))",
            border: "1px solid rgba(0,212,255,0.35)",
            display: "flex", alignItems: "center", justifyContent: "center",
            color: "#00d4ff", flexShrink: 0,
            boxShadow: "0 0 8px rgba(0,212,255,0.15)",
          }}>
            {Icon.shield}
          </div>
          <div>
            <div style={{
              fontSize: "14px", fontWeight: 700, letterSpacing: "1.5px",
              fontFamily: "'SF Mono','Fira Code',monospace",
              color: "#f1f5f9",
            }}>
              QALQAN<span style={{ color: "#00d4ff" }}>.AI</span>
            </div>
            <div style={{ fontSize: "9px", color: C.muted, letterSpacing: "1px", fontFamily: "'SF Mono',monospace", marginTop: "1px" }}>
              v{APP_VERSION} · CYBER SHIELD
            </div>
          </div>
        </div>
      </div>

      {/* Nav icons */}
      <div style={{ display: "flex", gap: "3px" }}>
        {[
          { icon: Icon.stats,    fn: onStats,    tip: t("stats"),         col: null },
          { icon: Icon.history,  fn: onHistory,  tip: t("history"),       col: null },
          { icon: Icon.link,     fn: onScanner,  tip: t("linkScanner"),   col: null },
          { icon: Icon.gov,      fn: onGoszakup, tip: "Госзакупки",       col: "#22c55e" },
          { icon: Icon.trends,   fn: onTrends,   tip: t("trends"),        col: null },
          { icon: Icon.settings, fn: onSettings, tip: t("settings"),      col: null },
        ].map(({ icon, fn, tip, col }, i) => (
          <NavBtn key={i} icon={icon} onClick={fn} title={tip} color={col} />
        ))}
      </div>
    </div>
  );
}

function NavBtn({ icon, onClick, title, color }) {
  const [hover, setHover] = useState(false);
  return (
    <button
      onClick={onClick}
      title={title}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        width: "30px", height: "30px",
        background: hover ? "rgba(0,212,255,0.08)" : "rgba(13,20,38,0.8)",
        border: hover ? "1px solid rgba(0,212,255,0.35)" : `1px solid ${C.border}`,
        borderRadius: "7px", cursor: "pointer",
        color: hover ? (color || "#00d4ff") : (color || C.muted),
        display: "flex", alignItems: "center", justifyContent: "center",
        transition: "all 0.15s",
        boxShadow: hover ? "0 0 8px rgba(0,212,255,0.15)" : "none",
      }}
    >
      {icon}
    </button>
  );
}

// ── Onboarding ─────────────────────────────────────────────────────────────
function OnboardingScreen({ lang, onLangChange, t, onDone }) {
  const features = [
    {
      icon: <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00d4ff" strokeWidth="2" strokeLinecap="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>,
      title: t("onboardFeature1Title") || "Авто-тексеру",
      desc: t("onboardFeature1Desc") || "Сайтты ашқанда автоматты фишинг анализі",
    },
    {
      icon: <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fbbf24" strokeWidth="2" strokeLinecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>,
      title: t("onboardFeature2Title") || "ҚЗ брендтер",
      desc: t("onboardFeature2Desc") || "Kaspi, Halyk, eGov жалған сайттарын анықтайды",
    },
    {
      icon: <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#34d399" strokeWidth="2" strokeLinecap="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>,
      title: t("onboardFeature3Title") || "Офлайн база",
      desc: t("onboardFeature3Desc") || "4500+ скам домен интернетсіз тексеріледі",
    },
  ];
  const langs = [
    { code: "kk", label: "ҚАЗ" },
    { code: "ru", label: "РУС" },
    { code: "en", label: "ENG" },
  ];
  return (
    <div style={{ animation: "fadeUp 0.3s ease", textAlign: "center" }}>
      {/* Shield hero */}
      <div style={{
        width: 56, height: 56, borderRadius: 14, margin: "0 auto 12px",
        background: "linear-gradient(135deg, rgba(0,212,255,0.18), rgba(0,212,255,0.05))",
        border: "1px solid rgba(0,212,255,0.4)",
        display: "flex", alignItems: "center", justifyContent: "center",
        boxShadow: "0 0 24px rgba(0,212,255,0.2)",
        color: "#00d4ff",
      }}>
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      </div>

      <div style={{ fontSize: 18, fontWeight: 800, letterSpacing: "2px", fontFamily: "'SF Mono','Fira Code',monospace", color: "#f1f5f9", marginBottom: 4 }}>
        QALQAN<span style={{ color: "#00d4ff" }}>.AI</span>
      </div>
      <div style={{ fontSize: 11, color: C.muted, letterSpacing: "1px", marginBottom: 20 }}>
        {t("onboardSubtitle") || "Сіздің киберқорғаныс қалқаныңыз"}
      </div>

      {/* Features */}
      <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 20, textAlign: "left" }}>
        {features.map((f, i) => (
          <div key={i} style={{
            display: "flex", alignItems: "flex-start", gap: 10,
            background: "rgba(13,20,38,0.7)", borderRadius: 10,
            padding: "10px 12px", border: "1px solid rgba(51,65,85,0.5)",
          }}>
            <div style={{ flexShrink: 0, marginTop: 1 }}>{f.icon}</div>
            <div>
              <div style={{ fontSize: 12, fontWeight: 700, color: "#e2e8f0", marginBottom: 2 }}>{f.title}</div>
              <div style={{ fontSize: 10, color: C.muted, lineHeight: 1.4 }}>{f.desc}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Lang selector */}
      <div style={{ display: "flex", gap: 6, justifyContent: "center", marginBottom: 16 }}>
        {langs.map(l => (
          <button key={l.code} onClick={() => onLangChange(l.code)} style={{
            padding: "5px 14px", borderRadius: 7, cursor: "pointer", fontSize: 11, fontWeight: 700,
            background: lang === l.code ? "rgba(0,212,255,0.15)" : "rgba(13,20,38,0.7)",
            border: lang === l.code ? "1px solid rgba(0,212,255,0.5)" : "1px solid rgba(51,65,85,0.5)",
            color: lang === l.code ? "#00d4ff" : C.muted,
            transition: "all 0.15s",
          }}>{l.label}</button>
        ))}
      </div>

      {/* CTA */}
      <button onClick={onDone} style={{
        width: "100%", padding: "12px", borderRadius: 10, cursor: "pointer",
        background: "linear-gradient(135deg, rgba(0,212,255,0.25), rgba(0,212,255,0.1))",
        border: "1px solid rgba(0,212,255,0.5)", color: "#00d4ff",
        fontSize: 13, fontWeight: 700, letterSpacing: "1px",
        fontFamily: "'SF Mono','Fira Code',monospace",
        boxShadow: "0 0 16px rgba(0,212,255,0.15)",
        transition: "all 0.2s",
      }}
      onMouseEnter={e => { e.currentTarget.style.background = "rgba(0,212,255,0.3)"; e.currentTarget.style.boxShadow = "0 0 24px rgba(0,212,255,0.3)"; }}
      onMouseLeave={e => { e.currentTarget.style.background = "linear-gradient(135deg, rgba(0,212,255,0.25), rgba(0,212,255,0.1))"; e.currentTarget.style.boxShadow = "0 0 16px rgba(0,212,255,0.15)"; }}
      >
        {t("onboardStart") || "БАСТАУ →"}
      </button>
    </div>
  );
}
