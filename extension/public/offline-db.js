// клауд Елдоса N1 — Qalqan AI v5.0
// Offline database: works without API when internet is down

const OFFLINE_PYRAMIDS = new Set([
  "crowd1.com","finiko.com","onecoin.eu","forsage.io","bitconnect.co",
  "qubittech.ai","hermes-management.com","lifeisgood.company","dagcoin.org",
  "plustoken.io","antares.trade","lion-bit.com","skyway.capital","amir-capital.com",
  "g-time.kz","kilt.kz","smartbusiness.kz","bepic.com","qnet.net",
  "crowd1.club","joy-way.club","garantbox.kz","imperialfinance.kz"
]);

const OFFLINE_WHITELIST = new Set([
  "google.com","google.kz","youtube.com","github.com","kaspi.kz",
  "halykbank.kz","egov.kz","wikipedia.org","microsoft.com","apple.com",
  "kolesa.kz","krisha.kz","tengrinews.kz","nur.kz","telegram.org"
]);

const FREE_TLDS = new Set([".tk",".ml",".ga",".cf",".gq",".xyz",".top",".click"]);

function offlineCheck(url) {
  try {
    const domain = new URL(url).hostname.replace("www.", "").toLowerCase();
    const tld = "." + domain.split(".").pop();

    if (OFFLINE_WHITELIST.has(domain)) {
      return { verdict: "SAFE", threat_score: 0, source: "offline_whitelist" };
    }

    if (OFFLINE_PYRAMIDS.has(domain)) {
      return { verdict: "DANGEROUS", threat_score: 95, source: "offline_pyramid",
        detail: "Known financial pyramid (offline check)" };
    }

    if (FREE_TLDS.has(tld)) {
      return { verdict: "SUSPICIOUS", threat_score: 40, source: "offline_tld",
        detail: "Free TLD detected — potential risk" };
    }

    return null; // Unknown — need API
  } catch {
    return null;
  }
}

// Export for use in background.js
if (typeof globalThis !== "undefined") globalThis.offlineCheck = offlineCheck;
