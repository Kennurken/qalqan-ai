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
  "kz-profit.com","tenge-profit.com","kazfinance.pro","capitalinvest.kz",
  // Additional KZ pyramid/MLM schemes
  "aqsha-kz.com","tenge-bonus.kz","invest100.kz","promo-kz.com",
  "kz-cashback.com","depozit-kz.com","vklad-kz.com","rentakz.com",
  "stockkz.com","cryptokz.pro","nft-kz.com","metaverse-kz.com",
  "web3-kz.com","dao-kz.com","defi-kz.com","yield-kz.com",
  "hype-kz.com","hyip-kz.com","hyips.kz","mmm-kz.com",
  "mmm2023.kz","mmm2024.kz","mmm2025.kz","mmmglobal.kz",
  "goldminers.kz","diamondclub.kz","eliteclub.kz","vipclub.kz",
  "smartinvest.kz","fastmoney.kz","quickprofit.kz","easyprofit.kz",
  "passivedaily.kz","earnkz.com","biznes-kz.com","mlmkz.com",
  // International MLM/pyramid
  "imarketsLive.com","worldventures.com","herbalife-scam.com",
  "acn.com","amway-kz.com","nuskin-kz.com","oriflame-mlm.com",
  "betteravenue.com","clubshop.net","viralcash.io","cashfxgroup.com",
  "ovato.com","zennoa.com","growthchips.io","coinbase-invest.pro",
  "eth-double.com","btc-double.com","ton-earn.com","usdt-earn.com"
]);

