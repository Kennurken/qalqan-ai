// Qalqan AI v5.1 REDESIGN
import { useState } from "react";
import { C } from "../App";

const ShieldScanIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    <line x1="12" y1="9" x2="12" y2="13" strokeWidth="2.5"/>
    <circle cx="12" cy="15.5" r="0.8" fill="currentColor" stroke="none"/>
  </svg>
);

const SpinnerIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"
    style={{ animation: "spin 0.8s linear infinite" }}>
    <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
  </svg>
);

export default function CheckButton({ loading, onClick, t }) {
  const [hover, setHover] = useState(false);

  return (
    <button
      onClick={onClick}
      disabled={loading}
      onMouseEnter={() => !loading && setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        width: "100%",
        padding: "13px 16px",
        marginBottom: "10px",
        position: "relative",
        overflow: "hidden",
        background: loading
          ? "rgba(0,212,255,0.06)"
          : hover
          ? "rgba(0,212,255,0.12)"
          : "rgba(0,212,255,0.07)",
        border: `1.5px solid ${loading ? "rgba(0,212,255,0.25)" : hover ? "#00d4ff" : "rgba(0,212,255,0.4)"}`,
        borderRadius: "10px",
        cursor: loading ? "not-allowed" : "pointer",
        color: loading ? "rgba(0,212,255,0.6)" : "#00d4ff",
        fontFamily: "'SF Mono','Fira Code','Consolas',monospace",
        fontWeight: 600,
        fontSize: "13px",
        letterSpacing: "1.5px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "9px",
        transition: "all 0.2s",
        boxShadow: hover && !loading
          ? "0 0 20px rgba(0,212,255,0.2), inset 0 0 20px rgba(0,212,255,0.04)"
          : "0 0 0 rgba(0,212,255,0)",
        textTransform: "uppercase",
      }}
    >
      {/* Scan sweep animation during loading */}
      {loading && (
        <div style={{
          position: "absolute", top: 0, left: "-100%", width: "60%", height: "100%",
          background: "linear-gradient(90deg, transparent, rgba(0,212,255,0.12), transparent)",
          animation: "scan 1.4s ease-in-out infinite",
          pointerEvents: "none",
        }} />
      )}

      {loading ? <SpinnerIcon /> : <ShieldScanIcon />}
      <span>{loading ? t("checking") : t("checkSite")}</span>

      {/* Corner accent */}
      {!loading && (
        <>
          <div style={{ position:"absolute",top:0,left:0,width:"8px",height:"8px",borderTop:`1.5px solid #00d4ff`,borderLeft:`1.5px solid #00d4ff`,borderRadius:"2px 0 0 0" }} />
          <div style={{ position:"absolute",top:0,right:0,width:"8px",height:"8px",borderTop:`1.5px solid #00d4ff`,borderRight:`1.5px solid #00d4ff`,borderRadius:"0 2px 0 0" }} />
          <div style={{ position:"absolute",bottom:0,left:0,width:"8px",height:"8px",borderBottom:`1.5px solid #00d4ff`,borderLeft:`1.5px solid #00d4ff`,borderRadius:"0 0 0 2px" }} />
          <div style={{ position:"absolute",bottom:0,right:0,width:"8px",height:"8px",borderBottom:`1.5px solid #00d4ff`,borderRight:`1.5px solid #00d4ff`,borderRadius:"0 0 2px 0" }} />
        </>
      )}
    </button>
  );
}
