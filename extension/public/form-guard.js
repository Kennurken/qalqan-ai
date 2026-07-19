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
      ? "Qalqan AI: бұл сайт КҮДІКТІ (" + (score ?? "?") + "/100). Құпиясөзді енгізбес бұрын мұқият тексеріңіз!"
      : "Qalqan AI: бұл сайт ҚАУІПТІ. Құпиясөзді енгізбеңіз!";
    const ic = document.createElement("span");
    ic.innerHTML = '<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="width:1em;height:1em;vertical-align:-0.14em"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg>';
    ic.style.marginRight = "8px";
    b.appendChild(ic);
    b.appendChild(document.createTextNode(msg + (detail ? " — " + String(detail).slice(0, 120) : "")));
    const x = document.createElement("button");
    x.textContent = "×";
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
