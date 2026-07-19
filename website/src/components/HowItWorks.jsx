import { motion } from "framer-motion";
import { useRef, useEffect, useState } from "react";

const STEPS = [
  {
    n: "01", icon: "", color: "#3b82f6",
    title: "Сайтты ашасыз",
    desc: "Chrome-де кез келген сайтқа кіресіз. Qalqan AI фонда автоматты тексеруді бастайды немесе батырма арқылы қолмен іске қосасыз.",
    tags: ["Auto-check", "Manual trigger", "0ms start"],
  },
  {
    n: "02", icon: "", color: "#f59e0b",
    title: "Офлайн + KZ тексеру",
    desc: "200+ белгілі домен API-сыз тексеріледі. Whitelist, Pyramid DB, KZ Intel, Gambling DB — жергілікті тізімдерде. 0ms нәтиже.",
    tags: ["0ms", "Pyramid DB", "KZ Intel", "Gambling DB"],
  },
  {
    n: "03", icon: "", color: "#6366f1",
    title: "URL + Domain талдауы",
    desc: "30+ параметр параллельді тексеріледі: URL белгілері, RDAP домен жасы, SSL сертификат, homoglyph шабуыл, KZ бренд имитациясы.",
    tags: ["RDAP", "SSL", "30+ features", "Homoglyph"],
  },
  {
    n: "04", icon: "", color: "#10b981",
    title: "Сыртқы дерекқорлар",
    desc: "PhishTank, Google Safe Browsing, URLhaus, OpenPhish — параллельді asyncio.gather арқылы. Нақты уақыт threat intelligence.",
    tags: ["PhishTank", "SafeBrowsing", "URLhaus", "OpenPhish"],
  },
  {
    n: "05", icon: "", color: "#8b5cf6",
    title: "AI талдауы + XAI",
    desc: "Groq Llama + Gemini Vision — беттің мазмұнын оқиды, скриншоттан алаяқтықты анықтайды. XAI факторлар неге қауіпті екенін түсіндіреді.",
    tags: ["Groq AI", "Gemini Vision", "XAI", "SHAP-style"],
  },
  {
    n: "06", icon: "", color: "#ef4444",
    title: "Вердикт + Қорғаныс",
    desc: "SAFE / SUSPICIOUS / DANGEROUS вердикт 0.8с ішінде. Қауіпті сайт автоматты бұғатталады. 5с кері санау + апелляция мүмкіндігі.",
    tags: ["Auto-block", "Appeal", "5s countdown", "Notification"],
  },
];

export default function HowItWorks() {
  const ref = useRef(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const obs = new IntersectionObserver(
      ([e]) => { if (e.isIntersecting) { setVisible(true); obs.disconnect(); } },
      { threshold: 0.1 }
    );
    if (ref.current) obs.observe(ref.current);
    return () => obs.disconnect();
  }, []);

  return (
    <section id="how" style={{
      padding: "100px 24px",
      background: "linear-gradient(180deg, transparent 0%, rgba(15,23,42,0.5) 50%, transparent 100%)",
    }}>
      <div style={{ maxWidth: 860, margin: "0 auto" }}>
        {/* Title */}
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 30 }}
          animate={visible ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.7 }}
          style={{ textAlign: "center", marginBottom: 80 }}
        >
          <div style={{
            display: "inline-flex", alignItems: "center", gap: 8,
            padding: "5px 16px", borderRadius: 20,
            background: "rgba(16,185,129,0.08)",
            border: "1px solid rgba(16,185,129,0.25)",
            fontSize: 11, color: "#34d399", marginBottom: 20, letterSpacing: "0.15em", fontWeight: 700,
          }}>
            ҚАЛАЙ ЖҰМЫС ІСТЕЙДІ
          </div>
          <h2 style={{ fontSize: "clamp(28px,4vw,48px)", fontWeight: 900, marginBottom: 16, lineHeight: 1.1 }}>
            6 деңгейлі{" "}
            <span style={{
              background: "linear-gradient(135deg, #3b82f6, #6366f1, #8b5cf6)",
              WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
            }}>
              тексеру конвейері
            </span>
          </h2>
          <p style={{ fontSize: 16, color: "#94a3b8", maxWidth: 480, margin: "0 auto" }}>
            Секундтың ішінде — офлайн тексеруден AI талдауына дейін
          </p>
        </motion.div>

        {/* Steps */}
        <div style={{ position: "relative" }}>
          {/* Animated vertical line */}
          <div style={{
            position: "absolute", left: 39, top: 0, bottom: 0,
            width: 2, background: "rgba(255,255,255,0.05)",
          }}>
            <motion.div
              initial={{ scaleY: 0 }}
              animate={visible ? { scaleY: 1 } : {}}
              transition={{ duration: 1.4, delay: 0.3, ease: "easeOut" }}
              style={{
                height: "100%", width: "100%",
                background: "linear-gradient(180deg, #3b82f6, #6366f1, #8b5cf6, #ec4899, #ef4444)",
                transformOrigin: "top",
              }}
            />
          </div>

          {STEPS.map((s, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -30 }}
              animate={visible ? { opacity: 1, x: 0 } : {}}
              transition={{ duration: 0.55, delay: 0.4 + i * 0.13 }}
              style={{
                display: "flex", gap: 24, marginBottom: i < STEPS.length - 1 ? 36 : 0,
              }}
            >
              {/* Step circle */}
              <div style={{
                width: 80, flexShrink: 0, display: "flex",
                flexDirection: "column", alignItems: "center",
              }}>
                <motion.div
                  initial={{ scale: 0 }}
                  animate={visible ? { scale: 1 } : {}}
                  transition={{ type: "spring", stiffness: 300, delay: 0.5 + i * 0.13 }}
                  style={{
                    width: 44, height: 44, borderRadius: "50%",
                    background: `${s.color}18`,
                    border: `2px solid ${s.color}`,
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: 20,
                    boxShadow: `0 0 16px ${s.color}30`,
                    zIndex: 1, position: "relative",
                    background: `radial-gradient(circle at center, ${s.color}22, ${s.color}08)`,
                  }}
                >
                  {s.icon}
                </motion.div>
              </div>

              {/* Content card */}
              <motion.div
                whileHover={{ x: 4 }}
                transition={{ type: "spring", stiffness: 400 }}
                style={{
                  flex: 1, background: "rgba(15,23,42,0.7)",
                  border: `1px solid rgba(255,255,255,0.06)`,
                  borderRadius: 16, padding: "20px 24px",
                  backdropFilter: "blur(12px)",
                  borderLeft: `3px solid ${s.color}`,
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
                  <span style={{ fontSize: 10, fontWeight: 800, color: s.color, letterSpacing: "0.2em" }}>
                    TIER {s.n}
                  </span>
                </div>
                <h3 style={{ fontSize: 17, fontWeight: 800, color: "#f1f5f9", marginBottom: 8 }}>
                  {s.title}
                </h3>
                <p style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.65, marginBottom: 12 }}>
                  {s.desc}
                </p>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {s.tags.map((t, j) => (
                    <span key={j} style={{
                      fontSize: 10, padding: "2px 9px", borderRadius: 20,
                      background: `${s.color}12`, color: s.color,
                      border: `1px solid ${s.color}25`, fontWeight: 600,
                    }}>{t}</span>
                  ))}
                </div>
              </motion.div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