// === АЗАРТНЫЕ ИГРЫ / GAMBLING / КАЗИНО ===
const OFFLINE_GAMBLING = new Set([
  // Казино
  "1xbet.com","1xbet.kz","1xbet.ng","1xbet.ug","1xbet.tz","1xbet.et","1xstavka.ru","1xbet.org","1xbet.cd","1x-bet.net",
  "mostbet.com","mostbet.kz","mostbet.uz","mostbet-az.com","mostbet.tj","mostbet.tm","mostbet.kg","mostbet.co",
  "pin-up.com","pin-up.kz","pinup.ru","pin-up.bet","pinupbet.kz","pin-up.casino","pinupcasino.kz",
  "vulkan-vegas.com","vulkan-platinum.com","vulkan-casino.com","vulkan24.com","vulkanstars.com","vulkan-royal.com","vulkan-milion.com",
  "joycasino.com","joycasino.kz",
  "casino-x.com","casino-x.kz",
  "azino777.com","azino888.com","azino999.com","azino-777.com",
  "vavada.com","vavada.casino","vavada.kz",
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
  "winner-casino.com","winnercasino.kz",
  "888casino.com","888poker.com","888sport.com",
  "betway.com","betwinner.com","betwinner.kz",
  "melbet.com","melbet.kz","melbet.org","melbetaff.com",
  "linebet.com","linebet.kz","linebets.kz",
  "megapari.com","megapari.kz","megapari.org",
  "parimatch.com","parimatch.kz","pari-match.kz",
  "fonbet.com","fonbet.kz","fonbet.ru",
  "olimp.com","olimp.kz","olimpbet.kz","olimp-bet.kz",
  "betandreas.com","betandreas.kz",
  "leon.bet","leonbets.com",
  "22bet.com","22bet.kz",
  "4rabet.com","4rabet.kz","4r-abet.com",
  "betboom.ru","betcity.ru",
  "marathonbet.com","marathon.bet",
  // Extra operators active in KZ
  "ggbet.com","ggbet.kz","gg.bet",
  "winline.ru","winline.kz",
  "zenit.bet","zenitbet.com",
  "sbobet.com","1win.com","1win.kz","1win.pro",
  "betfair.com","bwin.com","unibet.com",
  "winmasters.com","wbet.kz","wbet.com",
  "betssen.com","1xsport.kz","xbets.kz",
  "quasar.bet","quasargaming.com",
  "maxbet.kz","maxbets.kz",
  "olimp-sport.kz","olimpsport.kz",
  "bets.kz","betskz.com","kzbets.com",
  "luckycasino.kz","fortunecasino.kz",
  "sportaza.com","sportaza.kz",
  "powbet.com","ivibet.com","ivi.bet",
  "fresh-bets.com","megaslot.com","megaslot.kz",
  "spinwin.kz","azart.kz","kazino.kz",
  "casino.kz","kazino-online.kz","onlinecasino.kz",
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
  "egov24.kz","egov365.kz","egovsupport.kz","egovonline.kz",
  "gosuslugi-kz.com","mgovsupport.kz","digitalgov.kz","egov-help.kz",
  // Kaspi фишинг (expanded)
  "kaspi-bank.kz","kaspi-verify.com","kaspi-qr.kz","kaspi.com.kz",
  "kaspikz.com","kaspi-shop.com","kaspi-pay.kz","my-kaspi.kz",
  "kaspibank-kz.com","kaspi-gold.com","kaspi-support.com","kaspi-id.kz",
  "kaspi-login.tk","kaspi-login.ml","kaspi-online.xyz","kaspii.kz",
  "kaspi-bonus.com","kaspi-cash.com","kaspibonus.kz","kaspigold.kz",
  "kaspi-credit.kz","kaspi-loan.kz","kaspi-card.kz","kaspi-transfer.kz",
  "kaspishop.com","kaspimarket.kz","kaspi-market.com","kaspi-mall.kz",
  "kaspipay.com","kaspi-qr-pay.com","qaspi.kz","kaspi-app.kz",
  // Halyk фишинг (expanded)
  "halyk-bank.com","homebank-kz.com","halykbank-login.kz",
  "halyk-online.com","my-homebank.kz","halyk-support.com",
  "homebank-login.kz","halyk-id.com","halykbank.com.kz",
  "halyk-bonus.com","halyk-transfer.kz","halyk-card.kz","halykpay.kz",
  "halyk-gold.kz","homebank-support.kz","halyk24.kz","halyk-online.kz",
  // Jysan фишинг
  "jysan-bank.com","jysanbank-kz.com","jysan-online.kz",
  "jysan-login.com","my-jysan.kz","jysanpay.kz","jysan-card.kz",
  // Bereke (ex-Sberbank KZ) фишинг
  "bereke-bank.com","berekebank-kz.com","bereke-online.kz","bereke-login.kz",
  "bereke-support.kz","berekepay.kz","bereke-card.kz",
  // Forte / Freedom фишинг
  "forte-bank.kz","fortebank-kz.com","forte-login.kz",
  "freedom-bank.kz","freedombank-kz.com","freedomfinance-kz.com",
  // Kcell/Beeline/Tele2 фишинг
  "kcell-kz.com","kcell-bonus.kz","kcell-promo.com",
  "beeline-kz.com","beeline-bonus.kz","beeline-promo.com",
  "mobile-kcell.kz","kcell.com.kz","kcell-internet.kz","kcell-sim.kz",
  "tele2-kz.com","tele2bonus.kz","tele2-bonus.kz","tele2promo.kz",
  "activ-kz.com","altel-kz.com","tele2-login.kz","kcell-login.kz",
  // Wildberries/Ozon/Kolesa KZ фишинг
  "wb-kz.com","wildberries-kz.com","wb-bonus.kz","wb-prize.kz",
  "ozon-kz.com","ozonbonus.kz","ozon-prize.kz",
  "kolesa-kz.com","kolesa-bonus.kz","kolesa-prize.kz",
  "krisha-kz.com","krisha-prize.kz","olx-kz.com",
  // Крипто-фишинг
  "binance-login.com","coinbase-verify.com","metamask-verify.com",
  "trustwallet-verify.com","phantom-wallet.com",
  "blockchain-verify.com","crypto-airdrop.com","binance-earn.pro",
  "bnb-earn.com","toncoin-claim.com","hamsterkombat-airdrop.com",
  "hamster-claim.com","okx-bonus.com","bybit-earn.com",
  "ton-airdrop.com","ton-claim.com","notcoin-claim.com","dogs-airdrop.com",
  "blum-claim.com","tapswap-claim.com","major-claim.com","cati-airdrop.com",
  "binance-kz.com","okx-kz.com","bybit-kz.com","bitget-kz.com",
  "mexc-kz.com","gate-kz.com","kucoin-kz.com","huobi-kz.com",
  // Банки и платежи
  "paypal-verify.com","visa-secure.com","mastercard-verify.com",
  "qiwi-kz.com","qiwi-bonus.kz","webmoney-kz.com",
  // Соцсети фишинг
  "instagram-verify.com","facebook-login.com","tiktok-verify.com",
  "telegram-verify.com","whatsapp-verify.com","vk-login.com",
  "tg-verify.com","telegram-login.com","tg-login.com","telegram-kz.com",
  // Госуслуги / ЕНПФ / НАО фишинг
  "enpf-kz.com","enpfonline.kz","enpf-login.kz","enpf-verify.kz",
  "salyk-kz.com","salyk-online.kz","salyk-login.kz","nalogkz.com",
  "eenlik.kz","sozaqkz.com","enbek-kz.com","enbek-login.kz",
  "otbasy-bank.kz","otbasypay.kz","otbasy-kz.com"
]);

