# Felix Crypto Edge — Zero-Spend Launch Plan

## Goal
Launch a credible MVP in 48 hours without paying for tools upfront. Spend money only after Hans approves it. Do not send outreach, payment links, or public posts until Hans approves the exact message/channel.

## Offer
Felix Crypto Edge is beginner crypto chart education: a practical PDF guide plus an educational chart-analysis assistant that helps users understand trend, support/resistance, possible zones, and risk checks.

Core positioning:
- Education only, not financial or investment advice.
- No profit guarantees, no “signals that make money” claims.
- Risk-first: every example includes invalidation, stop-loss thinking, and position-size caution.
- Beginner-friendly: clear process, not hype.

## Initial product packages

### Weekly Access — €25/week
Best for trial users.
Includes:
- PDF guide access
- Tool MVP access while subscription is active
- Setup checklist
- Educational examples

### Monthly Access — €50/month
Main offer.
Includes:
- Everything in Weekly
- Ongoing updates
- Additional example setups

### Yearly Access — €220/year
Best-value annual plan.
Includes:
- Everything in Monthly
- Future beginner resources during the active subscription

## Zero-spend payment and delivery architecture

### Phase 0: Waitlist only, no payments yet
Use the current landing page email form to collect interest. This costs nothing.

Flow:
1. Visitor reads landing page.
2. Visitor submits early-access form or emails Felix20261970@outlook.com.
3. Leads are tracked manually in a spreadsheet or plain text file.
4. Hans approves when to invite first buyers.

No payment links are created or sent without Hans approval.

### Phase 1: Manual paid MVP after Hans approves payments
Lowest-friction setup once Hans approves accepting money:
1. Create Stripe Payment Links or PayPal subscription buttons for weekly/monthly/yearly plans.
2. Add links to the website only after approval.
3. Customer pays.
4. Payment notification arrives by email.
5. Josh/Hans manually sends:
   - welcome email
   - PDF guide attachment or private download link
   - tool access instructions
   - risk disclaimer
6. Access is tracked manually in a small customer sheet.

Manual access tracking fields:
- Customer name
- Email
- Plan: weekly/monthly/yearly
- Payment platform
- Start date
- Renewal/cancel date
- PDF delivered: yes/no
- Tool access delivered: yes/no
- Notes/support issues

### Phase 2: Lightweight automation later
Only after first validation and Hans approval for any paid services.

Options:
- Stripe Payment Links + Stripe customer portal for subscriptions.
- PayPal subscriptions if Stripe onboarding is slow.
- Gumroad/Payhip for easier digital-product delivery, accepting platform fees.
- Stripe webhook + small server script to email PDF/tool credentials.
- Make/Zapier automation for payment-success email delivery.
- Memberstack, Lemon Squeezy, or Firebase/Supabase auth for gated tool access.

Recommendation: start manual, validate demand, then automate once there are enough paying users to justify complexity.

## Manual MVP process

### Lead capture
- Keep current mailto form for zero spend.
- Also add a clearer fallback: “Email Felix20261970@outlook.com with subject: Early Access.”
- Manually log each lead.

### Qualification reply draft — do not send without approval
Subject: Felix Crypto Edge early access

Hi {{name}},

Thanks for joining the Felix Crypto Edge early-access list.

Quick question so we can shape the first version: what is your biggest problem when reading crypto charts — entries, exits, risk, indicators, or knowing when not to trade?

Important: Felix Crypto Edge is educational only. It is not financial advice, investment advice, or a promise of profit. Crypto trading is risky and you can lose money.

Felix Crypto Edge

### First buyer delivery draft — do not send without approval
Subject: Your Felix Crypto Edge access

Hi {{name}},

Thanks for joining Felix Crypto Edge.

Here is your beginner guide: {{pdf_link_or_attachment}}
Your chart-tool access: {{tool_access_instructions}}

Please treat everything as education and analysis support only. This is not financial advice or a guarantee of profit. Crypto trading is risky and you can lose money.

Felix Crypto Edge

## Tool MVP options with zero spend

### Option A — Manual “analysis request” MVP
Fastest validation. Customers email a coin/timeframe and receive a structured educational chart breakdown manually.

Pros:
- Launchable immediately.
- Tests whether people pay for the outcome.
- No software build needed.

Cons:
- Not scalable.
- Must avoid personalized financial advice language.

Safe format:
- Market context
- Trend observation
- Support/resistance zones
- Possible scenario A/B
- Risk reminders
- “Not a recommendation to buy or sell.”

### Option B — Static browser tool MVP
Build a simple local/web page where users enter price levels manually and get a checklist-style educational output.

Pros:
- Feels like software.
- Can be hosted free on GitHub Pages/Netlify.
- Avoids live exchange API complexity.

Cons:
- Less impressive than live charts.

### Option C — TradingView-based MVP
Use public TradingView charts and provide a written checklist/template that users apply while viewing charts.

Pros:
- No paid data feed.
- Familiar to crypto learners.

Cons:
- Tool is more of a process assistant than standalone software.

Recommendation: combine A + B for the first 48 hours. Sell the guide plus an educational analysis/checklist workflow, then build automation only if leads respond.

## Legal and risk disclaimers

Use clear disclaimers everywhere: landing page, checkout, PDF, emails, and tool screen.

Suggested disclaimer:
“Felix Crypto Edge provides educational content and analysis support only. It is not financial advice, investment advice, trading advice, or a recommendation to buy or sell any asset. Crypto trading is highly risky and you can lose some or all of your money. Past performance does not predict future results. Always do your own research and consider speaking with a qualified financial professional.”

