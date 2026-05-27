// 21st.dev-inspired dark hero with particle grid + Framer Motion
import { motion, AnimatePresence } from "framer-motion";
import { useEffect, useRef, useState } from "react";

// Animated dot grid background (canvas-based, like 21st.dev)
function ParticleGrid() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let animFrame;
    let dots = [];

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      dots = [];
      const spacing = 40;
      for (let x = 0; x < canvas.width; x += spacing) {
        for (let y = 0; y < canvas.height; y += spacing) {
          dots.push({ x, y, r: Math.random() * 0.8 + 0.2, phase: Math.random() * Math.PI * 2 });
        }
      }
    };

    let t = 0;
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      t += 0.008;
      dots.forEach(d => {
        const alpha = 0.08 + 0.06 * Math.sin(t + d.phase);
        ctx.beginPath();
        ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(99,102,241,${alpha})`;
        ctx.fill();
      });
      animFrame = requestAnimationFrame(draw);
    };

    resize();
    draw();
    window.addEventListener("resize", resize);
    return () => { cancelAnimationFrame(animFrame); window.removeEventListener("resize", resize); };
  }, []);

  return (
    <canvas ref={canvasRef} style={{
      position: "absolute", inset: 0,
      width: "100%", height: "100%",
      pointerEvents: "none",
    }} />
  );
}

// Threat pill that fades in, floats up, fades out in loop
function ThreatPill({ label, color, bg, delay, style }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.7, y: 0 }}
      animate={{ opacity: [0, 1, 1, 0], scale: [0.7, 1, 1, 0.85], y: [0, -8, -8, -20] }}
      transition={{ duration: 3.5, delay, repeat: Infinity, repeatDelay: 3 + delay * 0.5 }}
      style={{
        position: "absolute", ...style,
        padding: "6px 14px", borderRadius: 20,
        background: bg, border: `1px solid ${color}66`,
        color, fontSize: 12, fontWeight: 700,
        whiteSpace: "nowrap", pointerEvents: "none",
        backdropFilter: "blur(8px)",
      }}
    >
      {label}
    </motion.div>
  );
}

const PILLS = [
  { label: "⛔ kaspi-login.tk — DANGEROUS", color: "#f87171", bg: "rgba(239,68,68,0.15)", delay: 0.3, style: { left: "4%", top: "22%" } },
  { label: "⚠️ Күдікті URL анықталды", color: "#fbbf24", bg: "rgba(245,158,11,0.15)", delay: 2.1, style: { right: "5%", top: "18%" } },
  { label: "✅ google.com — SAFE", color: "#34d399", bg: "rgba(16,185,129,0.15)", delay: 3.8, style: { right: "6%", top: "55%" } },
  { label: "⛔ Финансовая пирамида", color: "#f87171", bg: "rgba(239,68,68,0.15)", delay: 1.4, style: { left: "3%", top: "65%" } },
  { label: "🛡️ KZ Intel: egov жалған", color: "#a5b4fc", bg: "rgba(99,102,241,0.15)", delay: 5.0, style: { left: "20%", top: "80%" } },
  { label: "🔒 SSL жоқ — +30 score", color: "#fb923c", bg: "rgba(249,115,22,0.15)", delay: 2.8, style: { right: "18%", top: "78%" } },
];

const STATS = [
  { n: "5+", label: "Тексеру деңгейі" },
  { n: "10+", label: "Threat Intelligence" },
  { n: "97%", label: "Дәлдік" },
  { n: "0.8s", label: "Орташа уақыт" },
];

export default function Hero() {
  return (
    <section style={{
      position: "relative", minHeight: "100vh",
      display: "flex", alignItems: "center", justifyContent: "center",
      padding: "80px 24px 40px", overflow: "hidden",
    }}>
      <ParticleGrid />

      {/* Glow orbs */}
      <div style={{
        position: "absolute", top: "15%", left: "20%",
        width: 700, height: 500,
        background: "radial-gradient(ellipse, rgba(99,102,241,0.1) 0%, transparent 70%)",
        pointerEvents: "none",
      }} />
      <div style={{
        position: "absolute", bottom: "10%", right: "15%",
        width: 500, height: 400,
        background: "radial-gradient(ellipse, rgba(239,68,68,0.07) 0%, transparent 70%)",
        pointerEvents: "none",
      }} />

      {/* Floating pills */}
      {PILLS.map((p, i) => <ThreatPill key={i} {...p} />)}

      {/* Main content */}
      <div style={{ position: "relative", zIndex: 1, textAlign: "center", maxWidth: 820 }}>

        {/* Live badge */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          style={{
            display: "inline-flex", alignItems: "center", gap: 8,
            padding: "6px 18px", borderRadius: 20,
            background: "rgba(99,102,241,0.08)",
            border: "1px solid rgba(99,102,241,0.25)",
            marginBottom: 36, fontSize: 12, color: "#a5b4fc",
            letterSpacing: "0.1em",
          }}
        >
          <span style={{
            width: 7, height: 7, borderRadius: "50%", background: "#10b981",
            boxShadow: "0 0 10px #10b981",
            animation: "hero-pulse 2s infinite",
          }} />
          Қазақстанда жасалған • ДЭР байқауы 2026
        </motion.div>

        {/* Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 32 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.75, delay: 0.1 }}
          style={{
            fontSize: "clamp(38px,6.5vw,76px)",
            fontWeight: 900, lineHeight: 1.05,
            marginBottom: 28, letterSpacing: "-1px",
          }}
        >
          <span style={{
            background: "linear-gradient(135deg, #60a5fa, #818cf8, #a78bfa)",
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
          }}>
            Қазақстанның
          </span>
          <br />
          <span style={{ color: "#f8fafc" }}>киберқалқаны</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.22 }}
          style={{
            fontSize: "clamp(15px,2vw,19px)",
            color: "#94a3b8", maxWidth: 600,
            margin: "0 auto 52px", lineHeight: 1.75,
          }}
        >
          Фишинг, алаяқтық, қаржылық пирамида сайттарын нақты уақытта анықтайтын{" "}
          <strong style={{ color: "#c7d2fe" }}>Chrome кеңейтімі</strong>.
          5 деңгейлі тексеру + жасанды интеллект.
        </motion.p>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.34 }}
          style={{ display: "flex", gap: 14, justifyContent: "center", flexWrap: "wrap" }}
        >
          <motion.a
            href="https://github.com/Kennurken/qalqan-ai"
            target="_blank" rel="noopener noreferrer"
            whileHover={{ scale: 1.04, boxShadow: "0 16px 48px rgba(99,102,241,0.5)" }}
            whileTap={{ scale: 0.97 }}
            style={{
              display: "inline-flex", alignItems: "center", gap: 10,
              padding: "14px 34px", borderRadius: 12,
              background: "linear-gradient(135deg, #3b82f6, #6366f1)",
              color: "#fff", fontWeight: 800, fontSize: 15,
              boxShadow: "0 8px 32px rgba(99,102,241,0.35)",
              letterSpacing: "0.02em",
            }}
          >
            🛡️ Chrome-ге орнату
          </motion.a>
          <motion.a
            href="#features"
            whileHover={{ scale: 1.03, borderColor: "#6366f1", color: "#f8fafc" }}
            style={{
              display: "inline-flex", alignItems: "center", gap: 8,
              padding: "14px 28px", borderRadius: 12,
              background: "rgba(255,255,255,0.03)",
              border: "1px solid rgba(255,255,255,0.12)",
              color: "#94a3b8", fontWeight: 600, fontSize: 15,
              transition: "all 0.2s",
            }}
          >
            Мүмкіндіктер →
          </motion.a>
        </motion.div>

        {/* Stats row */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.9, duration: 0.8 }}
          style={{
            display: "flex", gap: 0, justifyContent: "center",
            marginTop: 80, flexWrap: "wrap",
          }}
        >
          {STATS.map((s, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1 + i * 0.1 }}
              style={{
                textAlign: "center", padding: "0 36px",
                borderRight: i < STATS.length - 1 ? "1px solid rgba(255,255,255,0.07)" : "none",
              }}
            >
              <div style={{
                fontSize: 32, fontWeight: 900, color: "#f8fafc",
                background: "linear-gradient(135deg, #60a5fa, #818cf8)",
                WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
              }}>
                {s.n}
              </div>
              <div style={{ fontSize: 11, color: "#64748b", marginTop: 4, letterSpacing: "0.05em" }}>
                {s.label}
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>

      {/* Scroll hint */}
      <motion.div
        animate={{ y: [0, 6, 0] }}
        transition={{ duration: 1.8, repeat: Infinity }}
        style={{
          position: "absolute", bottom: 28, left: "50%",
          transform: "translateX(-50%)",
          color: "#334155", fontSize: 20,
        }}
      >
        ↓
      </motion.div>

      <style>{`
        @keyframes hero-pulse {
          0%, 100% { opacity: 1; box-shadow: 0 0 10px #10b981; }
          50% { opacity: 0.4; box-shadow: 0 0 4px #10b981; }
        }
      `}</style>
    </section>
  );
}
