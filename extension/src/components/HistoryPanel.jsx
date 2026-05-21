// Qalqan AI v5.0
// History of checked sites

import { useState, useEffect } from "react";

export default function HistoryPanel({ t, onBack }) {
  const [history, setHistory] = useState([]);
  const [filter, setFilter] = useState("ALL"); // ALL | DANGEROUS | SUSPICIOUS | SAFE
  const [search, setSearch] = useState("");

  useEffect(() => {
    chrome.storage.local.get("qalqan_history", (r) => {
      setHistory((r.qalqan_history || []).reverse().slice(0, 100));
    });
  }, []);

  const clearHistory = () => {
    chrome.storage.local.set({ qalqan_history: [] });
    setHistory([]);
  };

  const verdictColors = { DANGEROUS: "#f87171", SUSPICIOUS: "#fbbf24", SAFE: "#34d399" };

  const counts = history.reduce((acc, h) => {
    acc[h.verdict] = (acc[h.verdict] || 0) + 1;
    return acc;
  }, {});

  const filtered = history
    .filter(h => filter === "ALL" || h.verdict === filter)
    .filter(h => !search || (h.domain || h.url || "").toLowerCase().includes(search.toLowerCase()));

  const filterBtnStyle = (v) => ({
    fontSize: "10px", fontWeight: 700, padding: "3px 8px", borderRadius: "6px",
    border: "none", cursor: "pointer",
    background: filter === v ? (verdictColors[v] || "rgba(99,102,241,0.3)") + "33" : "rgba(30,41,59,0.4)",
    color: filter === v ? (verdictColors[v] || "#94a3b8") : "#64748b",
    outline: filter === v ? `1px solid ${verdictColors[v] || "#6366f1"}55` : "none"
  });

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
        <button onClick={onBack} style={{ background: "transparent", color: "#94a3b8", border: "none", cursor: "pointer", fontSize: "14px" }}>
          ← {t("back")}
        </button>
        <span style={{ fontSize: "16px", fontWeight: 700, color: "#f1f5f9" }}>
          📜 {t("history")} <span style={{ fontSize: "11px", color: "#64748b", fontWeight: 400 }}>({history.length})</span>
        </span>
        <button onClick={clearHistory} title={t("clearHistory")} style={{ background: "transparent", color: "#64748b", border: "none", cursor: "pointer", fontSize: "11px" }}>
          🗑
        </button>
      </div>

      {/* Search */}
      {history.length > 0 && (
        <input
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder={t("searchHistory")}
          style={{
            width: "100%", padding: "7px 10px", marginBottom: "8px",
            background: "#0f172a", color: "#f1f5f9",
            border: "1px solid #334155", borderRadius: "7px",
            fontSize: "12px", outline: "none", fontFamily: "inherit",
            boxSizing: "border-box"
          }}
        />
      )}

      {/* Filter tabs */}
      {history.length > 0 && (
        <div style={{ display: "flex", gap: "4px", marginBottom: "10px", flexWrap: "wrap" }}>
          <button onClick={() => setFilter("ALL")} style={filterBtnStyle("ALL")}>
            ALL {history.length}
          </button>
          {counts.DANGEROUS > 0 && (
            <button onClick={() => setFilter("DANGEROUS")} style={filterBtnStyle("DANGEROUS")}>
              🛑 {counts.DANGEROUS}
            </button>
          )}
          {counts.SUSPICIOUS > 0 && (
            <button onClick={() => setFilter("SUSPICIOUS")} style={filterBtnStyle("SUSPICIOUS")}>
              ⚠️ {counts.SUSPICIOUS}
            </button>
          )}
          {counts.SAFE > 0 && (
            <button onClick={() => setFilter("SAFE")} style={filterBtnStyle("SAFE")}>
              ✅ {counts.SAFE}
            </button>
          )}
        </div>
      )}

      {filtered.length === 0 ? (
        <p style={{ textAlign: "center", color: "#64748b", fontSize: "13px", padding: "20px 0" }}>{t("noHistory")}</p>
      ) : (
        <div style={{ maxHeight: "310px", overflowY: "auto" }}>
          {filtered.map((item, i) => (
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
