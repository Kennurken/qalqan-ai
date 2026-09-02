# Qalqan AI — Аудит безопасности и качества кода

**Дата:** 2026-07-02
**Версия:** 5.1.0
**Аудитор:** Елдос Қыдырбек (внутренний аудит)
**Метод:** статический анализ всего репозитория (api/, extension/, utils/, services/) + проверка live-деплоя

---

## Резюме (TL;DR)

Найдено **1 HIGH**, **4 MEDIUM**, **6 LOW**. Один HIGH — реальный stored XSS, который надо чинить до презентации. Остальное — усиление безопасности (constant-time сравнения, SSRF-hardening, cron-защита) и false-positive шумы в эвристиках.

Live-деплой здоров: `supabase: ok`, `redis: ok`, `3/6 API-ключей`, `data_files 5/5`, `demo_mode: false`.

| # | Severity | Проблема | Файл |
|---|----------|----------|------|
| H1 | **HIGH** | Stored XSS в /admin и публичном /stats | api/index.py |
| M1 | MEDIUM | Cron-эндпоинты открыты при пустом CRON_SECRET | api/index.py |
| M2 | MEDIUM | /telegram/set-webhook открыт при пустом секрете | api/index.py |
| M3 | MEDIUM | Не-constant-time сравнение секретов + нет lockout на /admin | api/index.py, api_auth.py |
| M4 | MEDIUM | SSRF TOCTOU / DNS-rebinding в domain_intel | api/services/domain_intel.py |
| L1 | LOW | XFF-spoofing → обход rate-limit (только на VPS-деплое) | api/index.py |
| L2 | LOW | Общий `_mem` dict для кэша и rate-limit | api/utils/cache.py |
| L3 | LOW | In-memory состояние на serverless (per-instance) | несколько |
| L4 | LOW | Слишком широкие эвристики → false positives | background.js, goszakup.py |
| L5 | LOW | Наивный фильтр prompt-injection | api/services/ai_analyzer.py |
| L6 | LOW | Emoji вместо SVG-иконок (косметика) | HTML-шаблоны |

---

## H1 — Stored XSS в admin-панели и публичной статистике (HIGH)

**Где:** `api/index.py` — функции `_build_rows_logs/_reports/_appeals` (эндпоинт `/admin`) и HTML-генерация в `/stats` (`top_dom_html`, `top_rep_html`).

**Суть:** пользовательские данные вставляются в HTML через f-строки **без экранирования**. `import html` / `html.escape` в файле отсутствует вообще.

Векторы (всё контролируется атакующим без авторизации):
- `POST /report` → поле `note` (500 символов свободного текста) сохраняется в Supabase `reports.comment` и рендерится сырым в `/admin`.
- `domain` берётся из `urlparse(url).hostname`, который **пропускает** HTML-метасимволы. Проверено:
  ```
  urlparse("https://abc<script>alert(1)</script>.kz").hostname
  → 'abc<script>alert(1)<'
  ```
- `/stats` (публичная страница) рендерит `top_reported_domains[].domain` сырым → XSS для любого посетителя.
- `/vote` и `/appeal` тоже кладут неэкранированные данные, которые видит админ.

**Последствие:** JS исполняется в origin `/admin` (сессия администратора) и на публичном `/stats`. На презентации это критично — судья открывает dashboard, срабатывает чужой payload.

**Фикс:**
```python
import html
# в каждой f-строке, где встраивается значение из БД:
f"<td>{html.escape(str(r.get('comment','') or '—'))}</td>"
f"<td>{html.escape(r.get('domain',''))}</td>"
# и в /stats:
f'<span class="ri-name">{html.escape(d["domain"])}</span>'
```
Плюс валидировать формат домена при приёме (`/report`, `/vote`): разрешить только `^[a-z0-9.-]+$`.

---

## M1 — Cron-эндпоинты открыты при незаданном CRON_SECRET (MEDIUM)

