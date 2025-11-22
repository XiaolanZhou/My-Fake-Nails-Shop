# MY1STWEBSITE

## Payments (Stripe)

This project uses [Stripe Checkout](https://stripe.com/docs/checkout) for secure payments.

1. Create a Stripe account and generate API keys.
2. In your `.env` (backend) add:

```
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
FRONTEND_URL=http://localhost:5173
```

3. Start the backend as usual (`python server/run.py`).
4. In a separate terminal, forward Stripe webhooks:

```
stripe listen --forward-to localhost:5001/api/payments/webhook
```

5. Copy the signing secret shown in the CLI to `STRIPE_WEBHOOK_SECRET`.

Once configured, pressing **Checkout** in the cart will redirect customers to a Stripe-hosted payment page. After successful payment, they are returned to `/orders` and their order is recorded in the database.


To run:
at root, source .venv/bin/activate

run the backend:
python server/run.py

run the frontend:
cd client
npm run dev