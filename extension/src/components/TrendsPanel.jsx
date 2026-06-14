// Qalqan AI v5.0
// Trends panel: community-reported top threat domains from /trends API

import { useState, useEffect } from "react";
import { API_URL } from "../config";
import { C } from "../App";
import { PanelHeader } from "./StatsPanel";

export default function TrendsPanel({ t, onBack }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/trends`, { signal: AbortSignal.timeout(10000) })
      .then(r => r.ok ? r.json() : Promise.reject(r.status))
      .then(d => { setData(d); setLoading(false); })
      .catch(e => { setError(String(e)); setLoading(false); });
  }, []);

  const threatColor = (types = []) => {
    if (types.includes("phishing")) return "#ef4444";
    if (types.includes("pyramid")) return "#f59e0b";
    if (types.includes("scam")) return "#f97316";
    if (types.includes("gambling")) return "#8b5cf6";
    return "#6366f1";
  };

  return (
    <div>
      <PanelHeader onBack={onBack} title={t("trends")} t={t} />

      {loading && (
        <div style={{ textAlign: "center", padding: "32px 0", color: "#64748b" }}>
          <div style={{ fontSize: 24, marginBottom: 8 }}>⏳</div>
          <div style={{ fontSize: 12 }}>{t("checking")}</div>
        </div>
      )}

      {error && (
        <div style={{ background: "rgba(239,68,68,0.1)", borderRadius: 10, padding: 12, border: "1px solid #ef444444" }}>
          <p style={{ color: "#f87171", fontSize: 12, margin: 0 }}>⚠️ {error}</p>
        </div>
      )}

      {data && (
        <>
          {/* Summary stats */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: 12 }}>
            {[
              { label: t("totalChecked"), value: data.total_reports || 0, color: "#6366f1" },
              { label: t("blocked"), value: data.unique_domains_reported || 0, color: "#ef4444" },
            ].map((s, i) => (
              <div key={i} style={{
                background: "rgba(30,41,59,0.6)", borderRadius: 10, padding: "10px 12px",
                border: "1px solid #334155",
              }}>
                <div style={{ fontSize: 20, fontWeight: 800, color: s.color }}>{s.value}</div>
                <div style={{ fontSize: 10, color: "#64748b" }}>{s.label}</div>
              </div>
            ))}
          </div>

          {/* Top domains */}
          <div style={{ background: "rgba(30,41,59,0.4)", borderRadius: 12, padding: 12, marginBottom: 12, border: "1px solid #334155" }}>
            <div style={{ fontSize: 11, color: "#64748b", marginBottom: 10, letterSpacing: 1 }}>
              🔥 {t("topThreats")}
            </div>
            {(!data.top_domains || data.top_domains.length === 0) ? (
              <div style={{ fontSize: 12, color: "#64748b", textAlign: "center", padding: "12px 0" }}>
                {t("noTrends")}
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                {data.top_domains.slice(0, 8).map((d, i) => {
                  const color = threatColor(d.types);
                  const maxReports = data.top_domains[0]?.reports || 1;
                  const pct = Math.round((d.reports / maxReports) * 100);
                  return (
                    <div key={i}>
                      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 3 }}>
                        <span style={{ fontSize: 10, color: "#64748b", minWidth: 16, textAlign: "right" }}>
                          #{i + 1}
                        </span>
                        <span style={{ fontSize: 12, color: "#e2e8f0", fontFamily: "monospace", flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                          {d.domain}
                        </span>
                        <span style={{ fontSize: 10, color: color, fontWeight: 700, minWidth: 28 }}>
                          {d.reports}
                        </span>
                        {d.auto_blocked && (
                          <span style={{ fontSize: 9, padding: "1px 5px", borderRadius: 8, background: "rgba(239,68,68,0.15)", color: "#f87171", border: "1px solid #ef444433" }}>
                            AUTO
                          </span>
                        )}
                      </div>
                      {/* Bar */}
                      <div style={{ height: 3, background: "rgba(255,255,255,0.05)", borderRadius: 2, marginLeft: 24, overflow: "hidden" }}>
                        <div style={{ width: `${pct}%`, height: "100%", background: color, borderRadius: 2, transition: "width 0.6s ease" }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Threat type breakdown */}
          {data.threat_type_counts && Object.keys(data.threat_type_counts).length > 0 && (
            <div style={{ background: "rgba(30,41,59,0.4)", borderRadius: 12, padding: 12, border: "1px solid #334155" }}>
              <div style={{ fontSize: 11, color: "#64748b", marginBottom: 10, letterSpacing: 1 }}>
                🎯 {t("threatType")}
              </div>
              {Object.entries(data.threat_type_counts)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5)
                .map(([type, count], i) => {
                  const total = Object.values(data.threat_type_counts).reduce((a, b) => a + b, 0);
                  const pct = Math.round((count / total) * 100);
                  const typeColor = { phishing: "#ef4444", pyramid: "#f59e0b", scam: "#f97316", gambling: "#8b5cf6", malware: "#ec4899" }[type] || "#6366f1";
                  return (
                    <div key={i} style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                      <span style={{ fontSize: 10, color: typeColor, minWidth: 80 }}>{t(type) || type}</span>
                      <div style={{ flex: 1, height: 4, background: "rgba(255,255,255,0.05)", borderRadius: 2, overflow: "hidden" }}>
                        <div style={{ width: `${pct}%`, height: "100%", background: typeColor, borderRadius: 2 }} />
                      </div>
                      <span style={{ fontSize: 10, color: "#64748b", minWidth: 28, textAlign: "right" }}>{pct}%</span>
                    </div>
                  );
                })}
            </div>
          )}
        </>
      )}
    </div>
  );
}
