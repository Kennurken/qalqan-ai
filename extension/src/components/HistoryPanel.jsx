// Qalqan AI v5.0
// History Panel — search, filter, CSV export, re-check

import { useState, useEffect, useMemo } from "react";
import { C } from "../App";
import { PanelHeader } from "./StatsPanel";

const VERDICT_COLORS = { DANGEROUS: "#f87171", SUSPICIOUS: "#fbbf24", SAFE: "#34d399" };
const VERDICT_ICONS  = { DANGEROUS: "■", SUSPICIOUS: "▲", SAFE: "●" };

function domainOf(item) {
  if (item.domain) return item.domain;
  try { return new URL(item.url).hostname.replace(/^www\./, ""); } catch { return item.url || ""; }
}

function ScoreBar({ score, color }) {
  return (
    <div style={{
      width: 36, height: 4, borderRadius: 2,
      background: "rgba(255,255,255,0.06)", overflow: "hidden",
    }}>
      <div style={{
        height: "100%", borderRadius: 2,
        width: `${score}%`,
        background: color,
        transition: "width 0.4s",
      }} />
    </div>
  );
}

export default function HistoryPanel({ t, onBack }) {
  const [history, setHistory]   = useState([]);
  const [filter, setFilter]     = useState("ALL");
  const [search, setSearch]     = useState("");
  const [sortBy, setSortBy]     = useState("time"); // time | score | verdict
  const [exportMsg, setExportMsg] = useState("");

  useEffect(() => {
    chrome.storage.local.get("qalqan_history", (r) => {
      setHistory((r.qalqan_history || []).reverse().slice(0, 200));
    });
  }, []);

  const counts = useMemo(() => history.reduce((acc, h) => {
    acc[h.verdict] = (acc[h.verdict] || 0) + 1;
    return acc;
  }, {}), [history]);

  const filtered = useMemo(() => {
    let list = history.filter(h => filter === "ALL" || h.verdict === filter);
    if (search) {
      const q = search.toLowerCase();
      list = list.filter(h => (h.domain || h.url || "").toLowerCase().includes(q));
    }
    if (sortBy === "score") list = [...list].sort((a, b) => b.score - a.score);
    else if (sortBy === "verdict") {
      const order = { DANGEROUS: 0, SUSPICIOUS: 1, SAFE: 2 };
      list = [...list].sort((a, b) => (order[a.verdict] ?? 3) - (order[b.verdict] ?? 3));
    }
    return list;
  }, [history, filter, search, sortBy]);

  const clearHistory = () => {
    if (!window.confirm("Тарихты тазалау керек пе? / Очистить историю?")) return;
    chrome.storage.local.set({ qalqan_history: [] });
    setHistory([]);
  };

  const exportCSV = () => {
    const rows = [["domain", "verdict", "score", "threat_type", "source", "time"]];
    filtered.forEach(h => rows.push([
      h.domain || h.url,
      h.verdict,
      h.score,
      h.threat_type || "",
      h.source || "",
      h.time
    ]));
    const csv = rows.map(r => r.map(v => `"${v}"`).join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `qalqan_history_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    setExportMsg("CSV saved!");
    setTimeout(() => setExportMsg(""), 2000);
  };

  const recheck = (url) => {
    const fullUrl = url.startsWith("http") ? url : `https://${url}`;
    chrome.runtime.sendMessage({ action: "MANUAL_CHECK", url: fullUrl });
    setExportMsg("↻ Rechecking...");
    setTimeout(() => setExportMsg(""), 1500);
  };

  return (
    <div>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "14px" }}>
        <PanelHeader onBack={onBack} title={t("history")} t={t} />
        <div style={{ display: "flex", gap: 5, alignItems: "center", marginLeft: "auto" }}>
          {filtered.length > 0 && (
            <button onClick={exportCSV} title="Export CSV" style={{
              background: "rgba(0,212,255,0.08)", color: "#00d4ff",
              border: "1px solid rgba(0,212,255,0.2)", cursor: "pointer",
              fontSize: "9px", padding: "3px 8px", borderRadius: "5px", fontWeight: 700,
              letterSpacing: "0.5px",
            }}>
              CSV
            </button>
          )}
          <button onClick={clearHistory} title={t("clearHistory")} style={{
            background: "transparent", color: "#475569", border: "none",
            cursor: "pointer", fontSize: "12px", padding: "2px",
            transition: "color 0.2s",
          }}
          onMouseEnter={e => e.currentTarget.style.color = "#ff8096"}
          onMouseLeave={e => e.currentTarget.style.color = "#475569"}
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
            </svg>
          </button>
        </div>
      </div>

      {exportMsg && (
        <div style={{
          fontSize: "11px", textAlign: "center", marginBottom: "6px",
          color: "#34d399", padding: "4px", borderRadius: "5px",
          background: "rgba(16,185,129,0.1)",
        }}>
          {exportMsg}
        </div>
      )}

      {history.length === 0 ? (
        <p style={{ textAlign: "center", color: "#64748b", fontSize: "13px", padding: "30px 0" }}>
          {t("noHistory")}
        </p>
      ) : (
        <>
          {/* Stat pills */}
          <div style={{ display: "flex", gap: "6px", marginBottom: "8px", flexWrap: "wrap" }}>
            <button onClick={() => setFilter("ALL")} style={{
              fontSize: "10px", fontWeight: 700, padding: "3px 9px", borderRadius: "6px",
              border: "none", cursor: "pointer",
              background: filter === "ALL" ? "rgba(99,102,241,0.2)" : "rgba(30,41,59,0.4)",
              color: filter === "ALL" ? "#a5b4fc" : "#64748b",
              outline: filter === "ALL" ? "1px solid rgba(99,102,241,0.35)" : "none",
            }}>
              ALL {history.length}
            </button>
            {["DANGEROUS", "SUSPICIOUS", "SAFE"].filter(v => counts[v] > 0).map(v => (
              <button key={v} onClick={() => setFilter(v)} style={{
                fontSize: "10px", fontWeight: 700, padding: "3px 9px", borderRadius: "6px",
                border: "none", cursor: "pointer",
                background: filter === v ? `${VERDICT_COLORS[v]}22` : "rgba(30,41,59,0.4)",
                color: filter === v ? VERDICT_COLORS[v] : "#64748b",
                outline: filter === v ? `1px solid ${VERDICT_COLORS[v]}44` : "none",
              }}>
                {VERDICT_ICONS[v]} {counts[v]}
              </button>
            ))}
          </div>

          {/* Search + sort row */}
          <div style={{ display: "flex", gap: "6px", marginBottom: "8px" }}>
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder={t("searchHistory") || "Іздеу..."}
              style={{
                flex: 1, padding: "6px 9px",
                background: "#0f172a", color: "#f1f5f9",
                border: "1px solid #1e293b", borderRadius: "7px",
                fontSize: "11px", outline: "none", fontFamily: "inherit",
              }}
            />
            <select
              value={sortBy}
              onChange={e => setSortBy(e.target.value)}
              style={{
                background: "#0f172a", color: "#64748b",
                border: "1px solid #1e293b", borderRadius: "7px",
                fontSize: "10px", padding: "4px 6px", cursor: "pointer",
              }}
            >
              <option value="time">Уақыт</option>
              <option value="score">Балл</option>
              <option value="verdict">Вердикт</option>
            </select>
          </div>

          {/* List */}
          <div style={{ maxHeight: "270px", overflowY: "auto" }}>
            {filtered.length === 0 ? (
              <p style={{ textAlign: "center", color: "#64748b", fontSize: "12px", padding: "16px 0" }}>
                Нәтиже жоқ
              </p>
            ) : filtered.map((item, i) => {
              const color = VERDICT_COLORS[item.verdict] || "#64748b";
              return (
                <div key={i} style={{
                  display: "flex", alignItems: "center", gap: "8px",
                  padding: "7px 9px", marginBottom: "3px",
                  background: "rgba(15,23,42,0.6)",
                  border: "1px solid rgba(255,255,255,0.04)",
                  borderRadius: "8px", borderLeft: `3px solid ${color}`,
                }}>
                  <div style={{ flex: 1, overflow: "hidden", minWidth: 0 }}>
                    <div style={{
                      fontSize: "11px", color: "#e2e8f0",
                      overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
                      fontWeight: 600,
                    }}>
                      {domainOf(item)}
                    </div>
                    <div style={{ display: "flex", gap: "6px", alignItems: "center", marginTop: "2px" }}>
                      <span style={{ fontSize: "9px", color: "#334155" }}>{item.time}</span>
                      {item.threat_type && item.threat_type !== "safe" && (
                        <span style={{
                          fontSize: "9px", color: "#64748b",
                          background: "rgba(255,255,255,0.03)",
                          padding: "1px 5px", borderRadius: "4px",
                          border: "1px solid rgba(255,255,255,0.05)",
                        }}>
                          {item.threat_type}
                        </span>
                      )}
                    </div>
                  </div>
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: "3px", flexShrink: 0 }}>
                    <span style={{
                      fontSize: "9px", fontWeight: 800, padding: "2px 6px", borderRadius: "4px",
                      background: `${color}18`, color,
                    }}>
                      {item.score}
                    </span>
                    <ScoreBar score={item.score} color={color} />
                  </div>
                  <button
                    onClick={() => recheck(item.url || item.domain)}
                    title="Re-check"
                    style={{
                      background: "transparent", color: "#334155", border: "none",
                      cursor: "pointer", fontSize: "12px", padding: "2px", flexShrink: 0,
                    }}
                  >
                    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>
                  </button>
                </div>
              );
            })}
          </div>

          <div style={{ marginTop: "8px", fontSize: "10px", color: "#1e293b", textAlign: "right" }}>
            {filtered.length}/{history.length} жазба
          </div>
        </>
      )}
    </div>
  );
}
