import { motion, AnimatePresence, useInView } from "framer-motion";
import { useRef, useState, useEffect } from "react";

const demos = [
  {
    url: "kaspi-login.tk",
    verdict: "DANGEROUS",
    score: 97,
    type: "Фишинг — KZ Impersonation",
    source: "kz_intel",
    reason: "Kaspi Bank жалған клоны. Сайт kaspi.kz-ті имитациялайды. Тіркелу деректерін ұрлауға арналған.",
    indicators: ["kz_impersonation_kaspi", "free_tld_.tk", "domain_age_3d", "no_ssl"],
    color: "#ef4444",
    emoji: "⛔",
    tiers: ["offline_db", "kz_intel"],
  },
  {
    url: "100k-ay-investiciya.ru",
    verdict: "DANGEROUS",
    score: 95,
    type: "Қаржылық пирамида",
    source: "pyramid_list",
    reason: "Қазақстандық пирамида тізімінде анықталды. 100 000 ₸ айлық кіреберіс — алаяқтық белгісі.",
    indicators: ["pyramid_scheme_kz", "unrealistic_returns", "social_engineering"],
    color: "#ef4444",
    emoji: "⛔",
    tiers: ["offline_db", "pyramid_db"],
  },
  {
    url: "google.com",
    verdict: "SAFE",
    score: 2,
    type: "Қауіпсіз",
    source: "whitelist",
    reason: "Сенімді сайт. Ешбір қауіп белгісі жоқ. Барлық дерекқорларда таза.",
    indicators: [],
    color: "#10b981",
    emoji: "✅",
    tiers: ["whitelist"],
  },
  {
    url: "login-egov-kz.net",
    verdict: "DANGEROUS",
    score: 97,
    type: "Мемлекеттік портал жалғаны",
    source: "kz_intel",
    reason: "eGov.kz порталын имитациялайды. .net доменінде мемлекеттік сайт болмайды.",
    indicators: ["kz_impersonation_egov", "wrong_tld_gov", "domain_age_7d"],
    color: "#ef4444",
    emoji: "⛔",
    tiers: ["kz_intel", "domain_intel"],
  },
];

const TIER_LABELS = {
  whitelist: { label: "Whitelist", color: "#10b981" },
  offline_db: { label: "Offline DB", color: "#3b82f6" },
  pyramid_db: { label: "Pyramid DB", color: "#f59e0b" },
  kz_intel: { label: "KZ Intel", color: "#a78bfa" },
  domain_intel: { label: "Domain Intel", color: "#6366f1" },
};

// Score ring
function ScoreRing({ score, color }) {
  const r = 30;
  const circ = 2 * Math.PI * r;
  const dash = (score / 100) * circ;

  return (
    <div style={{ position: "relative", width: 80, height: 80 }}>
      <svg width="80" height="80" style={{ transform: "rotate(-90deg)" }}>
        <circle cx="40" cy="40" r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="5" />
        <motion.circle
          cx="40" cy="40" r={r}
          fill="none" stroke={color} strokeWidth="5"
          strokeLinecap="round"
          strokeDasharray={`${circ}`}
          initial={{ strokeDashoffset: circ }}
          animate={{ strokeDashoffset: circ - dash }}
          transition={{ duration: 1, delay: 0.2, ease: "easeOut" }}
        />
      </svg>
      <div style={{
        position: "absolute", inset: 0,
        display: "flex", flexDirection: "column",
        alignItems: "center", justifyContent: "center",
      }}>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          style={{ fontSize: 18, fontWeight: 900, color, lineHeight: 1 }}
        >
          {score}
        </motion.div>
        <div style={{ fontSize: 9, color: "#64748b" }}>/100</div>
      </div>
    </div>
  );
}

