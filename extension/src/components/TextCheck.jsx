// Qalqan AI v3.0

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
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
        <span style={{ fontSize: "10px", color: text.length > 8000 ? "#f87171" : "#64748b" }}>
          {text.length}/10000
        </span>
        <button onClick={() => { setExpanded(false); setText(""); }}
          style={{ background: "transparent", border: "none", color: "#64748b", cursor: "pointer", fontSize: "13px", padding: "0 4px" }}>
          ✕
        </button>
      </div>
      <button
        onClick={() => { if (text.trim()) onCheck(text.trim()); }}
        disabled={loading || !text.trim()}
        style={{
          width: "100%", padding: "8px",
          background: text.trim() ? "#6366f1" : "#334155",
          color: "white", border: "none", borderRadius: "8px",
          cursor: text.trim() ? "pointer" : "not-allowed",
          fontWeight: 600, fontSize: "12px"
        }}
      >
        {loading ? "⏳" : "⚡"} {t("analyzeText")}
      </button>
    </div>
  );
}
