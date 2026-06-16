// Qalqan AI v5.1 REDESIGN
import { useState } from "react";
import { C } from "../App";

const CopyIcon = () => (
  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
  </svg>
);
const CheckIcon = () => (
  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="20 6 9 17 4 12"/>
  </svg>
);
const ChevronIcon = ({ open }) => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"
    style={{ transform: open ? "rotate(180deg)" : "rotate(0deg)", transition: "transform 0.2s" }}>
    <polyline points="6 9 12 15 18 9"/>
  </svg>
);
const LockIcon = ({ status }) => {
  const open = ["expired","no_ssl"].includes(status);
  return open
    ? <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>
    : <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>;
};
const CalendarIcon = () => (
  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
  </svg>
);
const InfoIcon = () => (
  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>
  </svg>
);
const BoltIcon = () => (
  <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor" stroke="none">
    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
  </svg>
);
const ScanIcon = () => (
  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
  </svg>
);

const SOURCE_NAMES = {
  phishtank: "PhishTank", google_safe_browsing: "Google Safe Browsing",
  urlhaus: "URLhaus", openphish: "OpenPhish", virustotal: "VirusTotal",
  pyramid_list: "Pyramid DB", gambling_list: "Gambling DB",
  kz_intel_gambling: "KZ Gambling DB", phishing_list: "Phishing DB",
  local_blacklist: "Blacklist", domain_intel: "Domain Intel",
  groq_ai: "AI · llama-70b", gemini_ai: "AI · Gemini",
  groq_vision: "Vision AI", gemini_vision: "Vision AI",
  kz_intel: "KZ Intelligence", user_whitelist: "Your Whitelist",
  whitelist: "Trusted List", url_features: "URL Analysis",
  offline_pyramid: "Offline DB · Pyramid", offline_gambling: "Offline DB · Gambling",
  offline_casebattle: "Offline DB · Case Battle", offline_phishing: "Offline DB · Phishing",
  offline_scam: "Offline DB · Scam", offline_tld: "TLD Check",
  offline_whitelist: "Offline · Trusted", quick_check: "Quick Check",
  kz_impersonation: "KZ Brand Protection", demo_cache: "Demo Mode",
  no_data: "—", ai_error: "AI Error",
};

const THREAT_TYPE_LABELS = {
  phishing: "Phishing", malware: "Malware", pyramid: "Pyramid Scheme",
  scam: "Scam", gambling: "Gambling", casino: "Casino",
  fake_shop: "Fake Shop", social_engineering: "Social Eng.",
  suspicious_infrastructure: "Suspicious Infra",
};

