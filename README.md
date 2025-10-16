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
│   │   └── Customize.jsx      # Customization wizard
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── aipart/
│   ├── generated_image.py     # Flask backend
│   ├── requirements.txt       # Python dependencies
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
- [ ] Stripe payment integration
- [ ] Complete book generation (multiple pages)
- [ ] PDF download functionality
- [ ] Physical book ordering
- [ ] User accounts and order history
- [ ] Admin dashboard

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
