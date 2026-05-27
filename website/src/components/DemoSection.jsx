import { motion, AnimatePresence } from "framer-motion";
import { useInView } from "framer-motion";
import { useRef, useState } from "react";

const demos = [
  {
    url: "kaspi-login.tk",
    verdict: "DANGEROUS",
    score: 97,
    type: "Фишинг — KZ Impersonation",
    source: "kz_intel",
    reason: "Kaspi Bank жалған клоны. Сайт kaspi.kz-ті имитациялайды. Тіркелу деректерін ұрлауға арналған.",
    indicators: ["kz_impersonation_kaspi", "free_tld_tk", "domain_age_3d"],
    color: "#ef4444",
    emoji: "⛔",
  },
  {
    url: "100k-ay-investiciya.ru",
    verdict: "DANGEROUS",
    score: 95,
    type: "Қаржылық пирамида",
    source: "pyramid_list",
    reason: "Казахстандық пирамида тізімінде анықталды. 100 000 ₸ айлық кіреберіс — алаяқтық белгісі.",
    indicators: ["pyramid_scheme_kz", "unrealistic_returns", "social_engineering"],
    color: "#ef4444",
    emoji: "⛔",
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
  },
  {
    url: "login-egov-kz.net",
    verdict: "DANGEROUS",
    score: 97,
    type: "Мемлекеттік портал жалғаны",
    source: "kz_intel",
    reason: "eGov.kz порталын имитациялайды. .net доменінде мемлекеттік сайт болмайды.",
    indicators: ["kz_impersonation_egov", "wrong_tld_government", "domain_age_7d"],
    color: "#ef4444",
    emoji: "⛔",
  },
];

export default function DemoSection() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });
  const [active, setActive] = useState(0);

  const d = demos[active];

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
            display: "inline-block", padding: "4px 14px", borderRadius: 20,
            background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.3)",
            fontSize: 12, color: "#a5b4fc", marginBottom: 16, letterSpacing: 1,
          }}>
            ДЕМО
          </div>
          <h2 style={{ fontSize: "clamp(28px,4vw,44px)", fontWeight: 900 }}>
            Нәтиже{" "}<span className="gradient-text">осылай көрінеді</span>
          </h2>
        </motion.div>

        <div style={{
          display: "grid", gridTemplateColumns: "1fr 1fr",
          gap: 32, alignItems: "start",
        }}>
          {/* URL list */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div style={{
              background: "rgba(15,23,42,0.8)", borderRadius: 16, overflow: "hidden",
              border: "1px solid var(--border)",
            }}>
              <div style={{
                padding: "12px 20px",
                background: "rgba(30,41,59,0.5)",
                borderBottom: "1px solid var(--border)",
                fontSize: 12, color: "var(--text3)", letterSpacing: 1,
              }}>
                URL МЫСАЛДАРЫ
              </div>
              {demos.map((item, i) => (
                <div
                  key={i}
                  onClick={() => setActive(i)}
                  style={{
                    padding: "14px 20px",
                    cursor: "pointer",
                    background: active === i ? "rgba(99,102,241,0.1)" : "transparent",
                    borderLeft: active === i ? "3px solid #6366f1" : "3px solid transparent",
                    borderBottom: i < demos.length - 1 ? "1px solid rgba(51,65,85,0.4)" : "none",
                    transition: "all 0.2s",
                    display: "flex", alignItems: "center", gap: 12,
                  }}
                >
                  <span style={{ fontSize: 16 }}>{item.emoji}</span>
                  <span style={{ fontSize: 13, color: active === i ? "var(--text)" : "var(--text2)", fontFamily: "monospace" }}>
                    {item.url}
                  </span>
                  <span style={{
                    marginLeft: "auto", fontSize: 10, padding: "2px 8px", borderRadius: 10,
                    background: `${item.color}22`, color: item.color, fontWeight: 700,
                  }}>
                    {item.verdict}
                  </span>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Result card */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={inView ? { opacity: 1, x: 0 } : {}}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <AnimatePresence mode="wait">
              <motion.div
                key={active}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
                style={{
                  background: "rgba(15,23,42,0.8)", borderRadius: 16,
                  border: `1px solid ${d.color}33`,
                  overflow: "hidden",
                }}
              >
                {/* Header */}
                <div style={{
                  padding: "16px 20px",
                  background: `${d.color}12`,
                  borderBottom: `1px solid ${d.color}22`,
                  display: "flex", alignItems: "center", gap: 12,
                }}>
                  <span style={{ fontSize: 24 }}>{d.emoji}</span>
                  <div>
                    <div style={{ fontSize: 16, fontWeight: 800, color: d.color }}>{d.verdict}</div>
                    <div style={{ fontSize: 11, color: "var(--text3)", fontFamily: "monospace" }}>{d.url}</div>
                  </div>
                  <div style={{
                    marginLeft: "auto",
                    fontSize: 28, fontWeight: 900, color: d.color,
                  }}>
                    {d.score}<span style={{ fontSize: 14 }}>/100</span>
                  </div>
                </div>

                {/* Body */}
                <div style={{ padding: 20 }}>
                  <div style={{ marginBottom: 16 }}>
                    <div style={{ fontSize: 11, color: "var(--text3)", marginBottom: 4 }}>ҚАУІП ТҮРІ</div>
                    <div style={{ fontSize: 14, fontWeight: 600, color: "var(--text)" }}>{d.type}</div>
                  </div>
                  <div style={{ marginBottom: 16 }}>
                    <div style={{ fontSize: 11, color: "var(--text3)", marginBottom: 4 }}>СЕБЕБІ</div>
                    <div style={{ fontSize: 13, color: "var(--text2)", lineHeight: 1.6 }}>{d.reason}</div>
                  </div>
                  {d.indicators.length > 0 && (
                    <div>
                      <div style={{ fontSize: 11, color: "var(--text3)", marginBottom: 8 }}>XAI ФАКТОРЛАР</div>
                      <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                        {d.indicators.map((ind, i) => (
                          <span key={i} style={{
                            fontSize: 10, padding: "3px 8px", borderRadius: 6,
                            background: `${d.color}15`, color: d.color,
                            border: `1px solid ${d.color}30`,
                            fontFamily: "monospace",
                          }}>
                            {ind}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  <div style={{
                    marginTop: 16, fontSize: 11, color: "var(--text3)",
                    display: "flex", alignItems: "center", gap: 6,
                  }}>
                    🔍 Дерек көзі: <span style={{ color: "#a5b4fc" }}>{d.source}</span>
                  </div>
                </div>
              </motion.div>
            </AnimatePresence>
          </motion.div>
        </div>

        <style>{`
          @media (max-width: 768px) {
            #demo > div > div:last-child { grid-template-columns: 1fr !important; }
          }
        `}</style>
      </div>
    </section>
  );
}
