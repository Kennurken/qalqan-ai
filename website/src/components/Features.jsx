import { motion } from "framer-motion";
import { useInView } from "framer-motion";
import { useRef } from "react";

function FeatureCard({ icon, title, desc, color, delay, tags }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-60px" });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay }}
      style={{
        background: "rgba(30,41,59,0.4)",
        border: `1px solid rgba(${color},0.2)`,
        borderRadius: 16, padding: 28,
        backdropFilter: "blur(12px)",
        transition: "border-color 0.3s, transform 0.3s, box-shadow 0.3s",
      }}
      whileHover={{
        scale: 1.02,
        boxShadow: `0 8px 32px rgba(${color},0.15)`,
      }}
    >
      <div style={{
        width: 52, height: 52, borderRadius: 14,
        background: `rgba(${color},0.15)`, border: `1px solid rgba(${color},0.3)`,
        display: "flex", alignItems: "center", justifyContent: "center",
        fontSize: 24, marginBottom: 16,
      }}>
        {icon}
      </div>
      <h3 style={{ fontSize: 18, fontWeight: 700, marginBottom: 10, color: "var(--text)" }}>
        {title}
      </h3>
      <p style={{ fontSize: 14, color: "var(--text2)", lineHeight: 1.7, marginBottom: 16 }}>
        {desc}
      </p>
      {tags && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
          {tags.map((t, i) => (
            <span key={i} style={{
              fontSize: 11, padding: "3px 10px", borderRadius: 20,
              background: `rgba(${color},0.1)`, color: `rgb(${color})`,
              border: `1px solid rgba(${color},0.2)`,
            }}>{t}</span>
          ))}
        </div>
      )}
    </motion.div>
  );
}

export default function Features() {
  const titleRef = useRef(null);
  const titleInView = useInView(titleRef, { once: true });

  const features = [
    {
      icon: "🔍",
      title: "5 деңгейлі тексеру",
      desc: "Whitelist → Cache → Pyramid DB → KZ Impersonation → External DBs → Domain Intel → AI — әр сайт жан-жақты тексеріледі.",
      color: "59,130,246",
      tags: ["PhishTank", "Google Safe Browsing", "URLhaus", "OpenPhish"],
    },
    {
      icon: "🤖",
      title: "Жасанды интеллект",
      desc: "Groq Llama + Gemini Vision — беттің мазмұнын оқып, скриншоттан фишингті анықтайды. XAI факторлар түсіндіреді.",
      color: "99,102,241",
      tags: ["Groq AI", "Gemini Vision", "XAI Explainability"],
    },
    {
      icon: "🇰🇿",
      title: "KZ Intelligence",
      desc: "eGov, Kaspi, Halyk, Jysan жалған клондарын мгновенно анықтайды. Қазақстанның 50+ банк/сервис брендтері қорғалған.",
      color: "16,185,129",
      tags: ["egov.kz", "kaspi.kz", "halyk.kz", "kcell.kz"],
    },
    {
      icon: "⚡",
      title: "Офлайн тексеру",
      desc: "Интернет жоқ болса да жұмыс істейді. 200+ белгілі қауіпті домен офлайн дерекқорда. API-ға дейін мгновенды нәтиже.",
      color: "245,158,11",
      tags: ["Offline DB", "Instant Check", "0ms latency"],
    },
    {
      icon: "🔒",
      title: "SSL + RDAP талдауы",
      desc: "Domain жасы (RDAP), SSL сертификат, Let's Encrypt анықтауы — инфрақұрылым деңгейінде тексеру.",
      color: "139,92,246",
      tags: ["RDAP", "SSL Check", "Domain Age"],
    },
    {
      icon: "📊",
      title: "XAI Түсіндіру",
      desc: "SHAP/LIME стилінде — неге қауіпті деп танылды, қандай факторлар анықталды. Толық ашықтылық.",
      color: "239,68,68",
      tags: ["Explainability", "Risk Factors", "Confidence"],
    },
    {
      icon: "🔗",
      title: "Link Scanner",
      desc: "Беттегі барлық сілтемелерді бір рет басумен тексеру. 15 URL параллель — қауіпті сілтемелер бөлектеледі.",
      color: "14,165,233",
      tags: ["Batch Scan", "Export JSON", "Page Links"],
    },
    {
      icon: "🌐",
      title: "3 тіл қолдауы",
      desc: "Интерфейс, нәтижелер, себептер — бәрі қазақ, орыс, ағылшын тілдерінде. Автоматты тіл анықтау.",
      color: "34,197,94",
      tags: ["Қазақша", "Русский", "English"],
    },
  ];

  return (
    <section id="features" style={{ padding: "100px 24px", maxWidth: 1200, margin: "0 auto" }}>
      {/* Title */}
      <motion.div
        ref={titleRef}
        initial={{ opacity: 0, y: 30 }}
        animate={titleInView ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.7 }}
        style={{ textAlign: "center", marginBottom: 64 }}
      >
        <div style={{
          display: "inline-block", padding: "4px 14px", borderRadius: 20,
          background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.3)",
          fontSize: 12, color: "#a5b4fc", marginBottom: 16, letterSpacing: 1,
        }}>
          МҮМКІНДІКТЕР
        </div>
        <h2 style={{ fontSize: "clamp(28px,4vw,44px)", fontWeight: 900, marginBottom: 16, lineHeight: 1.2 }}>
          Толық{" "}
          <span className="gradient-text">киберқорғаныс</span>
          {" "}жүйесі
        </h2>
        <p style={{ fontSize: 16, color: "var(--text2)", maxWidth: 560, margin: "0 auto" }}>
          Бір кеңейтімде — 10+ threat intelligence дерек көзі, жасанды интеллект, офлайн тексеру
        </p>
      </motion.div>

      {/* Grid */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
        gap: 20,
      }}>
        {features.map((f, i) => (
          <FeatureCard key={i} {...f} delay={i * 0.08} />
        ))}
      </div>
    </section>
  );
}
