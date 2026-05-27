import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

const NAV_LINKS = [
  { href: "#features", label: "Мүмкіндіктер", id: "features" },
  { href: "#how", label: "Қалай жұмыс", id: "how" },
  { href: "#stats", label: "Статистика", id: "stats" },
  { href: "#demo", label: "Демо", id: "demo" },
  { href: "#tech", label: "Технологиялар", id: "tech" },
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [activeSection, setActiveSection] = useState("");

  useEffect(() => {
    const onScroll = () => {
      setScrolled(window.scrollY > 40);

      // Active section tracking
      const sections = NAV_LINKS.map(l => l.id);
      let current = "";
      for (const id of sections) {
        const el = document.getElementById(id);
        if (el) {
          const rect = el.getBoundingClientRect();
          if (rect.top <= 100) current = id;
        }
      }
      setActiveSection(current);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <motion.nav
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      style={{
        position: "fixed", top: 0, left: 0, right: 0, zIndex: 100,
        padding: "0 24px",
        background: scrolled ? "rgba(2,6,23,0.88)" : "transparent",
        backdropFilter: scrolled ? "blur(24px)" : "none",
        borderBottom: scrolled ? "1px solid rgba(255,255,255,0.06)" : "none",
        transition: "all 0.35s ease",
      }}
    >
      {/* Bottom progress bar */}
      {scrolled && (
        <motion.div
          style={{
            position: "absolute", bottom: 0, left: 0,
            height: 1,
            background: "linear-gradient(90deg, #3b82f6, #6366f1, #a78bfa)",
            width: `${Math.min((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100, 100)}%`,
          }}
        />
      )}

      <div style={{
        maxWidth: 1200, margin: "0 auto",
        display: "flex", alignItems: "center", justifyContent: "space-between",
        height: 64,
      }}>
        {/* Logo */}
        <a href="#" style={{
          display: "flex", alignItems: "center", gap: 10, textDecoration: "none",
        }}>
          <motion.span
            whileHover={{ rotate: [-5, 5, 0] }}
            transition={{ duration: 0.4 }}
            style={{ fontSize: 26, display: "inline-block" }}
          >
            🛡️
          </motion.span>
          <div>
            <div style={{
              fontSize: 17, fontWeight: 900, letterSpacing: "0.05em",
              background: "linear-gradient(135deg, #f8fafc, #94a3b8)",
              WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
            }}>
              QALQAN AI
            </div>
            <div style={{ fontSize: 8, color: "#334155", letterSpacing: "0.2em", fontWeight: 700 }}>
              CYBER SHIELD v5.0
            </div>
          </div>
        </a>

        {/* Desktop links */}
        <div style={{ display: "flex", gap: 4, alignItems: "center" }} className="desktop-nav">
          {NAV_LINKS.map((l) => (
            <a
              key={l.href}
              href={l.href}
              style={{
                position: "relative",
                fontSize: 13, fontWeight: 500,
                color: activeSection === l.id ? "#f8fafc" : "#64748b",
                padding: "6px 12px", borderRadius: 8,
                transition: "color 0.2s",
                textDecoration: "none",
              }}
              onMouseEnter={e => { e.currentTarget.style.color = "#f8fafc"; e.currentTarget.style.background = "rgba(255,255,255,0.05)"; }}
              onMouseLeave={e => {
                e.currentTarget.style.color = activeSection === l.id ? "#f8fafc" : "#64748b";
                e.currentTarget.style.background = "transparent";
              }}
            >
              {l.label}
              {activeSection === l.id && (
                <motion.div
                  layoutId="activeNav"
                  style={{
                    position: "absolute", inset: 0, borderRadius: 8,
                    background: "rgba(99,102,241,0.12)",
                    border: "1px solid rgba(99,102,241,0.2)",
                    zIndex: -1,
                  }}
                  transition={{ type: "spring", stiffness: 500, damping: 30 }}
                />
              )}
            </a>
          ))}

          <motion.a
            href="https://github.com/Kennurken/qalqan-ai"
            target="_blank" rel="noopener noreferrer"
            whileHover={{ scale: 1.05, boxShadow: "0 8px 24px rgba(99,102,241,0.45)" }}
            whileTap={{ scale: 0.97 }}
            style={{
              marginLeft: 8,
              padding: "8px 20px", borderRadius: 9,
              background: "linear-gradient(135deg, #3b82f6, #6366f1)",
              color: "white", fontSize: 13, fontWeight: 800,
              boxShadow: "0 4px 16px rgba(99,102,241,0.3)",
              textDecoration: "none",
            }}
          >
            Орнату →
          </motion.a>
        </div>

        {/* Mobile burger */}
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          style={{
            display: "none", background: "none", border: "none",
            color: "#94a3b8", cursor: "pointer", fontSize: 20, padding: 4,
          }}
          className="burger-btn"
        >
          {menuOpen ? "✕" : "☰"}
        </button>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {menuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            style={{
              background: "rgba(2,6,23,0.97)", backdropFilter: "blur(24px)",
              borderBottom: "1px solid rgba(255,255,255,0.06)",
              overflow: "hidden",
            }}
          >
            <div style={{ padding: "16px 24px 24px", display: "flex", flexDirection: "column", gap: 4 }}>
              {NAV_LINKS.map((l, i) => (
                <motion.a
                  key={l.href}
                  href={l.href}
                  initial={{ opacity: 0, x: -16 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  onClick={() => setMenuOpen(false)}
                  style={{
                    fontSize: 15, color: "#94a3b8", padding: "10px 12px",
                    borderRadius: 8, textDecoration: "none",
                  }}
                >
                  {l.label}
                </motion.a>
              ))}
              <motion.a
                href="https://github.com/Kennurken/qalqan-ai"
                target="_blank" rel="noopener noreferrer"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: NAV_LINKS.length * 0.05 + 0.05 }}
                style={{
                  marginTop: 8, padding: "12px 20px", borderRadius: 10,
                  background: "linear-gradient(135deg, #3b82f6, #6366f1)",
                  color: "white", fontSize: 14, fontWeight: 800,
                  textAlign: "center", textDecoration: "none",
                }}
              >
                🛡️ Орнату
              </motion.a>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <style>{`
        @media (max-width: 768px) {
          .desktop-nav { display: none !important; }
          .burger-btn { display: block !important; }
        }
      `}</style>
    </motion.nav>
  );
}
