import { motion, useInView, useMotionValue, animate } from "framer-motion";
import { useRef, useEffect, useState } from "react";

function AnimatedCounter({ value, suffix = "", duration = 2.2, inView }) {
  const ref = useRef(null);
  const count = useMotionValue(0);

  useEffect(() => {
    if (!inView) return;
    const num = parseFloat(value);
    const controls = animate(count, num, {
      duration,
      ease: [0.25, 0.46, 0.45, 0.94],
      onUpdate(v) {
        if (ref.current) {
          const display = Number.isInteger(num) ? Math.round(v).toLocaleString() : v.toFixed(1);
          ref.current.textContent = display + suffix;
        }
      },
    });
    return controls.stop;
  }, [inView, value, suffix, duration, count]);

  return <span ref={ref}>0{suffix}</span>;
}

// Moving halo orb around card
function HaloOrb({ color }) {
  return (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
      style={{
        position: "absolute", inset: -2, borderRadius: 22,
        background: `conic-gradient(from 0deg, transparent 70%, ${color}55 85%, ${color}99 90%, ${color}55 95%, transparent 100%)`,
        pointerEvents: "none", zIndex: 0,
      }}
    />
  );
}

const statCards = [
  {
    value: "50000", suffix: "+",
    label: "Тексерілген URL",
    sub: "Kazakhstan users",
    color: "#3b82f6",
    icon: "🔍",
    delay: 0,
  },
  {
    value: "4200", suffix: "+",
    label: "Бұғатталған сайт",
    sub: "Dangerous blocked",
    color: "#ef4444",
    icon: "⛔",
    delay: 0.1,
  },
  {
    value: "97", suffix: "%",
    label: "Анықтау дәлдігі",
    sub: "Detection accuracy",
    color: "#10b981",
    icon: "✅",
    delay: 0.2,
  },
  {
    value: "0.8", suffix: "s",
    label: "Орташа уақыт",
    sub: "Average check time",
    color: "#f59e0b",
    icon: "⚡",
    delay: 0.3,
  },
];

function StatCard({ s, inView }) {
  const [hovered, setHovered] = useState(false);

  return (
    <motion.div
      onHoverStart={() => setHovered(true)}
      onHoverEnd={() => setHovered(false)}
      initial={{ opacity: 0, y: 30, scale: 0.92 }}
      animate={inView ? { opacity: 1, y: 0, scale: 1 } : {}}
      transition={{ duration: 0.6, delay: s.delay, ease: [0.21, 0.47, 0.32, 0.98] }}
      style={{
        position: "relative",
        borderRadius: 20,
        padding: 2,
        overflow: "hidden",
      }}
    >
      {/* Rotating halo border */}
      {hovered && <HaloOrb color={s.color} />}

      {/* Card inner */}
      <div style={{
        position: "relative", zIndex: 1,
        background: "rgba(15,23,42,0.95)",
        border: `1px solid rgba(${hexToRgb(s.color)},${hovered ? 0.3 : 0.12})`,
        borderRadius: 18, padding: "32px 24px",
        textAlign: "center",
        backdropFilter: "blur(16px)",
        transition: "border-color 0.3s, box-shadow 0.3s",
        boxShadow: hovered ? `0 12px 40px rgba(${hexToRgb(s.color)},0.2), inset 0 0 30px rgba(${hexToRgb(s.color)},0.03)` : "none",
        overflow: "hidden",
      }}>
        {/* Radial glow behind number */}
        <div style={{
          position: "absolute", top: "30%", left: "50%", transform: "translate(-50%, -50%)",
          width: 120, height: 80,
          background: `radial-gradient(ellipse, rgba(${hexToRgb(s.color)},${hovered ? 0.15 : 0.06}) 0%, transparent 70%)`,
          pointerEvents: "none",
          transition: "all 0.4s",
        }} />

        {/* Icon */}
        <motion.div
          animate={hovered ? { scale: 1.15, rotate: -5 } : { scale: 1, rotate: 0 }}
          transition={{ type: "spring", stiffness: 400 }}
          style={{ fontSize: 32, marginBottom: 16 }}
        >
          {s.icon}
        </motion.div>

        {/* Counter */}
        <div style={{
          fontSize: 44, fontWeight: 900,
          color: s.color,
          lineHeight: 1, marginBottom: 10,
          fontVariantNumeric: "tabular-nums",
          letterSpacing: "-1px",
        }}>
          <AnimatedCounter value={s.value} suffix={s.suffix} inView={inView} />
        </div>

        {/* Label */}
        <div style={{ fontSize: 13, fontWeight: 700, color: "#e2e8f0", marginBottom: 4 }}>
          {s.label}
        </div>
        <div style={{ fontSize: 11, color: "#475569", letterSpacing: "0.05em" }}>{s.sub}</div>

        {/* Bottom gradient line */}
        <div style={{
          position: "absolute", bottom: 0, left: 0, right: 0, height: 2,
          background: `linear-gradient(90deg, transparent, rgba(${hexToRgb(s.color)},${hovered ? 0.7 : 0.25}), transparent)`,
          transition: "all 0.4s",
        }} />
      </div>
    </motion.div>
  );
}

