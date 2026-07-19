// Qalqan AI — Messenger link badges (Telegram Web / WhatsApp Web).
// Scam links spread through chats more than through search. Same offline-first
// annotation path as search-guard: domains go to the background worker, which
// answers from the offline DB instantly and batches unknowns to /batch.

(() => {
  "use strict";

  const BADGE_CLASS = "qalqan-mg-badge";
  const seenDomains = new Map();   // domain -> {verdict, score}

  const STYLE = `
    .${BADGE_CLASS}{display:inline-flex;align-items:center;gap:3px;font-size:10.5px;font-weight:700;
      padding:0 6px;border-radius:999px;margin-left:6px;vertical-align:middle;line-height:1.6;
      font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;cursor:help;
      white-space:nowrap}
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

  // Hosts that are the messenger's own infra — never badge them.
  const SKIP = /(^|\.)(telegram\.org|t\.me|whatsapp\.com|whatsapp\.net|wa\.me|facebook\.com|fbcdn\.net|twimg\.com)$/;

  function hostOf(href) {
    try { return new URL(href).hostname.replace(/^www\./, "").toLowerCase(); }
    catch { return null; }
  }
  function domainOf(host) {
    const p = host.split(".");
    return p.length >= 2 ? p.slice(-2).join(".") : host;
  }

  function badge(verdict, score) {
    const b = document.createElement("span");
    b.className = BADGE_CLASS + " " + (verdict === "DANGEROUS" ? "d" : verdict === "SUSPICIOUS" ? "s" : "k");
    b.textContent = verdict === "DANGEROUS" ? "🛡 Қауіпті!" : verdict === "SUSPICIOUS" ? "🛡 Күдікті" : "🛡 ✓";
    b.title = "Qalqan AI: " + verdict + (score != null ? " (" + score + "/100)" : "");
    return b;
  }

  function collect() {
    const out = [];
    document.querySelectorAll('a[href^="http"]').forEach((a) => {
      if (a.dataset.qalqanMg) return;
      const host = hostOf(a.href);
      if (!host || SKIP.test(host)) return;
      a.dataset.qalqanMg = "1";
      out.push({ a, domain: domainOf(host), href: a.href });
    });
    return out;
  }

  function place(a, verdict, score) {
    if (a.querySelector("." + BADGE_CLASS)) return;
    // Only visibly flag non-safe links; a ✓ on every chat link would be noise.
    if (verdict !== "DANGEROUS" && verdict !== "SUSPICIOUS") return;
    a.appendChild(badge(verdict, score));
  }

  function annotate() {
    const items = collect();
    if (!items.length) return;
    const need = [];
    for (const it of items) {
      const cached = seenDomains.get(it.domain);
      if (cached) place(it.a, cached.verdict, cached.score);
      else need.push(it);
    }
    if (!need.length) return;
    const byDomain = new Map();
    for (const it of need) if (!byDomain.has(it.domain)) byDomain.set(it.domain, it.href);
    const urls = [...byDomain.values()].slice(0, 20);

    chrome.runtime.sendMessage({ action: "ANNOTATE_SEARCH", urls }, (resp) => {
      if (chrome.runtime.lastError || !resp || !resp.results) return;
      const byDom = new Map();
      for (const r of resp.results) {
        const h = hostOf(r.url); if (!h) continue;
        byDom.set(domainOf(h), r);
      }
      for (const it of need) {
        const r = byDom.get(it.domain);
        if (!r) continue;
        seenDomains.set(it.domain, { verdict: r.verdict, score: r.threat_score });
        place(it.a, r.verdict, r.threat_score);
      }
    });
  }

  let t = null;
  const schedule = () => { clearTimeout(t); t = setTimeout(annotate, 600); };
  schedule();
  new MutationObserver(schedule).observe(document.documentElement, { childList: true, subtree: true });
})();
