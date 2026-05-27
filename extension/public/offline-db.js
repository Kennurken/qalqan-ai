// Qalqan AI v5.0
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
  "binance-earn.pro","bnb-earn.com","hamsterkombat-airdrop.com","hamster-claim.com",
  // 2024-2025 KZ-specific pyramids
  "mir-invest.kz","profit-kg.com","kazinvest.pro","invest-top.kz",
  "money-farm.kz","passive-kz.com","doublemoney.kz","cryptoearn.kz",
  "globalshare.kz","worldshare.com","evergrow.io","tripleclicks.com",
  "imetrics.kz","kztrade.io","astana-invest.com","almaty-profit.com",
  "kz-profit.com","tenge-profit.com","kazfinance.pro","capitalinvest.kz"
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
  "egov-kz.net","e-gov.com.kz","egov-site.kz","gov-kz-portal.com",
  "kz-gov.com","kazakhstan-gov.com","gosgov-kz.com",
  // Kaspi фишинг (expanded)
  "kaspi-bank.kz","kaspi-verify.com","kaspi-qr.kz","kaspi.com.kz",
  "kaspikz.com","kaspi-shop.com","kaspi-pay.kz","my-kaspi.kz",
  "kaspibank-kz.com","kaspi-gold.com","kaspi-support.com","kaspi-id.kz",
  "kaspi-login.tk","kaspi-login.ml","kaspi-online.xyz","kaspii.kz",
  // Halyk фишинг (expanded)
  "halyk-bank.com","homebank-kz.com","halykbank-login.kz",
  "halyk-online.com","my-homebank.kz","halyk-support.com",
  "homebank-login.kz","halyk-id.com","halykbank.com.kz",
  // Jysan фишинг
  "jysan-bank.com","jysanbank-kz.com","jysan-online.kz",
  "jysan-login.com","my-jysan.kz",
  // Kcell/Beeline фишинг
  "kcell-kz.com","kcell-bonus.kz","kcell-promo.com",
  "beeline-kz.com","beeline-bonus.kz","beeline-promo.com",
  "mobile-kcell.kz","kcell.com.kz",
  // Крипто-фишинг
  "binance-login.com","coinbase-verify.com","metamask-verify.com",
  "trustwallet-verify.com","phantom-wallet.com",
  "blockchain-verify.com","crypto-airdrop.com","binance-earn.pro",
  "bnb-earn.com","toncoin-claim.com","hamsterkombat-airdrop.com",
  "hamster-claim.com","okx-bonus.com","bybit-earn.com",
  // Банки и платежи
  "paypal-verify.com","visa-secure.com","mastercard-verify.com",
  // Соцсети фишинг
  "instagram-verify.com","facebook-login.com","tiktok-verify.com",
  "telegram-verify.com","whatsapp-verify.com","vk-login.com"
]);

// === СКАМ / МОШЕННИЧЕСТВО ===
const OFFLINE_SCAM = new Set([
  // Фейковые магазины
  "super-sale.kz","mega-skidka.kz","iphone-free.com",
  "aliexpress-sale.kz","wildberries-sale.com","ozon-sale.kz",
  "lamoda-sale.kz","kaspi-mall.com","kaspi-shop.kz",
  // Фейковые инвестиции
  "tesla-invest.com","amazon-invest.kz","gazprom-invest.com",
  "easy-money-bot.com","crypto-doubler.com","bitcoin-generator.com",
  "forex-profit.kz","trading-signals.kz","invest-kz.com",
  "tenge-cash.com","tenge-invest.kz","profit-kz.com",
  // Фейковые лотереи
  "free-lottery.com","mega-prize.com","lucky-winner.com",
  "kcell-prize.com","beeline-lucky.com","kaspi-winner.kz",
  // Дропшиппинг скам
  "dropship-guru.com","passive-income-bot.com",
  // Tech support scam
  "microsoft-support.kz","google-support.kz","apple-support.kz",
  // Fake job offers
  "job-kz.com","rabota-kz.com","headhunter-kz.com"
]);

