// Qalqan AI — Search-results annotation (like Bitdefender TrafficLight / WOT).
// Runs ONLY on search-engine result pages. Marks each result link with a safety
// badge BEFORE the user clicks — the highest-leverage moment to stop a scam.
// No API keys here: domains go to the background worker, which answers from the
// offline DB instantly and batches the unknowns to /batch.

(() => {
  "use strict";

  // Per-engine: how to find the clickable result headings on this page.
  const ENGINES = [
    { host: /(^|\.)google\./,     sel: "a:has(h3)", anchor: (a) => a.querySelector("h3") || a },
    { host: /(^|\.)yandex\./,     sel: "a.OrganicTitle-Link, a.organic__url, a.Link_theme_normal", anchor: (a) => a },
    { host: /(^|\.)bing\./,       sel: "#b_results h2 a, #b_results .b_algo a[href]", anchor: (a) => a },
    { host: /(^|\.)duckduckgo\./, sel: 'a[data-testid="result-title-a"]', anchor: (a) => a },
    { host: /(^|\.)mail\.ru/,     sel: "a.link[href], a.result__link", anchor: (a) => a },
    { host: /(^|\.)ecosia\.|(^|\.)brave\.com|(^|\.)startpage\./, sel: "a[href^='http']:has(h3), a.result-title", anchor: (a) => a.querySelector("h3") || a },
  ];

  const engine = ENGINES.find((e) => e.host.test(location.hostname));
  if (!engine) return;

  const SELF = location.hostname.replace(/^www\./, "");
  const BADGE_CLASS = "qalqan-sg-badge";
  const seenDomains = new Map();   // domain -> verdict (cache within the page)

  const STYLE = `
    .${BADGE_CLASS}{display:inline-flex;align-items:center;gap:3px;font-size:11px;font-weight:700;
      padding:1px 7px;border-radius:999px;margin-left:8px;vertical-align:middle;line-height:1.5;
      font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;cursor:help;
      white-space:nowrap;letter-spacing:.2px}
    .${BADGE_CLASS}.d{background:#fde2e4;color:#b00020;border:1px solid #f5a3ad}
    .${BADGE_CLASS}.s{background:#fff3d6;color:#8a5a00;border:1px solid #f0cf87}
    .${BADGE_CLASS}.k{background:#e3f5e6;color:#116b2b;border:1px solid #a7ddb2}
    @media(prefers-color-scheme:dark){
      .${BADGE_CLASS}.d{background:#3a1417;color:#ff9aa6;border-color:#5c2126}
      .${BADGE_CLASS}.s{background:#3a2f12;color:#f0cf87;border-color:#5c4a1e}
      .${BADGE_CLASS}.k{background:#12301a;color:#8fe0a3;border-color:#1e4d2c}
    }`;
  const st = document.createElement("style");
  st.textContent = STYLE;
  document.documentElement.appendChild(st);

  function hostOf(href) {
    try {
      const h = new URL(href, location.href).hostname.replace(/^www\./, "").toLowerCase();
      return h;
    } catch { return null; }
  }
  function domainOf(host) {
    const p = host.split(".");
    return p.length >= 2 ? p.slice(-2).join(".") : host;
  }

  function badge(verdict, score) {
    const b = document.createElement("span");
    b.className = BADGE_CLASS + " " + (verdict === "DANGEROUS" ? "d" : verdict === "SUSPICIOUS" ? "s" : "k");
    const SH = '<svg class="qi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="width:1em;height:1em;vertical-align:-0.14em"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg>';
    if (verdict === "DANGEROUS") b.innerHTML = SH + " Қауіпті · Qalqan";
    else if (verdict === "SUSPICIOUS") b.innerHTML = SH + " Күдікті";
    else b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="width:1em;height:1em;vertical-align:-0.14em"><path d="M20 6 9 17l-5-5"/></svg>';
    b.title = "Qalqan AI: " + verdict + (score != null ? " (" + score + "/100)" : "");
    return b;
  }

  function place(anchorEl, verdict, score) {
    if (!anchorEl || anchorEl.querySelector("." + BADGE_CLASS)) return;
    anchorEl.appendChild(badge(verdict, score));
  }

  // Collect result anchors that still need a badge.
  function collect() {
    const out = [];
    let anchors;
    try { anchors = document.querySelectorAll(engine.sel); }
    catch { anchors = document.querySelectorAll("a[href^='http']"); }
    anchors.forEach((a) => {
      const target = engine.anchor(a);
      if (!target || target.dataset.qalqanSg) return;
      const host = hostOf(a.href);
      if (!host || host === SELF || host.endsWith("." + SELF)) return;
      // skip search-engine infra / cache / translate links
      if (/(^|\.)(google|bing|yandex|duckduckgo|microsoft|gstatic|googleusercontent)\./.test(host)) return;
      target.dataset.qalqanSg = "1";
      out.push({ target, href: a.href, domain: domainOf(host) });
    });
    return out;
  }

  function annotate() {
    const items = collect();
    if (!items.length) return;

    // Apply cached verdicts immediately; gather uncached URLs for the worker.
    const need = [];
    for (const it of items) {
      const cached = seenDomains.get(it.domain);
      if (cached) place(it.target, cached.verdict, cached.score);
      else need.push(it);
    }
    if (!need.length) return;

    // De-dup by domain for the request (one lookup per domain, not per link).
    const byDomain = new Map();
    for (const it of need) if (!byDomain.has(it.domain)) byDomain.set(it.domain, it.href);
    const urls = [...byDomain.values()].slice(0, 30);

    chrome.runtime.sendMessage({ action: "ANNOTATE_SEARCH", urls }, (resp) => {
      if (chrome.runtime.lastError || !resp || !resp.results) return;
      const verdictByDomain = new Map();
      for (const r of resp.results) {
        const h = hostOf(r.url); if (!h) continue;
        verdictByDomain.set(domainOf(h), r);
      }
      for (const it of need) {
        const r = verdictByDomain.get(it.domain);
        if (!r) continue;
        seenDomains.set(it.domain, { verdict: r.verdict, score: r.threat_score });
        place(it.target, r.verdict, r.threat_score);
      }
    });
  }

  // Initial pass + observe for infinite scroll / SPA result swaps (debounced).
  let t = null;
  const schedule = () => { clearTimeout(t); t = setTimeout(annotate, 400); };
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", schedule, { once: true });
  else schedule();
  new MutationObserver(schedule).observe(document.documentElement, { childList: true, subtree: true });
})();
