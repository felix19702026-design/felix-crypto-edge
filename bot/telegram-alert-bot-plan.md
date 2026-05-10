# Felix Crypto Edge Telegram Alert Bot Plan

Goal: paid subscribers receive Telegram educational watch alerts generated from TradingView indicator alerts.

## MVP flow

1. Subscriber pays for Weekly / Monthly / Yearly access.
2. We create subscriber record with:
   - Telegram chat ID
   - subscription status
   - unique webhook secret
   - plan expiry date
3. Subscriber installs the TradingView Pine Script indicator.
4. Subscriber creates TradingView alert using the webhook JSON from their account page.
5. TradingView sends webhook to our VPS.
6. VPS verifies secret + active subscription.
7. Bot sends Telegram message.

## Example Telegram message

BTCUSDT possible BUY WATCH zone on 1H

Trend: bullish
Context: near support, RSI neutral
Price: {{close}}

Educational alert only. Not financial advice. Crypto trading is risky.

## Needed later

- Bot token from BotFather
- Small VPS webhook server
- Subscriber database/file
- Stripe subscription webhook integration
- Access dashboard login

No external messages or bot setup should happen without Hans approval.