export default function ResultCard({ result, t, lang = "kk" }) {
  const [showXAI, setShowXAI] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!result) return null;

  const detail = result[`detail_${lang}`] || result.detail_kk || result.detail || "—";

  const isDangerous = result.verdict === "DANGEROUS" || result.verdict === "ҚАУІПТІ";
  const isSuspicious = result.verdict === "SUSPICIOUS" || (!isDangerous && result.threat_score >= 40);
  const isSafe = !isDangerous && !isSuspicious;

  const col     = isDangerous ? "#ff3b5c" : isSuspicious ? "#fbbf24" : "#22c55e";
  const colDim  = isDangerous ? "rgba(255,59,92,0.12)" : isSuspicious ? "rgba(251,191,36,0.10)" : "rgba(34,197,94,0.10)";
  const colBorder = isDangerous ? "rgba(255,59,92,0.35)" : isSuspicious ? "rgba(251,191,36,0.35)" : "rgba(34,197,94,0.3)";
  const verdictLabel = isDangerous ? t("dangerous") : isSuspicious ? t("suspicious") : t("safe");

  const explanation = result.explanation;
  const aiExplanation = explanation?.counterfactual || null;
  const hasXAI = !!aiExplanation;

  const copyResult = () => {
    const text = [
      `QALQAN AI`,
      `${result.verdict} — ${result.threat_score}/100`,
      result.threat_type && result.threat_type !== "safe" ? `Type: ${result.threat_type}` : "",
      detail,
      `Source: ${SOURCE_NAMES[result.source] || result.source}`,
      explanation?.counterfactual ? `\n${explanation.counterfactual}` : "",
    ].filter(Boolean).join("\n");
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div style={{
      borderRadius: "12px",
      border: `1px solid ${colBorder}`,
      background: colDim,
      padding: "14px",
      marginBottom: "10px",
      position: "relative",
      overflow: "hidden",
      animation: isDangerous ? "pulse-danger 2.5s ease-in-out infinite" : undefined,
    }}>
      {/* Left accent bar */}
      <div style={{
        position: "absolute", left: 0, top: 0, bottom: 0, width: "3px",
        background: col,
        borderRadius: "12px 0 0 12px",
        boxShadow: `0 0 12px ${col}60`,
      }} />

      <div style={{ paddingLeft: "4px" }}>
        {/* Verdict row */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "10px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            {/* Score badge */}
            <div style={{
              fontFamily: C.mono,
              fontSize: "26px",
              fontWeight: 700,
              color: col,
              lineHeight: 1,
              textShadow: `0 0 20px ${col}80`,
            }}>
              {result.threat_score}
              <span style={{ fontSize: "12px", color: col + "80", fontWeight: 500 }}>/100</span>
            </div>
            {/* Verdict label */}
            <div>
              <div style={{
                fontSize: "13px", fontWeight: 700,
                color: col, letterSpacing: "0.5px",
                textTransform: "uppercase",
              }}>
                {verdictLabel}
              </div>
              {result.risk_level && result.risk_level !== "low" && (
                <div style={{
                  fontSize: "9px", fontWeight: 600, letterSpacing: "0.8px",
                  color: col, opacity: 0.7, textTransform: "uppercase",
                }}>
                  {result.risk_level} risk
                </div>
              )}
            </div>
          </div>

          {/* Action buttons top-right */}
          <div style={{ display: "flex", gap: "4px" }}>
            {result.ai_skipped && (
              <span title="AI offline — heuristics only" style={{
                display: "flex", alignItems: "center", gap: "3px",
                fontSize: "9px", color: "#fbbf24",
                background: "rgba(251,191,36,0.1)", border: "1px solid rgba(251,191,36,0.25)",
                padding: "2px 6px", borderRadius: "4px", letterSpacing: "0.3px",
              }}>
                <BoltIcon /> AI offline
              </span>
            )}
            <button onClick={copyResult} title={t("copyResult")} style={{
              display: "flex", alignItems: "center", gap: "4px",
              padding: "4px 8px", borderRadius: "6px", cursor: "pointer",
              background: copied ? "rgba(34,197,94,0.12)" : "rgba(255,255,255,0.04)",
              border: copied ? "1px solid rgba(34,197,94,0.35)" : `1px solid ${C.border}`,
              color: copied ? "#22c55e" : C.muted, fontSize: "10px",
              transition: "all 0.2s", fontFamily: C.sans,
            }}>
              {copied ? <CheckIcon /> : <CopyIcon />}
              {copied ? t("copied") : t("copyResult")}
            </button>
          </div>
        </div>

        {/* Detail text */}
        <p style={{
          fontSize: "12.5px", color: "#cbd5e1", lineHeight: 1.55,
          margin: "0 0 10px", fontFamily: C.sans,
        }}>
          {detail}
        </p>

        {/* Meta chips row */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: "5px", marginBottom: "8px" }}>
          {result.threat_type && result.threat_type !== "safe" && (
            <MetaChip color={col}>
              {THREAT_TYPE_LABELS[result.threat_type] || result.threat_type}
            </MetaChip>
          )}
          <MetaChip icon={<ScanIcon />}>
            {SOURCE_NAMES[result.source] || result.source}
          </MetaChip>
          {result.cached && (
            <MetaChip icon={<BoltIcon />} color="#00d4ff">cached</MetaChip>
          )}
          {result.metadata?.processing_time_ms && (
            <MetaChip>{result.metadata.processing_time_ms}ms</MetaChip>
          )}
        </div>

        {/* Domain intel row */}
        {result.domain_details && (
          <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "8px" }}>
            {result.domain_details.domain_age_days !== undefined && (() => {
              const age = result.domain_details.domain_age_days;
              const c = age < 30 ? "#ff3b5c" : age < 90 ? "#fbbf24" : C.muted;
              return (
                <div style={{ display:"flex",alignItems:"center",gap:"4px",fontSize:"11px",color:c }}>
                  <CalendarIcon /> {age}d old
                </div>
              );
            })()}
            {(() => {
              const ssl = result.domain_details.ssl;
              if (!ssl) return null;
              const sslCols = { valid:"#22c55e", expired:"#ff3b5c", self_signed:"#fbbf24", no_ssl:"#ff3b5c", expiring_soon:"#fbbf24" };
              const c = sslCols[ssl.status] || C.muted;
              let label = `SSL: ${ssl.status.replace(/_/g," ")}`;
              if (ssl.days_left && ssl.status === "valid") label += ` · ${ssl.days_left}d`;
              if (ssl.issuer && ssl.issuer !== "Unknown") label += ` · ${ssl.issuer.slice(0,18)}`;
              return (
                <div style={{ display:"flex",alignItems:"center",gap:"4px",fontSize:"11px",color:c }}>
                  <LockIcon status={ssl.status} /> {label}
                </div>
              );
            })()}
          </div>
        )}

        {/* Indicators */}
        {result.indicators?.length > 0 && (
          <div style={{ display: "flex", gap: "4px", flexWrap: "wrap", marginBottom: "8px" }}>
            {result.indicators.slice(0, 5).map((ind, i) => (
              <span key={i} style={{
                fontSize: "9.5px", fontFamily: C.mono,
                background: "rgba(255,255,255,0.05)",
                border: `1px solid ${C.border}`,
                padding: "2px 6px", borderRadius: "4px", color: "#94a3b8",
                letterSpacing: "0.3px",
              }}>
                {ind}
              </span>
            ))}
          </div>
        )}

        {/* XAI toggle */}
        {hasXAI && (
          <button onClick={() => setShowXAI(!showXAI)} style={{
            width: "100%", padding: "7px",
            background: showXAI ? "rgba(0,212,255,0.06)" : "rgba(255,255,255,0.03)",
            border: `1px solid ${showXAI ? "rgba(0,212,255,0.25)" : C.border}`,
            borderRadius: "7px", color: showXAI ? "#00d4ff" : C.muted,
            cursor: "pointer", fontSize: "11px", fontFamily: C.sans,
            display: "flex", alignItems: "center", justifyContent: "center", gap: "5px",
            transition: "all 0.2s", letterSpacing: "0.3px",
          }}>
            <InfoIcon /> {showXAI ? t("xaiHide") : t("xaiTitle")}
            <span style={{ marginLeft: "auto" }}><ChevronIcon open={showXAI} /></span>
          </button>
        )}

        {/* AI explanation */}
        {showXAI && aiExplanation && (
          <div style={{
            marginTop: "8px", padding: "10px 12px",
            background: "rgba(0,0,0,0.25)",
            borderRadius: "8px",
            border: `1px solid ${C.border}`,
            animation: "fadeUp 0.15s ease",
          }}>
            <span style={{ fontSize: "12px", color: "#94a3b8", lineHeight: 1.65 }}>
              {aiExplanation}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}

function MetaChip({ children, icon, color }) {
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: "3px",
      fontSize: "10px", fontFamily: C.sans,
      color: color || C.muted,
      background: color ? `${color}12` : "rgba(255,255,255,0.04)",
      border: `1px solid ${color ? `${color}25` : C.border}`,
      padding: "2px 7px", borderRadius: "4px",
      letterSpacing: "0.2px",
    }}>
      {icon}{children}
    </span>
  );
}

