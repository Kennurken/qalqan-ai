// клауд Елдоса N1 — Qalqan AI v5.0

import { useState, useEffect } from "react";

export default function SettingsPanel({ lang, onLangChange, t, onBack, onWhitelist }) {
  const [theme, setTheme] = useState("dark");
  const [autoCheck, setAutoCheck] = useState(true);
  const [notifications, setNotifications] = useState(true);

  useEffect(() => {
    chrome.storage.local.get(["qalqan_theme", "qalqan_autocheck", "qalqan_notifications"], (r) => {
      if (r.qalqan_theme) setTheme(r.qalqan_theme);
      if (r.qalqan_autocheck !== undefined) setAutoCheck(r.qalqan_autocheck);
      if (r.qalqan_notifications !== undefined) setNotifications(r.qalqan_notifications);
    });
  }, []);

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

  const languages = [
    { code: "kk", label: "Қазақша", flag: "🇰🇿" },
    { code: "ru", label: "Русский", flag: "🇷🇺" },
    { code: "en", label: "English", flag: "🇬🇧" },
  ];

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
        <button onClick={onBack} style={{
          background: "transparent", color: "#94a3b8", border: "none",
          cursor: "pointer", fontSize: "14px"
        }}>
          ← {t("back")}
        </button>
        <span style={{ fontSize: "16px", fontWeight: 700, color: "#f1f5f9" }}>
          ⚙️ {t("settings")}
        </span>
        <div style={{ width: 40 }} />
      </div>

      <div style={{
        background: "rgba(30,41,59,0.6)", borderRadius: "12px",
        padding: "14px", marginBottom: "12px"
      }}>
        <div style={{ fontSize: "13px", color: "#94a3b8", marginBottom: "10px" }}>
          🌐 {t("language")}
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
          { label: "🌓 " + (theme === "dark" ? "Dark Mode" : "Light Mode"), value: theme === "dark", toggle: toggleTheme },
          { label: "🔄 Auto-check", value: autoCheck, toggle: toggleAutoCheck },
          { label: "🔔 Notifications", value: notifications, toggle: toggleNotifications },
        ].map((item, i) => (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 0", borderBottom: i < 2 ? "1px solid rgba(255,255,255,0.05)" : "none" }}>
            <span style={{ fontSize: "13px", color: "#e2e8f0" }}>{item.label}</span>
            <button onClick={item.toggle} style={{
              width: "44px", height: "24px", borderRadius: "12px", border: "none", cursor: "pointer",
              background: item.value ? "#3b82f6" : "#334155", position: "relative", transition: "all 0.3s"
            }}>
              <div style={{
                width: "18px", height: "18px", borderRadius: "50%", background: "white",
                position: "absolute", top: "3px", transition: "all 0.3s",
                left: item.value ? "23px" : "3px"
              }} />
            </button>
          </div>
        ))}
      </div>

      {/* Whitelist button */}
      {onWhitelist && (
        <button onClick={onWhitelist} style={{
          width: "100%", padding: "12px", marginBottom: "12px",
          background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.2)",
          borderRadius: "12px", color: "#34d399", cursor: "pointer", fontSize: "14px", fontWeight: 600,
          display: "flex", alignItems: "center", justifyContent: "center", gap: "8px"
        }}>
          ✅ Whitelist Manager
        </button>
      )}

      <div style={{
        background: "rgba(30,41,59,0.6)", borderRadius: "12px",
        padding: "14px", textAlign: "center"
      }}>
        <div style={{ fontSize: "11px", color: "#64748b" }}>
          Qalqan AI v5.0 — Cyber Shield
        </div>
        <div style={{ fontSize: "10px", color: "#475569", marginTop: "4px" }}>
          Made in Kazakhstan 🇰🇿
        </div>
      </div>
    </div>
  );
}
