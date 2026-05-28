#!/usr/bin/env bash
# Qalqan AI — Telegram webhook бір рет орнату скрипті
# Пайдаланылуы: ./scripts/setup_telegram_webhook.sh
#
# .env файлынан кілттерді оқиды немесе env vars ретінде алады.

set -euo pipefail

# Load .env if exists
if [[ -f ".env" ]]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
SECRET="${TELEGRAM_WEBHOOK_SECRET:-}"
API_URL="${QALQAN_API_URL:-}"

if [[ -z "$BOT_TOKEN" ]]; then
    echo "❌  TELEGRAM_BOT_TOKEN орнатылмаған (.env немесе env var)"
    exit 1
fi

if [[ -z "$API_URL" ]]; then
    echo "❌  QALQAN_API_URL орнатылмаған (мысал: https://qalqan-ai.vercel.app)"
    exit 1
fi

WEBHOOK_URL="${API_URL}/telegram/webhook"
echo "🔗  Webhook URL: $WEBHOOK_URL"

# Build payload
PAYLOAD="{\"url\": \"${WEBHOOK_URL}\", \"allowed_updates\": [\"message\", \"inline_query\"]"
if [[ -n "$SECRET" ]]; then
    PAYLOAD="${PAYLOAD}, \"secret_token\": \"${SECRET}\""
fi
PAYLOAD="${PAYLOAD}}"

echo "📡  Telegram setWebhook жіберілуде..."
RESPONSE=$(curl -s -X POST \
    "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

echo "✅  Жауап: $RESPONSE"

# Verify
echo ""
echo "🔍  Тексеру getWebhookInfo..."
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo" | python3 -m json.tool