function hexToRgb(hex) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `${r},${g},${b}`;
}

const THREAT_BARS = [
  { label: "Фишинг", pct: 38, color: "#ef4444" },
  { label: "Алаяқтық / Scam", pct: 24, color: "#f97316" },
  { label: "Қаржылық пирамида", pct: 18, color: "#f59e0b" },
  { label: "Зиянды БҚ", pct: 12, color: "#8b5cf6" },
  { label: "Басқа", pct: 8, color: "#64748b" },
];

export default function StatsSection() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <section id="stats" style={{ padding: "100px 24px", maxWidth: 1200, margin: "0 auto" }}>
      {/* Header */}
      <motion.div
        ref={ref}
        initial={{ opacity: 0, y: 30 }}
        animate={inView ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.7 }}
        style={{ textAlign: "center", marginBottom: 64 }}
      >
        <div style={{
          display: "inline-flex", alignItems: "center", gap: 8,
          padding: "5px 16px", borderRadius: 20,
          background: "rgba(239,68,68,0.08)", border: "1px solid rgba(239,68,68,0.25)",
          fontSize: 11, color: "#fca5a5", marginBottom: 20,
          letterSpacing: "0.15em", fontWeight: 700,
        }}>
          СТАТИСТИКА
        </div>
        <h2 style={{ fontSize: "clamp(28px,4vw,48px)", fontWeight: 900, lineHeight: 1.1, marginBottom: 16 }}>
          Нақты{" "}
          <span style={{
            background: "linear-gradient(135deg, #ef4444, #f97316)",
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
          }}>
            сандар
          </span>
        </h2>
        <p style={{ fontSize: 16, color: "#94a3b8", maxWidth: 440, margin: "0 auto" }}>
          Қолданушылар деректері негізіндегі нақты уақыт статистикасы
        </p>
      </motion.div>

      {/* Stat cards */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
        gap: 20, marginBottom: 80,
      }}>
        {statCards.map((s, i) => (
          <StatCard key={i} s={s} inView={inView} />
        ))}
      </div>

      {/* Threat breakdown */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={inView ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.7, delay: 0.5 }}
        style={{
          background: "rgba(15,23,42,0.7)", borderRadius: 20, padding: "32px 36px",
          border: "1px solid rgba(255,255,255,0.06)",
          backdropFilter: "blur(16px)",
          position: "relative", overflow: "hidden",
        }}
      >
        {/* Background grid */}
        <div style={{
          position: "absolute", inset: 0, pointerEvents: "none", borderRadius: 20,
          backgroundImage: "linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px)",
          backgroundSize: "24px 24px",
        }} />

        <div style={{ position: "relative", zIndex: 1 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 28 }}>
            <span style={{ fontSize: 20 }}>🎯</span>
            <h3 style={{ fontSize: 17, fontWeight: 800, color: "#f1f5f9" }}>
              Қауіп түрлері бойынша бөлінім
            </h3>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
            {THREAT_BARS.map((item, i) => (
              <div key={i}>
                <div style={{
                  display: "flex", justifyContent: "space-between",
                  marginBottom: 7, fontSize: 13,
                }}>
                  <span style={{ color: "#94a3b8", fontWeight: 500 }}>{item.label}</span>
                  <motion.span
                    initial={{ opacity: 0 }}
                    animate={inView ? { opacity: 1 } : {}}
                    transition={{ delay: 0.8 + i * 0.12 }}
                    style={{ color: item.color, fontWeight: 800, fontSize: 13 }}
                  >
                    {item.pct}%
                  </motion.span>
                </div>
                <div style={{
                  height: 8, borderRadius: 4,
                  background: "rgba(255,255,255,0.04)",
                  overflow: "hidden",
                  position: "relative",
                }}>
                  <motion.div
                    initial={{ width: 0 }}
                    animate={inView ? { width: `${item.pct}%` } : {}}
                    transition={{ duration: 1.2, delay: 0.7 + i * 0.12, ease: [0.25, 0.46, 0.45, 0.94] }}
                    style={{
                      height: "100%", borderRadius: 4,
                      background: `linear-gradient(90deg, ${item.color}cc, ${item.color})`,
                      position: "relative",
                    }}
                  >
                    {/* Shimmer */}
                    <motion.div
                      animate={{ x: ["-100%", "200%"] }}
                      transition={{ duration: 2, delay: 1.5 + i * 0.12, repeat: Infinity, repeatDelay: 4 }}
                      style={{
                        position: "absolute", inset: 0, width: "40%",
                        background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent)",
                      }}
                    />
                  </motion.div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    </section>
  );
}
