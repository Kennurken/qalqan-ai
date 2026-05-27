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
    </>
  );
}
