// клауд Елдоса N1 — Qalqan AI v3.0

import { useStats } from "../hooks/useStats";

export default function StatsPanel({ t, onBack }) {
  const { stats, resetStats } = useStats();

  const statItems = [
    { label: t("totalChecked"), value: stats.checked, color: "#3b82f6", icon: "🔍" },
    { label: t("blocked"), value: stats.blocked, color: "#ef4444", icon: "🛑" },
    { label: t("suspiciousCount"), value: stats.suspicious, color: "#f59e0b", icon: "⚠️" },
    { label: t("safeCount"), value: stats.safe, color: "#10b981", icon: "✅" },
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
          📊 {t("stats")}
        </span>
        <div style={{ width: 40 }} />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", marginBottom: "16px" }}>
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
        🗑 Reset
      </button>
    </div>
  );
}
