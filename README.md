# QALQAN AI v5.1 — Кибер Қалқан / Кибер Щит

AI-powered Chrome extension protecting Kazakhstani users from phishing, financial pyramids, illegal gambling, and scams. Built for the national cybersecurity competition.

**Live**: [qalqan-ai-nu.vercel.app](https://qalqan-ai-nu.vercel.app) · **Extension**: Chrome MV3 · **3 languages**: Қазақша / Русский / English

---

## What it detects

| Threat | Detection method |
|---|---|
| KZ brand phishing (Kaspi, eGov, Halyk fakes) | Offline patterns + KZ brand DB |
| Financial pyramids / MLM | JSON blacklist (166+ schemes) + AI |
| Illegal gambling (1xBet, Mostbet, Vulkan, 80+ sites) | Offline DB + regex patterns |
| Phishing (general) | PhishTank + OpenPhish + URLhaus + Google Safe Browsing |
| New suspicious domains (<30 days old) | RDAP domain intelligence |
| Homoglyph attacks (Cyrillic in URL) | URL feature extraction |
| Fraudulent government procurement | Goszakup.gov.kz API (10 red-flag rules) |
| Scam SMS / messages in Kazakh & Russian | Text analysis endpoint |

---

## How it works — 7-tier pipeline

```
Every site visit → background.js (Service Worker)
│
├── Phase 1: INSTANT (before page renders, <1ms)
│   ├── Offline DB — 390+ known domains in memory
│   ├── Regex patterns — gambling keywords, KZ brand + free TLD
│   └── DANGEROUS → block page immediately
│
└── Phase 2: Full API (800ms debounce)
    └── POST /check → Vercel FastAPI
        ├── Tier 0   — Whitelist
        ├── Tier 0.5 — Cache (Redis)
        ├── Tier 1.5 — URL features (30+ ML signals)
        ├── Tier 1   — Pyramid DB + blacklist
        ├── Tier 1.7 — KZ brand impersonation
        ├── Tier 1.8 — Gambling DB
        ├── Tier 1.9 — Goszakup fraud detection
        ├── Tier 2   — PhishTank + SafeBrowsing + URLhaus + OpenPhish
        ├── Tier 2.5 — RDAP domain age + SSL check
        └── Tier 3   — Groq llama-3.3-70b → Gemini 2.5-flash → heuristics
```

---

## Tech Stack

**Backend**
- FastAPI (Python 3.11) — Vercel serverless, 60s timeout
- Groq `llama-3.3-70b-versatile` — primary AI (14,400 req/day free)
- Groq `llama-3.1-8b-instant` — fallback if rate-limited
- Groq `llama-4-scout-17b` — Vision AI (screenshot analysis)
- Gemini 2.5-flash — AI backup + vision backup
- httpx — async HTTP, all external calls

**Extension**
- React 19 + Vite — Chrome Manifest V3
- Service Worker — auto-check on every navigation
- Content Script — block page rendering
- Offline DB — 390+ domains, works without internet

**Data sources**
- PhishTank, OpenPhish, URLhaus, Google Safe Browsing
- Custom KZ pyramid/gambling/phishing databases
- RDAP (domain age, free, no key needed)
- Goszakup.gov.kz open data API

---

## Setup

### 1. Backend (local dev)

```bash
cd api
pip install -r requirements.txt
cp .env.example .env  # fill in API keys
uvicorn api.index:app --reload --port 8000
```

### 2. Extension

```bash
cd extension
npm install
# For local dev: set IS_DEV = true in src/config.js
npm run build
# Chrome → chrome://extensions → Developer mode → Load unpacked → select dist/
```

### 3. Environment variables

Copy `.env.example` → `.env`. All keys are free, no credit card required.

| Variable | Service | Limit | Required |
|---|---|---|---|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) | 14,400 req/day | Yes |
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com/apikey) | 250 req/day | Recommended |
| `GOOGLE_SAFE_BROWSING_KEY` | Google Cloud Console | 10,000 req/day | Recommended |
| `PHISHTANK_API_KEY` | phishtank.org | — | Optional |
| `VIRUSTOTAL_API_KEY` | virustotal.com | 500 req/day | Optional |
| `TELEGRAM_BOT_TOKEN` | @BotFather | — | Optional |
| `TELEGRAM_CHAT_ID` | @userinfobot | — | Optional |
| `SUPABASE_URL` | supabase.com | — | Recommended |
| `SUPABASE_SERVICE_KEY` | supabase.com | — | Recommended |
| `DEMO_MODE` | — | — | For presentations |

> For production deploy: add all variables to Vercel → Settings → Environment Variables.

### 4. Demo mode

Set `DEMO_MODE=true` in Vercel env vars for presentations — returns deterministic results without calling external APIs.

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/check` | POST | Main 7-tier URL check |
| `/check-text` | POST | Analyze SMS/message text for scams |
| `/batch` | POST | Check up to 10 URLs at once |
| `/analyze-screen` | POST | Vision AI screenshot analysis |
| `/appeal` | POST | Appeal a wrongful block |
| `/report` | POST | Report a malicious site |
| `/goszakup/check/{number}` | GET | Check tender number for fraud |
| `/goszakup/analyse` | POST | Analyse procurement data |
| `/report/generate` | GET | Generate PDF KZ Threat Report |
| `/health` | GET | Service status |
| `/stats` | GET | Statistics |
| `/trends` | GET | Threat trends |

---

## Project structure

```
qalqan-ai/
├── api/
│   ├── index.py              # Main router, 19 endpoints
│   ├── services/
│   │   ├── ai_analyzer.py    # Groq → Gemini → fallback chain
│   │   ├── threat_db.py      # PhishTank, SafeBrowsing, URLhaus, OpenPhish
│   │   ├── kz_intel.py       # KZ brand protection + social engineering
│   │   ├── pyramid_detector.py
│   │   ├── domain_intel.py   # RDAP + SSL
│   │   ├── goszakup.py       # Gov procurement fraud (10 rules)
│   │   ├── url_features.py   # 30+ ML features
│   │   ├── scoring.py        # Final verdict aggregation
│   │   ├── explainer.py      # XAI factor breakdown
│   │   ├── bot_handler.py    # Telegram Bot
│   │   └── threat_report.py  # PDF KZ Threat Report
│   └── data/
│       ├── pyramid_schemes.json
│       ├── kz_brands.json
│       └── kz_phishing_patterns.json
├── extension/
│   ├── public/
│   │   ├── background.js     # Service Worker, auto-check
│   │   ├── content.js        # Block page
│   │   └── offline-db.js     # 390+ domains, works offline
│   └── src/
│       ├── App.jsx
│       ├── components/       # 13 components
│       └── i18n/             # kk / ru / en (84 keys each)
└── website/                  # Landing page
```

---

## Made in Kazakhstan

Built by Eldos Kennurken for the national cybersecurity competition 2026.

`Qalqan AI`
