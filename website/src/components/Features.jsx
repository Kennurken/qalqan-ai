// Adapted from 21st.dev Bento Monochrome pattern + Framer Motion
import { useRef, useEffect, useState } from "react";
import { motion } from "framer-motion";

const features = [
  {
    icon: "", meta: "TIER 1-6", span: "lg:col-span-3 lg:row-span-2",
    title: "6 деңгейлі тексеру",
    desc: "Whitelist → Pyramid/KZ/Gambling DB → External DBs → Domain Intel → AI + XAI. Секундтың ішінде — офлайннан AI-ға дейін. 35+ URL белгілері.",
    tags: ["PhishTank", "SafeBrowsing", "URLhaus", "Gambling DB", "KZ Intel"],
    color: "59,130,246",
    large: true,
  },
  {
    icon: "", meta: "KZ INTEL",
    title: "KZ брендтері",
    desc: "eGov, Kaspi, Halyk, Jysan жалған клондарын мгновенды анықтайды.",
    tags: ["egov.kz", "kaspi.kz"],
    color: "16,185,129",
  },
  {
    icon: "", meta: "AI",
    title: "Groq + Gemini Vision",
    desc: "Скриншоттан алаяқтықты анықтайды. XAI факторлар береді.",
    tags: ["Groq Llama", "Gemini"],
    color: "99,102,241",
  },
  {
    icon: "", meta: "OFFLINE",
    title: "Офлайн тексеру",
    desc: "200+ белгілі домен. API-сыз, 0ms нәтиже.",
    tags: ["0ms", "200+ domains"],
    color: "245,158,11",
  },
  {
    icon: "", meta: "RDAP + SSL",
    title: "Domain Intel",
    desc: "Домен жасы, SSL сертификат, Let's Encrypt анықтауы.",
    tags: ["RDAP", "SSL Check"],
    color: "139,92,246",
  },
  {
    icon: "", meta: "XAI",
    title: "Түсіндіру жүйесі",
    desc: "SHAP/LIME стилінде — неге қауіпті, қандай факторлар.",
    tags: ["Explainability", "95%+ conf"],
    color: "239,68,68",
  },
  {
    icon: "", meta: "GAMBLING DB",
    title: "Лицензиясыз сайттар",
    desc: "50+ тыйым салынған онлайн казино мен букмекерлер. 1xbet, Mostbet, PIN-UP, Vavada және т.б.",
    tags: ["Gambling", "Bookmaker", "KZ ban"],
    color: "234,179,8",
  },
  {
    icon: "", meta: "SCANNER",
    title: "Link Scanner",
    desc: "Беттегі 15 URL параллель тексеру. CSV + JSON экспорт.",
    tags: ["Batch", "CSV", "Export"],
    color: "14,165,233",
  },
  {
    icon: "", meta: "I18N", span: "lg:col-span-2",
    title: "3 тіл",
    desc: "Интерфейс, нәтижелер, себептер — қазақ, орыс, ағылшын тілдерінде.",
    tags: ["KK", "RU", "EN"],
    color: "34,197,94",
  },
];

