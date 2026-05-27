import { motion } from "framer-motion";

const LINKS = [
  { label: "Мүмкіндіктер", href: "#features" },
  { label: "Қалай жұмыс", href: "#how" },
  { label: "Статистика", href: "#stats" },
  { label: "Демо", href: "#demo" },
  { label: "Технологиялар", href: "#tech" },
  { label: "GitHub", href: "https://github.com/Kennurken/qalqan-ai", external: true },
];

const TECH = ["FastAPI", "Vercel Edge", "Groq AI", "Gemini Vision", "PhishTank", "Google Safe Browsing", "URLhaus", "RDAP", "React", "Chrome MV3"];

export default function Footer() {
  return (
    <footer style={{
      position: "relative",
      borderTop: "1px solid rgba(255,255,255,0.06)",
      padding: "64px 24px 40px",
      background: "rgba(2,6,23,0.95)",
      overflow: "hidden",
    }}>
      {/* Top glow */}
      <div style={{
        position: "absolute", top: 0, left: "30%", right: "30%", height: 1,
        background: "linear-gradient(90deg, transparent, rgba(99,102,241,0.4), rgba(16,185,129,0.3), transparent)",
        pointerEvents: "none",
      }} />

      {/* Background orb */}
      <div style={{
        position: "absolute", bottom: -100, left: "50%", transform: "translateX(-50%)",
        width: 600, height: 300,
        background: "radial-gradient(ellipse, rgba(99,102,241,0.06) 0%, transparent 70%)",
        pointerEvents: "none",
      }} />

      <div style={{ maxWidth: 1200, margin: "0 auto", position: "relative" }}>
        {/* Top row: logo + links */}
        <div style={{
          display: "flex", justifyContent: "space-between", alignItems: "flex-start",
          marginBottom: 48, gap: 40, flexWrap: "wrap",
        }}>
          {/* Brand */}
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
              <span style={{ fontSize: 28 }}>🛡️</span>
              <div>
                <div style={{
                  fontSize: 18, fontWeight: 900, letterSpacing: "0.05em",
                  background: "linear-gradient(135deg, #f8fafc, #94a3b8)",
                  WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
                }}>
                  QALQAN AI
                </div>
                <div style={{ fontSize: 9, color: "#334155", letterSpacing: "0.2em", fontWeight: 700 }}>
                  CYBER SHIELD v5.0
                </div>
              </div>
            </div>
            <p style={{ fontSize: 13, color: "#475569", maxWidth: 240, lineHeight: 1.6, margin: 0 }}>
              Қазақстанның 1-ші AI-негізделген киберқорғаныс кеңейтімі.
              ДЭР Республикалық байқауы 2026.
            </p>
          </div>

          {/* Navigation */}
          <div>
            <div style={{ fontSize: 10, fontWeight: 800, color: "#334155", letterSpacing: "0.15em", marginBottom: 14 }}>
              НАВИГАЦИЯ
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {LINKS.map((l) => (
                <a
                  key={l.href}
                  href={l.href}
                  target={l.external ? "_blank" : undefined}
                  rel={l.external ? "noopener noreferrer" : undefined}
                  style={{
                    fontSize: 13, color: "#475569",
                    transition: "color 0.2s", textDecoration: "none",
                  }}
                  onMouseEnter={e => e.currentTarget.style.color = "#94a3b8"}
                  onMouseLeave={e => e.currentTarget.style.color = "#475569"}
                >
                  {l.label} {l.external && "↗"}
                </a>
              ))}
            </div>
          </div>

          {/* Competition info */}
          <div style={{
            background: "rgba(99,102,241,0.06)",
            border: "1px solid rgba(99,102,241,0.15)",
            borderRadius: 16, padding: "20px 24px",
            maxWidth: 240,
          }}>
            <div style={{ fontSize: 10, fontWeight: 800, color: "#6366f1", letterSpacing: "0.15em", marginBottom: 10 }}>
              ДЭР БАЙҚАУЫ
            </div>
            <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.6 }}>
              <div style={{ marginBottom: 6 }}>📅 2026 жылы 22 мамыр</div>
              <div style={{ marginBottom: 6 }}>🏆 Республикалық кезең</div>
              <div style={{ marginBottom: 6 }}>🇰🇿 Қазақстан</div>
              <div>🧑‍💻 Автор: Елдос Кыдырбек</div>
            </div>
          </div>
        </div>

        {/* Tech badges */}
        <div style={{
          display: "flex", gap: 6, flexWrap: "wrap",
          marginBottom: 32,
          paddingTop: 24,
          borderTop: "1px solid rgba(255,255,255,0.04)",
        }}>
          <span style={{ fontSize: 10, color: "#334155", letterSpacing: "0.1em", fontWeight: 700, marginRight: 4, alignSelf: "center" }}>
            STACK:
          </span>
          {TECH.map(tech => (
            <span key={tech} style={{
              fontSize: 10, padding: "3px 10px", borderRadius: 20,
              background: "rgba(30,41,59,0.6)",
              border: "1px solid rgba(255,255,255,0.05)",
              color: "#475569",
            }}>
              {tech}
            </span>
          ))}
        </div>

        {/* Bottom row */}
        <div style={{
          display: "flex", justifyContent: "space-between", alignItems: "center",
          flexWrap: "wrap", gap: 12,
        }}>
          <div style={{ fontSize: 12, color: "#334155" }}>
            © 2025–2026 QALQAN AI. Made with ❤️ in Kazakhstan 🇰🇿
          </div>
          <div style={{ display: "flex", gap: 16 }}>
            <motion.a
              href="https://github.com/Kennurken/qalqan-ai"
              target="_blank" rel="noopener noreferrer"
              whileHover={{ scale: 1.05 }}
              style={{
                fontSize: 11, color: "#475569",
                padding: "5px 14px", borderRadius: 8,
                border: "1px solid rgba(255,255,255,0.06)",
                textDecoration: "none",
                transition: "color 0.2s",
              }}
              onMouseEnter={e => e.currentTarget.style.color = "#94a3b8"}
              onMouseLeave={e => e.currentTarget.style.color = "#475569"}
            >
              ⭐ GitHub
            </motion.a>
            <motion.a
              href="https://github.com/Kennurken/qalqan-ai"
              target="_blank" rel="noopener noreferrer"
              whileHover={{ scale: 1.05 }}
              style={{
                fontSize: 11, color: "white",
                padding: "5px 14px", borderRadius: 8,
                background: "linear-gradient(135deg, #3b82f6, #6366f1)",
                textDecoration: "none",
              }}
            >
              🛡️ Орнату
            </motion.a>
          </div>
        </div>
      </div>
    </footer>
  );
}
