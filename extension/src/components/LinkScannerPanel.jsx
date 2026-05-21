// Qalqan AI v5.0
// Link Scanner: batch checks all external links on current page

import { useState } from "react";
import { API_URL } from "../config";

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
        body: JSON.stringify({ urls: links.slice(0, 10), lang })
      });
      const data = await res.json();
      setResults(data.results || []);
      setStatus("done");
    } catch (e) {
      console.error("Link scan error:", e);
      setStatus("error");
    }
  };

  const verdictColor = { DANGEROUS: "#f87171", SUSPICIOUS: "#fbbf24", SAFE: "#34d399" };
  const verdictBg = { DANGEROUS: "rgba(239,68,68,0.1)", SUSPICIOUS: "rgba(245,158,11,0.1)", SAFE: "rgba(16,185,129,0.1)" };

  const stats = results.reduce((acc, r) => {
    acc[r.verdict] = (acc[r.verdict] || 0) + 1;
    return acc;
  }, {});

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
        <button onClick={onBack} style={{ background: "transparent", color: "#94a3b8", border: "none", cursor: "pointer", fontSize: "14px" }}>
          ← {t("back")}
        </button>
        <span style={{ fontSize: "16px", fontWeight: 700, color: "#f1f5f9" }}>🔗 Link Scanner</span>
        <div style={{ width: 40 }} />
      </div>

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
        {status === "scanning" ? "⏳ Тексеруде..." : "🔍 Беттегі сілтемелерді тексеру"}
      </button>

      {status === "done" && results.length === 0 && (
        <p style={{ textAlign: "center", color: "#64748b", fontSize: "13px" }}>
          Сыртқы сілтемелер табылмады ({totalLinks} барлығы)
        </p>
      )}

      {status === "error" && (
        <p style={{ textAlign: "center", color: "#f87171", fontSize: "13px" }}>
          ⚠️ Сканерлеу қатесі. Бетті жаңартып, қайталаңыз.
        </p>
      )}

      {results.length > 0 && (
        <>
          {/* Summary bar */}
          <div style={{ display: "flex", gap: "8px", marginBottom: "10px", flexWrap: "wrap" }}>
            {stats.DANGEROUS > 0 && (
              <span style={{ fontSize: "11px", background: "rgba(239,68,68,0.15)", color: "#f87171", padding: "3px 8px", borderRadius: "6px", fontWeight: 700 }}>
                🛑 {stats.DANGEROUS} қауіпті
              </span>
            )}
            {stats.SUSPICIOUS > 0 && (
              <span style={{ fontSize: "11px", background: "rgba(245,158,11,0.15)", color: "#fbbf24", padding: "3px 8px", borderRadius: "6px", fontWeight: 700 }}>
                ⚠️ {stats.SUSPICIOUS} күдікті
              </span>
            )}
            {stats.SAFE > 0 && (
              <span style={{ fontSize: "11px", background: "rgba(16,185,129,0.15)", color: "#34d399", padding: "3px 8px", borderRadius: "6px", fontWeight: 700 }}>
                ✅ {stats.SAFE} қауіпсіз
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
          <p style={{ fontSize: "10px", color: "#64748b", textAlign: "center", marginTop: "8px" }}>
            {results.length} / {totalLinks} сілтеме тексерілді
          </p>
        </>
      )}
    </div>
  );
}
