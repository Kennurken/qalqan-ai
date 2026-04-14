// клауд Елдоса N1 — Qalqan AI v5.0
// Offline database: works without API when internet is down
// Expanded: pyramids, gambling, case battles, phishing, scam sites

// === ПИРАМИДАЛАР / MLM ===
const OFFLINE_PYRAMIDS = new Set([
  "crowd1.com","finiko.com","onecoin.eu","forsage.io","bitconnect.co",
  "qubittech.ai","hermes-management.com","lifeisgood.company","dagcoin.org",
  "plustoken.io","antares.trade","lion-bit.com","skyway.capital","amir-capital.com",
  "g-time.kz","kilt.kz","smartbusiness.kz","bepic.com","qnet.net",
  "crowd1.club","joy-way.club","garantbox.kz","imperialfinance.kz",
  "telexfree.com","tradeallcrypto.com","esperio.org","forexoptimum.com",
  "binance-earn.pro","bnb-earn.com","hamsterkombat-airdrop.com","hamster-claim.com"
]);

// === АЗАРТНЫЕ ИГРЫ / GAMBLING / КАЗИНО ===
const OFFLINE_GAMBLING = new Set([
  // Казино
  "1xbet.com","1xbet.kz","1xstavka.ru","1xbet.org",
  "mostbet.com","mostbet.kz","mostbet.uz","mostbet-az.com",
  "pin-up.com","pin-up.kz","pinup.ru","pin-up.bet",
  "vulkan-vegas.com","vulkan-platinum.com","vulkan-casino.com","vulkan24.com",
  "joycasino.com","joycasino.kz",
  "casino-x.com","casino-x.kz",
  "azino777.com","azino888.com","azino999.com",
  "vavada.com","vavada.casino",
  "fairspin.io","stake.com","stake.us",
  "riobet.com","riobet.kz",
  "cat-casino.com","catcasino.com",
  "bollywood-casino.com",
  "drip-casino.com","dripcasino.com",
  "izzi-casino.com","izzicasino.com",
  "legzo-casino.com","legzo.casino",
  "monro-casino.com","monrocasino.com",
  "fresh-casino.com","freshcasino.com",
  "sol-casino.com","solcasino.com",
  "jet-casino.com","jetcasino.com",
  "kent-casino.com","kentcasino.com",
  "glory-casino.com","glorycasino.com",
  "winner-casino.com",
  "888casino.com","888poker.com","888sport.com",
  "betway.com","betwinner.com","betwinner.kz",
  "melbet.com","melbet.kz","melbet.org",
  "linebet.com","linebet.kz",
  "megapari.com","megapari.kz",
  "parimatch.com","parimatch.kz",
  "fonbet.com","fonbet.kz","fonbet.ru",
  "olimp.com","olimp.kz","olimpbet.kz",
  "betandreas.com","betandreas.kz",
  "leon.bet","leonbets.com",
  "22bet.com","22bet.kz",
  "4rabet.com","4rabet.kz",
  "betboom.ru","betcity.ru",
  "marathonbet.com","marathon.bet",
  "ggbet.com","ggbet.kz","ggbet.ru",
  "winline.ru","winline.kz",
  "maxline.by",
  // Покер
  "pokerdom.com","pokerstars.com","pokermatch.com",
  "ggpoker.com","ggpokerok.com",
  // Слоты
  "slottica.com","slotozal.com","slotv.com",
  "play-fortuna.com","playfortuna.com",
  "booi.com","booi-casino.com",
  "spinbetter.com",
  "luckyland.com",
  // Ставки на спорт
  "betfair.com","bwin.com","unibet.com",
  "pinnacle.com","sbobet.com",
  "tonybet.com","dafabet.com",
  "powbet.com","rabona.com"
]);

// === КЕЙС-БАТТЛЫ / OPEN CASES / CS2 GAMBLING ===
const OFFLINE_CASE_BATTLES = new Set([
  // Кейс-баттлы и открытие кейсов CS2/CSGO
  "hellcase.com","hellcase.org",
  "csgofast.com","csgofast.ru",
  "csgopolygon.com",
  "csgoroll.com","csgoroll.gg",
  "csgoluck.com",
  "csgoempire.com","csgoempire.gg",
  "skinclub.gg","skinclub.com",
  "farmskins.com",
  "daddyskins.com",
  "keydrop.com",
  "csgo500.com","csgo500.gg",
  "gamdom.com",
  "clash.gg",
  "packdraw.com",
  "cases.gg",
  "datdrop.com",
  "csgoatse.com",
  "csgocases.com",
  "bloodycase.com",
  "key-drop.com",
  "skinhub.com",
  "csgopositive.com",
  "wtfskins.com",
  "rustyloot.gg",
  "bandit.camp",
  "rustclash.com",
  "howl.gg",
  "ggdrop.com",
  "forcedrop.com","forcedrop.gg",
  "opencases.gg",
  "caseworld.gg",
  "hellspin.com",
  "rain.gg",
  "hypedrop.com",
  "lootbox.com",
  "lootie.com",
  "hahalol.com",
  "csgo.net",
  "skinsback.com",
  "tradeit.gg",
  "g2g.com",
  "pvpro.com"
]);

