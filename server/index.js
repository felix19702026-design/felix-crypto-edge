const express = require('express');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const nodemailer = require('nodemailer');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../')));

const SUBSCRIBERS_FILE = path.join(__dirname, '../subscribers.json');

// Email setup using Outlook SMTP
const transporter = nodemailer.createTransporter({
  host: 'smtp-mail.outlook.com',
  port: 587,
  secure: false,
  auth: {
    user: 'Felix20261970@outlook.com',
    pass: process.env.OUTLOOK_APP_PASSWORD
  }
});

function sendSetupEmail(to) {
  const mailOptions = {
    from: 'Felix Crypto Edge <Felix20261970@outlook.com>',
    to: to,
    subject: 'Your Felix Crypto Edge Access',
    html: `
      <h2>Welcome to Felix Crypto Edge!</h2>
      <p>Your account has been activated. Here's how to get started:</p>
      
      <h3>1. TradingView Indicator</h3>
      <p>Download the Pine Script indicator here:</p>
      <a href="https://github.com/felix19702026-design/felix-crypto-edge/raw/main/tradingview/felix-crypto-edge-indicator.pine">Download Indicator</a>
      
      <h3>2. Web Dashboard</h3>
      <p>Access your dashboard:</p>
      <a href="http://92.112.180.196:8080/tool/">Open Dashboard</a>
      
      <h3>3. Telegram Alerts</h3>
      <p>Join our Telegram channel for alerts:</p>
      <p>Link coming soon</p>
      
      <h3>4. Setup Guide</h3>
      <p>Read the setup instructions:</p>
      <a href="https://github.com/felix19702026-design/felix-crypto-edge/blob/main/tradingview/README.md">Setup Guide</a>
      
      <hr>
      <p><strong>Important:</strong> Felix Crypto Edge is for education only. Not financial advice. Crypto trading is risky.</p>
      <p>Questions? Reply to this email.</p>
    `
  };
  
  return transporter.sendMail(mailOptions);
}

function getSubscribers() {
  if (!fs.existsSync(SUBSCRIBERS_FILE)) return [];
  return JSON.parse(fs.readFileSync(SUBSCRIBERS_FILE, 'utf8'));
}

function saveSubscribers(subs) {
  fs.writeFileSync(SUBSCRIBERS_FILE, JSON.stringify(subs, null, 2));
}

// Free coupon activation
app.post('/api/activate-free', (req, res) => {
  const { email, coupon } = req.body;
  
  if (coupon !== 'THISISMYTEST128903') {
    return res.status(400).json({ error: 'Invalid coupon' });
  }
  
  const subscribers = getSubscribers();
  
  // Check if already used
  if (subscribers.find(s => s.email === email)) {
    return res.status(400).json({ error: 'Email already activated' });
  }
  
  const subscriber = {
    email,
    coupon,
    plan: 'free_trial',
    activatedAt: new Date().toISOString(),
    expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // 24 hours
    status: 'active'
  };
  
  subscribers.push(subscriber);
  saveSubscribers(subscribers);
  
  // Send email with setup instructions
  try {
    await sendSetupEmail(email);
    res.json({ 
      success: true, 
      message: 'Activated! Check your email for setup instructions.',
      subscriber
    });
  } catch (err) {
    // Still activate even if email fails
    res.json({ 
      success: true, 
      message: 'Activated! Email failed to send. Contact support for setup instructions.',
      subscriber
    });
  }
});

// Stripe checkout for paid plans
app.post('/api/create-checkout', async (req, res) => {
  try {
    const { priceId, email } = req.body;
    
    const sessionData = {
      payment_method_types: ['card'],
      line_items: [{ price: priceId, quantity: 1 }],
      mode: 'subscription',
      success_url: 'http://92.112.180.196:8080/success.html',
      cancel_url: 'http://92.112.180.196:8080/checkout.html',
      customer_email: email,
    };
    
    const session = await stripe.checkout.sessions.create(sessionData);
    res.json({ url: session.url });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// Stripe webhook for successful payments
app.post('/api/stripe-webhook', express.raw({type: 'application/json'}), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;
  
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }
  
  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    const subscribers = getSubscribers();
    subscribers.push({
      email: session.customer_email,
      plan: session.subscription ? 'paid' : 'trial',
      stripeSessionId: session.id,
      activatedAt: new Date().toISOString(),
      status: 'active'
    });
    saveSubscribers(subscribers);
  }
  
  res.json({received: true});
});

// Check coupon validity
app.get('/api/check-coupon/:code', (req, res) => {
  const valid = req.params.code === 'THISISMYTEST128903';
  res.json({ valid, percent_off: valid ? 100 : 0 });
});

app.listen(3000, '0.0.0.0', () => {
  console.log('Server running on port 3000');
});
