// Qalqan AI v5.0

import { useState, useEffect } from "react";
import { useStats } from "../hooks/useStats";

export default function StatsPanel({ t, onBack }) {
  const { stats, resetStats } = useStats();
  const [threatBreakdown, setThreatBreakdown] = useState({});

  useEffect(() => {
    chrome.storage.local.get("qalqan_history", (r) => {
      const history = r.qalqan_history || [];
      const counts = {};
      history.forEach(h => {
        if (h.threat_type && h.threat_type !== "safe") {
          counts[h.threat_type] = (counts[h.threat_type] || 0) + 1;
        }
      });
      setThreatBreakdown(counts);
    });
  }, []);

  const statItems = [
    { label: t("totalChecked"), value: stats.checked, color: "#3b82f6", icon: "🔍" },
    { label: t("blocked"), value: stats.blocked, color: "#ef4444", icon: "🛑" },
    { label: t("suspiciousCount"), value: stats.suspicious, color: "#f59e0b", icon: "⚠️" },
    { label: t("safeCount"), value: stats.safe, color: "#10b981", icon: "✅" },
  ];

  const detectionRate = stats.checked > 0
    ? Math.round(((stats.blocked + stats.suspicious) / stats.checked) * 100)
    : 0;

  const threatTypeLabels = {
    phishing: t("phishing"), malware: t("malware"), pyramid: t("pyramid"),
    scam: t("scam"), gambling: t("gambling"), fake_shop: t("fakeShop"),
    social_engineering: t("socialEngineering"), suspicious_infrastructure: t("suspiciousInfra"),
    casino: t("gambling"), case_battle: "Case Battle"
  };

  const topThreats = Object.entries(threatBreakdown)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 4);

  const maxThreat = topThreats[0]?.[1] || 1;

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
          📊 {t("stats")}
        </span>
        <div style={{ width: 40 }} />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", marginBottom: "12px" }}>
        {statItems.map((item, i) => (
          <div key={i} style={{
            background: "rgba(30,41,59,0.6)", borderRadius: "12px",
            padding: "14px", textAlign: "center",
            border: `1px solid ${item.color}22`
          }}>
            <div style={{ fontSize: "24px", marginBottom: "4px" }}>{item.icon}</div>
            <div style={{ fontSize: "22px", fontWeight: 800, color: item.color }}>{item.value}</div>
            <div style={{ fontSize: "11px", color: "#94a3b8" }}>{item.label}</div>
          </div>
        ))}
      </div>

      {/* Detection rate bar */}
      {stats.checked > 0 && (
        <div style={{ marginBottom: "12px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", color: "#94a3b8", marginBottom: "4px" }}>
            <span>Threat detection rate</span>
            <span style={{ color: detectionRate > 20 ? "#f87171" : "#34d399", fontWeight: 700 }}>{detectionRate}%</span>
          </div>
          <div style={{ height: "6px", background: "rgba(30,41,59,0.8)", borderRadius: "3px", overflow: "hidden" }}>
            <div style={{
              width: `${detectionRate}%`, height: "100%", borderRadius: "3px",
              background: detectionRate > 20 ? "linear-gradient(90deg,#f59e0b,#ef4444)" : "linear-gradient(90deg,#3b82f6,#10b981)",
              transition: "width 0.5s"
            }} />
          </div>
        </div>
      )}

      {/* Threat type breakdown */}
      {topThreats.length > 0 && (
        <div style={{ marginBottom: "12px" }}>
          <div style={{ fontSize: "11px", color: "#64748b", marginBottom: "6px" }}>Top threats detected:</div>
          {topThreats.map(([type, count]) => (
            <div key={type} style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
              <span style={{ fontSize: "10px", color: "#94a3b8", width: "110px", flexShrink: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {threatTypeLabels[type] || type}
              </span>
              <div style={{ flex: 1, height: "8px", background: "rgba(239,68,68,0.1)", borderRadius: "4px", overflow: "hidden" }}>
                <div style={{
                  width: `${(count / maxThreat) * 100}%`, height: "100%",
                  background: "#ef4444", borderRadius: "4px"
                }} />
              </div>
              <span style={{ fontSize: "10px", color: "#f87171", width: "20px", textAlign: "right" }}>{count}</span>
            </div>
          ))}
        </div>
      )}

      {stats.since && (
        <p style={{ textAlign: "center", fontSize: "11px", color: "#64748b" }}>
          {t("since")}: {new Date(stats.since).toLocaleDateString()}
        </p>
      )}

      <button onClick={resetStats} style={{
        width: "100%", padding: "8px", marginTop: "8px",
        background: "transparent", color: "#64748b",
        border: "1px solid #334155", borderRadius: "8px",
        cursor: "pointer", fontSize: "11px"
      }}>
        🗑 {t("clearHistory")}
      </button>
    </div>
  );
}