// === ФИШИНГ САЙТЫ ===
const OFFLINE_PHISHING = new Set([
  // eGov фишинг
  "eg0v.kz","egov-kz.com","egov-verify.kz","egov.kz.com","e-gov-kz.com",
  "egov-login.kz","my-egov.kz","egov.com.kz","egov-portal.com",
  // Kaspi фишинг
  "kaspi-bank.kz","kaspi-verify.com","kaspi-qr.kz","kaspi.com.kz",
  "kaspikz.com","kaspi-shop.com","kaspi-pay.kz","my-kaspi.kz",
  // Halyk фишинг
  "halyk-bank.com","homebank-kz.com","halykbank-login.kz",
  "halyk-online.com","my-homebank.kz",
  // Крипто-фишинг
  "binance-login.com","coinbase-verify.com","metamask-verify.com",
  "trustwallet-verify.com","phantom-wallet.com",
  "blockchain-verify.com","crypto-airdrop.com",
  // Банки и платежи
  "paypal-verify.com","visa-secure.com","mastercard-verify.com",
  // Соцсети фишинг
  "instagram-verify.com","facebook-login.com","tiktok-verify.com",
  "telegram-verify.com","whatsapp-verify.com"
]);

// === СКАМ / МОШЕННИЧЕСТВО ===
const OFFLINE_SCAM = new Set([
  // Фейковые магазины
  "super-sale.kz","mega-skidka.kz","iphone-free.com",
  "aliexpress-sale.kz","wildberries-sale.com",
  // Фейковые инвестиции
  "tesla-invest.com","amazon-invest.kz","gazprom-invest.com",
  "easy-money-bot.com","crypto-doubler.com","bitcoin-generator.com",
  // Фейковые лотереи
  "free-lottery.com","mega-prize.com","lucky-winner.com",
  // Дропшиппинг скам
  "dropship-guru.com","passive-income-bot.com"
]);

// === БЕЛЫЙ СПИСОК ===
const OFFLINE_WHITELIST = new Set([
  "google.com","google.kz","youtube.com","github.com","kaspi.kz",
  "halykbank.kz","egov.kz","wikipedia.org","microsoft.com","apple.com",
  "kolesa.kz","krisha.kz","tengrinews.kz","nur.kz","telegram.org",
  "instagram.com","facebook.com","twitter.com","linkedin.com",
  "reddit.com","stackoverflow.com","amazon.com","netflix.com"
]);

const FREE_TLDS = new Set([".tk",".ml",".ga",".cf",".gq",".xyz",".top",".click",".buzz",".rest",".icu",".work",".link"]);

function offlineCheck(url) {
  try {
    const hostname = new URL(url).hostname.replace("www.", "").toLowerCase();
    const tld = "." + hostname.split(".").pop();

    // Extract base domain (e.g. sub.example.com -> example.com)
    const parts = hostname.split(".");
    const domain = parts.length >= 2 ? parts.slice(-2).join(".") : hostname;

    if (OFFLINE_WHITELIST.has(domain) || OFFLINE_WHITELIST.has(hostname)) {
      return { verdict: "SAFE", threat_score: 0, source: "offline_whitelist",
        detail: "Trusted site (offline check)", threat_type: "safe" };
    }

    if (OFFLINE_PYRAMIDS.has(domain) || OFFLINE_PYRAMIDS.has(hostname)) {
      return { verdict: "DANGEROUS", threat_score: 95, source: "offline_pyramid",
        detail: "Known financial pyramid / MLM scheme (offline check)", threat_type: "pyramid" };
    }

    if (OFFLINE_GAMBLING.has(domain) || OFFLINE_GAMBLING.has(hostname)) {
      return { verdict: "DANGEROUS", threat_score: 90, source: "offline_gambling",
        detail: "Gambling / casino / betting site (offline check)", threat_type: "gambling" };
    }

    if (OFFLINE_CASE_BATTLES.has(domain) || OFFLINE_CASE_BATTLES.has(hostname)) {
      return { verdict: "DANGEROUS", threat_score: 85, source: "offline_casebattle",
        detail: "Case battle / case opening / skin gambling (offline check)", threat_type: "gambling" };
    }

    if (OFFLINE_PHISHING.has(domain) || OFFLINE_PHISHING.has(hostname)) {
      return { verdict: "DANGEROUS", threat_score: 95, source: "offline_phishing",
        detail: "Known phishing site (offline check)", threat_type: "phishing" };
    }

    if (OFFLINE_SCAM.has(domain) || OFFLINE_SCAM.has(hostname)) {
      return { verdict: "DANGEROUS", threat_score: 90, source: "offline_scam",
        detail: "Known scam / fraud site (offline check)", threat_type: "scam" };
    }

    if (FREE_TLDS.has(tld)) {
      return { verdict: "SUSPICIOUS", threat_score: 40, source: "offline_tld",
        detail: "Free TLD detected — potential risk", threat_type: "suspicious_infrastructure" };
    }

    return null; // Unknown — need API
  } catch {
    return null;
  }
}

// Export for use in background.js
if (typeof globalThis !== "undefined") globalThis.offlineCheck = offlineCheck;
