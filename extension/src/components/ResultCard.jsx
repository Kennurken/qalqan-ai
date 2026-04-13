// клауд Елдоса N1 — Qalqan AI v5.0
// ResultCard with XAI factor breakdown bars

import { useState } from "react";

export default function ResultCard({ result, t }) {
  const [showXAI, setShowXAI] = useState(false);

  if (!result) return null;

  const isDangerous = result.verdict === "DANGEROUS" || result.verdict === "ҚАУІПТІ";
  const isSuspicious = result.verdict === "SUSPICIOUS" || result.threat_score >= 40;
  const isSafe = !isDangerous && !isSuspicious;

  const borderColor = isDangerous ? "#ef4444" : isSuspicious ? "#f59e0b" : "#10b981";
  const bgColor = isDangerous ? "rgba(239,68,68,0.08)" : isSuspicious ? "rgba(245,158,11,0.08)" : "rgba(16,185,129,0.08)";
  const verdictColor = isDangerous ? "#f87171" : isSuspicious ? "#fbbf24" : "#34d399";
  const verdictText = isDangerous ? t("dangerous") : isSuspicious ? t("suspicious") : t("safe");
  const emoji = isDangerous ? "❌" : isSuspicious ? "⚠️" : "✅";

  const sourceNames = {
    phishtank: "PhishTank", google_safe_browsing: "Google Safe Browsing",
    urlhaus: "URLhaus", openphish: "OpenPhish", pyramid_list: "Qalqan Pyramid DB",
    local_blacklist: "Blacklist", groq_ai: "Qalqan AI", gemini_ai: "Gemini AI",
    gemini_vision: "Qalqan Vision", domain_intel: "Domain Intel",
    whitelist: "Trusted List", no_data: "—", ai_error: "AI Error"
  };

  const explanation = result.explanation;
  const hasXAI = explanation && (explanation.top_factors?.length > 0 || explanation.safe_factors?.length > 0);

  return (
    <div style={{ background: bgColor, borderLeft: `4px solid ${borderColor}`, borderRadius: "12px", padding: "14px", marginBottom: "12px" }}>
      {/* Verdict + Score */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
        <span style={{ fontSize: "16px", fontWeight: 800, color: verdictColor }}>
          {emoji} {verdictText}
        </span>
        <span style={{
          fontSize: "11px", fontWeight: 700,
          background: "rgba(255,255,255,0.1)", padding: "3px 8px", borderRadius: "6px",
          color: verdictColor
        }}>
          {result.threat_score}/100
        </span>
      </div>

      {/* Detail */}
      <p style={{ fontSize: "13px", color: "#cbd5e1", lineHeight: 1.5, margin: "0 0 8px" }}>
        {result.detail || result.detail_kk || "—"}
      </p>

      {/* Meta */}
      <div style={{ fontSize: "11px", color: "#64748b", display: "flex", gap: "12px", flexWrap: "wrap" }}>
        {result.threat_type && result.threat_type !== "safe" && <span>🏷 {result.threat_type}</span>}
        <span>🔍 {sourceNames[result.source] || result.source}</span>
        {result.cached && <span>⚡ cached</span>}
        {result.metadata?.processing_time_ms && <span>⏱ {result.metadata.processing_time_ms}ms</span>}
      </div>

      {/* Indicators */}
      {result.indicators && result.indicators.length > 0 && (
        <div style={{ marginTop: "8px", display: "flex", gap: "4px", flexWrap: "wrap" }}>
          {result.indicators.slice(0, 5).map((ind, i) => (
            <span key={i} style={{
              fontSize: "10px", background: "rgba(255,255,255,0.06)",
              padding: "2px 6px", borderRadius: "4px", color: "#94a3b8"
            }}>{ind}</span>
          ))}
        </div>
      )}

      {/* XAI Toggle */}
      {hasXAI && (
        <button
          onClick={() => setShowXAI(!showXAI)}
          style={{
            marginTop: "10px", width: "100%", padding: "6px",
            background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)",
            borderRadius: "8px", color: "#94a3b8", cursor: "pointer",
            fontSize: "11px", display: "flex", alignItems: "center", justifyContent: "center", gap: "4px"
          }}
        >
          {showXAI ? "▼" : "▶"} {showXAI ? "Жасыру" : "Неге? (XAI)"}
        </button>
      )}

      {/* XAI Factor Bars */}
      {showXAI && explanation && (
        <div style={{ marginTop: "10px", background: "rgba(0,0,0,0.15)", borderRadius: "8px", padding: "10px" }}>
          {/* Risk factors */}
          {explanation.top_factors?.map((f, i) => (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "6px" }}>
              <span style={{ fontSize: "11px", color: "#e2e8f0", width: "130px", flexShrink: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {f.factor.replace(/_/g, " ")}
              </span>
              <div style={{ flex: 1, height: "12px", background: "rgba(239,68,68,0.1)", borderRadius: "6px", overflow: "hidden" }}>
                <div style={{
                  width: `${Math.min(f.impact, 100)}%`, height: "100%",
                  background: f.impact >= 30 ? "#ef4444" : f.impact >= 15 ? "#f59e0b" : "#3b82f6",
                  borderRadius: "6px", transition: "width 0.3s"
                }} />
              </div>
              <span style={{ fontSize: "10px", fontWeight: 700, color: f.impact >= 30 ? "#f87171" : "#fbbf24", width: "30px", textAlign: "right" }}>
                +{f.impact}
              </span>
            </div>
          ))}

          {/* Safe factors */}
          {explanation.safe_factors?.map((f, i) => (
            <div key={`s${i}`} style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
              <span style={{ fontSize: "11px", color: "#94a3b8", width: "130px", flexShrink: 0 }}>
                {f.factor.replace(/_/g, " ")}
              </span>
              <div style={{ flex: 1, height: "8px", background: "rgba(16,185,129,0.1)", borderRadius: "4px", overflow: "hidden" }}>
                <div style={{ width: `${Math.min(Math.abs(f.impact), 30)}%`, height: "100%", background: "#10b981", borderRadius: "4px" }} />
              </div>
              <span style={{ fontSize: "10px", color: "#34d399", width: "30px", textAlign: "right" }}>{f.impact}</span>
            </div>
          ))}

          {/* Counterfactual */}
          {explanation.counterfactual && (
            <div style={{ marginTop: "8px", padding: "6px 8px", background: "rgba(59,130,246,0.08)", borderRadius: "6px", border: "1px solid rgba(59,130,246,0.15)" }}>
              <span style={{ fontSize: "10px", color: "#93c5fd" }}>
                💡 {explanation.counterfactual}
              </span>
            </div>
          )}

          {/* Confidence */}
          {explanation.confidence && (
            <div style={{ marginTop: "6px", fontSize: "10px", color: "#64748b", textAlign: "right" }}>
              Confidence: {Math.round(explanation.confidence * 100)}% ({explanation.evidence_sources?.length || 0} sources)
            </div>
          )}
        </div>
      )}
    </div>
  );
}
