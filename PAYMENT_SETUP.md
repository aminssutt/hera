# 💳 Stripe Payment Integration Guide

## ✅ Setup Complete!

Your Hera project now has full Stripe payment integration with:
- 💳 Korean payment methods (Kakao Pay, Naver Pay, Samsung Pay, PayCo)
- 🌍 International cards (Visa, Mastercard, Amex)
- 📧 Automated email delivery with Resend
- 📄 PDF generation with ReportLab

---

## 🚀 How to Run

### 1. Start Backend (Flask)
```bash
cd aipart
python generated_image.py
```
Backend runs on: `http://localhost:5000`

### 2. Start Frontend (React)
```bash
npm run dev
```
Frontend runs on: `http://localhost:3000`

---

## 🧪 Testing Payment (Test Mode)

### Use Test Cards:
- **Success Card**: `4242 4242 4242 4242`
- **Expiry**: Any future date (e.g., `12/25`)
- **CVC**: Any 3 digits (e.g., `123`)
- **Postal Code**: Any code

### Test Flow:
1. Go to `http://localhost:3000/customize`
2. Complete Steps 1-3
3. Generate preview in Step 4
4. Choose format (PDF/Physical) and type (B&W/Colored)
5. Click "Proceed to Payment"
6. You'll be redirected to Stripe Checkout
7. Use test card `4242 4242 4242 4242`
8. Complete payment
9. You'll be redirected back to `/success`

---

## 📧 Email Configuration

Emails are sent using **Resend API** from:
- **From**: `hera.work.noreply@gmail.com`
- **API Key**: Configured in `.env`

### Important Note:
For emails to work in production, you need to:
1. Verify your domain in Resend dashboard
2. Or use Resend's test domain for development

---

## 🔗 Webhook Setup (For Production)

Currently, the webhook works without signature verification for development.

### To enable webhook signature verification:

1. Install Stripe CLI:
   ```bash
   # Windows (PowerShell)
   scoop install stripe
   
   # Or download from https://stripe.com/docs/stripe-cli
   ```

2. Login to Stripe:
   ```bash
   stripe login
   ```

3. Forward webhooks to local server:
   ```bash
   stripe listen --forward-to localhost:5000/api/webhook
   ```

4. Copy the webhook secret (starts with `whsec_...`)

5. Add to `.env`:
   ```
   STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
   ```

---

## 📊 Payment Flow

```
User → Step 4 → Proceed to Payment
    ↓
Frontend calls /api/create-checkout
    ↓
Backend creates Stripe Session
    ↓
User redirected to Stripe Checkout
    ↓
User pays with Kakao/Naver/Card
    ↓
Stripe redirects to /success
    ↓
Stripe sends webhook to /api/webhook
    ↓
Backend generates book (TODO)
    ↓
Backend sends email with PDF
```

---

## 🛠️ Next Steps (TODO)

### 1. Complete Book Generation
The webhook currently logs payment success but doesn't generate the full book yet.

To implement:
- [ ] In `payment.py`, uncomment `generate_and_send_book(session)`
- [ ] Create function to generate multiple pages
- [ ] Use `pdf_generator.py` to compile PDF
- [ ] Use `email_service.py` to send email

### 2. Test Full Flow
- [ ] Test PDF generation with multiple pages
- [ ] Test email delivery
- [ ] Test physical book order flow

### 3. Production Deployment
- [ ] Update URLs in `.env` for production domain
- [ ] Enable webhook signature verification
- [ ] Switch to Stripe Live Mode (`pk_live_...`, `sk_live_...`)
- [ ] Setup proper domain for Resend emails

---

## 🔑 Environment Variables

All sensitive keys are stored in `aipart/.env`:

```env
# Google Imagen API
GOOGLE_API_KEY=AIzaSy...

# Stripe API (Test Mode)
STRIPE_SECRET_KEY=sk_test_51...
STRIPE_PUBLISHABLE_KEY=pk_test_51...

# Resend API
RESEND_API_KEY=re_6e7HK...
RESEND_FROM_EMAIL=hera.work.noreply@gmail.com

# Application URLs
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:5000
```

**⚠️ Never commit `.env` to Git!** (Already in `.gitignore`)

---

## 💰 Pricing

- **PDF Version**: $9.99 USD
- **Physical Book**: $24.99 USD

Prices are defined in `aipart/payment.py` line 30:
```python
amount = 999 if format_type == 'pdf' else 2499  # in cents
```

---

## 🌍 Supported Countries

Shipping address collection is enabled for:
- 🇰🇷 South Korea
- 🇺🇸 United States
- 🇨🇦 Canada
- 🇬🇧 United Kingdom
- 🇫🇷 France
- 🇩🇪 Germany
- 🇯🇵 Japan
- 🇦🇺 Australia

To add more countries, edit `payment.py` line 68.

---

## 📞 Support

For issues:
- Stripe Dashboard: https://dashboard.stripe.com/test/
- Resend Dashboard: https://resend.com/
- Check backend logs for errors

---

**🎉 Your payment system is ready to test!**
