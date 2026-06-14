// Qalqan AI v5.1 REDESIGN
import { useState } from "react";
import { API_URL } from "../config";
import { C } from "../App";

const FlagIcon = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/>
  </svg>
);
const SendIcon = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
  </svg>
);
const CheckIcon = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="20 6 9 17 4 12"/>
  </svg>
);

const TYPES = ["scam","phishing","pyramid","malware","gambling","fakeShop"];

export default function ReportButton({ t }) {
  const [show, setShow] = useState(false);
  const [type, setType] = useState("scam");
  const [note, setNote] = useState("");
  const [sent, setSent] = useState(false);

  const submit = async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    await fetch(`${API_URL}/report`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: tab?.url || "", threat_type: type, note }),
    });
    setSent(true);
    setTimeout(() => { setSent(false); setShow(false); }, 2500);
  };

  if (sent) return (
    <div style={{
      display: "flex", alignItems: "center", justifyContent: "center", gap: "6px",
      padding: "10px", color: "#22c55e", fontSize: "12px",
      background: "rgba(34,197,94,0.06)", borderRadius: "8px",
      border: "1px solid rgba(34,197,94,0.2)", marginTop: "8px",
    }}>
      <CheckIcon /> {t("reportSent")}
    </div>
  );

  if (!show) return (
    <button onClick={() => setShow(true)} style={{
      width: "100%", padding: "8px", marginTop: "8px",
      background: "transparent", color: C.muted,
      border: `1px dashed rgba(100,116,139,0.4)`, borderRadius: "8px",
      cursor: "pointer", fontSize: "11px", fontFamily: C.sans,
      display: "flex", alignItems: "center", justifyContent: "center", gap: "6px",
      transition: "all 0.2s",
    }}
    onMouseEnter={e => { e.currentTarget.style.borderColor = "rgba(255,59,92,0.4)"; e.currentTarget.style.color = "#ff8096"; }}
    onMouseLeave={e => { e.currentTarget.style.borderColor = "rgba(100,116,139,0.4)"; e.currentTarget.style.color = C.muted; }}
    >
      <FlagIcon /> {t("reportSite")}
    </button>
  );

  return (
    <div style={{
      marginTop: "8px", borderRadius: "10px", padding: "12px",
      background: "rgba(255,59,92,0.04)",
      border: "1px solid rgba(255,59,92,0.2)",
      animation: "fadeUp 0.15s ease",
    }}>
      <div style={{ display: "flex", gap: "4px", flexWrap: "wrap", marginBottom: "10px" }}>
        {TYPES.map(tp => (
          <button key={tp} onClick={() => setType(tp)} style={{
            padding: "4px 9px", borderRadius: "5px",
            fontSize: "10px", cursor: "pointer", fontFamily: C.sans,
            background: type === tp ? "rgba(255,59,92,0.15)" : "rgba(255,255,255,0.03)",
            border: `1px solid ${type === tp ? "rgba(255,59,92,0.5)" : C.border}`,
            color: type === tp ? "#ff8096" : C.muted,
            transition: "all 0.15s",
          }}>
            {t(tp)}
          </button>
        ))}
      </div>
      <textarea value={note} onChange={e => setNote(e.target.value)}
        placeholder={t("reportNote")}
        style={{
          width: "100%", height: "42px",
          background: "rgba(8,12,22,0.8)", color: "#e2e8f0",
          border: `1px solid ${C.border}`, borderRadius: "7px",
          padding: "7px 9px", fontSize: "12px", resize: "none",
          outline: "none", fontFamily: C.sans, lineHeight: 1.4,
          boxSizing: "border-box",
          transition: "border-color 0.2s",
        }}
        onFocus={e => e.target.style.borderColor = "rgba(255,59,92,0.4)"}
        onBlur={e => e.target.style.borderColor = C.border}
      />
      <button onClick={submit} style={{
        width: "100%", padding: "9px", marginTop: "8px",
        background: "rgba(220,38,38,0.8)", color: "white",
        border: "none", borderRadius: "7px", cursor: "pointer",
        fontWeight: 700, fontSize: "12px", fontFamily: C.sans,
        display: "flex", alignItems: "center", justifyContent: "center", gap: "6px",
        transition: "all 0.2s",
      }}
      onMouseEnter={e => e.currentTarget.style.background = "rgba(220,38,38,0.95)"}
      onMouseLeave={e => e.currentTarget.style.background = "rgba(220,38,38,0.8)"}
      >
        <SendIcon /> {t("submit")}
      </button>
    </div>
  );
}
