// Qalqan AI — Goszakupki Fraud Check Panel
// Checks a tender number or BIN against the goszakup.gov.kz API

import { useState } from "react";
import { API_URL } from "../config";
import { PanelHeader } from "./StatsPanel";

const C = {
  bg:      "#020617",
  card:    "#0d162a",
  card2:   "#121e36",
  border:  "#1e293b",
  blue:    "#3b82f6",
  green:   "#10b981",
  red:     "#ef4444",
  amber:   "#f59e0b",
  white:   "#f8fafc",
  gray:    "#94a3b8",
  lgray:   "#cbd5e1",
};

const VERDICT_COLOR = { DANGEROUS: C.red, SUSPICIOUS: C.amber, SAFE: C.green, UNKNOWN: C.gray };
const VERDICT_ICON  = { DANGEROUS: "■ DANGEROUS", SUSPICIOUS: "▲ SUSPICIOUS", SAFE: "● SAFE", UNKNOWN: "? UNKNOWN" };

export default function GoszakupPanel({ t, onBack }) {
  const [input, setInput]       = useState("");
  const [loading, setLoading]   = useState(false);
  const [result, setResult]     = useState(null);
  const [error, setError]       = useState("");

  const isNumeric = (v) => /^\d+$/.test(v.trim());

  const runCheck = async () => {
    const val = input.trim();
    if (!val) return;
    setLoading(true);
    setResult(null);
    setError("");
    try {
      const endpoint = isNumeric(val)
        ? `${API_URL}/goszakup/check/${val}`
        : `${API_URL}/check?url=${encodeURIComponent(val)}&lang=ru`;

      const res = await fetch(endpoint, { method: "GET" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setResult(data);
    } catch (e) {
      setError(e.message || "Ошибка запроса");
    } finally {
      setLoading(false);
    }
  };

  const verdict = result?.verdict || "UNKNOWN";
  const vColor  = VERDICT_COLOR[verdict] || C.gray;
  const score   = result?.threat_score ?? 0;

  const scoreBarColor = score >= 50 ? C.red : score >= 20 ? C.amber : C.green;
  const scoreBarW     = `${Math.min(score, 100)}%`;

  return (
    <div style={{ padding: "10px 0" }}>
      <PanelHeader onBack={onBack} title="ГОСЗАКУПКИ FRAUD CHECK" />

      {/* Description */}
      <div style={{ background: C.card, border: `1px solid ${C.border}`, borderRadius: "6px",
                    padding: "8px 10px", marginBottom: "10px" }}>
        <div style={{ color: C.lgray, fontSize: "11px", lineHeight: "1.6" }}>
          Введите <b style={{ color: C.cyan }}>номер тендера</b> или <b style={{ color: C.amber }}>URL goszakup.gov.kz</b>
          {" "}для проверки на 10 признаков мошенничества: монополия, завышение цен, подставные компании и др.
        </div>
      </div>

      {/* Input */}
      <div style={{ display: "flex", gap: "6px", marginBottom: "8px" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && runCheck()}
          placeholder="Номер тендера или URL..."
          style={{
            flex: 1, background: C.card2, border: `1px solid ${C.border}`,
            color: C.white, borderRadius: "5px", padding: "7px 10px",
            fontSize: "12px", outline: "none",
          }}
        />
        <button
          onClick={runCheck}
          disabled={loading || !input.trim()}
          style={{
            background: C.green, color: C.bg, border: "none", borderRadius: "5px",
            padding: "7px 14px", fontSize: "12px", fontWeight: "bold",
            cursor: loading ? "wait" : "pointer", opacity: loading ? 0.7 : 1,
          }}
        >
          {loading ? "..." : "Проверить"}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div style={{ background: "#1a0a0a", border: `1px solid ${C.red}`, borderRadius: "5px",
                      padding: "6px 10px", color: C.red, fontSize: "11px", marginBottom: "8px" }}>
          ■ {error}
        </div>
      )}

      {/* Result */}
      {result && (
        <div style={{ background: C.card, border: `1px solid ${vColor}`, borderRadius: "6px",
                      overflow: "hidden" }}>
          {/* Verdict header */}
          <div style={{ background: `${vColor}22`, borderBottom: `1px solid ${vColor}`,
                        padding: "8px 12px", display: "flex", justifyContent: "space-between",
                        alignItems: "center" }}>
            <span style={{ color: vColor, fontWeight: "bold", fontSize: "13px" }}>
              {VERDICT_ICON[verdict]}
            </span>
            <span style={{ color: C.gray, fontSize: "11px" }}>
              Fraud score: <b style={{ color: vColor }}>{score}/100</b>
            </span>
          </div>

          {/* Score bar */}
          <div style={{ height: "3px", background: C.border }}>
            <div style={{ height: "100%", width: scoreBarW, background: scoreBarColor,
                          transition: "width 0.4s" }} />
          </div>

          <div style={{ padding: "10px 12px" }}>
            {/* Red flags */}
            {result.red_flags?.length > 0 && (
              <div style={{ marginBottom: "8px" }}>
                <div style={{ color: C.amber, fontSize: "11px", fontWeight: "bold",
                              marginBottom: "4px" }}>
                  RED FLAGS ({result.red_flags.length}):
                </div>
                {result.red_flags.map((flag, i) => (
                  <div key={i} style={{
                    display: "flex", alignItems: "flex-start", gap: "6px",
                    padding: "4px 0", borderBottom: `1px solid ${C.border}`,
                  }}>
                    <span style={{
                      color: flag.score >= 30 ? C.red : C.amber,
                      fontSize: "10px", fontWeight: "bold", minWidth: "28px",
                    }}>+{flag.score}</span>
                    <div>
                      <div style={{ color: C.lgray, fontSize: "11px" }}>{flag.ru}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* No flags */}
            {(!result.red_flags || result.red_flags.length === 0) && (
              <div style={{ color: C.green, fontSize: "11px", padding: "4px 0" }}>
                ● Аномалий не обнаружено — тендер выглядит чистым
              </div>
            )}

            {/* Source */}
            <div style={{ color: C.gray, fontSize: "10px", marginTop: "6px" }}>
              Источник: goszakup.gov.kz  ·  Qalqan AI v5.1
            </div>
          </div>
        </div>
      )}

      {/* Example hints */}
      {!result && !loading && (
        <div style={{ marginTop: "8px" }}>
          <div style={{ color: C.gray, fontSize: "10px", marginBottom: "4px" }}>Примеры:</div>
          {["123456789", "goszakup.gov.kz/ru/lot/view/id/12345"].map((ex, i) => (
            <div
              key={i}
              onClick={() => setInput(ex)}
              style={{ color: C.blue, fontSize: "10px", fontFamily: "monospace",
                       cursor: "pointer", padding: "2px 0",
                       textDecoration: "underline" }}
            >
              {ex}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
