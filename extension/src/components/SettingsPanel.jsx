// Qalqan AI v5.0

import { useState, useEffect } from "react";
import { C } from "../App";
import { PanelHeader } from "./StatsPanel";

export default function SettingsPanel({ lang, onLangChange, t, onBack, onWhitelist }) {
  const [theme, setTheme] = useState("dark");
  const [autoCheck, setAutoCheck] = useState(true);
  const [notifications, setNotifications] = useState(true);
  const [sensitivity, setSensitivity] = useState("medium");
  const [privacyMode, setPrivacyMode] = useState(false);

  useEffect(() => {
    chrome.storage.local.get(["qalqan_theme", "qalqan_autocheck", "qalqan_notifications", "qalqan_sensitivity", "qalqan_privacy_mode"], (r) => {
      if (r.qalqan_theme) setTheme(r.qalqan_theme);
      if (r.qalqan_autocheck !== undefined) setAutoCheck(r.qalqan_autocheck);
      if (r.qalqan_notifications !== undefined) setNotifications(r.qalqan_notifications);
      if (r.qalqan_sensitivity) setSensitivity(r.qalqan_sensitivity);
      if (r.qalqan_privacy_mode !== undefined) setPrivacyMode(r.qalqan_privacy_mode);
    });
  }, []);

  const changeSensitivity = (s) => {
    setSensitivity(s);
    chrome.storage.local.set({ qalqan_sensitivity: s });
  };

  const toggleTheme = () => {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    chrome.storage.local.set({ qalqan_theme: next });
    document.body.className = next === "light" ? "light" : "";
  };

  const toggleAutoCheck = () => {
    setAutoCheck(!autoCheck);
    chrome.storage.local.set({ qalqan_autocheck: !autoCheck });
  };

  const toggleNotifications = () => {
    setNotifications(!notifications);
    chrome.storage.local.set({ qalqan_notifications: !notifications });
  };

  const togglePrivacyMode = () => {
    setPrivacyMode(!privacyMode);
    chrome.storage.local.set({ qalqan_privacy_mode: !privacyMode });
  };

  const languages = [
    { code: "kk", label: "Қазақша", flag: "🇰🇿" },
    { code: "ru", label: "Русский", flag: "🇷🇺" },
    { code: "en", label: "English", flag: "🇬🇧" },
  ];

  return (
    <div>
      <PanelHeader onBack={onBack} title={t("settings")} t={t} />

      <div style={{
        background: "rgba(30,41,59,0.6)", borderRadius: "12px",
        padding: "14px", marginBottom: "12px"
      }}>
        <div style={{ fontSize: "13px", color: "#94a3b8", marginBottom: "10px", display: "flex", alignItems: "center", gap: 6 }}>
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          {t("language")}
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
          {languages.map((l) => (
            <button
              key={l.code}
              onClick={() => onLangChange(l.code)}
              style={{
                display: "flex", alignItems: "center", gap: "10px",
                padding: "10px 12px", borderRadius: "8px",
                background: lang === l.code ? "rgba(99,102,241,0.2)" : "transparent",
                border: lang === l.code ? "1px solid #6366f1" : "1px solid #334155",
                color: lang === l.code ? "#a5b4fc" : "#94a3b8",
                cursor: "pointer", fontWeight: lang === l.code ? 700 : 400,
                fontSize: "13px", width: "100%", textAlign: "left"
              }}
            >
              <span style={{ fontSize: "18px" }}>{l.flag}</span>
              {l.label}
              {lang === l.code && <span style={{ marginLeft: "auto" }}>✓</span>}
            </button>
          ))}
        </div>
      </div>

      {/* Toggles */}
      <div style={{ background: "rgba(30,41,59,0.6)", borderRadius: "12px", padding: "14px", marginBottom: "12px" }}>
        {[
          { icon: <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>, label: theme === "dark" ? t("darkMode") : t("lightMode"), value: theme === "dark", toggle: toggleTheme },
          { icon: <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>, label: t("autocheck"), value: autoCheck, toggle: toggleAutoCheck },
          { icon: <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>, label: t("notifications"), value: notifications, toggle: toggleNotifications },
          { icon: <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>, label: t("privacyMode"), value: privacyMode, toggle: togglePrivacyMode },
        ].map((item, i) => (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 0", borderBottom: i < 3 ? "1px solid rgba(255,255,255,0.05)" : "none" }}>
            <span style={{ fontSize: "13px", color: "#e2e8f0", display: "flex", alignItems: "center", gap: 6 }}>{item.icon}{item.label}</span>
            <button onClick={item.toggle} style={{
              width: "44px", height: "24px", borderRadius: "12px", border: "none", cursor: "pointer",
              background: item.value ? (i === 3 ? "#10b981" : "#3b82f6") : "#334155", position: "relative", transition: "all 0.3s"
            }}>
              <div style={{
                width: "18px", height: "18px", borderRadius: "50%", background: "white",
                position: "absolute", top: "3px", transition: "all 0.3s",
                left: item.value ? "23px" : "3px"
              }} />
            </button>
          </div>
        ))}
        {privacyMode && (
          <div style={{ marginTop: "8px", padding: "8px 10px", background: "rgba(16,185,129,0.08)", borderRadius: "8px", border: "1px solid rgba(16,185,129,0.2)" }}>
            <div style={{ fontSize: "11px", color: "#34d399", display: "flex", alignItems: "center", gap: 5 }}>
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            {t("privacyModeHint")}
          </div>
          </div>
        )}
      </div>

      {/* Sensitivity */}
      <div style={{ background: "rgba(30,41,59,0.6)", borderRadius: "12px", padding: "14px", marginBottom: "12px" }}>
        <div style={{ fontSize: "12px", color: "#94a3b8", marginBottom: "8px", display: "flex", alignItems: "center", gap: 5 }}>
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
          {t("sensitivity")}
        </div>
        <div style={{ display: "flex", gap: "6px" }}>
          {["high", "medium", "low"].map(level => (
            <button key={level} onClick={() => changeSensitivity(level)} style={{
              flex: 1, padding: "7px 4px", borderRadius: "7px", cursor: "pointer",
              fontSize: "10px", fontWeight: sensitivity === level ? 700 : 400,
              background: sensitivity === level ? "rgba(99,102,241,0.25)" : "rgba(30,41,59,0.6)",
              border: sensitivity === level ? "1px solid #6366f1" : "1px solid #334155",
              color: sensitivity === level ? "#a5b4fc" : "#64748b"
            }}>
              {t(`sensitivity${level.charAt(0).toUpperCase() + level.slice(1)}`)}
            </button>
          ))}
        </div>
      </div>

      {/* Whitelist button */}
      {onWhitelist && (
        <button onClick={onWhitelist} style={{
          width: "100%", padding: "12px", marginBottom: "12px",
          background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.2)",
          borderRadius: "12px", color: "#34d399", cursor: "pointer", fontSize: "14px", fontWeight: 600,
          display: "flex", alignItems: "center", justifyContent: "center", gap: "8px"
        }}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          {t("whitelist")}
        </button>
      )}

      <div style={{
        background: "rgba(30,41,59,0.6)", borderRadius: "12px",
        padding: "14px", textAlign: "center"
      }}>
        <div style={{ fontSize: "11px", color: "#64748b" }}>
          Qalqan AI v5.1.0 — Cyber Shield
        </div>
        <div style={{ fontSize: "10px", color: "#475569", marginTop: "4px" }}>
          Made in Kazakhstan 🇰🇿
        </div>
      </div>
    </div>
  );
}
