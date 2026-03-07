<div align="center">

# Hēra · AI-Powered Custom Kids Coloring Books

Build personalized coloring books in minutes with a playful React experience and an AI + payments backend.

![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-38B2AC?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white)

</div>

## Why Hēra
Hēra helps families and creators generate kid-friendly coloring books from custom themes, styles, and difficulty levels.
The project combines:
- a **modern, animated frontend** for guided customization,
- a **Python backend** for generation and order workflow,
- and **Stripe-powered checkout** for digital and physical products.

## Hera Brand Palette
Use the project palette for product pages, previews, and social/portfolio showcases:

![Hera Pink](https://img.shields.io/badge/Hera%20Pink-%23E891C8-E891C8?style=for-the-badge)
![Hera Purple](https://img.shields.io/badge/Hera%20Purple-%23A97DC0-A97DC0?style=for-the-badge)
![Hera Blue](https://img.shields.io/badge/Hera%20Blue-%235EB3E4-5EB3E4?style=for-the-badge)
![Hera Green](https://img.shields.io/badge/Hera%20Green-%237FD687-7FD687?style=for-the-badge)
![Hera Yellow](https://img.shields.io/badge/Hera%20Yellow-%23FFE347-FFE347?style=for-the-badge)
![Hera Orange](https://img.shields.io/badge/Hera%20Orange-%23FFAA7A-FFAA7A?style=for-the-badge)

## Core Features
- **Step-by-step customization wizard** (theme, art style, pages, difficulty, colors)
- **AI-assisted preview generation** for personalized content
- **Child-friendly and responsive interface** with smooth motion transitions
- **Multi-method checkout support** via Stripe (including Korean payment options)
- **Email and PDF workflow hooks** for digital delivery

## Tech Stack
### Frontend
- React 18
- Vite
- Tailwind CSS
- Framer Motion
- React Router
- i18next

### Backend
- Flask (Python)
- Google Imagen client integration
- Stripe
- Resend
- ReportLab

## Quick Start
### 1) Frontend
```bash
cd /home/runner/work/hera/hera
npm install
npm run dev
```
Frontend runs on `http://localhost:3000`.

### 2) Backend
```bash
cd /home/runner/work/hera/hera/aipart
pip install -r requirements.txt
python generated_image.py
```
Backend runs on `http://localhost:5000`.

> Both frontend and backend must run together for end-to-end generation and checkout flow.

## Payments
Supported methods include:
- **Kakao Pay**
- **Naver Pay**
- **Samsung Pay**
- **PayCo**
- **Credit/Debit cards**
- **Apple Pay / Google Pay**

Pricing:
- **Digital PDF**: $9.99
- **Physical Book**: $24.99

Test card:
- `4242 4242 4242 4242`
- Exp: `12/25`, CVC: `123`

## Security Notes
For a production-ready deployment, keep the following controls in place:
- Keep API keys and payment secrets only in `.env` files (never in source control).
- Use `/home/runner/work/hera/hera/.env.example` and `/home/runner/work/hera/hera/aipart/.env.example` as templates.
- Rotate compromised or shared keys immediately.
- Restrict backend CORS and callback URLs to trusted domains only.
- Validate payment/session state server-side before fulfillment.
- Run regular dependency checks (`npm audit`, Python dependency scans) before releases.

## Project Structure
```text
/home/runner/work/hera/hera
├── src/                  # React app (pages, components, steps)
├── public/               # Static assets
├── aipart/               # Flask backend and generation/payment services
├── images/               # Design assets
├── package.json          # Frontend scripts
└── README.md             # Project overview
```

## Roadmap
- [x] Home page + guided customization flow
- [x] Backend generation integration
- [x] Stripe payment integration
- [x] Success/cancel flow
- [ ] Multi-page full-book generation
- [ ] Automated PDF delivery pipeline
- [ ] Physical fulfillment workflow
- [ ] User accounts and order history
- [ ] Admin dashboard

## License
MIT

---
Built for a creative, family-friendly experience — ready to showcase on portfolio and LinkedIn.
