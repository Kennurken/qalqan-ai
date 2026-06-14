// Qalqan AI v5.1 REDESIGN
import { useState, useEffect } from "react";
import { useStats } from "../hooks/useStats";
import { C } from "../App";

const BackArrow = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="15 18 9 12 15 6"/>
  </svg>
);
const TrashIcon = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
  </svg>
);

const STAT_ICONS = {
  checked: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
    </svg>
  ),
  blocked: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      <line x1="9" y1="9" x2="15" y2="15" strokeWidth="1.5"/><line x1="15" y1="9" x2="9" y2="15" strokeWidth="1.5"/>
    </svg>
  ),
  suspicious: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
      <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
  ),
  safe: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      <polyline points="9 12 11 14 15 10" strokeWidth="2.5"/>
    </svg>
  ),
};

const THREAT_TYPE_LABELS = {
  phishing: "Phishing", malware: "Malware", pyramid: "Pyramid", scam: "Scam",
  gambling: "Gambling", fake_shop: "Fake Shop", social_engineering: "Social Eng.",
  suspicious_infrastructure: "Susp. Infra", casino: "Casino", case_battle: "Case Battle",
};

export default function StatsPanel({ t, onBack }) {
  const { stats, resetStats } = useStats();
  const [threatBreakdown, setThreatBreakdown] = useState({});

  useEffect(() => {
    chrome.storage.local.get("qalqan_history", (r) => {
      const history = r.qalqan_history || [];
      const counts = {};
      history.forEach(h => {
        if (h.threat_type && h.threat_type !== "safe")
          counts[h.threat_type] = (counts[h.threat_type] || 0) + 1;
      });
      setThreatBreakdown(counts);
    });
  }, []);

  const detectionRate = stats.checked > 0
    ? Math.round(((stats.blocked + stats.suspicious) / stats.checked) * 100)
    : 0;

  const topThreats = Object.entries(threatBreakdown).sort((a, b) => b[1] - a[1]).slice(0, 4);
  const maxThreat = topThreats[0]?.[1] || 1;

  const statItems = [
    { key: "checked",    label: t("totalChecked"),    value: stats.checked,    color: "#00d4ff" },
    { key: "blocked",    label: t("blocked"),          value: stats.blocked,    color: "#ff3b5c" },
    { key: "suspicious", label: t("suspiciousCount"),  value: stats.suspicious, color: "#fbbf24" },
    { key: "safe",       label: t("safeCount"),        value: stats.safe,       color: "#22c55e" },
  ];

  return (
    <div style={{ animation: "fadeUp 0.2s ease" }}>
      {/* Panel header */}
      <PanelHeader onBack={onBack} title={t("stats")} />

      {/* Stat cards grid */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px", marginBottom: "12px" }}>
        {statItems.map(({ key, label, value, color }) => (
          <div key={key} style={{
            background: `${color}09`,
            border: `1px solid ${color}28`,
            borderRadius: "10px", padding: "12px 14px",
            textAlign: "center", position: "relative", overflow: "hidden",
          }}>
            <div style={{ color, opacity: 0.35, position: "absolute", top: 8, right: 8 }}>
              {STAT_ICONS[key]}
            </div>
            <div style={{
              fontSize: "28px", fontWeight: 800, fontFamily: C.mono,
              color, lineHeight: 1, textShadow: `0 0 16px ${color}60`,
            }}>
              {value}
            </div>
            <div style={{ fontSize: "10px", color: C.muted, marginTop: "4px", letterSpacing: "0.3px" }}>
              {label}
            </div>
          </div>
        ))}
      </div>

      {/* Detection rate */}
      {stats.checked > 0 && (
        <div style={{
          background: "rgba(13,20,38,0.8)", border: `1px solid ${C.border}`,
          borderRadius: "10px", padding: "12px", marginBottom: "10px",
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", marginBottom: "6px" }}>
            <span style={{ color: C.muted }}>Threat detection rate</span>
            <span style={{
              fontFamily: C.mono, fontWeight: 700,
              color: detectionRate > 20 ? "#ff3b5c" : "#22c55e",
            }}>
              {detectionRate}%
            </span>
          </div>
          <div style={{ height: "5px", background: "rgba(255,255,255,0.05)", borderRadius: "3px", overflow: "hidden" }}>
            <div style={{
              width: `${detectionRate}%`, height: "100%", borderRadius: "3px",
              background: detectionRate > 20 ? "linear-gradient(90deg,#fbbf24,#ff3b5c)" : "linear-gradient(90deg,#00d4ff,#22c55e)",
              boxShadow: detectionRate > 20 ? "0 0 8px rgba(255,59,92,0.5)" : "0 0 8px rgba(34,197,94,0.4)",
              transition: "width 0.6s ease",
            }} />
          </div>
        </div>
      )}

      {/* Threat breakdown */}
      {topThreats.length > 0 && (
        <div style={{
          background: "rgba(13,20,38,0.8)", border: `1px solid ${C.border}`,
          borderRadius: "10px", padding: "12px", marginBottom: "10px",
        }}>
          <div style={{ fontSize: "10px", color: C.muted, marginBottom: "8px", letterSpacing: "0.5px", textTransform: "uppercase" }}>
            Top threats detected
          </div>
          {topThreats.map(([type, count]) => (
            <div key={type} style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "5px" }}>
              <span style={{ fontSize: "10.5px", color: "#94a3b8", width: "100px", flexShrink: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", fontFamily: C.sans }}>
                {THREAT_TYPE_LABELS[type] || type}
              </span>
              <div style={{ flex: 1, height: "5px", background: "rgba(255,59,92,0.1)", borderRadius: "3px", overflow: "hidden" }}>
                <div style={{
                  width: `${(count / maxThreat) * 100}%`, height: "100%", borderRadius: "3px",
                  background: "#ff3b5c", boxShadow: "0 0 6px rgba(255,59,92,0.4)",
                  transition: "width 0.4s ease",
                }} />
              </div>
              <span style={{ fontSize: "10px", fontFamily: C.mono, color: "#ff8096", width: "20px", textAlign: "right" }}>
                {count}
              </span>
            </div>
          ))}
        </div>
      )}

      {stats.since && (
        <p style={{ textAlign: "center", fontSize: "10px", color: C.muted, fontFamily: C.mono, margin: "0 0 10px" }}>
          tracking since {new Date(stats.since).toLocaleDateString()}
        </p>
      )}

      <button onClick={resetStats} style={{
        width: "100%", padding: "8px",
        background: "transparent", color: C.muted,
        border: `1px solid ${C.border}`, borderRadius: "8px",
        cursor: "pointer", fontSize: "11px", fontFamily: C.sans,
        display: "flex", alignItems: "center", justifyContent: "center", gap: "6px",
        transition: "all 0.2s",
      }}
      onMouseEnter={e => { e.currentTarget.style.borderColor = "rgba(255,59,92,0.4)"; e.currentTarget.style.color = "#ff8096"; }}
      onMouseLeave={e => { e.currentTarget.style.borderColor = C.border; e.currentTarget.style.color = C.muted; }}
      >
        <TrashIcon /> {t("resetStats")}
      </button>
    </div>
  );
}

// Shared panel header used across all sub-panels
export function PanelHeader({ onBack, title, t }) {
  const [hover, setHover] = useState(false);
  return (
    <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "14px" }}>
      <button
        onClick={onBack}
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
        style={{
          display: "flex", alignItems: "center", gap: "4px",
          background: hover ? "rgba(0,212,255,0.08)" : "transparent",
          border: `1px solid ${hover ? "rgba(0,212,255,0.3)" : C.border}`,
          color: hover ? "#00d4ff" : C.muted,
          borderRadius: "7px", padding: "5px 9px", cursor: "pointer",
          fontSize: "11px", fontFamily: C.sans, transition: "all 0.15s",
        }}
      >
        <BackArrow /> {t ? t("back") : "Back"}
      </button>
      <span style={{
        fontSize: "13px", fontWeight: 700,
        color: "#f1f5f9", letterSpacing: "0.5px",
        fontFamily: C.sans,
      }}>
        {title}
      </span>
    </div>
  );
}
