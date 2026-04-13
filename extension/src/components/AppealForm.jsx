// клауд Елдоса N1 — Qalqan AI v3.0

import { useState } from "react";

export default function AppealForm({ result, onSendAppeal, t }) {
  const [showForm, setShowForm] = useState(false);
  const [reason, setReason] = useState("");
  const [sent, setSent] = useState(false);

  const isDangerous = result?.verdict === "DANGEROUS" || result?.verdict === "ҚАУІПТІ";
  if (!isDangerous || sent) return null;

  if (!showForm) {
    return (
      <button
        onClick={() => setShowForm(true)}
        style={{
          width: "100%", padding: "10px",
          background: "transparent", color: "#64748b",
          border: "1px solid #334155", borderRadius: "10px",
          cursor: "pointer", fontSize: "12px"
        }}
      >
        ⚠️ {t("appeal")}
      </button>
    );
  }

  const handleSend = async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    await onSendAppeal(tab?.url || "", reason);
    setSent(true);
    alert(t("appealSent"));
  };

  return (
    <div style={{
      background: "#1e293b", borderRadius: "12px",
      padding: "12px", border: "1px solid #334155"
    }}>
      <textarea
        value={reason}
        onChange={(e) => setReason(e.target.value)}
        placeholder={t("appealReason")}
        style={{
          width: "100%", height: "60px",
          background: "#0f172a", color: "#f1f5f9",
          border: "1px solid #3b82f6", borderRadius: "8px",
          padding: "8px", resize: "none", fontSize: "13px",
          fontFamily: "inherit", outline: "none"
        }}
      />
      <button
        onClick={handleSend}
        disabled={!reason.trim()}
        style={{
          width: "100%", padding: "10px", marginTop: "8px",
          background: reason.trim() ? "#16a34a" : "#334155",
          color: "white", border: "none", borderRadius: "8px",
          cursor: reason.trim() ? "pointer" : "not-allowed",
          fontWeight: 700, fontSize: "13px"
        }}
      >
        📨 {t("sendAppeal")}
      </button>
    </div>
  );
}
