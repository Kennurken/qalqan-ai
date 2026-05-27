import { motion } from "framer-motion";
import { useInView } from "framer-motion";
import { useRef } from "react";

const steps = [
  { n: "1", text: "Chrome Web Store-ге өтіңіз", icon: "🌐" },
  { n: "2", text: '"QALQAN AI" деп іздеңіз', icon: "🔍" },
  { n: "3", text: '"Орнату" батырмасын басыңыз', icon: "📥" },
  { n: "4", text: "Кеңейтім белгішесін басыңыз", icon: "🛡️" },
];

export default function InstallSection() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <section id="install" style={{ padding: "100px 24px" }}>
      <div style={{ maxWidth: 900, margin: "0 auto" }}>
        {/* Main CTA card */}
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 40 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          style={{
            background: "linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.9))",
            border: "1px solid rgba(99,102,241,0.3)",
            borderRadius: 24, padding: "60px 40px",
            textAlign: "center", position: "relative", overflow: "hidden",
          }}
        >
          {/* Background glow */}
          <div style={{
            position: "absolute", top: "50%", left: "50%",
            transform: "translate(-50%, -50%)",
            width: 500, height: 300,
            background: "radial-gradient(ellipse, rgba(99,102,241,0.15) 0%, transparent 70%)",
            pointerEvents: "none",
          }} />

          <motion.div
            animate={{ rotate: [0, 5, -5, 0] }}
            transition={{ duration: 4, repeat: Infinity }}
            style={{ fontSize: 64, marginBottom: 24, display: "inline-block" }}
          >
            🛡️
          </motion.div>

          <h2 style={{ fontSize: "clamp(28px,4vw,44px)", fontWeight: 900, marginBottom: 16 }}>
            Бүгін{" "}<span className="gradient-text">орнатыңыз</span>
            {" "}— тегін
          </h2>
          <p style={{ fontSize: 16, color: "var(--text2)", maxWidth: 500, margin: "0 auto 48px" }}>
            Қазақстанның 1-ші AI-негізделген киберқорғаныс кеңейтімі.
            Орнату — 30 секунд. Жұмыс — автоматты.
          </p>

          {/* Steps */}
          <div style={{
            display: "flex", gap: 0, justifyContent: "center",
            marginBottom: 48, flexWrap: "wrap",
          }}>
            {steps.map((s, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={inView ? { opacity: 1, y: 0 } : {}}
                transition={{ delay: 0.3 + i * 0.1 }}
                style={{
                  display: "flex", alignItems: "center",
                }}
              >
                <div style={{ textAlign: "center", width: 140 }}>
                  <div style={{
                    width: 48, height: 48, borderRadius: "50%",
                    background: "rgba(99,102,241,0.15)", border: "1px solid rgba(99,102,241,0.3)",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: 22, margin: "0 auto 10px",
                  }}>
                    {s.icon}
                  </div>
                  <div style={{ fontSize: 11, color: "#a5b4fc", fontWeight: 700, marginBottom: 4 }}>
                    ҚАДАМ {s.n}
                  </div>
                  <div style={{ fontSize: 12, color: "var(--text2)", lineHeight: 1.4 }}>{s.text}</div>
                </div>
                {i < steps.length - 1 && (
                  <div style={{ color: "var(--text3)", fontSize: 18, padding: "0 8px", marginBottom: 24 }}>
                    →
                  </div>
                )}
              </motion.div>
            ))}
          </div>

          {/* Buttons */}
          <div style={{ display: "flex", gap: 16, justifyContent: "center", flexWrap: "wrap" }}>
            <motion.a
              href="https://github.com/Kennurken/qalqan-ai"
              target="_blank" rel="noopener noreferrer"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
              style={{
                display: "inline-flex", alignItems: "center", gap: 10,
                padding: "16px 36px", borderRadius: 14,
                background: "linear-gradient(135deg, #3b82f6, #6366f1)",
                color: "white", fontWeight: 800, fontSize: 16,
                boxShadow: "0 8px 32px rgba(99,102,241,0.4)",
              }}
            >
              <span>🛡️</span> Chrome-ге орнату
            </motion.a>
            <motion.a
              href="https://github.com/Kennurken/qalqan-ai"
              target="_blank" rel="noopener noreferrer"
              whileHover={{ scale: 1.05 }}
              style={{
                display: "inline-flex", alignItems: "center", gap: 10,
                padding: "16px 28px", borderRadius: 14,
                border: "1px solid var(--border)",
                color: "var(--text2)", fontWeight: 600, fontSize: 15,
              }}
            >
              <span>⭐</span> GitHub
            </motion.a>
          </div>

          <p style={{ marginTop: 24, fontSize: 12, color: "var(--text3)" }}>
            Chrome 90+ • Тегін • Жарнамасыз • Ашық бастапқы код
          </p>
        </motion.div>
      </div>
    </section>
  );
}
