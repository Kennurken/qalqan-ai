// Qalqan AI v5.1 REDESIGN
import { useState } from "react";
import { C } from "../App";

const SendIcon = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
  </svg>
);
const AlertIcon = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
    <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
  </svg>
);

export default function AppealForm({ result, onSendAppeal, t }) {
  const [showForm, setShowForm] = useState(false);
  const [reason, setReason] = useState("");
  const [sent, setSent] = useState(false);

  const isDangerous = result?.verdict === "DANGEROUS" || result?.verdict === "ҚАУІПТІ";
  if (!isDangerous || sent) return null;

  const handleSend = async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    await onSendAppeal(tab?.url || "", reason);
    setSent(true);
    alert(t("appealSent"));
  };

  if (!showForm) return (
    <button onClick={() => setShowForm(true)} style={{
      width: "100%", padding: "9px", marginBottom: "8px",
      background: "transparent", color: C.muted,
      border: `1px solid ${C.border}`, borderRadius: "9px",
      cursor: "pointer", fontSize: "11px", fontFamily: C.sans,
      display: "flex", alignItems: "center", justifyContent: "center", gap: "6px",
      transition: "all 0.2s",
    }}
    onMouseEnter={e => { e.currentTarget.style.borderColor = "rgba(251,191,36,0.4)"; e.currentTarget.style.color = "#fbbf24"; }}
    onMouseLeave={e => { e.currentTarget.style.borderColor = C.border; e.currentTarget.style.color = C.muted; }}
    >
      <AlertIcon /> {t("appeal")}
    </button>
  );

  return (
    <div style={{
      marginBottom: "8px", borderRadius: "10px", padding: "12px",
      background: "rgba(251,191,36,0.04)",
      border: "1px solid rgba(251,191,36,0.2)",
      animation: "fadeUp 0.15s ease",
    }}>
      <div style={{ fontSize: "11px", color: "#fbbf24", marginBottom: "8px", fontFamily: C.sans }}>
        {t("appealReason")}
      </div>
      <textarea value={reason} onChange={e => setReason(e.target.value)}
        placeholder={t("appealReason")}
        style={{
          width: "100%", height: "60px",
          background: "rgba(8,12,22,0.8)", color: "#e2e8f0",
          border: "1px solid rgba(251,191,36,0.3)", borderRadius: "7px",
          padding: "8px 9px", resize: "none", fontSize: "12px",
          fontFamily: C.sans, outline: "none", lineHeight: 1.4,
          boxSizing: "border-box",
        }}
        onFocus={e => e.target.style.borderColor = "rgba(251,191,36,0.6)"}
        onBlur={e => e.target.style.borderColor = "rgba(251,191,36,0.3)"}
      />
      <button onClick={handleSend} disabled={!reason.trim()} style={{
        width: "100%", padding: "9px", marginTop: "8px",
        background: reason.trim() ? "rgba(22,163,74,0.8)" : "rgba(30,41,59,0.6)",
        color: reason.trim() ? "white" : C.muted,
        border: "none", borderRadius: "7px",
        cursor: reason.trim() ? "pointer" : "not-allowed",
        fontWeight: 700, fontSize: "12px", fontFamily: C.sans,
        display: "flex", alignItems: "center", justifyContent: "center", gap: "6px",
        transition: "all 0.2s",
      }}>
        <SendIcon /> {t("sendAppeal")}
      </button>
    </div>
  );
}
