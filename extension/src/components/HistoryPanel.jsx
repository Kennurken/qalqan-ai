// клауд Елдоса N1 — Qalqan AI v5.0
// History of checked sites

import { useState, useEffect } from "react";

export default function HistoryPanel({ t, onBack }) {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    chrome.storage.local.get("qalqan_history", (r) => {
      setHistory((r.qalqan_history || []).reverse().slice(0, 50));
    });
  }, []);

  const clearHistory = () => {
    chrome.storage.local.set({ qalqan_history: [] });
    setHistory([]);
  };

  const verdictColors = { DANGEROUS: "#f87171", SUSPICIOUS: "#fbbf24", SAFE: "#34d399" };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
        <button onClick={onBack} style={{ background: "transparent", color: "#94a3b8", border: "none", cursor: "pointer", fontSize: "14px" }}>
          ← {t("back")}
        </button>
        <span style={{ fontSize: "16px", fontWeight: 700, color: "#f1f5f9" }}>📜 History</span>
        <button onClick={clearHistory} style={{ background: "transparent", color: "#64748b", border: "none", cursor: "pointer", fontSize: "11px" }}>
          🗑
        </button>
      </div>

      {history.length === 0 ? (
        <p style={{ textAlign: "center", color: "#64748b", fontSize: "13px", padding: "20px 0" }}>No history yet</p>
      ) : (
        <div style={{ maxHeight: "350px", overflowY: "auto" }}>
          {history.map((item, i) => (
            <div key={i} style={{
              display: "flex", justifyContent: "space-between", alignItems: "center",
              padding: "8px 10px", marginBottom: "4px",
              background: "rgba(30,41,59,0.4)", borderRadius: "8px",
              borderLeft: `3px solid ${verdictColors[item.verdict] || "#64748b"}`
            }}>
              <div style={{ flex: 1, overflow: "hidden" }}>
                <div style={{ fontSize: "12px", color: "#e2e8f0", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {item.domain || item.url}
                </div>
                <div style={{ fontSize: "10px", color: "#64748b" }}>{item.time}</div>
              </div>
              <span style={{
                fontSize: "10px", fontWeight: 700, padding: "2px 6px", borderRadius: "4px",
                background: `${verdictColors[item.verdict] || "#64748b"}22`,
                color: verdictColors[item.verdict] || "#64748b"
              }}>
                {item.verdict} {item.score}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