function BentoCard({ icon, meta, title, desc, tags, color, large, span, index, isVisible }) {
  const [hovered, setHovered] = useState(false);
  const [mousePos, setMousePos] = useState({ x: 50, y: 50 });
  const cardRef = useRef(null);

  const handleMouseMove = (e) => {
    const rect = cardRef.current?.getBoundingClientRect();
    if (!rect) return;
    setMousePos({
      x: ((e.clientX - rect.left) / rect.width) * 100,
      y: ((e.clientY - rect.top) / rect.height) * 100,
    });
  };

  return (
    <motion.article
      ref={cardRef}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onMouseMove={handleMouseMove}
      initial={{ opacity: 0, y: 24, scale: 0.96 }}
      animate={isVisible ? { opacity: 1, y: 0, scale: 1 } : {}}
      transition={{ duration: 0.55, delay: index * 0.07, ease: [0.21, 0.47, 0.32, 0.98] }}
      style={{
        gridColumn: span || undefined,
        position: "relative",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: large ? 32 : 24,
        borderRadius: 20,
        background: "rgba(15,23,42,0.85)",
        border: `1px solid rgba(${color},${hovered ? 0.35 : 0.12})`,
        overflow: "hidden",
        cursor: "default",
        transition: "border-color 0.3s, transform 0.3s, box-shadow 0.3s",
        transform: hovered ? "translateY(-3px)" : "none",
        boxShadow: hovered ? `0 12px 40px rgba(${color},0.18)` : "none",
        backdropFilter: "blur(16px)",
      }}
    >
      {/* Radial spotlight on hover */}
      {hovered && (
        <div style={{
          position: "absolute", inset: 0, pointerEvents: "none", borderRadius: 20,
          background: `radial-gradient(200px circle at ${mousePos.x}% ${mousePos.y}%, rgba(${color},0.08), transparent 70%)`,
          transition: "background 0.1s",
        }} />
      )}

      {/* Subtle grid bg */}
      <div style={{
        position: "absolute", inset: 0, borderRadius: 20, pointerEvents: "none",
        backgroundImage: `linear-gradient(rgba(${color},0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(${color},0.03) 1px, transparent 1px)`,
        backgroundSize: "20px 20px",
      }} />

      <div style={{ position: "relative", zIndex: 1 }}>
        {/* Meta + icon row */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
          <span style={{
            fontSize: 10, letterSpacing: "0.2em", color: `rgb(${color})`,
            fontWeight: 700, opacity: 0.8,
          }}>
            {meta}
          </span>
          <div style={{
            width: large ? 56 : 44, height: large ? 56 : 44,
            borderRadius: 14,
            background: `rgba(${color},0.12)`,
            border: `1px solid rgba(${color},0.25)`,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: large ? 26 : 20,
            transition: "transform 0.3s",
            transform: hovered ? "scale(1.1) rotate(-4deg)" : "none",
          }}>
            {icon}
          </div>
        </div>

        <h3 style={{
          fontSize: large ? 22 : 16,
          fontWeight: 800, color: "#f1f5f9",
          marginBottom: 10, lineHeight: 1.25,
        }}>
          {title}
        </h3>
        <p style={{
          fontSize: 13, color: "#94a3b8",
          lineHeight: 1.65, marginBottom: 16,
          maxWidth: large ? 400 : "none",
        }}>
          {desc}
        </p>
      </div>

      {/* Tags */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6, position: "relative", zIndex: 1 }}>
        {tags.map((t, i) => (
          <span key={i} style={{
            fontSize: 10, padding: "3px 10px", borderRadius: 20,
            background: `rgba(${color},0.1)`,
            color: `rgb(${color})`,
            border: `1px solid rgba(${color},0.2)`,
            fontWeight: 600,
            letterSpacing: "0.05em",
          }}>
            {t}
          </span>
        ))}
      </div>

      {/* Bottom accent line */}
      <div style={{
        position: "absolute", bottom: 0, left: 0, right: 0, height: 2, borderRadius: "0 0 20px 20px",
        background: `linear-gradient(90deg, transparent, rgba(${color},${hovered ? 0.6 : 0.2}), transparent)`,
        transition: "opacity 0.3s",
      }} />
    </motion.article>
  );
}

export default function Features() {
  const ref = useRef(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const obs = new IntersectionObserver(
      ([e]) => { if (e.isIntersecting) { setIsVisible(true); obs.disconnect(); } },
      { threshold: 0.1 }
    );
    if (ref.current) obs.observe(ref.current);
    return () => obs.disconnect();
  }, []);

  return (
    <section id="features" style={{ padding: "100px 24px", maxWidth: 1200, margin: "0 auto" }}>
      {/* Header */}
      <motion.div
        ref={ref}
        initial={{ opacity: 0, y: 30 }}
        animate={isVisible ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.7 }}
        style={{ textAlign: "center", marginBottom: 64 }}
      >
        <div style={{
          display: "inline-flex", alignItems: "center", gap: 8,
          padding: "5px 16px", borderRadius: 20,
          background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.3)",
          fontSize: 11, color: "#a5b4fc", marginBottom: 20,
          letterSpacing: "0.15em", fontWeight: 700,
        }}>
          МҮМКІНДІКТЕР
        </div>
        <h2 style={{
          fontSize: "clamp(28px,4vw,48px)", fontWeight: 900,
          lineHeight: 1.1, marginBottom: 16,
        }}>
          Толық{" "}
          <span style={{
            background: "linear-gradient(135deg, #3b82f6, #6366f1, #8b5cf6)",
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
          }}>
            киберқорғаныс
          </span>
        </h2>
        <p style={{ fontSize: 16, color: "#94a3b8", maxWidth: 520, margin: "0 auto" }}>
          Бір кеңейтімде — 10+ threat intelligence дерек көзі, жасанды интеллект, офлайн тексеру
        </p>
      </motion.div>

      {/* Bento Grid */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(5, 1fr)",
        gridAutoRows: "minmax(160px, auto)",
        gap: 16,
      }}>
        {features.map((f, i) => (
          <BentoCard key={i} {...f} index={i} isVisible={isVisible} />
        ))}
      </div>

      <style>{`
        @media (max-width: 1024px) {
          #features > div:last-child {
            grid-template-columns: repeat(2, 1fr) !important;
          }
        }
        @media (max-width: 640px) {
          #features > div:last-child {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </section>
  );
}
