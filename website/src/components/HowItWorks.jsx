import { motion } from "framer-motion";
import { useInView } from "framer-motion";
import { useRef } from "react";

const steps = [
  {
    n: "01",
    icon: "🌐",
    title: "Сайтты ашасыз",
    desc: "Chrome-де кез келген сайтқа кіресіз. Qalqan AI автоматты түрде немесе батырма арқылы тексеруді бастайды.",
    color: "#3b82f6",
  },
  {
    n: "02",
    icon: "⚡",
    title: "Офлайн тексеру",
    desc: "200+ белгілі қауіпті домен мгновенды тексеріледі. API-сыз, 0ms. Whitelist, Pyramid DB, Phishing DB.",
    color: "#6366f1",
  },
  {
    n: "03",
    icon: "🔬",
    title: "Терең талдау",
    desc: "URL белгілері, домен жасы (RDAP), SSL сертификат, KZ брендтері — 20+ параметр паралельді тексеріледі.",
    color: "#8b5cf6",
  },
  {
    n: "04",
    icon: "🤖",
    title: "AI талдауы",
    desc: "Groq Llama мен Gemini — беттің мазмұнын оқып, скриншоттан алаяқтықты анықтайды. XAI факторлар беріледі.",
    color: "#ec4899",
  },
  {
    n: "05",
    icon: "🛡️",
    title: "Нәтиже + Қорғаныс",
    desc: "SAFE / SUSPICIOUS / DANGEROUS вердикт. Қауіпті сайт автоматты бұғатталады. Апелляция мүмкіндігі бар.",
    color: "#ef4444",
  },
];

export default function HowItWorks() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <section id="how" style={{
      padding: "100px 24px",
      background: "linear-gradient(180deg, transparent, rgba(15,23,42,0.8), transparent)",
    }}>
      <div style={{ maxWidth: 1000, margin: "0 auto" }}>
        {/* Title */}
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7 }}
          style={{ textAlign: "center", marginBottom: 80 }}
        >
          <div style={{
            display: "inline-block", padding: "4px 14px", borderRadius: 20,
            background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.3)",
            fontSize: 12, color: "#34d399", marginBottom: 16, letterSpacing: 1,
          }}>
            ҚАЛАЙ ЖҰМЫС ІСТЕЙДІ
          </div>
          <h2 style={{ fontSize: "clamp(28px,4vw,44px)", fontWeight: 900, marginBottom: 16 }}>
            5 деңгейлі{" "}
            <span className="gradient-text">тексеру конвейері</span>
          </h2>
          <p style={{ fontSize: 16, color: "var(--text2)", maxWidth: 500, margin: "0 auto" }}>
            Секундтың ішінде — офлайн тексеруден AI талдауына дейін
          </p>
        </motion.div>

        {/* Steps */}
        <div style={{ position: "relative" }}>
          {/* Vertical line */}
          <motion.div
            initial={{ scaleY: 0 }}
            animate={inView ? { scaleY: 1 } : {}}
            transition={{ duration: 1.2, delay: 0.3 }}
            style={{
              position: "absolute", left: "50%", top: 0, bottom: 0,
              width: 2, background: "linear-gradient(180deg, #3b82f6, #6366f1, #8b5cf6, #ec4899, #ef4444)",
              transformOrigin: "top",
            }}
          />

          {steps.map((s, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: i % 2 === 0 ? -50 : 50 }}
              animate={inView ? { opacity: 1, x: 0 } : {}}
              transition={{ duration: 0.6, delay: 0.4 + i * 0.15 }}
              style={{
                display: "flex",
                justifyContent: i % 2 === 0 ? "flex-end" : "flex-start",
                marginBottom: 40,
                paddingLeft: i % 2 === 0 ? 0 : "calc(50% + 40px)",
                paddingRight: i % 2 === 0 ? "calc(50% + 40px)" : 0,
              }}
            >
              <div style={{
                background: "rgba(30,41,59,0.7)",
                border: `1px solid ${s.color}33`,
                borderRadius: 16, padding: "20px 24px",
                maxWidth: 360, width: "100%",
                backdropFilter: "blur(12px)",
                position: "relative",
              }}>
                {/* Connector dot */}
                <div style={{
                  position: "absolute",
                  top: "50%", transform: "translateY(-50%)",
                  [i % 2 === 0 ? "right" : "left"]: -44,
                  width: 16, height: 16, borderRadius: "50%",
                  background: s.color,
                  boxShadow: `0 0 16px ${s.color}80`,
                }} />

                <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
                  <span style={{
                    fontSize: 11, fontWeight: 800, color: s.color,
                    fontFamily: "monospace", letterSpacing: 1,
                  }}>
                    TIER {s.n}
                  </span>
                  <span style={{ fontSize: 20 }}>{s.icon}</span>
                </div>
                <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 8, color: "var(--text)" }}>
                  {s.title}
                </h3>
                <p style={{ fontSize: 13, color: "var(--text2)", lineHeight: 1.6 }}>
                  {s.desc}
                </p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Mobile steps (single column) */}
        <style>{`
          @media (max-width: 640px) {
            .pipeline-step { padding-left: 0 !important; padding-right: 0 !important; justify-content: center !important; }
            .pipeline-line { display: none; }
          }
        `}</style>
      </div>
    </section>
  );
}