**Где:** `api/index.py` → `_authorize_cron`:
```python
def _authorize_cron(req):
    secret = os.getenv("CRON_SECRET", "")
    if not secret:
        return True   # ← открыто всем
```
Затрагивает `/telegram/weekly-report` (рассылка в админ-чат) и `/health/check` (alert в Telegram). Если `CRON_SECRET` не задан в Vercel — любой может дёргать эндпоинт и спамить админский Telegram.

**Фикс:** задать `CRON_SECRET` в Vercel (`openssl rand -hex 32`). Дополнительно — логировать/отклонять при отсутствии секрета в проде вместо «разрешить всё». **Проверь, что переменная реально стоит в Vercel env.**

---

## M2 — /telegram/set-webhook открыт при пустом секрете (MEDIUM)

**Где:** `api/index.py` → `set_telegram_webhook`:
```python
if secret and caller_secret != secret:
    return 403
```
Если `TELEGRAM_WEBHOOK_SECRET` не задан — проверка пропускается, и любой знающий URL может перерегистрировать webhook. В проде секрет задан (ты его ставил), но защита должна быть безусловной.

**Фикс:** требовать секрет всегда; если он не сконфигурирован — возвращать 403, а не пускать.

---

## M3 — Не-constant-time сравнение секретов + нет lockout (MEDIUM)

**Где:**
- `/admin`: `provided != admin_secret`
- webhook: `incoming != secret`
- `api_auth.verify_api_key`: обычный dict-lookup

Обычный `!=`/lookup уязвим к timing-атаке. На `/admin` вдобавок **нет rate-limit / lockout** → ADMIN_SECRET можно брутить.

**Фикс:**
```python
import hmac
if not hmac.compare_digest(provided, admin_secret): ...
```
и добавить `check_rate_limit` на `/admin` (напр. 10/min на IP).

---

## M4 — SSRF TOCTOU / DNS-rebinding в domain_intel (MEDIUM)

**Где:** `api/services/domain_intel.py`. `_is_internal_host()` резолвит DNS **как guard**, но затем `_ip_intel` (`gethostbyname`), `_check_ssl_cert` (`create_connection`) и RDAP резолвят имя **заново, независимо**. Между проверкой и подключением DNS может «перепривязаться» на внутренний IP (169.254.169.254 — cloud metadata, 127.0.0.1 и т.д.).

Также валидатор `/check` (`_PRIVATE_IP_RE`) проверяет только строку присланного host — публичное имя, указывающее A-записью на приватный IP, проходит.

**Фикс:** резолвить один раз, дальше подключаться по уже проверенному публичному IP (pin), или после connect проверять реальный peer-IP сокета. На serverless (Vercel) риск ниже, но на VPS-деплое (Hetzner из `deploy/`) — реальный.

---

## L1 — XFF-spoofing обходит rate-limit (LOW, зависит от деплоя)

`_get_client_ip` берёт первый элемент `X-Forwarded-For`. На Vercel это доверенное значение. На VPS за Caddy клиент может подставить свой XFF → обход всех per-IP лимитов + подделка geo. **Фикс:** на VPS брать реальный remote-addr доверенного прокси / крайний правый hop XFF.

## L2 — Общий `_mem` для кэша вердиктов и rate-limit (LOW)

`api/utils/cache.py`: `_mem` хранит и `(dict, expires)` вердиктов, и `([timestamps], expires)` лимитов. Коллизий ключей нет (`rl:` vs хэши), но LRU-вытеснение перемешано, а `cache_entries` в `/stats` завышен. **Фикс:** разнести в два словаря.

## L3 — In-memory состояние на serverless (LOW)

`_usage` (partner API), mem-fallback rate-limit, `_feed_domains`, `register_bot_ui` — per-instance. При недоступном Redis лимиты фактически per-instance (слабые). Это архитектурное ограничение — полагаться на Redis; просто зафиксировать в доке.

## L4 — Широкие эвристики → false positives (LOW)

- `extension/public/background.js` `quickRiskCheck`: regex `(bet|casino|slots?|poker|...)` может пометить легитимные домены с этими токенами.
- `api/services/goszakup.py` `is_goszakup_url`: ключевые слова `лот`/`tender`/`конкурс` в любом path/query маршрутизируют посторонние URL во внешний fetch к goszakup.gov.kz.

