import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Features from "./components/Features";
import HowItWorks from "./components/HowItWorks";
import StatsSection from "./components/StatsSection";
import DemoSection from "./components/DemoSection";
import TechStack from "./components/TechStack";
import InstallSection from "./components/InstallSection";
import Footer from "./components/Footer";
import "./index.css";

function ScrollToTop() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const onScroll = () => setVisible(window.scrollY > 600);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <AnimatePresence>
      {visible && (
        <motion.button
          initial={{ opacity: 0, scale: 0.7 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.7 }}
          whileHover={{ scale: 1.1, boxShadow: "0 8px 24px rgba(99,102,241,0.5)" }}
          whileTap={{ scale: 0.9 }}
          onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
          style={{
            position: "fixed", bottom: 28, right: 24, zIndex: 90,
            width: 44, height: 44, borderRadius: "50%",
            background: "linear-gradient(135deg, #3b82f6, #6366f1)",
            border: "none", color: "white", fontSize: 18,
            cursor: "pointer",
            boxShadow: "0 4px 16px rgba(99,102,241,0.3)",
            display: "flex", alignItems: "center", justifyContent: "center",
          }}
        >
          ↑
        </motion.button>
      )}
    </AnimatePresence>
  );
}

export default function App() {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <Features />
        <HowItWorks />
        <StatsSection />
        <DemoSection />
        <TechStack />
        <InstallSection />
      </main>
      <Footer />
      <ScrollToTop />
    </>
  );
}