// === СКАМ / МОШЕННИЧЕСТВО ===
const OFFLINE_SCAM = new Set([
  // Фейковые магазины
  "super-sale.kz","mega-skidka.kz","iphone-free.com",
  "aliexpress-sale.kz","wildberries-sale.com","ozon-sale.kz",
  "lamoda-sale.kz","kaspi-mall.com","kaspi-shop.kz",
  "iphone15-free.com","samsung-free.kz","apple-promo.kz","airpods-free.kz",
  "blackfriday-kz.com","sale99.kz","megasale.kz","supersale.kz",
  "onlinesale.kz","internet-magazin.kz","shopkz.com","buy-kz.com",
  // Фейковые инвестиции
  "tesla-invest.com","amazon-invest.kz","gazprom-invest.com",
  "easy-money-bot.com","crypto-doubler.com","bitcoin-generator.com",
  "forex-profit.kz","trading-signals.kz","invest-kz.com",
  "tenge-cash.com","tenge-invest.kz","profit-kz.com",
  "trading-bot-kz.com","ai-invest.kz","robot-trader.kz","autotrader.kz",
  "fx-kz.com","fxkz.com","forexkz.com","forex-kz.com",
  "invest-500.kz","invest-1000.kz","x2money.kz","doublemoney.com",
  "elon-invest.kz","tesla-token.com","spacex-invest.kz",
  // Фейковые лотереи
  "free-lottery.com","mega-prize.com","lucky-winner.com",
  "kcell-prize.com","beeline-lucky.com","kaspi-winner.kz",
  "lottery-kz.com","loto-kz.com","bingo-kz.com","jackpot-kz.com",
  "winner2024.kz","winner2025.kz","prizekz.com","prize-kz.com",
  "kaspi-lottery.kz","halyk-lottery.kz","kcell-lottery.kz",
  // Дропшиппинг скам / Фейковые работы
  "dropship-guru.com","passive-income-bot.com",
  "rabota-iz-doma.kz","udalenka.kz","freelance-kz.com","earn-kz.com",
  "work-online.kz","zarabotok-kz.com","biznes-online.kz",
  "operator-kz.com","menedzher-kz.com","kurier-kz.com",
  // Tech support scam
  "microsoft-support.kz","google-support.kz","apple-support.kz",
  "windows-support.kz","virus-support.kz","pc-support.kz",
  // Fake job offers (поддельные вакансии)
  "job-kz.com","rabota-kz.com","headhunter-kz.com",
  "vakansii-kz.com","trud-kz.com","career-kz.com","jobkz.com",
  // Fake car sales / real estate
  "auto-kz.com","avto-kz.com","car-kz.com","mashina-kz.com",
  "house-kz.com","kvartira-kz.com","nedvizhimost-kz.com",
  // Social engineering / romance scam
  "love-kz.com","dating-kz.com","poznakomsya.kz","anketa-kz.com",
  // KZ gov impersonation
  "nalogi-kz.com","pfu-kz.com","minfin-kz.com","mintrud-kz.com",
  "covid-vyplata.kz","pensiya-kz.com","lgota-kz.com","subsidiya.kz"
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