**Фикс:** ужесточить границы слов / ограничить срабатывание доменами из `_GOSZAKUP_DOMAINS` + явными путями.

## L5 — Наивный фильтр prompt-injection (LOW)

`ai_analyzer._sanitize_for_prompt` вырезает только первое вхождение из фикс-списка и обрезает длину. Инъекция в LLM всё ещё возможна. Смягчение уже есть: `response_format=json_object`, `temperature=0.05`, и scoring трактует AI как advisory. Достаточно для конкурса; для прода — усилить.

## L6 — Emoji-иконки вместо SVG (LOW, косметика)

HTML-шаблоны (`🛡`, `🔍` и т.п.) используют emoji как UI-иконки. По гайдлайну UI/UX — заменить на SVG (Heroicons/Lucide). На безопасность не влияет.

---

## Что проверено и признано ОК

- **Секреты не в git:** `.env` в `.gitignore`, `.vercel` игнорируется, service_role-ключ только в env. Grep по JWT/`sk-`/`gsk_`/`AIza` в трекнутых файлах — только false positives (integrity-хэши в package-lock, URL в датасете phishtank).
- **Логи не пишут полные URL с query** (только path) — PII/токены не текут в логи.
- **Хэширование:** в Supabase кладётся `url_hash`/`reporter_ip_hash`, не сырые значения.
- **CORS:** origin валидируется против allowlist, credentials не разрешены (cross-origin JS не читает ответы с cookie).
- **Pydantic-валидация:** max_length на всех входных полях, SSRF-regex на `/check` (частично, см. M4), image magic-bytes на `/analyze-screen`, cap на batch (15) и graph (300/1000).
- **Telegram webhook** проверяет `X-Telegram-Bot-Api-Secret-Token` (когда секрет задан).
- **Circuit breaker** на Redis — не молотит мёртвый инстанс.
- **Fire-and-forget логирование** в Supabase не блокирует ответ.

---

## Приоритет фиксов до презентации (ДЭР) — security-часть

1. **H1** — HTML-escape в /admin и /stats. ~20 минут, критично.
2. **M1** — задать `CRON_SECRET` в Vercel. 2 минуты.
3. **M2 + M3** — безусловные проверки + `hmac.compare_digest`. ~15 минут.
4. Остальное — после конкурса.

---
---

# ЧАСТЬ 2 — Полный аудит (корректность, архитектура, качество)

Прошёлся по всему коду: 17 сервисов, extension (background/content/offline-db/fingerprint), utils, ML, website, тесты, CI, деплой.

## Баги корректности

### B1 — `/stats` в Telegram-боте всегда показывает нули (HIGH по функционалу)
**Где:** `api/services/bot_handler.py` → `handle_stats` (~526–556). Бот читает ключи, которых `/stats` JSON **не возвращает**:
```python
total    = data.get("total_checks", 0)   # API отдаёт "total_reports"
blocked  = data.get("blocked", 0)        # ключа нет
phishing = data.get("by_type", {})...    # ключа нет
```
Реальные ключи `/stats`: `total_reports`, `total_reported_domains`, `auto_blocked`, `whitelist_size`, `cache_entries`. → команда `/stats` в боте **всегда 0/0/0**. Фикс: читать реальные ключи или дёргать `/trends`.

### B2 — Неверный fallback-домен в `handle_stats`
`base_url = os.getenv("QALQAN_API_URL", "https://qalqan-ai.vercel.app")` — без `-nu`. Везде в проекте `qalqan-ai-nu.vercel.app`. Если env не задан → бьёт по несуществующему домену.

### B3 — Два разных определения «auto_blocked»
`utils/supabase.py::community_auto_block` (Sybil-стойкое: `reports+confirms>=5 AND unique_ips>=3 AND confirms>disputes`) vs `get_trends` (`auto_blocked = c >= 5`, только счётчик). Публичный `/stats` и реальная блокировка расходятся. Одна функция-источник истины.

