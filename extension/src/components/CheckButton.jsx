// клауд Елдоса N1 — Qalqan AI v3.0

export default function CheckButton({ loading, onClick, t }) {
  return (
    <button
      onClick={onClick}
      disabled={loading}
      style={{
        width: "100%",
        padding: "14px",
        background: loading
          ? "rgba(59,130,246,0.3)"
          : "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
        color: "white",
        border: "none",
        borderRadius: "12px",
        cursor: loading ? "not-allowed" : "pointer",
        fontWeight: 700,
        fontSize: "15px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "8px",
        transition: "all 0.2s",
        marginBottom: "12px"
      }}
    >
      {loading ? (
        <>
          <span style={{ animation: "spin 1s linear infinite", display: "inline-block" }}>⏳</span>
          {t("checking")}
        </>
      ) : (
        <>🛡️ {t("checkSite")}</>
      )}
    </button>
  );
}
