# 🛡️ Qalqan AI

AI-powered protection for Kazakhstan against phishing, phone-call fraud, financial
pyramids, illegal gambling, and public-procurement fraud — across a browser
extension, a mobile PWA, and a Telegram bot.

**97% accuracy · F1 0.98 · zero false positives** on the built-in benchmark.
Three languages (Қазақша / Русский / English).

**Live:** [qalqan-ai-nu.vercel.app](https://qalqan-ai-nu.vercel.app) · **Bot:** [@QalqanAI_bot](https://t.me/QalqanAI_bot)

---

## Try it live

| | Link |
|---|---|
| Landing + URL check | [`/`](https://qalqan-ai-nu.vercel.app/) |
| Website security grade (A–F) | [`/scan`](https://qalqan-ai-nu.vercel.app/scan) |
| Brand-protection radar (typosquats) | [`/brand`](https://qalqan-ai-nu.vercel.app/brand) |
| Password-leak check (HIBP, k-anonymity) | [`/leak`](https://qalqan-ai-nu.vercel.app/leak) |
| Scam trainer (quiz, kk/ru) | [`/quiz`](https://qalqan-ai-nu.vercel.app/quiz) |
| Economic-impact calculator | [`/impact`](https://qalqan-ai-nu.vercel.app/impact) |
| Regulator dashboard + threat map | [`/dashboard`](https://qalqan-ai-nu.vercel.app/dashboard) |
| Procurement-fraud graph | [`/goszakup/graph`](https://qalqan-ai-nu.vercel.app/goszakup/graph) |
| Mobile PWA (offline) | [`/m`](https://qalqan-ai-nu.vercel.app/m) |
| Open KZ threat feed (CC-BY) | [`/feed/kz`](https://qalqan-ai-nu.vercel.app/feed/kz) |

```bash
# Check a Kaspi phishing clone (Cyrillic "а"):
curl -X POST https://qalqan-ai-nu.vercel.app/check \
  -H "Content-Type: application/json" -d '{"url":"https://kаspi.kz/login","lang":"ru"}'
# → DANGEROUS 100 · indicators: homoglyph_attack, brand_impersonation
```

---

## What it detects

| Threat | Method |
|---|---|
| KZ-brand phishing (Kaspi / eGov / Halyk clones) | Homoglyph & typosquat detection + brand DB |
| Phone-call fraud (voice) | Whisper transcription + KZ scam-pattern matching |
| Scam phone numbers | Prefix heuristics + pattern rules |
| Financial pyramids | AFM/ARDFM registry lookup + domain DB + AI |
| Illegal gambling | Offline DB + brand regex (1xBet, Mostbet…) |
| General phishing | PhishTank + OpenPhish + URLhaus + Google Safe Browsing |
| Newly registered domains | RDAP domain intelligence |
| Procurement fraud | Affiliation / collusion / cartel graph analysis |
| Scam SMS & messages (kk/ru) | Text analysis + link extraction |

---

## Platforms

- **Web** — landing with live checking, regulator dashboard with a KZ threat map, procurement-fraud graph
- **Mobile** — installable PWA (`/m`), works offline
- **Extension** — Chrome/Firefox MV3: blocks pages before they load, annotates search results, 390+ offline domains
- **Telegram bot** — URL / phone / SMS / voice / QR checks, inline mode, community voting
- **Partner API** — `X-API-Key`, `/v1/*` endpoints for banks and regulators, federated threat sharing

---

## Architecture — 7-tier pipeline

```
POST /check → FastAPI (Vercel)
  ├── Tier 0    — Whitelist
  ├── Tier 0.5  — Cache (Upstash Redis)
  ├── Tier 1    — Offline DB: pyramids, blacklist, KZ brands, gambling, threat feeds
  ├── Tier 1.9  — Procurement-fraud detection
  ├── Tier 2    — External DBs: PhishTank, Safe Browsing, URLhaus, OpenPhish + RDAP/SSL
  ├── Tier 2.7  — Community auto-block + fine-tuned XLM-RoBERTa (optional, ML_SERVICE_URL)
  └── Tier 3    — Groq llama-3.3-70b → Gemini 2.5-flash → heuristics
```

Crowd intelligence (user reports + community votes + partner contributions) auto-blocks
domains past a threshold. Only hashes are stored (`url_hash` / `ip_hash`), never raw URLs or IPs.

---

## Stack

- **Backend** — FastAPI (Python 3.11) on Vercel serverless · Groq (llama-3.3-70b + Whisper) · Gemini 2.5-flash · Supabase Postgres · Upstash Redis
- **Frontend** — React 19 + Vite (extension) · vanilla SVG dashboards/graph · PWA + service worker
- **Data** — PhishTank / OpenPhish / URLhaus / Safe Browsing · RDAP · goszakup.gov.kz API · custom KZ datasets
- **CI** — GitHub Actions (extension builds) · 150 automated tests (pytest)

---

## API

| Group | Endpoints |
|---|---|
| Checks | `POST /check` `/check-text` `/sms` `/phone` `/voice` `/advisor` `/batch` `/analyze-screen` |
| Tools | `POST /brand/scan` · `GET /scan/{domain}` |
| Pyramids / procurement | `POST /pyramid/check` `/goszakup/analyse` `/goszakup/graph` · `GET /goszakup/check/{n}` |
| Crowd | `POST /report` `/vote` · `GET /community/{domain}` |
| Analytics | `GET /dashboard/data` `/trends` `/stats` `/report/generate` (PDF) |
| Feeds | `GET /feed/kz` `/feed/federated` (CC-BY) |
| Partner (X-API-Key) | `POST /v1/check` `/v1/batch` `/v1/phone` `/v1/contribute` · `GET /v1/feed` `/v1/usage` |
| Ops | `GET /health` `/health/check` |

---

## Setup

```bash
# Backend
pip install -r api/requirements.txt
cp .env.example .env          # fill in keys (all free tiers, no card)
uvicorn api.index:app --reload --port 8000

# Tests
pip install pytest && pytest

# Extension
cd extension && npm install && npm run build   # → chrome://extensions → Load unpacked → dist/
```

Required keys: `GROQ_API_KEY`. Recommended: `GEMINI_API_KEY`, `GOOGLE_SAFE_BROWSING_KEY`,
`SUPABASE_URL` / `SUPABASE_SERVICE_KEY`, `TELEGRAM_BOT_TOKEN`, `UPSTASH_REDIS_*`.
Optional: `CRON_SECRET`, `ML_SERVICE_URL`, `QALQAN_API_KEYS`, `QALQAN_EXTENSION_IDS`, `DEMO_MODE`.
In production, set these in Vercel → Settings → Environment Variables.

---

## Security

Stores only hashes (`url_hash` / `ip_hash`), never raw URLs or IPs. SSRF protection
(blocks internal / metadata / encoded-IP targets). Per-IP rate limiting. Telegram
webhook secret-token verification. CORS pinning for the extension. Cron endpoints
gated behind `CRON_SECRET`. Constant-time secret comparison. Security headers on all responses.
