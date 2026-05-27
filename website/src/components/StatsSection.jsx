import { motion, useInView, useMotionValue, useTransform, animate } from "framer-motion";
import { useRef, useEffect } from "react";

function AnimatedCounter({ value, suffix = "", duration = 2 }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true });
  const count = useMotionValue(0);

  useEffect(() => {
    if (inView) {
      const num = parseFloat(value);
      const controls = animate(count, num, {
        duration,
        ease: "easeOut",
        onUpdate(v) {
          if (ref.current) {
            const display = Number.isInteger(num)
              ? Math.round(v).toString()
              : v.toFixed(1);
            ref.current.textContent = display + suffix;
          }
        },
      });
      return controls.stop;
    }
  }, [inView, value, suffix, duration, count]);

  return <span ref={ref}>0{suffix}</span>;
}

const statCards = [
  {
    value: "50000", suffix: "+",
    label: "Жалпы тексерілген URL",
    sub: "Kazakhstan users",
    color: "#3b82f6",
    icon: "🔍",
  },
  {
    value: "4200", suffix: "+",
    label: "Бұғатталған сайт",
    sub: "Dangerous sites blocked",
    color: "#ef4444",
    icon: "⛔",
  },
  {
    value: "97", suffix: "%",
    label: "Анықтау дәлдігі",
    sub: "Detection accuracy",
    color: "#10b981",
    icon: "✅",
  },
  {
    value: "0.8", suffix: "s",
    label: "Орташа тексеру уақыты",
    sub: "Average check time",
    color: "#f59e0b",
    icon: "⚡",
  },
];

export default function StatsSection() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <section id="stats" style={{ padding: "100px 24px", maxWidth: 1200, margin: "0 auto" }}>
      {/* Title */}
      <motion.div
        ref={ref}
        initial={{ opacity: 0, y: 30 }}
        animate={inView ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.7 }}
        style={{ textAlign: "center", marginBottom: 64 }}
      >
        <div style={{
          display: "inline-block", padding: "4px 14px", borderRadius: 20,
          background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)",
          fontSize: 12, color: "#fca5a5", marginBottom: 16, letterSpacing: 1,
        }}>
          СТАТИСТИКА
        </div>
        <h2 style={{ fontSize: "clamp(28px,4vw,44px)", fontWeight: 900 }}>
          Нақты{" "}<span className="gradient-red">сандар</span>
        </h2>
      </motion.div>

      {/* Stat cards */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
        gap: 24, marginBottom: 80,
      }}>
        {statCards.map((s, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={inView ? { opacity: 1, scale: 1 } : {}}
            transition={{ duration: 0.5, delay: 0.1 + i * 0.1 }}
            style={{
              background: "rgba(30,41,59,0.5)",
              border: `1px solid ${s.color}22`,
              borderRadius: 20, padding: "32px 24px", textAlign: "center",
              backdropFilter: "blur(12px)",
            }}
            whileHover={{ scale: 1.04, boxShadow: `0 8px 32px ${s.color}20` }}
          >
            <div style={{ fontSize: 36, marginBottom: 12 }}>{s.icon}</div>
            <div style={{
              fontSize: 42, fontWeight: 900, color: s.color,
              lineHeight: 1, marginBottom: 8,
            }}>
              <AnimatedCounter value={s.value} suffix={s.suffix} />
            </div>
            <div style={{ fontSize: 14, fontWeight: 600, color: "var(--text)", marginBottom: 4 }}>
              {s.label}
            </div>
            <div style={{ fontSize: 12, color: "var(--text3)" }}>{s.sub}</div>
          </motion.div>
        ))}
      </div>

      {/* Threat breakdown bar */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={inView ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.7, delay: 0.5 }}
        style={{
          background: "rgba(30,41,59,0.4)", borderRadius: 20, padding: 32,
          border: "1px solid var(--border)",
        }}
      >
        <h3 style={{ fontSize: 18, fontWeight: 700, marginBottom: 24, color: "var(--text)" }}>
          🎯 Қауіп түрлері бойынша бөлінім
        </h3>
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          {[
            { label: "Фишинг", pct: 38, color: "#ef4444" },
            { label: "Алаяқтық / Scam", pct: 24, color: "#f97316" },
            { label: "Қаржылық пирамида", pct: 18, color: "#f59e0b" },
            { label: "Зиянды БҚ", pct: 12, color: "#8b5cf6" },
            { label: "Басқа", pct: 8, color: "#64748b" },
          ].map((item, i) => (
            <div key={i}>
              <div style={{
                display: "flex", justifyContent: "space-between",
                marginBottom: 6, fontSize: 13,
              }}>
                <span style={{ color: "var(--text2)" }}>{item.label}</span>
                <span style={{ color: item.color, fontWeight: 700 }}>{item.pct}%</span>
              </div>
              <div style={{
                height: 8, borderRadius: 4,
                background: "rgba(255,255,255,0.05)",
                overflow: "hidden",
              }}>
                <motion.div
                  initial={{ width: 0 }}
                  animate={inView ? { width: `${item.pct}%` } : {}}
                  transition={{ duration: 1, delay: 0.7 + i * 0.12, ease: "easeOut" }}
                  style={{
                    height: "100%", borderRadius: 4,
                    background: `linear-gradient(90deg, ${item.color}, ${item.color}99)`,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </section>
  );
}