// === БЕЛЫЙ СПИСОК ===
const OFFLINE_WHITELIST = new Set([
  // International
  "google.com","google.kz","youtube.com","github.com","wikipedia.org",
  "microsoft.com","apple.com","amazon.com","cloudflare.com",
  "facebook.com","instagram.com","twitter.com","x.com","linkedin.com",
  "whatsapp.com","telegram.org","t.me","reddit.com","tiktok.com",
  "stackoverflow.com","mozilla.org","npmjs.com","pypi.org",
  // KZ Government
  "egov.kz","gov.kz","nationalbank.kz","elicense.kz","salyk.kz",
  "kgd.gov.kz","adilet.zan.kz","enbek.kz","otbasybank.kz","nca.kz",
  "pki.gov.kz","kazpost.kz","post.kz","akorda.kz","primeminister.kz",
  // KZ Banks
  "kaspi.kz","halykbank.kz","homebank.kz","bcc.kz","centercredit.kz",
  "jusan.kz","forte.kz","freedom.kz","berekebank.kz","rbk.kz",
  "altynbank.kz","eubank.kz",
  // KZ Telecom
  "beeline.kz","kcell.kz","activ.kz","tele2.kz","altel.kz",
  // KZ Services
  "kolesa.kz","krisha.kz","olx.kz","wildberries.kz","mechta.kz",
  "sulpak.kz","technodom.kz","flip.kz","aviata.kz","ticketon.kz",
  "chocofood.kz","2gis.kz","arbuz.kz","magnum.kz","small.kz",
  "hh.kz","hhkz.com","djazz.kz","tarlan.kz","market.kz",
  // KZ Media
  "tengrinews.kz","nur.kz","inform.kz","zakon.kz","kapital.kz",
  "forbes.kz","kursiv.media","bnews.kz","liter.kz",
  // KZ Education
  "nu.edu.kz","kaznu.kz","kbtu.kz","sdu.edu.kz","narxoz.kz",
  // KZ Payment
  "qpay.kz","wooppay.com","paybox.money","cloudpayments.kz"
]);

const FREE_TLDS = new Set([".tk",".ml",".ga",".cf",".gq",".xyz",".top",".click",".buzz",".rest",".icu",".work",".link",".online",".site",".win",".pw",".cc",".bid",".loan"]);

