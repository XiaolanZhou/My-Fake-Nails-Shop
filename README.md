# Visit my shop website! https://meowoem.com/

## Local Development

### Backend (Flask)
```bash
# At root directory
source .venv/bin/activate
python server/run.py
```

### Frontend (Vite + React)
```bash
cd client
npm install
npm run dev
```

---

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

```bash
stripe listen --forward-to localhost:5001/api/payments/webhook
```

5. Copy the signing secret shown in the CLI to `STRIPE_WEBHOOK_SECRET`.

---

## Deployment

### Frontend (Vercel)

1. **Push your code to GitHub**

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com) and sign in
   - Click "Add New Project" → Import your GitHub repo
   - Set the **Root Directory** to `client`
   - Framework Preset: **Vite** (auto-detected)

3. **Add Environment Variables** in Vercel Dashboard:
   ```
   VITE_API_URL=https://your-backend-url.com
   ```

4. **Deploy!** Vercel will build and deploy automatically.

### Backend Options

Since the Flask backend requires a persistent database (MySQL), you'll need to deploy it separately:

| Service | Best For | Notes |
|---------|----------|-------|
| **Railway** | Easy setup | One-click Flask deploy, MySQL addon available |
| **Render** | Free tier | Web service + managed PostgreSQL/MySQL |
| **Fly.io** | Global edge | Docker-based, good for low latency |
| **AWS (EC2/ECS)** | Full control | More complex setup |
| **PlanetScale** | Managed MySQL | Serverless MySQL, works with any backend host |

#### Backend Environment Variables (Production)
```
DATABASE_HOST=your-mysql-host
DATABASE_USER=your-user
DATABASE_PASSWORD=your-password
DATABASE_NAME=my1stwebsite
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
FRONTEND_URL=https://your-vercel-app.vercel.app
JWT_SECRET_KEY=your-secret-key
```

---

## Project Structure

```
├── client/                 # React frontend (Vite)
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── context/        # Auth context
│   │   ├── config/         # API configuration
│   │   └── layout/         # Navbar, Footer
│   ├── vercel.json         # Vercel config
│   └── package.json
│
├── server/                 # Flask backend
│   ├── app/
│   │   ├── routes/         # API endpoints
│   │   └── db.py           # Database connection
│   └── run.py
│
└── database/               # SQL migrations
```
