// клауд Елдоса N1 — Qalqan AI v3.0

export default function ResultCard({ result, t }) {
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
    phishtank: "PhishTank",
    google_safe_browsing: "Google Safe Browsing",
    urlhaus: "URLhaus",
    openphish: "OpenPhish",
    pyramid_list: "Qalqan Pyramid DB",
    local_blacklist: "Local Blacklist",
    ai: "Qalqan AI",
    ai_vision: "Qalqan AI Vision",
    whitelist: "Trusted List",
    no_data: "—"
  };

  return (
    <div style={{
      background: bgColor,
      borderLeft: `4px solid ${borderColor}`,
      borderRadius: "12px",
      padding: "14px",
      marginBottom: "12px"
    }}>
      {/* Вердикт + балл */}
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

      {/* Себебі */}
      <p style={{ fontSize: "13px", color: "#cbd5e1", lineHeight: 1.5, margin: "0 0 8px" }}>
        {result.detail || result.detail_kk || "—"}
      </p>

      {/* Мета-ақпарат */}
      <div style={{ fontSize: "11px", color: "#64748b", display: "flex", gap: "12px", flexWrap: "wrap" }}>
        {result.threat_type && result.threat_type !== "safe" && (
          <span>🏷 {result.threat_type}</span>
        )}
        <span>🔍 {sourceNames[result.source] || result.source}</span>
        {result.cached && <span>⚡ cached</span>}
      </div>

      {/* Индикаторлар */}
      {result.indicators && result.indicators.length > 0 && (
        <div style={{ marginTop: "8px", display: "flex", gap: "4px", flexWrap: "wrap" }}>
          {result.indicators.slice(0, 5).map((ind, i) => (
            <span key={i} style={{
              fontSize: "10px", background: "rgba(255,255,255,0.06)",
              padding: "2px 6px", borderRadius: "4px", color: "#94a3b8"
            }}>
              {ind}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
