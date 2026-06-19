# Qalqan AI — VPS Deployment (Hetzner CX22)

Move the backend off Vercel serverless to one small always-on box. This unlocks
real cron (no Hobby once/day limit), kills the `/ping` keep-alive hack, gives
warm in-process caching, and is a cleaner "production" story for the competition.

**Cost:** Hetzner CX22 ≈ **€4.49/mo** (2 vCPU / 4 GB / 40 GB). Supabase + Upstash
stay on their managed free tiers. Landing page can stay on Vercel (optional).

---

## 0. Prerequisites
- A domain (or subdomain) you control, e.g. `api.qalqan.kz`.
- Your filled-in `.env` (copy from `.env.example`) with **all** secrets, plus:
  - `DOMAIN=api.qalqan.kz`
  - `CRON_SECRET=$(openssl rand -hex 32)`
  - `ADMIN_SECRET=$(openssl rand -hex 16)`
  - `SUPABASE_DB_URL=...` (for backups)

## 1. Create the server
1. Hetzner Cloud → **CX22**, image **Ubuntu 24.04**, add your SSH key.
2. Note the public IPv4.

## 2. DNS
Add an **A record**: `api.qalqan.kz → <server IP>`. Wait for it to resolve
(`dig +short api.qalqan.kz`). Caddy needs this before it can issue TLS.

## 3. Server setup
```bash
ssh root@<server-ip>

# Firewall — only SSH + web
ufw allow OpenSSH && ufw allow 80 && ufw allow 443 && ufw --force enable

# Docker + compose plugin
curl -fsSL https://get.docker.com | sh

# Get the code
git clone https://github.com/Kennurken/qalqan-ai.git /opt/qalqan
cd /opt/qalqan

# Secrets — paste/scp your filled .env (NEVER commit it)
nano .env        # set DOMAIN, CRON_SECRET, ADMIN_SECRET, all API keys
```

## 4. Launch
```bash
cd /opt/qalqan/deploy
docker compose up -d --build
docker compose ps           # both services healthy?
curl -s https://api.qalqan.kz/health | head
```
Caddy auto-provisions a Let's Encrypt cert on first request.

## 5. Cron (real schedules, no Vercel limits)
```bash
# Edit DOMAIN/CRON_SECRET inside, then:
crontab /opt/qalqan/deploy/crontab.example
crontab -l
```

## 6. Repoint clients to the VPS
- **Telegram webhook:** `https://api.qalqan.kz/telegram/set-webhook?secret=<TELEGRAM_WEBHOOK_SECRET>`
- **Extension:** set the API base to `https://api.qalqan.kz` in
  `extension/src/config.js` (+ `extension-firefox`), rebuild, reload.
- **Landing/CORS:** once the extension is published, pin its ID in
  `api/index.py` `_cors_origin_allowed` instead of allowing every `chrome-extension://`.

## 7. Updates
```bash
cd /opt/qalqan && git pull && cd deploy && docker compose up -d --build
```

## 8. Monitoring (free)
Point **UptimeRobot** / **BetterStack** at `https://api.qalqan.kz/health` every
5 min → Telegram/email alert. `/health` already aggregates Supabase + Redis status.

---

### Why this beats serverless here
| Problem on Vercel | Fixed by VPS |
|---|---|
| Hobby cron = once/day → `*/10 ping` won't deploy | real `crontab`, any schedule |
| Keep-alive `/ping` hack | always-on process, delete it |
| In-process `_mem` cache resets every cold start | warm cache → ~80–90% fewer Upstash commands |
| ML tier can't run in serverless | optional in-process model later (room on the box) |
| No backups of Supabase | nightly `pg_dump` cron |

### Scaling past the demo
Containerized already → when traffic grows, run multiple `app` replicas behind
Caddy, move Redis in-process/self-hosted, and upgrade Supabase. ~€5/mo today →
~$50–80/mo at ~1M checks/day.
