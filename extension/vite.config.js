// клауд Елдоса N1 — Qalqan AI v3.0
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "dist",
    rollupOptions: {
      input: { popup: "index.html" },
    },
  },
  // Chrome extension popup-қа relative paths керек
  base: "./",
});
