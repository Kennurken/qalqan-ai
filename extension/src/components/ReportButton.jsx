// клауд Елдоса N1 — Qalqan AI v5.0
// Report suspicious site button

import { useState } from "react";
import { API_URL } from "../config";

export default function ReportButton({ t }) {
  const [show, setShow] = useState(false);
  const [type, setType] = useState("scam");
  const [note, setNote] = useState("");
  const [sent, setSent] = useState(false);

  const types = [
    { id: "scam", label: t("scam") },
    { id: "phishing", label: t("phishing") },
    { id: "pyramid", label: t("pyramid") },
    { id: "malware", label: t("malware") },
    { id: "gambling", label: t("gambling") },
    { id: "fakeShop", label: t("fakeShop") },
  ];

  const submit = async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    await fetch(`${API_URL}/report`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: tab?.url || "", threat_type: type, note })
    });
    setSent(true);
    setTimeout(() => { setSent(false); setShow(false); }, 2000);
  };

  if (sent) return (
    <div style={{ textAlign: "center", padding: "8px", color: "#34d399", fontSize: "13px" }}>
      ✅ {t("reportSite")} — sent!
    </div>
  );

  if (!show) return (
    <button onClick={() => setShow(true)} style={{
      width: "100%", padding: "8px", marginTop: "8px",
      background: "transparent", color: "#64748b",
      border: "1px dashed #334155", borderRadius: "8px",
      cursor: "pointer", fontSize: "11px"
    }}>
      🚨 {t("reportSite")}
    </button>
  );

  return (
    <div style={{ marginTop: "8px", background: "#1e293b", borderRadius: "10px", padding: "10px", border: "1px solid #334155" }}>
      <div style={{ display: "flex", gap: "4px", flexWrap: "wrap", marginBottom: "8px" }}>
        {types.map(tp => (
          <button key={tp.id} onClick={() => setType(tp.id)} style={{
            padding: "4px 8px", borderRadius: "6px", fontSize: "11px", cursor: "pointer",
            background: type === tp.id ? "rgba(239,68,68,0.2)" : "transparent",
            border: type === tp.id ? "1px solid #ef4444" : "1px solid #334155",
            color: type === tp.id ? "#f87171" : "#94a3b8"
          }}>{tp.label}</button>
        ))}
      </div>
      <textarea value={note} onChange={e => setNote(e.target.value)}
        placeholder="Ескерту (optional)..."
        style={{ width: "100%", height: "40px", background: "#0f172a", color: "#f1f5f9",
          border: "1px solid #334155", borderRadius: "6px", padding: "6px",
          fontSize: "12px", resize: "none", outline: "none", fontFamily: "inherit" }}
      />
      <button onClick={submit} style={{
        width: "100%", padding: "8px", marginTop: "6px",
        background: "#dc2626", color: "white", border: "none",
        borderRadius: "6px", cursor: "pointer", fontWeight: 700, fontSize: "12px"
      }}>🚨 Report</button>
    </div>
  );
}
