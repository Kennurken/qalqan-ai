# Qalqan AI — что сделать дальше (чек-лист для Елдоса)

Код готов и задеплоен. Ниже — ручные действия, которые я (Claude) не могу выполнить
за тебя (нужен доступ к твоим аккаунтам). Делай по порядку — отмечай галочки.

Прод: https://qalqan-ai-nu.vercel.app · Репо: Kennurken/qalqan-ai

---

## ✅ Шаг 1. SQL — включить карту угроз по областям (1 минута)

Без этого захват региона работает «вхолостую», карта живёт на demo-данных.

1. Открой https://supabase.com → войди → выбери проект Qalqan.
2. Слева **SQL Editor** → **New query**.
3. Вставь и нажми **Run**:
   ```sql
   ALTER TABLE check_logs ADD COLUMN IF NOT EXISTS country text,
                          ADD COLUMN IF NOT EXISTS region  text;
   ```
4. **Проверка:** должно написать `Success. No rows returned`.
   Дальше каждая проверка с казахстанского IP начнёт писать область →
   на `/dashboard` карта постепенно заполнится живыми данными.
   (Посмотреть полную demo-карту в любой момент: `/dashboard?demo=1`.)

---

## ✅ Шаг 2. Перерегистрировать Telegram-вебхук — включить кнопки голосования (1 минута)

Я добавил inline-кнопки (🚨 Растау / 🙅 Жалған дабыл / 📢 KZ-CERT). Чтобы Telegram
начал слать нажатия кнопок (callback_query), вебхук надо перерегистрировать.

1. Узнай значение `TELEGRAM_WEBHOOK_SECRET`:
   Vercel → проект **qalqan-ai** → **Settings** → **Environment Variables** →
   у `TELEGRAM_WEBHOOK_SECRET` нажми **Reveal**/глаз, скопируй.
2. Открой в браузере (подставь секрет вместо `ВСТАВЬ_СЕКРЕТ`):
   ```
   https://qalqan-ai-nu.vercel.app/telegram/set-webhook?secret=ВСТАВЬ_СЕКРЕТ
   ```
3. **Проверка:** ответ `{"ok": true, ...}`.
   Затем в боте @QalqanAI_bot: `/check kaspi-bonus123.kz` → под результатом
   появятся кнопки → нажми «Растау» → должна выскочить плашка с подтверждением.

---

## ✅ Шаг 3. CRON_SECRET — защитить cron-эндпоинты (2 минуты)

Сейчас `/telegram/weekly-report` открыт всем (если секрет не задан). Vercel сам
подставляет этот секрет в свои cron-запросы.

1. Сгенерируй секрет (в любом терминале): `openssl rand -hex 32`
   (или придумай длинную случайную строку).
2. Vercel → **qalqan-ai** → **Settings** → **Environment Variables** → **Add**:
   - Name: `CRON_SECRET`
   - Value: вставь сгенерированное
   - Environments: Production (+ Preview)
3. **Redeploy**: Deployments → последний → ⋯ → **Redeploy** (чтобы переменная подхватилась).
4. **Проверка:** открой `https://qalqan-ai-nu.vercel.app/telegram/weekly-report`
   в браузере → должно быть `403 Forbidden` (значит защита включилась).

---

## ✅ Шаг 4. Upstash → Pay-as-you-go (3 минуты)

Free-тариф ≈ 4 000 проверок/день (по ~3-4 Redis-команды на проверку). Для конкурса/
демо лучше включить PAYG — копейки (~$2-3/мес при 10k/день).

1. https://console.upstash.com → твоя Redis-база.
2. Раздел **Billing / Plan** → переключи на **Pay as you go**, привяжи карту.
3. **Проверка:** в дашборде базы лимит дневных команд больше не «hard cap».

---

## ⏳ Шаг 5. QALQAN_EXTENSION_IDS — после публикации расширения

Пока расширение не опубликовано — пропусти. После публикации в Chrome Web Store:

1. Скопируй ID расширения (из URL стора или `chrome://extensions`).
2. Vercel → Env Variables → добавь `QALQAN_EXTENSION_IDS` = `<твой_id>`
   (несколько — через запятую). Redeploy.
3. Это закроет CORS: API будут дёргать только твои расширения, не любые.

---

## 🏗️ Шаг 6. Hetzner VPS — перенос бэкенда (опционально, ~30 минут, €4.49/мес)

Даёт настоящий cron, тёплый кэш, и позже — реальную ML-модель. Полная инструкция
уже в репо: **`deploy/DEPLOY.md`**. Краткая версия:

1. Hetzner Cloud → сервер **CX22**, образ **Ubuntu 24.04**, добавь свой SSH-ключ.
2. DNS: A-запись `api.qalqan.kz → <IP сервера>`.
3. На сервере:
   ```bash
   ssh root@<ip>
   ufw allow OpenSSH && ufw allow 80 && ufw allow 443 && ufw --force enable
   curl -fsSL https://get.docker.com | sh
   git clone https://github.com/Kennurken/qalqan-ai.git /opt/qalqan
   cd /opt/qalqan && nano .env        # вставь все секреты + DOMAIN/CRON_SECRET/ADMIN_SECRET
   cd deploy && docker compose up -d --build
   curl -s https://api.qalqan.kz/health
   ```
4. Перенаправь клиентов: Telegram-вебхук на новый домен, в `extension/src/config.js`
   поменяй API-базу на `https://api.qalqan.kz`, пересобери.
5. **Мониторинг (бесплатно):** UptimeRobot на `/health` каждые 5 мин → алерт в Telegram.

Подробности и таблица «почему лучше serverless» — в `deploy/DEPLOY.md`.

---

## Приоритет
- **Сегодня (5 мин):** Шаги 1, 2, 3 — включают карту, кнопки бота, защиту cron.
- **На неделе:** Шаг 4 (Upstash).
- **Перед защитой / для масштаба:** Шаг 6 (Hetzner) + мониторинг.
- **После публикации расширения:** Шаг 5.
