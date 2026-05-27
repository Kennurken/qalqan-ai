import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const links = [
    { href: "#features", label: "Мүмкіндіктер" },
    { href: "#how", label: "Қалай жұмыс істейді" },
    { href: "#stats", label: "Статистика" },
    { href: "#install", label: "Орнату" },
  ];

  return (
    <motion.nav
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      style={{
        position: "fixed", top: 0, left: 0, right: 0, zIndex: 100,
        padding: "0 24px",
        background: scrolled ? "rgba(2,6,23,0.92)" : "transparent",
        backdropFilter: scrolled ? "blur(20px)" : "none",
        borderBottom: scrolled ? "1px solid rgba(51,65,85,0.5)" : "none",
        transition: "all 0.3s ease",
      }}
    >
      <div style={{
        maxWidth: 1200, margin: "0 auto",
        display: "flex", alignItems: "center", justifyContent: "space-between",
        height: 64,
      }}>
        {/* Logo */}
        <a href="#" style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 28 }}>🛡️</span>
          <div>
            <div style={{ fontSize: 18, fontWeight: 800, letterSpacing: 1 }}>QALQAN AI</div>
            <div style={{ fontSize: 9, color: "var(--text3)", letterSpacing: 2 }}>CYBER SHIELD</div>
          </div>
        </a>

        {/* Desktop links */}
        <div style={{ display: "flex", gap: 32, alignItems: "center" }} className="desktop-nav">
          {links.map((l) => (
            <a key={l.href} href={l.href} style={{
              fontSize: 14, color: "var(--text2)",
              transition: "color 0.2s",
            }}
              onMouseEnter={e => e.target.style.color = "var(--text)"}
              onMouseLeave={e => e.target.style.color = "var(--text2)"}
            >
              {l.label}
            </a>
          ))}
          <a
            href="https://chromewebstore.google.com"
            target="_blank" rel="noopener noreferrer"
            style={{
              padding: "8px 20px", borderRadius: 8,
              background: "linear-gradient(135deg, #3b82f6, #6366f1)",
              color: "white", fontSize: 13, fontWeight: 700,
            }}
          >
            Орнату →
          </a>
        </div>

        {/* Mobile burger */}
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          style={{
            display: "none", background: "none", border: "none",
            color: "var(--text)", cursor: "pointer", fontSize: 22,
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
              background: "var(--bg2)", borderBottom: "1px solid var(--border)",
              overflow: "hidden",
            }}
          >
            <div style={{ padding: "16px 24px", display: "flex", flexDirection: "column", gap: 16 }}>
              {links.map((l) => (
                <a key={l.href} href={l.href}
                  onClick={() => setMenuOpen(false)}
                  style={{ fontSize: 15, color: "var(--text2)" }}
                >
                  {l.label}
                </a>
              ))}
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
