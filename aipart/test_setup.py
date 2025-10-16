"""
Quick test script to verify Stripe payment integration setup
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("\n🔍 Checking Stripe Payment Integration Setup...\n")

# Check Stripe keys
stripe_secret = os.getenv('STRIPE_SECRET_KEY')
stripe_public = os.getenv('STRIPE_PUBLISHABLE_KEY')

if stripe_secret and stripe_secret.startswith('sk_test_'):
    print("✅ Stripe Secret Key configured (Test Mode)")
else:
    print("❌ Stripe Secret Key missing or invalid")

if stripe_public and stripe_public.startswith('pk_test_'):
    print("✅ Stripe Publishable Key configured (Test Mode)")
else:
    print("❌ Stripe Publishable Key missing or invalid")

# Check Resend
resend_key = os.getenv('RESEND_API_KEY')
resend_email = os.getenv('RESEND_FROM_EMAIL')

if resend_key and resend_key.startswith('re_'):
    print("✅ Resend API Key configured")
else:
    print("❌ Resend API Key missing or invalid")

if resend_email:
    print(f"✅ Resend From Email: {resend_email}")
else:
    print("❌ Resend From Email missing")

# Check URLs
frontend_url = os.getenv('FRONTEND_URL')
backend_url = os.getenv('BACKEND_URL')

if frontend_url:
    print(f"✅ Frontend URL: {frontend_url}")
else:
    print("❌ Frontend URL missing")

if backend_url:
    print(f"✅ Backend URL: {backend_url}")
else:
    print("❌ Backend URL missing")

# Check Google API
google_key = os.getenv('GOOGLE_API_KEY')
if google_key:
    print("✅ Google Imagen API Key configured")
else:
    print("❌ Google Imagen API Key missing")

print("\n📦 Checking Python packages...")

try:
    import stripe
    print(f"✅ stripe installed")
except ImportError:
    print("❌ stripe not installed")

try:
    import resend
    print(f"✅ resend installed")
except ImportError:
    print("❌ resend not installed")

try:
    import reportlab
    print(f"✅ reportlab installed")
except ImportError:
    print("❌ reportlab not installed")

try:
    from google import genai
    print(f"✅ google-genai installed")
except ImportError:
    print("❌ google-genai not installed")

print("\n🎉 Setup verification complete!")
print("\n📝 To start the backend: python generated_image.py")
print("📝 To start the frontend: npm run dev")
print("\n💳 Test card: 4242 4242 4242 4242 | Exp: 12/25 | CVC: 123")