Avoid:
- “Guaranteed profits”
- “Best signals”
- “Make €X per day”
- “We tell you when to buy/sell”
- Screenshots implying guaranteed gains
- Personalized instructions like “buy BTC now”

Prefer:
- “possible zone”
- “educational example”
- “scenario planning”
- “risk reminder”
- “not a recommendation”
- “learn a repeatable process”

## First 20 outreach/community channel ideas

Nothing should be posted or sent until Hans approves exact wording and channels.

1. Personal WhatsApp/Telegram contacts who are already interested in crypto.
2. Existing friends/family network with a soft feedback request.
3. Reddit r/CryptoCurrency beginners/daily discussion, following rules.
4. Reddit r/BitcoinBeginners, education-focused and no selling unless allowed.
5. Reddit r/CryptoMarkets, careful non-promotional feedback post if allowed.
6. Quora answers on “how to read crypto charts for beginners.”
7. Medium article: beginner crypto chart checklist.
8. LinkedIn post asking for beta testers learning crypto charts.
9. X/Twitter thread: “5 mistakes beginner crypto chart readers make.”
10. TikTok short educational clips with no income claims.
11. YouTube Shorts: support/resistance basics.
12. Instagram Reels: chart-reading mini lessons.
13. Facebook crypto beginner groups, only where self-promo is allowed.
14. Discord crypto education servers with feedback channels.
15. Telegram crypto education communities, admin permission first.
16. Product Hunt “coming soon” later, after MVP polish.
17. Indie Hackers build-in-public post.
18. Hacker News “Show HN” later if the tool has a working demo.
19. Local expat/entrepreneur Facebook groups, feedback angle.
20. Simple SEO blog posts on the website: beginner guides targeting search.

Best first approach: ask for feedback, not sales. Example angle: “I’m building a beginner-friendly crypto chart education tool and PDF. Looking for 5 beginners to review the first version.”

## Website copy improvement suggestions

Do not make external website writes without Hans approval, but these are recommended edits:

1. Hero headline
Current: “Learn where crypto trades start to make sense.”
Suggested: “Learn a safer process for reading crypto charts before you risk real money.”
Why: stronger beginner/risk positioning and less like a signal promise.

2. Hero subtext
Suggested: “A beginner PDF and educational chart assistant that helps you identify trend, support/resistance, possible scenarios, and risk checkpoints — without profit promises or hype.”

3. CTA
Current: “Join early access”
Suggested: “Get early access updates” or “Join the beginner beta list”
Why: clearer that payment/product is not live yet.

4. Pricing section note
Add: “Payments are not open yet. Early-access members will be invited first when the MVP is ready.”
Why: prevents confusion while there is no payment checkout.

5. Tool section
Change “possible buy/sell zones” to “possible scenario zones” in prominent copy.
Why: reduces financial-advice risk.

6. Early-access section
Add a stronger question: “Want to be one of the first 10 beginner testers?”
Why: creates scarcity without false claims.

7. Footer/legal
Add a short “Education only. Crypto is risky.” line in footer.

8. Add FAQ later
Questions:
- Is this financial advice? No.
- Does the tool guarantee profits? No.
- Do I need trading experience? No, it is beginner-focused.
- When do payments open? After early-access MVP approval.
- Can I cancel? Yes, if using weekly/monthly subscriptions.

## 48-hour execution checklist

### Hour 0-4: tighten the offer
- Confirm the exact promise: beginner education + chart-reading process.
- Decide MVP tool format: manual analysis, static checklist tool, or both.
- Finalize disclaimer wording.
- Create a lead tracker file/sheet.
- Prepare approved reply templates but do not send yet.

### Hour 4-12: product assets
- Finish the first PDF guide draft.
- Add examples with neutral language: scenarios, not calls.
- Create a one-page setup checklist.
- Create a sample educational chart breakdown.
- Package files into a simple delivery folder.

### Hour 12-20: website polish
- Update landing page copy to make payment status clear.
- Add FAQ/disclaimer section.
- Add “first 10 beta testers” angle if Hans approves.
- Test form/email flow.
- Host on a free platform if not already live.

### Hour 20-28: tool/checklist MVP
- Build static browser checklist or manual-analysis template.
- Add support/resistance, trend, RSI/momentum, invalidation, and risk sections.
- Create sample output for BTC/USDT as education only.
- Add disclaimer inside tool.

### Hour 28-36: outreach prep
- Pick 5 safest channels from the 20-channel list.
- Draft one feedback-first message per channel.
- Prepare a short founder story/build-in-public post.
- Hans approves exact messages before anything is posted.

### Hour 36-44: payment readiness
- Draft Stripe/PayPal plan setup steps.
- Do not create or publish paid links without Hans approval.
- Prepare customer tracker.
- Prepare delivery email and cancellation/refund policy draft.

### Hour 44-48: launch decision
- Review product, website, PDF, tool, and disclaimers.
- Hans approves either:
  - waitlist-only launch, or
  - paid beta with manual delivery.
- If approved, publish website updates and begin approved outreach.
- Track every lead and response.

## Recommended immediate next decision for Hans
Choose one launch mode:

1. Waitlist-only: safest, zero spend, collects feedback first.
2. Paid beta: faster validation, requires approved payment setup and manual delivery.
3. Free beta for 5-10 users: best product feedback, slower revenue.

Recommendation: launch waitlist/free beta first for 24-48 hours, then invite the warmest respondents into a paid beta once the guide and manual tool process feel credible.