## Архитектура

### A1 — Пайплайн продублирован 3 раза (риск дрейфа)
`_run_url_check` (`/check`), `_check_one` (`/batch`), `check_research` (`/check-research`) реализуют тиры заново. `/batch` **не вызывает** `community_verdict` и goszakup-тир, иначе трактует AI-fallback → `/batch` и `/check` дают **разные вердикты** для одного URL. Вынести в одну функцию с флагами.

### A2 — `index.py` = 2016 строк (монолит)
HTML `/stats` и `/admin` (~250 строк) инлайнятся в роутерах, хотя `templates.py` уже есть. Перенести. Плюс десятки локальных `from fastapi.responses import ...` — поднять наверх.

### A3 — ML-модель существует, но НЕ подключена
`ml/serve_model.py` (XLM-RoBERTa, torch) — отдельный сервис, `grep` по `api/` не находит ссылок. «ML-тир» — это на деле `url_features.py` (правила + Левенштейн + энтропия), не обученная модель. **На презентации:** не называй `url_features` «машинным обучением». Либо подключи модель тиром, либо позиционируй как «ML-features + эвристики».

### A4 — Дублирование лендинга
`website/` (React, отдельный Vercel-проект) и `templates.py::LANDING_HTML` (инлайн на `/`) — две посадочные. Решить, что канон.

## Производительность

- **P1** — `threat_report.py` тянет matplotlib (~50 МБ) + reportlab. Импорты ленивые (ок), но риск по размеру бандла / cold-start `/report/generate` на Vercel. Проверить лимит.
- **P2** — `load_openphish_feed` на старте качает OpenPhish+URLhaus (до 80k строк) in-memory, не персистит → каждый cold-start качает заново. Кэшировать в Redis/KV.
- **P3** — `check_domain_intelligence` = 4 сетевых round-trip на домен (getaddrinfo+gethostbyname+SSL:443+RDAP). Дорогой путь для «чистых» доменов; смягчено кэшем вердикта (6ч).

## Privacy

- **PR1** — `virustotal.py` при 404 **сабмитит URL на скан** в VT → посещённые пользователем URL уходят третьей стороне (VT их публикует). Задокументировать; рассмотреть только-lookup без submit.

## Мёртвый код / гигиена

- **G1** — 4 генератора PPTX в корне (`create_pptx.py`, `create_defense_pptx.py`, `create_roadmap_pptx.py`, `render_slides.py`) + `.pptx` артефакты. Вынести в `tools/` или gitignore.
- **G2** — escape-хелперы продублированы (`content.js::esc`, `telegram.py::_escape_md`, `bot_handler.py::_esc`), а в `index.py` его нет (см. H1). Централизовать серверный escape.
- **G3** — номер тира плавает: «6-tier» (API/stats), «7-tier» (память проекта). Привести к одному.

## Тесты и CI (положительное)

- **20 тест-файлов** (`test_security`, `test_ssrf`, `test_phone`, `test_scoring`, `test_bot`, `test_goszakup_graph`, …).
- **CI зелёный:** `Backend Tests` (pytest 3.12) и `Build Extension` проходят на последних пушах.
- Локально pytest не идёт: на машине только Python 3.14 без fastapi/pydantic. Прогон: `python3 -m venv .venv && .venv/bin/pip install -r api/requirements.txt pytest && .venv/bin/pytest -q`.
- **content.js — XSS-safe:** блок-страница строит DOM только через `esc()`. Клиентская часть сделана правильно (контраст с серверным H1).
- **CSP расширения** строгий: `script-src 'self'`, `connect-src` только свой домен.

## Приоритет (полный)

**До ДЭР:** H1 (XSS) → B1+B2 (бот `/stats` = нули, видно на демо) → M1 (CRON_SECRET) → A3 (не называть features «ML»).
**После:** M2, M3, M4, A1 (дедуп пайплайна), A2 (рефактор), P1/P2, G1 (чистка корня).
