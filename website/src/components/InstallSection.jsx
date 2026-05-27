import { motion, useInView } from "framer-motion";
import { useRef, useState } from "react";

const REQUIREMENTS = [
  { icon: "🌐", text: "Chrome 90+" },
  { icon: "🆓", text: "Тегін" },
  { icon: "🔇", text: "Жарнамасыз" },
  { icon: "📖", text: "Open Source" },
  { icon: "🇰🇿", text: "Made in KZ" },
];

const STEPS = [
  { n: "01", icon: "🌐", title: "Chrome Web Store", desc: "Дүкенге өтіңіз" },
  { n: "02", icon: "🔍", title: "Іздеу", desc: '"QALQAN AI" теріңіз' },
  { n: "03", icon: "📥", title: "Орнату", desc: '"Add to Chrome" басыңыз' },
  { n: "04", icon: "🛡️", title: "Қорғаныс", desc: "Автоматты қосылады" },
];

export default function InstallSection() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });
  const [hoveredBtn, setHoveredBtn] = useState(null);

  return (
    <section id="install" style={{ padding: "100px 24px" }}>
      <div style={{ maxWidth: 900, margin: "0 auto" }}>
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 40 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          style={{
            position: "relative",
            borderRadius: 28,
            overflow: "hidden",
          }}
        >
          {/* Multi-layer background */}
          <div style={{
            position: "absolute", inset: 0,
            background: "linear-gradient(135deg, rgba(30,41,59,0.95) 0%, rgba(15,23,42,0.98) 100%)",
            border: "1px solid rgba(99,102,241,0.25)",
            borderRadius: 28,
          }} />

          {/* Corner glow top-left */}
          <div style={{
            position: "absolute", top: -100, left: -100,
            width: 400, height: 300,
            background: "radial-gradient(ellipse, rgba(99,102,241,0.18) 0%, transparent 65%)",
            pointerEvents: "none",
          }} />
          {/* Corner glow bottom-right */}
          <div style={{
            position: "absolute", bottom: -60, right: -60,
            width: 300, height: 250,
            background: "radial-gradient(ellipse, rgba(16,185,129,0.12) 0%, transparent 65%)",
            pointerEvents: "none",
          }} />

          {/* Subtle grid */}
          <div style={{
            position: "absolute", inset: 0, borderRadius: 28, pointerEvents: "none",
            backgroundImage: "linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px)",
            backgroundSize: "32px 32px",
          }} />

          {/* Top accent line */}
          <div style={{
            position: "absolute", top: 0, left: "20%", right: "20%", height: 1,
            background: "linear-gradient(90deg, transparent, rgba(99,102,241,0.6), rgba(16,185,129,0.4), transparent)",
          }} />

          <div style={{ position: "relative", zIndex: 1, padding: "60px 48px", textAlign: "center" }}>
            {/* Animated shield */}
            <div style={{ position: "relative", display: "inline-block", marginBottom: 28 }}>
              <motion.div
                animate={{ rotate: [0, 3, -3, 0] }}
                transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
                style={{ fontSize: 72, lineHeight: 1 }}
              >
                🛡️
              </motion.div>
              {/* Orbit ring */}
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 12, repeat: Infinity, ease: "linear" }}
                style={{
                  position: "absolute", inset: -16,
                  border: "1px dashed rgba(99,102,241,0.2)",
                  borderRadius: "50%",
                }}
              />
              {/* Glow pulse */}
              <motion.div
                animate={{ scale: [1, 1.4, 1], opacity: [0.3, 0, 0.3] }}
                transition={{ duration: 3, repeat: Infinity }}
                style={{
                  position: "absolute", inset: -8,
                  background: "radial-gradient(ellipse, rgba(99,102,241,0.3), transparent 70%)",
                  borderRadius: "50%", pointerEvents: "none",
                }}
              />
            </div>

            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.2 }}
              style={{ fontSize: "clamp(28px,4vw,48px)", fontWeight: 900, lineHeight: 1.1, marginBottom: 16 }}
            >
              Бүгін{" "}
              <span style={{
                background: "linear-gradient(135deg, #3b82f6, #6366f1, #a78bfa)",
                WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
              }}>
                орнатыңыз
              </span>
              {" "}— тегін
            </motion.h2>

            <motion.p
              initial={{ opacity: 0 }}
              animate={inView ? { opacity: 1 } : {}}
              transition={{ delay: 0.35 }}
              style={{ fontSize: 16, color: "#94a3b8", maxWidth: 500, margin: "0 auto 48px", lineHeight: 1.7 }}
            >
              Қазақстанның 1-ші AI-негізделген киберқорғаныс кеңейтімі.
              Орнату — 30 секунд. Жұмыс — автоматты.
            </motion.p>

            {/* Install steps */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={inView ? { opacity: 1 } : {}}
              transition={{ delay: 0.4 }}
              style={{
                display: "flex", justifyContent: "center",
                alignItems: "center", gap: 0,
                marginBottom: 48, flexWrap: "wrap",
              }}
            >
              {STEPS.map((s, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 16 }}
                  animate={inView ? { opacity: 1, y: 0 } : {}}
                  transition={{ delay: 0.5 + i * 0.1 }}
                  style={{ display: "flex", alignItems: "center" }}
                >
                  <div style={{ textAlign: "center", width: 120 }}>
                    <motion.div
                      whileHover={{ scale: 1.12, rotate: -5 }}
                      style={{
                        width: 52, height: 52, borderRadius: "50%",
                        background: "rgba(99,102,241,0.12)",
                        border: "1px solid rgba(99,102,241,0.28)",
                        display: "flex", alignItems: "center", justifyContent: "center",
                        fontSize: 22, margin: "0 auto 10px",
                        boxShadow: "0 0 20px rgba(99,102,241,0.1)",
                      }}
                    >
                      {s.icon}
                    </motion.div>
                    <div style={{ fontSize: 10, color: "#6366f1", fontWeight: 800, marginBottom: 3, letterSpacing: "0.15em" }}>
                      {s.n}
                    </div>
                    <div style={{ fontSize: 12, fontWeight: 700, color: "#e2e8f0", marginBottom: 2 }}>{s.title}</div>
                    <div style={{ fontSize: 11, color: "#64748b" }}>{s.desc}</div>
                  </div>
                  {i < STEPS.length - 1 && (
                    <motion.div
                      animate={{ x: [0, 4, 0] }}
                      transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.3 }}
                      style={{ color: "#334155", fontSize: 16, padding: "0 4px", marginBottom: 18 }}
                    >
                      →
                    </motion.div>
                  )}
                </motion.div>
              ))}
            </motion.div>

            {/* CTA buttons */}
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.7 }}
              style={{ display: "flex", gap: 16, justifyContent: "center", flexWrap: "wrap", marginBottom: 36 }}
            >
              <motion.a
                href="https://github.com/Kennurken/qalqan-ai"
                target="_blank" rel="noopener noreferrer"
                onHoverStart={() => setHoveredBtn("install")}
                onHoverEnd={() => setHoveredBtn(null)}
                whileHover={{ scale: 1.04 }}
                whileTap={{ scale: 0.97 }}
                style={{
                  display: "inline-flex", alignItems: "center", gap: 10,
                  padding: "16px 38px", borderRadius: 14,
                  background: "linear-gradient(135deg, #3b82f6, #6366f1)",
                  color: "white", fontWeight: 800, fontSize: 16,
                  boxShadow: hoveredBtn === "install"
                    ? "0 16px 48px rgba(99,102,241,0.55)"
                    : "0 8px 32px rgba(99,102,241,0.35)",
                  transition: "box-shadow 0.3s",
                  textDecoration: "none",
                }}
              >
                <span>🛡️</span> Chrome-ге орнату
              </motion.a>
              <motion.a
                href="https://github.com/Kennurken/qalqan-ai"
                target="_blank" rel="noopener noreferrer"
                onHoverStart={() => setHoveredBtn("github")}
                onHoverEnd={() => setHoveredBtn(null)}
                whileHover={{ scale: 1.04, borderColor: "#6366f1" }}
                whileTap={{ scale: 0.97 }}
                style={{
                  display: "inline-flex", alignItems: "center", gap: 10,
                  padding: "16px 28px", borderRadius: 14,
                  border: "1px solid rgba(255,255,255,0.1)",
                  background: hoveredBtn === "github" ? "rgba(99,102,241,0.08)" : "rgba(255,255,255,0.03)",
                  color: "#94a3b8", fontWeight: 600, fontSize: 15,
                  transition: "background 0.2s, border-color 0.2s",
                  textDecoration: "none",
                }}
              >
                <span>⭐</span> GitHub
              </motion.a>
            </motion.div>

            {/* Requirements pills */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={inView ? { opacity: 1 } : {}}
              transition={{ delay: 0.85 }}
              style={{ display: "flex", gap: 8, justifyContent: "center", flexWrap: "wrap" }}
            >
              {REQUIREMENTS.map((r, i) => (
                <span key={i} style={{
                  fontSize: 11, padding: "4px 12px", borderRadius: 20,
                  background: "rgba(255,255,255,0.04)",
                  border: "1px solid rgba(255,255,255,0.07)",
                  color: "#64748b", display: "flex", alignItems: "center", gap: 5,
                }}>
                  {r.icon} {r.text}
                </span>
              ))}
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