function FactorBar({ label, value, type }) {
  const isRisk = type === "risk";
  const barColor = isRisk
    ? value >= 30 ? "#ff3b5c" : value >= 15 ? "#fbbf24" : "#3b82f6"
    : "#22c55e";
  const barBg = isRisk ? "rgba(255,59,92,0.08)" : "rgba(34,197,94,0.08)";
  const maxValue = isRisk ? 100 : 30;

  return (
    <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "5px" }}>
      <span style={{
        fontSize: "10.5px", color: isRisk ? "#e2e8f0" : "#94a3b8",
        width: "120px", flexShrink: 0,
        overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
        fontFamily: C.sans,
      }}>
        {label}
      </span>
      <div style={{
        flex: 1, height: isRisk ? "6px" : "4px",
        background: barBg, borderRadius: "3px", overflow: "hidden",
      }}>
        <div style={{
          width: `${Math.min((value / maxValue) * 100, 100)}%`,
          height: "100%", background: barColor, borderRadius: "3px",
          boxShadow: `0 0 6px ${barColor}80`,
          transition: "width 0.4s ease",
        }} />
      </div>
      <span style={{
        fontSize: "10px", fontFamily: C.mono, fontWeight: 600,
        color: isRisk ? (value >= 30 ? "#ff3b5c" : "#fbbf24") : "#22c55e",
        width: "28px", textAlign: "right",
      }}>
        {isRisk ? `+${value}` : `-${value}`}
      </span>
    </div>
  );
}
