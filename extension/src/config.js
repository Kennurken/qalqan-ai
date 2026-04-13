// клауд Елдоса N1 — Qalqan AI v3.0
// Конфигурация — бірыңғай API URL (Bug #2 fix: localhost hardcode жойылды)

const IS_DEV = false;

export const API_URL = IS_DEV
  ? "http://127.0.0.1:8000"
  : "https://qalqan-ai-nu.vercel.app";

export const APP_VERSION = "3.0.0";