function offlineCheck(url) {
  try {
    const hostname = new URL(url).hostname.replace("www.", "").toLowerCase();
    const tld = "." + hostname.split(".").pop();

    // Extract base domain (e.g. sub.example.com -> example.com)
    const parts = hostname.split(".");
    const domain = parts.length >= 2 ? parts.slice(-2).join(".") : hostname;

    if (OFFLINE_WHITELIST.has(domain) || OFFLINE_WHITELIST.has(hostname)) {
      return { verdict: "SAFE", threat_score: 0, source: "offline_whitelist",
        detail: "Сенімді сайт", detail_kk: "Сенімді сайт",
        detail_ru: "Надёжный сайт", detail_en: "Trusted site", threat_type: "safe" };
    }

    if (OFFLINE_PYRAMIDS.has(domain) || OFFLINE_PYRAMIDS.has(hostname)) {
      return { verdict: "DANGEROUS", threat_score: 95, source: "offline_pyramid",
        detail: "ҚАРЖЫЛЫҚ ПИРАМИДА: Бұл сайт белгілі алаяқтық схема. Ақша салмаңыз!",
        detail_kk: "ҚАРЖЫЛЫҚ ПИРАМИДА: Бұл сайт белгілі алаяқтық схема. Ақша салмаңыз!",
        detail_ru: "ФИНАНСОВАЯ ПИРАМИДА: Известная мошенническая схема. Не вкладывайте деньги!",
        detail_en: "FINANCIAL PYRAMID: Known MLM/pyramid scheme. Do not invest!",
        threat_type: "pyramid", indicators: ["pyramid_offline_db"] };
    }

    if (OFFLINE_GAMBLING.has(domain) || OFFLINE_GAMBLING.has(hostname)) {
      return { verdict: "DANGEROUS", threat_score: 90, source: "offline_gambling",
        detail: "ҚҰМАР ОЙЫН: Лицензиясыз казино немесе букмекер. ҚР-да тыйым салынған.",
        detail_kk: "ҚҰМАР ОЙЫН: Лицензиясыз казино немесе букмекер. ҚР-да тыйым салынған.",
        detail_ru: "ГЕМБЛИНГ: Нелицензированное казино или букмекер. Запрещено в РК.",
        detail_en: "GAMBLING: Unlicensed casino / bookmaker. Banned in Kazakhstan.",
        threat_type: "gambling", indicators: ["gambling_offline_db", "unlicensed_kz"] };
    }

    if (OFFLINE_CASE_BATTLES.has(domain) || OFFLINE_CASE_BATTLES.has(hostname)) {
      return { verdict: "DANGEROUS", threat_score: 85, source: "offline_casebattle",
        detail: "КЕЙС-БАТ: CS2 кейстерін ашу — азартты ойын. Жасөспірімдерге қауіпті.",
        detail_kk: "КЕЙС-БАТ: CS2 кейстерін ашу — азартты ойын. Жасөспірімдерге қауіпті.",
        detail_ru: "КЕЙС-БАТЛ: Открытие кейсов CS2 — азартная игра. Опасно для несовершеннолетних.",
        detail_en: "CASE BATTLE: CS2 case opening — gambling. Dangerous for minors.",
        threat_type: "gambling", indicators: ["case_battle_offline_db"] };
    }

    if (OFFLINE_PHISHING.has(domain) || OFFLINE_PHISHING.has(hostname)) {
      return { verdict: "DANGEROUS", threat_score: 95, source: "offline_phishing",
        detail: "ФИШИНГ: Белгілі жалған сайт. Жеке деректерді енгізбеңіз!",
        detail_kk: "ФИШИНГ: Белгілі жалған сайт. Жеке деректерді енгізбеңіз!",
        detail_ru: "ФИШИНГ: Известный поддельный сайт. Не вводите личные данные!",
        detail_en: "PHISHING: Known phishing site. Do not enter personal data!",
        threat_type: "phishing", indicators: ["phishing_offline_db"] };
    }

    if (OFFLINE_SCAM.has(domain) || OFFLINE_SCAM.has(hostname)) {
      return { verdict: "DANGEROUS", threat_score: 90, source: "offline_scam",
        detail: "АЛАЯҚТЫҚ: Жалған сайт немесе алаяқтық схема.",
        detail_kk: "АЛАЯҚТЫҚ: Жалған сайт немесе алаяқтық схема.",
        detail_ru: "МОШЕННИЧЕСТВО: Поддельный сайт или мошенническая схема.",
        detail_en: "SCAM: Known scam / fraud site.",
        threat_type: "scam", indicators: ["scam_offline_db"] };
    }

    if (FREE_TLDS.has(tld)) {
      return { verdict: "SUSPICIOUS", threat_score: 40, source: "offline_tld",
        detail: "Тегін домен — ықтимал фишинг белгісі",
        detail_kk: "Тегін домен — ықтимал фишинг белгісі",
        detail_ru: "Бесплатный домен — возможный признак фишинга",
        detail_en: "Free TLD detected — potential phishing risk",
        threat_type: "suspicious_infrastructure", indicators: [`free_tld_${tld.slice(1)}`] };
    }

    return null; // Unknown — need API
  } catch {
    return null;
  }
}

// Export for use in background.js
if (typeof globalThis !== "undefined") globalThis.offlineCheck = offlineCheck;
