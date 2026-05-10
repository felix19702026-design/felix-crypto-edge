# Felix Crypto Edge TradingView Indicator

Subscriber product component: a TradingView Pine Script indicator that highlights educational setup watch zones.

## What it does

- Plots fast/slow EMAs
- Detects simple trend state
- Marks recent support/resistance
- Calculates RSI momentum
- Highlights possible buy/watch zones near support during bullish conditions
- Highlights possible sell/take-profit watch zones near resistance or hot momentum
- Provides TradingView alert conditions for webhook delivery

## Positioning

Use careful wording:

- ✅ “possible buy watch zone”
- ✅ “possible sell / take-profit watch zone”
- ✅ “educational alert”
- ❌ “guaranteed buy signal”
- ❌ “guaranteed profit”
- ❌ “financial advice”

## Manual install for subscribers

1. Open TradingView.
2. Open a crypto chart, e.g. BTCUSDT.
3. Click **Pine Editor**.
4. Paste `felix-crypto-edge-indicator.pine`.
5. Click **Add to chart**.
6. Create alerts from the indicator conditions if their TradingView plan supports alerts.

## Telegram alert architecture

TradingView alert → webhook on VPS → subscriber lookup → Telegram bot message.

Example webhook payload:

```json
{
  "secret": "subscriber_secret_here",
  "symbol": "{{ticker}}",
  "interval": "{{interval}}",
  "type": "buy_watch",
  "price": "{{close}}",
  "message": "Felix possible buy watch zone. Educational only."
}
```

Important: TradingView webhook alerts may require a paid TradingView plan for the user or for us depending on architecture.
