# PDF Delivery Plan

Goal: when someone buys Weekly, Monthly, or Yearly access, they automatically receive the Felix Crypto Edge PDF by email.

## Best simple setup

Use Stripe Payment Links + Stripe automation/Zapier/Make later.

Flow:

1. Customer buys Weekly, Monthly, or Yearly subscription.
2. Payment succeeds in Stripe.
3. Automation triggers from `checkout.session.completed` or successful subscription event.
4. Buyer receives email with:
   - welcome message
   - PDF download link or attachment
   - tool access instructions
   - education/risk disclaimer

## No-cost/manual MVP

Before paying for automation tools:

1. Customer pays by Stripe/PayPal payment link.
2. Payment notification arrives by email.
3. Josh sends the PDF manually from Outlook.

Manual delivery is acceptable for first customers and avoids subscriptions before validation.

## Later automated options

- Stripe + Zapier/Make email automation
- Stripe webhook + small server script on VPS
- Gumroad/Payhip as an easier digital product platform, if fees are acceptable

## Email template

Subject: Your Felix Crypto Edge Guide + Early Access

Hi {{name}},

Thanks for joining Felix Crypto Edge.

Attached is your Beginner Crypto Chart Trading Guide. Your chart tool access instructions will follow separately / are below:

{{tool_access}}

Important: Felix Crypto Edge is for education only. It is not financial advice or a guarantee of profit. Crypto trading is risky and you can lose money.

Josh
Felix Crypto Edge
