// Qalqan AI — Form-guard: warn BEFORE the user types a password on a risky page.
// DANGEROUS pages are blocked outright by the background worker, so this guard
// covers the gap: SUSPICIOUS verdicts and pages the pipeline hasn't flagged hard
// enough to block. Shows a one-time banner when a password field gains focus.

(() => {
  "use strict";

  let warned = false;

  function showBanner(verdict, score, detail) {
    if (warned || document.getElementById("qalqan-fg-banner")) return;
    warned = true;
    const b = document.createElement("div");
    b.id = "qalqan-fg-banner";
    b.style.cssText = [
      "position:fixed", "top:0", "left:0", "right:0", "z-index:2147483647",
      "background:#b00020", "color:#fff",
      "font:600 14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif",
      "padding:12px 44px 12px 16px", "text-align:center",
      "box-shadow:0 2px 12px rgba(0,0,0,.35)",
    ].join(";");
    const msg = verdict === "SUSPICIOUS"
      ? "⚠️ Qalqan AI: бұл сайт КҮДІКТІ (" + (score ?? "?") + "/100). Құпиясөзді енгізбес бұрын мұқият тексеріңіз!"
      : "🛑 Qalqan AI: бұл сайт ҚАУІПТІ. Құпиясөзді енгізбеңіз!";
    b.textContent = msg + (detail ? " — " + String(detail).slice(0, 120) : "");
    const x = document.createElement("button");
    x.textContent = "✕";
    x.setAttribute("aria-label", "Жабу");
    x.style.cssText = "position:absolute;right:8px;top:8px;background:none;border:none;color:#fff;font-size:16px;cursor:pointer;padding:4px";
    x.onclick = () => b.remove();
    b.appendChild(x);
    (document.body || document.documentElement).appendChild(b);
    setTimeout(() => b.remove(), 15000);
  }

  function onPasswordFocus() {
    chrome.runtime.sendMessage({ action: "GET_RESULT" }, (result) => {
      if (chrome.runtime.lastError || !result) return;
      const v = (result.verdict || "").toUpperCase();
      if (v === "SUSPICIOUS" || v === "DANGEROUS") {
        showBanner(v, result.threat_score, result.detail_kk || result.detail_ru);
      }
    });
  }

  document.addEventListener("focusin", (e) => {
    if (e.target && e.target.matches && e.target.matches('input[type="password"]')) {
      onPasswordFocus();
    }
  }, true);
})();
