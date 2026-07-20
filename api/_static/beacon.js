// Qalqan ops beacon: client-error reports + privacy-safe pageview ping.
// No cookies, no fingerprinting; pageview skipped when Do Not Track is on.
(() => {
  "use strict";
  let sent = 0;
  function report(kind, msg, src, line) {
    if (sent >= 3) return;   // never spam on error loops
    sent++;
    const body = JSON.stringify({
      k: kind, m: String(msg || "").slice(0, 200),
      s: String(src || "").slice(0, 120), l: Number(line) || 0,
      p: location.pathname.slice(0, 60),
    });
    try {
      if (!navigator.sendBeacon || !navigator.sendBeacon("/client-error", new Blob([body], { type: "application/json" })))
        fetch("/client-error", { method: "POST", headers: { "Content-Type": "application/json" }, body, keepalive: true }).catch(() => {});
    } catch (e) { /* reporting must never break the page */ }
  }
  window.addEventListener("error", (e) => report("err", e.message, e.filename, e.lineno));
  window.addEventListener("unhandledrejection", (e) => report("rej", (e.reason && e.reason.message) || e.reason));

  if (navigator.doNotTrack !== "1") {
    const body = JSON.stringify({ p: location.pathname.slice(0, 60) });
    try {
      if (!navigator.sendBeacon || !navigator.sendBeacon("/pv", new Blob([body], { type: "application/json" })))
        fetch("/pv", { method: "POST", headers: { "Content-Type": "application/json" }, body, keepalive: true }).catch(() => {});
    } catch (e) { /* ignore */ }
  }
})();
