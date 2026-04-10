# Hēra - Project Architecture & Goals

## 🎯 Project Goal
Hēra is a web application designed to create magical, personalized coloring books for children using Generative AI. It allows users to customize themes, art styles, difficulty levels, and page counts. Once customized, the application generates unique coloring pages, processes payments, and delivers a compiled PDF coloring book directly to the user's email.

## 🏗️ High-Level Architecture
The project follows a decoupled Client-Server architecture:
- **Frontend (Client):** A React Single Page Application (SPA) that handles the user interface, customization wizard, and payment collection.
- **Backend (Server):** A Python Flask API that acts as the orchestrator for AI generation, payment processing, PDF creation, and email delivery.

---

## 💻 Frontend Architecture
**Tech Stack:** React 18, Vite, Tailwind CSS, Framer Motion, React Router.

### Key Components:
- **Customization Wizard (`src/components/steps/`):** A multi-step form where users select:
  1. Theme (Animals, Nature, etc.)
  2. Art Style (Cartoon, Ghibli, etc.)
  3. Book Details (Pages, Difficulty, Colors)
  4. AI Preview & Checkout
- **State Management:** React state is used to hold the user's configuration as they progress through the steps.
- **Animations:** Framer Motion provides smooth transitions between steps and playful interactions suitable for a child-friendly app.
- **Payment UI:** Integrates Stripe Elements for secure frontend payment tokenization.

---

## ⚙️ Backend Architecture
**Tech Stack:** Python, Flask, Google GenAI (Gemini/Imagen), Stripe, ReportLab, Resend/SendGrid.

### Key Modules (`aipart/` directory):
- **API Server (`generated_image.py`):** The main Flask application exposing endpoints for the frontend (e.g., `/api/generate`, `/api/current-price`).
- **AI Generation:** Constructs highly specific prompts based on frontend parameters and calls the Google Gemini/Imagen API to generate black-and-white line art.
- **Payment Processing (`payment.py`):** Communicates with Stripe to create payment intents, handle webhooks, and verify successful transactions (supporting international cards and Korean payment methods like Kakao Pay/Naver Pay).
- **PDF Generation (`pdf_generator.py`):** Uses ReportLab to compile the generated AI images into a single, printable PDF coloring book.
- **Email Service (`email_service.py`):** Uses Resend/SendGrid to deliver the final PDF to the user's email address after successful payment.

---

## 🔄 Data Flow & User Journey
1. **Customization:** The user interacts with the React frontend to select their coloring book preferences.
2. **Preview Generation:** The frontend sends a `POST` request to the backend (`/api/generate`). The backend calls the Google AI API to generate a preview image and returns it to the frontend.
3. **Checkout:** The user approves the preview and enters payment details. The frontend communicates with Stripe to process the payment.
4. **Fulfillment:** 
   - Upon successful payment, a webhook or success callback triggers the backend.
   - The backend generates the remaining requested pages via the AI API.
   - The images are compiled into a PDF.
   - The PDF is emailed to the user.
