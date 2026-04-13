// клауд Елдоса N1 — Qalqan AI v3.0
// Hook: chrome.storage-дан статистика оқу

import { useState, useEffect } from "react";

export function useStats() {
  const [stats, setStats] = useState({ checked: 0, blocked: 0, suspicious: 0, safe: 0, since: null });

  useEffect(() => {
    chrome.storage.local.get("qalqan_stats", (result) => {
      if (result.qalqan_stats) setStats(result.qalqan_stats);
    });
  }, []);

  const resetStats = () => {
    const fresh = { checked: 0, blocked: 0, suspicious: 0, safe: 0, since: new Date().toISOString() };
    chrome.storage.local.set({ qalqan_stats: fresh });
    setStats(fresh);
  };

  return { stats, resetStats };
}
