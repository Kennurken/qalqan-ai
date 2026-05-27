import { motion } from "framer-motion";

export default function Footer() {
  return (
    <footer style={{
      borderTop: "1px solid var(--border)",
      padding: "48px 24px",
      background: "rgba(15,23,42,0.8)",
    }}>
      <div style={{
        maxWidth: 1200, margin: "0 auto",
        display: "flex", flexDirection: "column", alignItems: "center",
        gap: 24, textAlign: "center",
      }}>
        {/* Logo */}
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 28 }}>🛡️</span>
          <div>
            <div style={{ fontSize: 18, fontWeight: 800 }}>QALQAN AI</div>
            <div style={{ fontSize: 9, color: "var(--text3)", letterSpacing: 2 }}>CYBER SHIELD v5.0</div>
          </div>
        </div>

        {/* Links */}
        <div style={{ display: "flex", gap: 32, flexWrap: "wrap", justifyContent: "center" }}>
          {[
            { href: "#features", label: "Мүмкіндіктер" },
            { href: "#how", label: "Қалай жұмыс істейді" },
            { href: "#stats", label: "Статистика" },
            { href: "https://github.com/Kennurken/qalqan-ai", label: "GitHub" },
          ].map((l) => (
            <a key={l.href} href={l.href}
              style={{ fontSize: 13, color: "var(--text3)", transition: "color 0.2s" }}
              onMouseEnter={e => e.target.style.color = "var(--text2)"}
              onMouseLeave={e => e.target.style.color = "var(--text3)"}
            >
              {l.label}
            </a>
          ))}
        </div>

        {/* Tech badges */}
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", justifyContent: "center" }}>
          {["FastAPI", "Vercel", "Groq AI", "Gemini", "PhishTank", "Chrome Extension", "React"].map(t => (
            <span key={t} style={{
              fontSize: 10, padding: "3px 10px", borderRadius: 20,
              background: "rgba(30,41,59,0.8)", border: "1px solid var(--border)",
              color: "var(--text3)",
            }}>{t}</span>
          ))}
        </div>

        <div style={{ fontSize: 12, color: "var(--text3)" }}>
          Made with ❤️ in Kazakhstan 🇰🇿 • ДЭР Республикалық байқауы 2026
        </div>
      </div>
    </footer>
  );
}
