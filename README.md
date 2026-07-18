# 🛡️ QALQAN AI — Кибер Қалқан

AI-платформа, защищающая казахстанцев от фишинга, телефонного мошенничества, финансовых пирамид, нелегального гемблинга и фрода в госзакупках. Сделана для республиканского конкурса ДЭР.

**Точность**: 97% accuracy · F1 0.98 · 0 ложных срабатываний на открытом бенчмарке · **Live**: [qalqan-ai-nu.vercel.app](https://qalqan-ai-nu.vercel.app) · **3 языка**: Қазақша / Русский / English · **Открытый код**

> За 10 мес. 2025 казахстанцы потеряли **16,4 млрд ₸** от киберскама (×29 к 2024), **26 300 случаев** (+86%). Телефонное мошенничество — угроза №1.

---

## Попробовать вживую

| Что | Ссылка |
|---|---|
| 🌐 Лендинг + проверка URL | [`/`](https://qalqan-ai-nu.vercel.app/) |
| 📊 Дашборд регулятора + KZ-карта угроз | [`/dashboard?demo=1`](https://qalqan-ai-nu.vercel.app/dashboard?demo=1) |
| 🕸️ Граф фрода в госзакупках | [`/goszakup/graph`](https://qalqan-ai-nu.vercel.app/goszakup/graph) |
| 📱 Мобильное PWA (offline) | [`/m`](https://qalqan-ai-nu.vercel.app/m) |
| 🏛️ B2G API для банков/регуляторов | [`/partners`](https://qalqan-ai-nu.vercel.app/partners) |
| 🤖 Telegram-бот (голос/SMS/URL + QR-сканер в Mini App) | [@QalqanAI_bot](https://t.me/QalqanAI_bot) |
| 🎯 Скам-тренажёр — узнаёшь ли ты мошенника? | [`/quiz`](https://qalqan-ai-nu.vercel.app/quiz) |
| 🔑 Проверка утечки пароля (HIBP, k-anonymity) | [`/leak`](https://qalqan-ai-nu.vercel.app/leak) |
| 🔬 Оценка безопасности сайта (A–F) | [`/scan`](https://qalqan-ai-nu.vercel.app/scan) |
| 🎯 Защита бренда от фишинга (typosquat radar) | [`/brand`](https://qalqan-ai-nu.vercel.app/brand) |
| 🆘 Обманули? Куда обращаться (1477) | [`/help`](https://qalqan-ai-nu.vercel.app/help) |
| 🌐 Открытый KZ threat-feed (CC-BY) | [`/feed/kz`](https://qalqan-ai-nu.vercel.app/feed/kz) |

```bash
# Проверить фишинговый клон Kaspi (кириллическая «а»):
curl -X POST https://qalqan-ai-nu.vercel.app/check \
  -H "Content-Type: application/json" -d '{"url":"https://kаspi.kz/login","lang":"ru"}'
# → DANGEROUS 100, indicators: homoglyph_attack, brand_impersonation
```

---

## Что детектит

| Угроза | Метод |
|---|---|
| Фишинг KZ-брендов (Kaspi/eGov/Halyk-фейки) | Homoglyph/typosquat + KZ brand DB |
| **Телефонное мошенничество (голос)** | Whisper-транскрипция → 11 KZ скам-паттернов |
| Скам-номера телефонов | Эвристики префиксов (КНБ) + паттерны |
| Финансовые пирамиды | АФМ/АРРФР-реестр по названию + домен-база + AI |
| Нелегальный гемблинг | Офлайн-база + regex (1xBet, Mostbet…) |
| Фишинг (общий) | PhishTank + OpenPhish + URLhaus + Google Safe Browsing |
| Новые домены (<30 дней) | RDAP domain intelligence |
| **Фрод в госзакупках (аффилированность/сговор/картель)** | Граф связей заказчик↔поставщик↔учредитель↔адрес↔чиновник |
| Скам SMS/сообщения (kk/ru) | Текст-анализ + извлечение ссылок |

---

## Платформы

- **🌐 Веб** — лендинг с живой проверкой, дашборд регулятора с KZ-картой угроз, граф госзакупок
- **📱 Мобилка** — installable PWA (`/m`), работает офлайн, на главный экран Android/iOS
- **🧩 Расширение** — Chrome/Firefox MV3, блок до загрузки страницы, офлайн-база 390+ доменов
- **🤖 Telegram-бот** — `/check`, `/phone`, `/pyramid`, голосовые сообщения, inline-кнопки голосования
- **🏛️ B2G API** — `X-API-Key`, эндпоинты `/v1/*` для банков/регуляторов, federated-обмен угрозами

---

## Архитектура — 7-уровневый pipeline

```
POST /check → FastAPI (Vercel)
  ├── Tier 0   — Whitelist
  ├── Tier 0.5 — Cache (Upstash Redis)
  ├── Tier 1   — Офлайн-база: пирамиды, blacklist, KZ-бренды, гемблинг, threat-feeds
  ├── Tier 1.9 — Goszakup fraud detection
  ├── Tier 2   — Внешние БД: PhishTank, SafeBrowsing, URLhaus, OpenPhish + RDAP/SSL
  ├── Tier 2.7 — Краудинтеллект (авто-блок сообщества) + fine-tuned XLM-RoBERTa
  │              (отдельный ML-сервис, ML_SERVICE_URL — опционально)
  └── Tier 3   — Groq llama-3.3-70b → Gemini 2.5-flash → эвристики
```

Краудинтеллект: жалобы граждан + голоса сообщества + контрибуции партнёров (federated) → авто-блок при пороге. Все данные анонимны — храним хеши URL/IP, не сырьё.

---

## Стек

**Backend** — FastAPI (Python 3.11) на Vercel serverless · Groq (llama-3.3-70b + Whisper) · Gemini 2.5-flash · Supabase Postgres · Upstash Redis · httpx (async)
**Frontend** — React 19 + Vite (расширение, website) · vanilla SVG-дашборды/граф · PWA + service worker
**Данные** — PhishTank/OpenPhish/URLhaus/SafeBrowsing · RDAP · Goszakup.gov.kz API · кастомные KZ-базы (пирамиды/гемблинг/бренды/АФМ)
**CI** — GitHub Actions (билд расширений) · 148 авто-тестов (pytest)

---

## API (основные эндпоинты, 45+)

| Группа | Эндпоинты |
|---|---|
| Проверка | `POST /check` `/check-text` `/sms` `/phone` `/voice` `/advisor` `/batch` `/analyze-screen` |
| Пирамиды/госзакуп | `POST /pyramid/check` `/goszakup/analyse` `/goszakup/graph` · `GET /goszakup/check/{n}` |
| Крауд | `POST /report` `/vote` · `GET /community/{domain}` |
| Аналитика | `GET /dashboard/data` `/trends` `/stats` `/report/generate` (PDF) |
| Фиды | `GET /feed/kz` `/feed/federated` (CC-BY) |
| B2G (X-API-Key) | `POST /v1/check` `/v1/batch` `/v1/phone` `/v1/contribute` · `GET /v1/feed` `/v1/usage` |
| Ops | `GET /health` `/health/check` (cron-gated) |

---

## Setup

```bash
# Backend (local)
pip install -r api/requirements.txt
cp .env.example .env          # вписать ключи (все бесплатные, без карты)
uvicorn api.index:app --reload --port 8000

# Тесты
pip install pytest && pytest

# Расширение
cd extension && npm install && npm run build   # → chrome://extensions → Load unpacked → dist/
```

Ключи (`.env.example`): `GROQ_API_KEY` (обязательно), `GEMINI_API_KEY`, `GOOGLE_SAFE_BROWSING_KEY`, `SUPABASE_URL`/`SUPABASE_SERVICE_KEY`, `TELEGRAM_BOT_TOKEN`, `UPSTASH_REDIS_*`. Прод: добавить в Vercel → Settings → Environment Variables.

**Опциональные env:** `TELEGRAM_CHANNEL_ID` (публичный канал угроз), `CRON_SECRET` (защита cron), `QALQAN_API_KEYS` (партнёрские B2G-ключи), `QALQAN_EXTENSION_IDS` (CORS-пин), `DEMO_MODE`.

---

## Мониторинг (рекомендуется)

`GET /health` — статус сервиса (Supabase/Redis/ключи). `GET /health/check` — алертит админу в Telegram при деградации (защищён `CRON_SECRET`).

**UptimeRobot (5 мин, бесплатно):** [uptimerobot.com](https://uptimerobot.com) → Add Monitor → HTTP(s) → `https://qalqan-ai-nu.vercel.app/health` → интервал 5 мин → алерт на email/Telegram. Падение прода видно мгновенно.

---

## Документы

- [`DEMO.md`](DEMO.md) — сценарий защиты (что показывать жюри, 8–10 мин)
- [`AUDIT_2026-06-20.md`](AUDIT_2026-06-20.md) — A-Z аудит, план масштабирования/инвестиций/языков

---

## Безопасность

Храним только хеши (`url_hash`/`ip_hash`), не сырые URL/IP. SSRF-защита (блок internal/metadata/encoded-IP). Rate-limiting по IP. Telegram-webhook с secret-token. CORS-пин для расширения. Cron-эндпоинты за `CRON_SECRET`.

---

**Сделано в Казахстане** · Республиканский конкурс ДЭР 2026
