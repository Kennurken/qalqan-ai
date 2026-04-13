// клауд Елдоса N1 — Qalqan AI v3.0

export default function ScreenshotCheck({ onCheck, loading, t }) {
  return (
    <button
      onClick={onCheck}
      disabled={loading}
      style={{
        width: "100%", padding: "10px",
        background: "#1e293b", color: "#94a3b8",
        border: "1px solid #334155", borderRadius: "10px",
        cursor: loading ? "not-allowed" : "pointer",
        fontSize: "13px", marginBottom: "12px",
        display: "flex", alignItems: "center", gap: "6px", justifyContent: "center"
      }}
    >
      📸 {t("analyzeScreen")}
    </button>
  );
}