// Scan animation
function ScanEffect({ active }) {
  return (
    <AnimatePresence>
      {active && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          style={{ position: "absolute", inset: 0, pointerEvents: "none", borderRadius: 16, overflow: "hidden" }}
        >
          <motion.div
            initial={{ top: 0 }}
            animate={{ top: "100%" }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.7, ease: "linear" }}
            style={{
              position: "absolute", left: 0, right: 0, height: 2,
              background: "linear-gradient(90deg, transparent, #6366f1, #a78bfa, #6366f1, transparent)",
              boxShadow: "0 0 20px rgba(99,102,241,0.8)",
            }}
          />
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default function DemoSection() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });
  const [active, setActive] = useState(0);
  const [scanning, setScanning] = useState(false);

  const d = demos[active];

  const handleSelect = (i) => {
    if (i === active) return;
    setScanning(true);
    setTimeout(() => {
      setActive(i);
      setScanning(false);
    }, 700);
  };

  return (
    <section id="demo" style={{
      padding: "100px 24px",
      background: "linear-gradient(180deg, transparent, rgba(15,23,42,0.6), transparent)",
    }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        {/* Title */}
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7 }}
          style={{ textAlign: "center", marginBottom: 56 }}
        >
          <div style={{
            display: "inline-flex", alignItems: "center", gap: 8,
            padding: "5px 16px", borderRadius: 20,
            background: "rgba(99,102,241,0.08)", border: "1px solid rgba(99,102,241,0.25)",
            fontSize: 11, color: "#a5b4fc", marginBottom: 20,
            letterSpacing: "0.15em", fontWeight: 700,
          }}>
            ДЕМО
          </div>
          <h2 style={{ fontSize: "clamp(28px,4vw,48px)", fontWeight: 900, lineHeight: 1.1, marginBottom: 16 }}>
            Нәтиже{" "}
            <span style={{
              background: "linear-gradient(135deg, #3b82f6, #6366f1, #a78bfa)",
              WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
            }}>
              осылай көрінеді
            </span>
          </h2>
          <p style={{ fontSize: 16, color: "#94a3b8", maxWidth: 440, margin: "0 auto" }}>
            Нақты мысалдарды таңдаңыз — жүйе қалай жұмыс істейтінін көріңіз
          </p>
        </motion.div>

        <div style={{
          display: "grid", gridTemplateColumns: "1fr 1.4fr",
          gap: 28, alignItems: "start",
        }}>
          {/* URL selector */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div style={{
              background: "rgba(15,23,42,0.85)",
              border: "1px solid rgba(255,255,255,0.07)",
              borderRadius: 16, overflow: "hidden",
              backdropFilter: "blur(16px)",
            }}>
              {/* Browser chrome */}
              <div style={{
                padding: "10px 16px",
                background: "rgba(30,41,59,0.6)",
                borderBottom: "1px solid rgba(255,255,255,0.06)",
                display: "flex", alignItems: "center", gap: 8,
              }}>
                <div style={{ display: "flex", gap: 5 }}>
                  {["#ef4444", "#f59e0b", "#10b981"].map((c, i) => (
                    <div key={i} style={{ width: 10, height: 10, borderRadius: "50%", background: c, opacity: 0.7 }} />
                  ))}
                </div>
                <div style={{
                  flex: 1, background: "rgba(255,255,255,0.04)", borderRadius: 6,
                  padding: "4px 10px", fontSize: 11, color: "#475569",
                  border: "1px solid rgba(255,255,255,0.05)",
                }}>
                  qalqan-ai.vercel.app/check
                </div>
              </div>

              {/* URL list */}
              <div style={{ padding: "8px 0" }}>
                {demos.map((item, i) => (
                  <motion.div
                    key={i}
                    onClick={() => handleSelect(i)}
                    whileHover={{ backgroundColor: "rgba(99,102,241,0.07)" }}
                    style={{
                      padding: "12px 16px",
                      cursor: "pointer",
                      background: active === i ? "rgba(99,102,241,0.1)" : "transparent",
                      borderLeft: active === i ? "3px solid #6366f1" : "3px solid transparent",
                      borderBottom: i < demos.length - 1 ? "1px solid rgba(51,65,85,0.3)" : "none",
                      transition: "background 0.15s, border-color 0.15s",
                      display: "flex", alignItems: "center", gap: 10,
                    }}
                  >
                    <span style={{ fontSize: 14 }}>{item.emoji}</span>
                    <span style={{
                      fontSize: 12, fontFamily: "monospace",
                      color: active === i ? "#e2e8f0" : "#64748b",
                      transition: "color 0.2s",
                      flex: 1,
                    }}>
                      {item.url}
                    </span>
                    <span style={{
                      fontSize: 9, padding: "2px 7px", borderRadius: 10,
                      background: `${item.color}20`, color: item.color, fontWeight: 800,
                      letterSpacing: "0.05em",
                    }}>
                      {item.verdict}
                    </span>
                  </motion.div>
                ))}
              </div>

              {/* Tier pipeline legend */}
              <div style={{
                padding: "12px 16px",
                borderTop: "1px solid rgba(255,255,255,0.05)",
                background: "rgba(15,23,42,0.4)",
              }}>
                <div style={{ fontSize: 9, color: "#475569", letterSpacing: "0.15em", marginBottom: 8 }}>
                  АНЫҚТАУ ДЕҢГЕЙЛЕРІ
                </div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
                  {Object.entries(TIER_LABELS).map(([key, val]) => (
                    <span key={key} style={{
                      fontSize: 9, padding: "2px 7px", borderRadius: 8,
                      background: `${val.color}15`, color: val.color,
                      border: `1px solid ${val.color}25`, fontWeight: 600,
                      opacity: d.tiers.includes(key) ? 1 : 0.3,
                      transition: "opacity 0.3s",
                    }}>
                      {val.label}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>

          {/* Result panel */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.3 }}
            style={{ position: "relative" }}
          >
            <AnimatePresence mode="wait">
              <motion.div
                key={active}
                initial={{ opacity: 0, y: 12, scale: 0.98 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -8, scale: 0.98 }}
                transition={{ duration: 0.35, ease: [0.21, 0.47, 0.32, 0.98] }}
                style={{
                  background: "rgba(15,23,42,0.9)",
                  border: `1px solid ${d.color}30`,
                  borderRadius: 16, overflow: "hidden",
                  backdropFilter: "blur(16px)",
                  position: "relative",
                  boxShadow: `0 8px 40px ${d.color}15`,
                }}
              >
                <ScanEffect active={scanning} />

                {/* Header */}
                <div style={{
                  padding: "18px 22px",
                  background: `${d.color}10`,
                  borderBottom: `1px solid ${d.color}20`,
                  display: "flex", alignItems: "center", gap: 14,
                }}>
                  <motion.span
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", stiffness: 400 }}
                    style={{ fontSize: 28 }}
                  >
                    {d.emoji}
                  </motion.span>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 18, fontWeight: 900, color: d.color, letterSpacing: "0.05em" }}>
                      {d.verdict}
                    </div>
                    <div style={{
                      fontSize: 11, color: "#475569", fontFamily: "monospace", marginTop: 2,
                    }}>
                      {d.url}
                    </div>
                  </div>
                  <ScoreRing score={d.score} color={d.color} />
                </div>

                {/* Body */}
                <div style={{ padding: "20px 22px" }}>
                  {/* Type + source row */}
                  <div style={{ display: "flex", gap: 16, marginBottom: 18 }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: 10, color: "#475569", letterSpacing: "0.15em", marginBottom: 5, fontWeight: 700 }}>
                        ҚАУІП ТҮРІ
                      </div>
                      <div style={{ fontSize: 13, fontWeight: 700, color: "#e2e8f0" }}>{d.type}</div>
                    </div>
                    <div>
                      <div style={{ fontSize: 10, color: "#475569", letterSpacing: "0.15em", marginBottom: 5, fontWeight: 700 }}>
                        ДЕРЕК КӨЗІ
                      </div>
                      <span style={{
                        fontSize: 11, padding: "3px 9px", borderRadius: 8,
                        background: "rgba(165,180,252,0.12)", color: "#a5b4fc",
                        border: "1px solid rgba(165,180,252,0.2)", fontFamily: "monospace",
                      }}>
                        {d.source}
                      </span>
                    </div>
                  </div>

                  {/* Reason */}
                  <div style={{ marginBottom: 18 }}>
                    <div style={{ fontSize: 10, color: "#475569", letterSpacing: "0.15em", marginBottom: 6, fontWeight: 700 }}>
                      СЕБЕБІ
                    </div>
                    <div style={{
                      fontSize: 13, color: "#94a3b8", lineHeight: 1.7,
                      background: "rgba(255,255,255,0.02)", borderRadius: 8,
                      padding: "10px 12px",
                      border: "1px solid rgba(255,255,255,0.04)",
                    }}>
                      {d.reason}
                    </div>
                  </div>

                  {/* XAI indicators */}
                  {d.indicators.length > 0 && (
                    <div style={{ marginBottom: 14 }}>
                      <div style={{ fontSize: 10, color: "#475569", letterSpacing: "0.15em", marginBottom: 8, fontWeight: 700 }}>
                        XAI ФАКТОРЛАР
                      </div>
                      <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                        {d.indicators.map((ind, i) => (
                          <motion.span
                            key={i}
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.1 + i * 0.06 }}
                            style={{
                              fontSize: 10, padding: "3px 9px", borderRadius: 6,
                              background: `${d.color}12`, color: d.color,
                              border: `1px solid ${d.color}25`,
                              fontFamily: "monospace",
                            }}
                          >
                            {ind}
                          </motion.span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Active tiers */}
                  <div style={{ borderTop: "1px solid rgba(255,255,255,0.05)", paddingTop: 14 }}>
                    <div style={{ fontSize: 10, color: "#475569", letterSpacing: "0.15em", marginBottom: 8, fontWeight: 700 }}>
                      СИГНАЛ АНЫҚТАҒАН ДЕҢГЕЙЛЕР
                    </div>
                    <div style={{ display: "flex", gap: 6 }}>
                      {d.tiers.map((t) => {
                        const tier = TIER_LABELS[t];
                        return (
                          <span key={t} style={{
                            fontSize: 10, padding: "3px 9px", borderRadius: 8,
                            background: `${tier.color}18`, color: tier.color,
                            border: `1px solid ${tier.color}35`, fontWeight: 700,
                          }}>
                            ✓ {tier.label}
                          </span>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </motion.div>
            </AnimatePresence>
          </motion.div>
        </div>

        <style>{`
          @media (max-width: 768px) {
            #demo > div > div:nth-child(3) { grid-template-columns: 1fr !important; }
          }
        `}</style>
      </div>
    </section>
  );
}
