import { motion, useInView } from "framer-motion";
import { useRef, useState } from "react";

const STACKS = [
  {
    category: "EXTENSION",
    color: "59,130,246",
    items: [
      { name: "Chrome MV3", desc: "Service Worker + Content Scripts", icon: "🌐" },
      { name: "React 18", desc: "Popup UI + hooks", icon: "⚛️" },
      { name: "Framer Motion", desc: "Smooth animations", icon: "🎬" },
      { name: "IndexedDB / Local Storage", desc: "Offline cache + history", icon: "💾" },
    ],
  },
  {
    category: "BACKEND API",
    color: "16,185,129",
    items: [
      { name: "FastAPI", desc: "Python async REST API", icon: "⚡" },
      { name: "Vercel Serverless", desc: "Edge deploy, auto-scale", icon: "▲" },
      { name: "RDAP Protocol", desc: "Domain age + registration", icon: "🔎" },
      { name: "SSL/TLS Inspector", desc: "Certificate analysis", icon: "🔒" },
    ],
  },
  {
    category: "AI & INTELLIGENCE",
    color: "99,102,241",
    items: [
      { name: "Groq Llama 3.3", desc: "70B — URL + content NLP", icon: "🤖" },
      { name: "Gemini Vision", desc: "Screenshot fraud detection", icon: "👁️" },
      { name: "XLM-RoBERTa", desc: "Fine-tuned KZ phishing classifier", icon: "🧠" },
      { name: "XAI / SHAP", desc: "Explainable risk factors", icon: "📊" },
    ],
  },
  {
    category: "THREAT INTELLIGENCE",
    color: "239,68,68",
    items: [
      { name: "PhishTank API", desc: "Real-time phishing DB", icon: "🎣" },
      { name: "Google Safe Browsing", desc: "Known malicious URLs", icon: "🛡️" },
      { name: "URLhaus", desc: "Malware URL tracker", icon: "🦠" },
      { name: "KZ Intel DB", desc: "Kazakhstan-specific brands", icon: "🇰🇿" },
    ],
  },
];

function TechCard({ item, color, delay, inView }) {
  const [hovered, setHovered] = useState(false);
  return (
    <motion.div
      onHoverStart={() => setHovered(true)}
      onHoverEnd={() => setHovered(false)}
      initial={{ opacity: 0, y: 16 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.45, delay, ease: [0.21, 0.47, 0.32, 0.98] }}
      style={{
        display: "flex", alignItems: "flex-start", gap: 12,
        padding: "14px 16px", borderRadius: 12,
        background: hovered ? `rgba(${color},0.08)` : "rgba(255,255,255,0.02)",
        border: `1px solid rgba(${color},${hovered ? 0.25 : 0.08})`,
        transition: "all 0.25s",
        cursor: "default",
      }}
    >
      <div style={{
        width: 34, height: 34, borderRadius: 9, flexShrink: 0,
        background: `rgba(${color},0.12)`,
        display: "flex", alignItems: "center", justifyContent: "center",
        fontSize: 16,
        transition: "transform 0.2s",
        transform: hovered ? "scale(1.1)" : "none",
      }}>
        {item.icon}
      </div>
      <div>
        <div style={{ fontSize: 13, fontWeight: 700, color: "#e2e8f0", marginBottom: 2 }}>
          {item.name}
        </div>
        <div style={{ fontSize: 11, color: "#64748b", lineHeight: 1.4 }}>{item.desc}</div>
      </div>
    </motion.div>
  );
}

function StackColumn({ stack, colIndex, inView }) {
  const [hovered, setHovered] = useState(false);
  return (
    <motion.div
      onHoverStart={() => setHovered(true)}
      onHoverEnd={() => setHovered(false)}
      initial={{ opacity: 0, y: 24 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay: colIndex * 0.1 }}
      style={{
        background: "rgba(15,23,42,0.8)",
        border: `1px solid rgba(${stack.color},${hovered ? 0.3 : 0.1})`,
        borderRadius: 20, padding: "24px 20px",
        backdropFilter: "blur(16px)",
        transition: "border-color 0.3s, box-shadow 0.3s",
        boxShadow: hovered ? `0 8px 32px rgba(${stack.color},0.12)` : "none",
        position: "relative", overflow: "hidden",
      }}
    >
      {/* Top accent */}
      <div style={{
        position: "absolute", top: 0, left: 0, right: 0, height: 2, borderRadius: "20px 20px 0 0",
        background: `linear-gradient(90deg, transparent, rgba(${stack.color},${hovered ? 0.7 : 0.35}), transparent)`,
        transition: "all 0.3s",
      }} />

      <div style={{
        fontSize: 10, fontWeight: 800, letterSpacing: "0.18em",
        color: `rgb(${stack.color})`, marginBottom: 16, opacity: 0.8,
      }}>
        {stack.category}
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        {stack.items.map((item, i) => (
          <TechCard
            key={i}
            item={item}
            color={stack.color}
            delay={colIndex * 0.1 + i * 0.06}
            inView={inView}
          />
        ))}
      </div>
    </motion.div>
  );
}

export default function TechStack() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <section id="tech" style={{
      padding: "100px 24px",
      background: "linear-gradient(180deg, transparent, rgba(15,23,42,0.4), transparent)",
    }}>
      <div style={{ maxWidth: 1200, margin: "0 auto" }}>
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
            background: "rgba(99,102,241,0.08)", border: "1px solid rgba(99,102,241,0.25)",
            fontSize: 11, color: "#a5b4fc", marginBottom: 20,
            letterSpacing: "0.15em", fontWeight: 700,
          }}>
            ТЕХНОЛОГИЯЛАР
          </div>
          <h2 style={{ fontSize: "clamp(28px,4vw,48px)", fontWeight: 900, lineHeight: 1.1, marginBottom: 16 }}>
            Заманауи{" "}
            <span style={{
              background: "linear-gradient(135deg, #3b82f6, #6366f1, #a78bfa)",
              WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
            }}>
              технологиялар стек
            </span>
          </h2>
          <p style={{ fontSize: 16, color: "#94a3b8", maxWidth: 520, margin: "0 auto" }}>
            Кеңейтімнен AI-ға дейін — тек ең жылдам және сенімді шешімдер
          </p>
        </motion.div>

        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
          gap: 20,
        }}>
          {STACKS.map((stack, i) => (
            <StackColumn key={i} stack={stack} colIndex={i} inView={inView} />
          ))}
        </div>

        {/* Bottom stat row */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ delay: 0.8 }}
          style={{
            display: "flex", gap: 0, justifyContent: "center",
            marginTop: 60,
            background: "rgba(15,23,42,0.6)",
            border: "1px solid rgba(255,255,255,0.06)",
            borderRadius: 16, overflow: "hidden",
            flexWrap: "wrap",
          }}
        >
          {[
            { n: "16+", label: "Технологиялар", color: "#3b82f6" },
            { n: "12+", label: "Threat Intel DB", color: "#ef4444" },
            { n: "250+", label: "Офлайн домен", color: "#f59e0b" },
            { n: "3", label: "AI модельдер", color: "#a78bfa" },
          ].map((s, i, arr) => (
            <div key={i} style={{
              flex: 1, minWidth: 140, padding: "24px 20px", textAlign: "center",
              borderRight: i < arr.length - 1 ? "1px solid rgba(255,255,255,0.05)" : "none",
            }}>
              <div style={{
                fontSize: 28, fontWeight: 900, color: s.color,
                marginBottom: 4,
              }}>{s.n}</div>
              <div style={{ fontSize: 11, color: "#64748b", letterSpacing: "0.05em" }}>{s.label}</div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
