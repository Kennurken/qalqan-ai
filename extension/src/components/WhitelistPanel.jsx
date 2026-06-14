// Qalqan AI v5.0
// User whitelist manager — add/remove trusted domains

import { useState, useEffect } from "react";
import { C } from "../App";
import { PanelHeader } from "./StatsPanel";

export default function WhitelistPanel({ t, onBack }) {
  const [domains, setDomains] = useState([]);
  const [newDomain, setNewDomain] = useState("");

  useEffect(() => {
    chrome.storage.local.get("qalqan_user_whitelist", (r) => {
      setDomains(r.qalqan_user_whitelist || []);
    });
  }, []);

  const save = (list) => {
    setDomains(list);
    chrome.storage.local.set({ qalqan_user_whitelist: list });
  };

  const addDomain = () => {
    const d = newDomain.trim().toLowerCase().replace(/^https?:\/\//, "").replace(/\/$/, "").replace(/^www\./, "");
    if (d && !domains.includes(d)) {
      save([...domains, d]);
      setNewDomain("");
    }
  };

  const removeDomain = (d) => save(domains.filter(x => x !== d));

  const addCurrentSite = async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab?.url) {
      try {
        const d = new URL(tab.url).hostname.replace("www.", "").toLowerCase();
        if (d && !domains.includes(d)) save([...domains, d]);
      } catch {}
    }
  };

  return (
    <div>
      <PanelHeader onBack={onBack} title={`${t("whitelist")}${domains.length > 0 ? ` (${domains.length})` : ""}`} t={t} />

      {/* Add current site */}
      <button onClick={addCurrentSite} style={{
        width: "100%", padding: "10px", marginBottom: "10px",
        background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.3)",
        borderRadius: "8px", color: "#34d399", cursor: "pointer", fontSize: "13px", fontWeight: 600,
        display: "flex", alignItems: "center", justifyContent: "center", gap: "6px"
      }}>
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
        {t("addCurrentSite")}
      </button>

      {/* Manual add */}
      <div style={{ display: "flex", gap: "6px", marginBottom: "12px" }}>
        <input
          value={newDomain}
          onChange={e => setNewDomain(e.target.value)}
          onKeyDown={e => e.key === "Enter" && addDomain()}
          placeholder="example.com"
          style={{
            flex: 1, padding: "8px", background: "#0f172a", color: "#f1f5f9",
            border: "1px solid #334155", borderRadius: "6px", fontSize: "13px",
            outline: "none", fontFamily: "inherit"
          }}
        />
        <button onClick={addDomain} style={{
          padding: "8px 14px", background: "#10b981", color: "white",
          border: "none", borderRadius: "6px", cursor: "pointer", fontWeight: 700, fontSize: "13px"
        }}>+</button>
      </div>

      {/* Domain list */}
      <div style={{ maxHeight: "250px", overflowY: "auto" }}>
        {domains.length === 0 ? (
          <p style={{ textAlign: "center", color: "#64748b", fontSize: "12px", padding: "20px 0" }}>
            {t("whitelistEmpty")}
          </p>
        ) : domains.map((d, i) => (
          <div key={i} style={{
            display: "flex", justifyContent: "space-between", alignItems: "center",
            padding: "8px 10px", marginBottom: "4px",
            background: "rgba(30,41,59,0.4)", borderRadius: "6px"
          }}>
            <span style={{ fontSize: "13px", color: "#e2e8f0", display: "flex", alignItems: "center", gap: "5px" }}>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
              {d}
            </span>
            <button onClick={() => removeDomain(d)} style={{
              background: "transparent", border: "none", color: "#ef4444",
              cursor: "pointer", fontSize: "16px", padding: "0 4px"
            }}>×</button>
          </div>
        ))}
      </div>

      <p style={{ marginTop: "10px", fontSize: "10px", color: "#64748b", textAlign: "center" }}>
        {t("whitelistHint")}
      </p>
    </div>
  );
}
