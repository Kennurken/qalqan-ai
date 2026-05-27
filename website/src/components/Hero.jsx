import { motion } from "framer-motion";
import { useEffect, useRef } from "react";

// Animated background grid
function GridBg() {
  return (
    <div style={{
      position: "absolute", inset: 0, overflow: "hidden",
      backgroundImage: `
        linear-gradient(rgba(59,130,246,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(59,130,246,0.04) 1px, transparent 1px)
      `,
      backgroundSize: "40px 40px",
      maskImage: "radial-gradient(ellipse 80% 60% at 50% 0%, black 40%, transparent 100%)",
    }} />
  );
}

// Floating threat indicator pill
function ThreatPill({ label, color, delay, x, y }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.5 }}
      animate={{
        opacity: [0, 1, 1, 0],
        scale: [0.5, 1, 1, 0.8],
        y: [y, y - 10, y - 10, y - 20],
      }}
      transition={{ duration: 4, delay, repeat: Infinity, repeatDelay: 3 }}
      style={{
        position: "absolute", left: x, top: y,
        padding: "6px 14px", borderRadius: 20,
        background: `${color}22`, border: `1px solid ${color}66`,
        color: color, fontSize: 12, fontWeight: 700,
        whiteSpace: "nowrap", pointerEvents: "none",
      }}
    >
      {label}
    </motion.div>
  );
}

export default function Hero() {
  const pills = [
    { label: "⛔ Фишинг анықталды", color: "#ef4444", delay: 0.5, x: "5%", y: "25%" },
    { label: "⚠️ Күдікті URL", color: "#f59e0b", delay: 1.8, x: "72%", y: "20%" },
    { label: "✅ Қауіпсіз", color: "#10b981", delay: 3.2, x: "80%", y: "55%" },
    { label: "🔒 SSL жоқ", color: "#f97316", delay: 2.5, x: "8%", y: "60%" },
    { label: "⛔ Пирамида", color: "#ef4444", delay: 4.0, x: "60%", y: "78%" },
    { label: "🛡️ KZ Intel", color: "#6366f1", delay: 1.2, x: "22%", y: "78%" },
  ];

  return (
    <section style={{
      position: "relative", minHeight: "100vh",
      display: "flex", alignItems: "center", justifyContent: "center",
      padding: "0 24px", overflow: "hidden",
    }}>
      <GridBg />

      {/* Glow orbs */}
      <div style={{
        position: "absolute", top: "10%", left: "30%",
        width: 600, height: 600,
        background: "radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%)",
        pointerEvents: "none",
      }} />
      <div style={{
        position: "absolute", top: "40%", left: "60%",
        width: 400, height: 400,
        background: "radial-gradient(circle, rgba(239,68,68,0.08) 0%, transparent 70%)",
        pointerEvents: "none",
      }} />

      {/* Floating pills */}
      {pills.map((p, i) => <ThreatPill key={i} {...p} />)}

      {/* Main content */}
      <div style={{ position: "relative", zIndex: 1, textAlign: "center", maxWidth: 780 }}>
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          style={{
            display: "inline-flex", alignItems: "center", gap: 8,
            padding: "6px 16px", borderRadius: 20,
            background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.3)",
            marginBottom: 32, fontSize: 13, color: "#a5b4fc",
          }}
        >
          <span style={{
            width: 8, height: 8, borderRadius: "50%", background: "#10b981",
            boxShadow: "0 0 8px #10b981",
            animation: "pulse 2s infinite",
          }} />
          Қазақстанда жасалған • Republican Competition 2026
        </motion.div>

        {/* Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          style={{ fontSize: "clamp(40px,6vw,72px)", fontWeight: 900, lineHeight: 1.1, marginBottom: 24 }}
        >
          <span className="gradient-text">Қазақстанның</span>
          <br />
          киберқорғаныс{" "}
          <span style={{ color: "var(--text)" }}>жүйесі</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          style={{ fontSize: 18, color: "var(--text2)", maxWidth: 580, margin: "0 auto 48px", lineHeight: 1.7 }}
        >
          QALQAN AI — фишинг, алаяқтық, қаржылық пирамида сайттарын
          нақты уақытта анықтайтын Chrome кеңейтімі.
          5 деңгейлі тексеру + жасанды интеллект.
        </motion.p>

        {/* CTA buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.3 }}
          style={{ display: "flex", gap: 16, justifyContent: "center", flexWrap: "wrap" }}
        >
          <a
            href="https://github.com/Kennurken/qalqan-ai"
            target="_blank" rel="noopener noreferrer"
            style={{
              padding: "14px 32px", borderRadius: 12,
              background: "linear-gradient(135deg, #3b82f6, #6366f1)",
              color: "white", fontWeight: 700, fontSize: 15,
              boxShadow: "0 8px 32px rgba(99,102,241,0.35)",
              transition: "transform 0.2s, box-shadow 0.2s",
            }}
            onMouseEnter={e => { e.currentTarget.style.transform = "translateY(-2px)"; e.currentTarget.style.boxShadow = "0 12px 40px rgba(99,102,241,0.5)"; }}
            onMouseLeave={e => { e.currentTarget.style.transform = "none"; e.currentTarget.style.boxShadow = "0 8px 32px rgba(99,102,241,0.35)"; }}
          >
            🛡️ Chrome-ге орнату
          </a>
          <a
            href="#how"
            style={{
              padding: "14px 32px", borderRadius: 12,
              background: "transparent", border: "1px solid var(--border)",
              color: "var(--text2)", fontWeight: 600, fontSize: 15,
              transition: "border-color 0.2s, color 0.2s",
            }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = "#6366f1"; e.currentTarget.style.color = "var(--text)"; }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = "var(--border)"; e.currentTarget.style.color = "var(--text2)"; }}
          >
            Қалай жұмыс істейді →
          </a>
        </motion.div>

        {/* Stats row */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          style={{
            display: "flex", gap: 48, justifyContent: "center",
            marginTop: 72, flexWrap: "wrap",
          }}
        >
          {[
            { n: "5+", label: "Тексеру деңгейі" },
            { n: "10+", label: "Threat Intelligence" },
            { n: "3", label: "Тіл қолдауы" },
            { n: "97%", label: "Анықтау дәлдігі" },
          ].map((s, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.9 + i * 0.1 }}
              style={{ textAlign: "center" }}
            >
              <div style={{ fontSize: 28, fontWeight: 800, color: "var(--text)" }}>{s.n}</div>
              <div style={{ fontSize: 12, color: "var(--text3)" }}>{s.label}</div>
            </motion.div>
          ))}
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        animate={{ y: [0, 8, 0] }}
        transition={{ duration: 1.5, repeat: Infinity }}
        style={{
          position: "absolute", bottom: 32, left: "50%", transform: "translateX(-50%)",
          color: "var(--text3)", fontSize: 12, display: "flex", flexDirection: "column",
          alignItems: "center", gap: 6,
        }}
      >
        <span>Төмен қарай</span>
        <span>↓</span>
      </motion.div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.4; }
        }
      `}</style>
    </section>
  );
}
