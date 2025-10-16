# 🎨 Hera - AI Coloring Book Platform

Create custom AI-generated coloring books with Stripe payments and email delivery.

## 🚀 Stack

- **Frontend**: React 18 + Vite
- **Backend**: Flask (Python)
- **Payment**: Stripe (Test Mode)
- **Email**: Gmail SMTP (Free - 500/day)
- **AI**: Google Imagen 4.0
- **PDF**: ReportLab

## 📦 Déploiement

### Backend (Render.com)
1. Push code to GitHub
2. Create Web Service on Render
3. Root Directory: `aipart`
4. Build: `pip install -r requirements.txt`
5. Start: `gunicorn generated_image:app --bind 0.0.0.0:$PORT --timeout 300`

### Frontend (Vercel)
1. Deploy from GitHub
2. Framework: Vite
3. Build: `npm run build`
4. Output: `dist`

## 🔑 Environment Variables

See `aipart/.env.example` for required variables.

## 📚 Documentation

- `DEPLOYMENT_GUIDE.md` - Full deployment instructions
- `GMAIL_SMTP_SETUP.md` - Gmail configuration guide
- `PAYMENT_SETUP.md` - Stripe integration details

## ✅ Features

- ✅ Multi-theme selection
- ✅ AI-generated coloring pages
- ✅ B&W and Colored editions
- ✅ Stripe payment integration (Korean wallets supported)
- ✅ Email delivery (confirmation + PDF)
- ✅ PDF generation with custom pages

## 🔒 Security

- All API keys in `.env` (not committed)
- HTTPS enforced in production
- Stripe webhook signature verification
- CORS configured

## 💰 Pricing

- **Digital PDF**: $9.99 USD
- **Physical Book**: $24.99 USD (shipping address collected)

## 🎯 Test Mode

Currently running in **Stripe Test Mode**:
- Test card: `4242 4242 4242 4242`
- No real charges
- Safe for development

## 📧 Support

Email: hera.work.noreply@gmail.com
