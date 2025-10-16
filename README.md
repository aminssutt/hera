# 🎨 Hēra - Custom Kids Coloring Books

Create magical, personalized coloring books for children using Generative AI! ✨

## 🌟 Features

- **Interactive Theme Selection**: Choose from Animals, Nature, Fantasy, Science, Transport, and more
- **Art Style Customization**: Ghibli, Cartoon, Comic, Minimal, and other styles
- **Fully Customizable**: 
  - Number of pages (10-30)
  - Difficulty levels (Easy, Medium, Hard)
  - Color themes
- **Beautiful Animations**: Smooth transitions and playful interactions
- **Child-Friendly Design**: Colorful, fun, and engaging interface

## 🚀 Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS
- **Framer Motion** - Animations
- **React Router** - Navigation
- **Flask (Python)** - Backend API server
- **Google Imagen AI** - Image generation
- **Stripe** - Payment processing (Kakao Pay, Naver Pay, Cards)
- **Resend** - Email delivery
- **ReportLab** - PDF generation

## 📦 Installation

### Frontend (React)

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will run on `http://localhost:3000`

### Backend (Python Flask)

```bash
# Navigate to backend folder
cd aipart

# Install Python dependencies
pip install -r requirements.txt

# Start Flask server
python generated_image.py
```

The backend will run on `http://localhost:5000`

**⚠️ Important:** Both frontend and backend must be running for the AI generation to work!

## 💳 Payment Integration

Hēra supports multiple payment methods through Stripe:

### 🇰🇷 Korean Payment Methods:
- **Kakao Pay** (카카오페이)
- **Naver Pay** (네이버페이)
- **Samsung Pay**
- **PayCo**

### 🌍 International:
- Credit/Debit Cards (Visa, Mastercard, Amex)
- Apple Pay
- Google Pay

### Pricing:
- **Digital PDF**: $9.99 USD
- **Physical Book**: $24.99 USD

### Testing Payment:
Use test card: `4242 4242 4242 4242` (Exp: `12/25`, CVC: `123`)

For detailed payment setup and testing instructions, see:
- **[PAYMENT_SETUP.md](PAYMENT_SETUP.md)** - Stripe configuration guide
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - How to test payments
- **[STRIPE_INTEGRATION_FR.md](STRIPE_INTEGRATION_FR.md)** - Guide en français

## 🎯 Project Structure

```
Hera/
├── src/
│   ├── components/
│   │   ├── AnimatedBackground.jsx
│   │   ├── Modal.jsx
│   │   └── steps/
│   │       ├── StepOne.jsx    # Theme selection
│   │       ├── StepTwo.jsx    # Art style selection
│   │       ├── StepThree.jsx  # Pages, difficulty, colors
│   │       └── StepFour.jsx   # AI Preview & Payment
│   ├── pages/
│   │   ├── Home.jsx           # Landing page
│   │   ├── Customize.jsx      # Customization wizard
│   │   ├── Success.jsx        # Payment success page
│   │   └── Cancel.jsx         # Payment cancelled page
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── aipart/
│   ├── generated_image.py     # Flask backend
│   ├── payment.py             # Stripe payment handling
│   ├── email_service.py       # Email delivery (Resend)
│   ├── pdf_generator.py       # PDF creation (ReportLab)
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # API keys (not in Git)
│   ├── .env.example           # Example configuration
│   ├── generated_images/      # Generated images folder
│   └── README.md              # Backend documentation
├── public/
│   └── images/                # Static images
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## 🎨 Design Features

- Animated background with rockets, stars, and planets
- Smooth slide animations between steps
- Responsive design for all devices
- Custom color palette:
  - Hera Pink: `#E891C8`
  - Hera Purple: `#A97DC0`
  - Hera Blue: `#5EB3E4`
  - Hera Green: `#7FD687`
  - Hera Yellow: `#FFE347`
  - Hera Orange: `#FFAA7A`

## 🛣️ Roadmap

- [x] Home page with "How it Works" section
- [x] Theme & style selection (Steps 1-2)
- [x] Customization options (Step 3)
- [x] AI preview generation (Step 4)
- [x] Flask backend integration
- [x] Stripe payment integration (Kakao Pay, Naver Pay, Samsung Pay, PayCo, Cards)
- [x] Success and Cancel pages
- [x] Email service setup (Resend)
- [x] PDF generator setup (ReportLab)
- [ ] Complete book generation (multiple pages)
- [ ] PDF download functionality via email
- [ ] Physical book ordering and fulfillment
- [ ] User accounts and order history
- [ ] Admin dashboard
- [ ] Colored page generation with user colors

## 👨‍💻 Development

This project uses:
- **Fredoka** font family for readable text
- **Bubblegum Sans** for playful headings
- Custom animations with Framer Motion
- Tailwind CSS for rapid styling

## 📝 License

MIT License - Feel free to use this project for learning or commercial purposes!

---

Made with 💖 for kids around the world! 🌈
