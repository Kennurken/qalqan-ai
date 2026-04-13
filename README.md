# 🛡️ QALQAN AI v3.0 — Cyber Shield

AI-powered cybersecurity browser extension. Protects users from scams, phishing, financial pyramids, and malicious content.

## Architecture: 3-Tier Threat Detection

```
Tier 0: Whitelist + Cache           (< 5ms)
Tier 1: Pyramid DB + Blacklist      (< 10ms)
Tier 2: PhishTank + SafeBrowsing +  (< 500ms)
        URLhaus + OpenPhish
Tier 3: Gemini AI Deep Analysis     (< 3s)
```

## Tech Stack

- **Backend**: FastAPI (Python) on Vercel
- **Extension**: React 19 + Vite, Chrome MV3
- **AI**: Google Gemini 2.5 Flash
- **Databases**: PhishTank, Google Safe Browsing, URLhaus, OpenPhish
- **Languages**: Қазақша / Русский / English

## Setup

### Backend (Vercel)
```bash
cd api
pip install -r requirements.txt
uvicorn index:app --reload
```

### Extension
```bash
cd extension
npm install
npm run build
# Load dist/ as unpacked extension in Chrome
```

### Environment Variables
Copy `.env.example` → `.env` and fill in API keys.

## Made in Kazakhstan 🇰🇿

клауд Елдоса N1
