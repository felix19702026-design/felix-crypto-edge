// Simple Stripe Checkout session creator
// Requires STRIPE_SECRET_KEY environment variable

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async (event) => {
  const { priceId, coupon } = JSON.parse(event.body);
  
  const sessionData = {
    payment_method_types: ['card'],
    line_items: [{
      price: priceId,
      quantity: 1,
    }],
    mode: 'subscription',
    success_url: 'https://felix19702026-design.github.io/felix-crypto-edge/success.html',
    cancel_url: 'https://felix19702026-design.github.io/felix-crypto-edge/checkout.html',
  };
  
  if (coupon) {
    sessionData.discounts = [{ coupon }];
  }
  
  const session = await stripe.checkout.sessions.create(sessionData);
  
  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
    body: JSON.stringify({ url: session.url })
  };
};
