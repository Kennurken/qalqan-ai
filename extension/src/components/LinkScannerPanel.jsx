// Qalqan AI v5.0
// Link Scanner: batch checks all external links on current page

import { useState } from "react";
import { API_URL } from "../config";
import { C } from "../App";
import { PanelHeader } from "./StatsPanel";

export default function LinkScannerPanel({ t, onBack }) {
  const [status, setStatus] = useState("idle"); // idle | scanning | done | error
  const [results, setResults] = useState([]);
  const [totalLinks, setTotalLinks] = useState(0);

  const scan = async () => {
    setStatus("scanning");
    setResults([]);
    try {
      // Get links from content script
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      let links = [];
      try {
        const resp = await chrome.tabs.sendMessage(tab.id, { action: "GET_LINKS" });
        links = resp?.links || [];
        setTotalLinks(resp?.total || 0);
      } catch {
        // Content script not ready — inject it
        await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ["content.js"] });
        const resp = await chrome.tabs.sendMessage(tab.id, { action: "GET_LINKS" });
        links = resp?.links || [];
        setTotalLinks(resp?.total || 0);
      }

      if (links.length === 0) {
        setStatus("done");
        return;
      }

      const lang = (await chrome.storage.local.get("qalqan_lang")).qalqan_lang || "kk";
      const res = await fetch(`${API_URL}/batch`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ urls: links.slice(0, 15), lang })
      });
      const data = await res.json();
      setResults(data.results || []);
      setStatus("done");
    } catch (e) {
      console.error("Link scan error:", e);
      setStatus("error");
    }
  };

  const exportReport = () => {
    const report = {
      scanned_at: new Date().toISOString(),
      total_links: totalLinks,
      checked: results.length,
      summary: stats,
      results: results.map(r => ({
        url: r.url,
        verdict: r.verdict,
        threat_score: r.threat_score,
        threat_type: r.threat_type,
        source: r.source
      }))
    };
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `qalqan-scan-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const verdictColor = { DANGEROUS: "#f87171", SUSPICIOUS: "#fbbf24", SAFE: "#34d399" };
  const verdictBg = { DANGEROUS: "rgba(239,68,68,0.1)", SUSPICIOUS: "rgba(245,158,11,0.1)", SAFE: "rgba(16,185,129,0.1)" };

  const stats = results.reduce((acc, r) => {
    acc[r.verdict] = (acc[r.verdict] || 0) + 1;
    return acc;
  }, {});

  return (
    <div>
      <PanelHeader onBack={onBack} title={t("linkScanner")} t={t} />

      <button
        onClick={scan}
        disabled={status === "scanning"}
        style={{
          width: "100%", padding: "12px", marginBottom: "12px",
          background: status === "scanning" ? "#334155" : "linear-gradient(135deg,#6366f1,#4f46e5)",
          color: "white", border: "none", borderRadius: "10px",
          cursor: status === "scanning" ? "not-allowed" : "pointer",
          fontWeight: 700, fontSize: "14px"
        }}
      >
        {status === "scanning"
          ? <span style={{display:"flex",alignItems:"center",gap:"6px"}}><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{animation:"spin 1s linear infinite"}}><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>{t("scanningLinks")}</span>
          : <span style={{display:"flex",alignItems:"center",gap:"6px"}}><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>{t("scanLinks")}</span>
        }
      </button>

      {status === "done" && results.length === 0 && (
        <p style={{ textAlign: "center", color: "#64748b", fontSize: "13px" }}>
          {t("noLinksFound")} ({totalLinks} total)
        </p>
      )}

      {status === "error" && (
        <p style={{ textAlign: "center", color: "#f87171", fontSize: "13px" }}>
          {t("scanError")}
        </p>
      )}

      {results.length > 0 && (
        <>
          {/* Summary bar */}
          <div style={{ display: "flex", gap: "8px", marginBottom: "10px", flexWrap: "wrap" }}>
            {stats.DANGEROUS > 0 && (
              <span style={{ fontSize: "11px", background: "rgba(239,68,68,0.15)", color: "#f87171", padding: "3px 8px", borderRadius: "6px", fontWeight: 700, display:"inline-flex", alignItems:"center", gap:"4px" }}>
                <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L1 21h22L12 2zm0 3l8.66 15H3.34L12 5zm-1 5v5h2v-5h-2zm0 7v2h2v-2h-2z"/></svg>
                {stats.DANGEROUS} {t("dangerousLinks")}
              </span>
            )}
            {stats.SUSPICIOUS > 0 && (
              <span style={{ fontSize: "11px", background: "rgba(245,158,11,0.15)", color: "#fbbf24", padding: "3px 8px", borderRadius: "6px", fontWeight: 700, display:"inline-flex", alignItems:"center", gap:"4px" }}>
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                {stats.SUSPICIOUS} {t("suspiciousLinks")}
              </span>
            )}
            {stats.SAFE > 0 && (
              <span style={{ fontSize: "11px", background: "rgba(16,185,129,0.15)", color: "#34d399", padding: "3px 8px", borderRadius: "6px", fontWeight: 700, display:"inline-flex", alignItems:"center", gap:"4px" }}>
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><polyline points="20 6 9 17 4 12"/></svg>
                {stats.SAFE} {t("safeLinks")}
              </span>
            )}
          </div>

          {/* Results list */}
          <div style={{ maxHeight: "280px", overflowY: "auto" }}>
            {results.map((r, i) => {
              const domain = (() => { try { return new URL(r.url).hostname.replace("www.", ""); } catch { return r.url; } })();
              return (
                <div key={i} style={{
                  display: "flex", justifyContent: "space-between", alignItems: "center",
                  padding: "7px 10px", marginBottom: "4px",
                  background: verdictBg[r.verdict] || "rgba(30,41,59,0.4)",
                  borderRadius: "8px",
                  borderLeft: `3px solid ${verdictColor[r.verdict] || "#64748b"}`
                }}>
                  <div style={{ flex: 1, overflow: "hidden" }}>
                    <div style={{ fontSize: "12px", color: "#e2e8f0", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      {domain}
                    </div>
                    {r.threat_type && r.threat_type !== "safe" && (
                      <div style={{ fontSize: "10px", color: "#94a3b8" }}>{r.threat_type}</div>
                    )}
                  </div>
                  <span style={{
                    fontSize: "10px", fontWeight: 700, marginLeft: "8px",
                    color: verdictColor[r.verdict] || "#64748b",
                    background: verdictBg[r.verdict] || "transparent",
                    padding: "2px 6px", borderRadius: "4px", flexShrink: 0
                  }}>
                    {r.threat_score || 0}
                  </span>
                </div>
              );
            })}
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "8px" }}>
            <p style={{ fontSize: "10px", color: "#64748b", margin: 0 }}>
              {results.length} / {totalLinks} {t("linksChecked")}
            </p>
            <button
              onClick={exportReport}
              style={{
                fontSize: "10px", color: "#6366f1", background: "rgba(99,102,241,0.1)",
                border: "1px solid rgba(99,102,241,0.3)", borderRadius: "6px",
                padding: "3px 8px", cursor: "pointer"
              }}
            >
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{display:"inline",verticalAlign:"middle",marginRight:"3px"}}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              {t("exportReport")}
            </button>
          </div>
        </>
      )}
    </div>
  );
}
