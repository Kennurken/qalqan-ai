# Qalqan AI — мониторинг (бесплатно, 10 минут)

Цель: если прод упадёт (Vercel/Supabase/Upstash), ты узнаёшь сразу, а не на защите.
Используем **UptimeRobot** (free) + готовый эндпоинт `/health`.

`/health` уже агрегирует статус Supabase + Redis:
```
GET https://qalqan-ai-nu.vercel.app/health
→ {"status":"ok","supabase":{...},"redis":{...}}
```

---

## Шаг 1. Аккаунт
1. [uptimerobot.com](https://uptimerobot.com) → **Register** (free, 50 мониторов).

## Шаг 2. Монитор на /health
1. Dashboard → **+ Add New Monitor**.
2. Параметры:
   - **Monitor Type:** `HTTP(s)` (или `Keyword`)
   - **Friendly Name:** `Qalqan AI`
   - **URL:** `https://qalqan-ai-nu.vercel.app/health`
   - **Monitoring Interval:** `5 minutes`
3. *(Лучше)* выбери **Keyword** тип и в поле keyword впиши `ok` —
   тогда алерт сработает не только при падении сервера, но и если
   `/health` вернёт `"status":"error"` (например, Supabase лёг).
4. **Create Monitor.**

## Шаг 3. Алерт в Telegram (рекомендую)
1. Settings → **Alert Contacts** → **Add Alert Contact**.
2. Type: **Telegram** → следуй инструкции (нажать Start у их бота, привязать чат).
3. Вернись в монитор → отметь этот контакт в **Alert Contacts To Notify**.
   *(Можно просто Email — он включён по умолчанию.)*

## Шаг 4. Проверка
- Через 5–10 минут монитор станет зелёным (**Up**).
- Тест алерта: можешь временно указать неверный URL → должен прийти алерт → верни обратно.

---

## Что покрывает
| Падает | `/health` показывает | UptimeRobot |
|---|---|---|
| Весь бэкенд (Vercel) | нет ответа | 🔴 алерт |
| Supabase | `supabase: error` | 🔴 алерт (Keyword) |
| Upstash Redis | `redis: error` | 🔴 алерт (Keyword) |

## Опционально (когда будет VPS)
На Hetzner добавь nightly `pg_dump` Supabase → object storage (бэкап детекций/жалоб),
и тот же UptimeRobot нацель на `https://api.qalqan.kz/health`. См. `deploy/DEPLOY.md`.
