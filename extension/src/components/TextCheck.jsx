// клауд Елдоса N1 — Qalqan AI v3.0

import { useState } from "react";

export default function TextCheck({ onCheck, loading, t }) {
  const [text, setText] = useState("");
  const [expanded, setExpanded] = useState(false);

  if (!expanded) {
    return (
      <button
        onClick={() => setExpanded(true)}
        style={{
          width: "100%", padding: "10px",
          background: "#1e293b", color: "#94a3b8",
          border: "1px solid #334155", borderRadius: "10px",
          cursor: "pointer", fontSize: "13px", marginBottom: "8px",
          display: "flex", alignItems: "center", gap: "6px", justifyContent: "center"
        }}
      >
        ⚡ {t("analyzeText")}
      </button>
    );
  }

  return (
    <div style={{
      background: "#1e293b", borderRadius: "12px",
      padding: "12px", marginBottom: "12px",
      border: "1px solid #334155"
    }}>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={t("pasteText")}
        style={{
          width: "100%", height: "80px",
          background: "transparent", color: "#f1f5f9",
          border: "none", outline: "none", resize: "none",
          fontSize: "13px", fontFamily: "inherit"
        }}
      />
      <div style={{ display: "flex", gap: "8px" }}>
        <button
          onClick={() => { if (text.trim()) onCheck(text.trim()); }}
          disabled={loading || !text.trim()}
          style={{
            flex: 1, padding: "8px",
            background: text.trim() ? "#6366f1" : "#334155",
            color: "white", border: "none", borderRadius: "8px",
            cursor: text.trim() ? "pointer" : "not-allowed",
            fontWeight: 600, fontSize: "12px"
          }}
        >
          {loading ? "⏳" : "⚡"} {t("analyzeText")}
        </button>
        <button
          onClick={() => { setExpanded(false); setText(""); }}
          style={{
            padding: "8px 12px", background: "transparent",
            color: "#64748b", border: "1px solid #334155",
            borderRadius: "8px", cursor: "pointer", fontSize: "12px"
          }}
        >
          ✕
        </button>
      </div>
    </div>
  );
}
