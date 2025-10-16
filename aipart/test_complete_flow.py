"""
Test complet du flux SANS paiement Stripe
Simule : confirmation email → génération livre (2 pages) → email PDF
"""
import sys
import os

print("=" * 80)
print("🧪 TEST COMPLET DU FLUX HERA")
print("=" * 80)
print("\n📋 Ce test va :")
print("  1️⃣  Envoyer un email de confirmation")
print("  2️⃣  Générer un mini-livre de 2 pages (rapide)")
print("  3️⃣  Créer un PDF")
print("  4️⃣  Envoyer l'email avec le PDF")
print("\n⏱️  Durée estimée : 2-3 minutes")
print("=" * 80)

input("\n▶️  Appuie sur ENTRÉE pour commencer le test...")

# ÉTAPE 1 : Email de confirmation
print("\n" + "=" * 80)
print("📧 ÉTAPE 1/4 : Email de confirmation")
print("=" * 80)

from email_service import send_payment_confirmation

order_details = {
    'format': 'pdf',
    'bookType': 'blackwhite',
    'pages': 2,  # Seulement 2 pages pour test rapide
    'theme': 'Animals, Nature (TEST)',
    'amount': '9.99'
}

result = send_payment_confirmation('lakhdarberache@gmail.com', order_details)

if result:
    print("✅ Email de confirmation envoyé !")
    print("📬 Vérifie ton inbox : lakhdarberache@gmail.com")
else:
    print("❌ Échec de l'email de confirmation")
    sys.exit(1)

input("\n⏸️  Vérifie ton email puis appuie sur ENTRÉE pour continuer...")

# ÉTAPE 2-4 : Génération du livre
print("\n" + "=" * 80)
print("📚 ÉTAPE 2-4/4 : Génération livre + PDF + Email final")
print("=" * 80)
print("⏳ Génération de 2 pages en cours...")
print("   (Cela prend environ 1-2 minutes)")

from book_generator import generate_complete_book

# Simuler une session Stripe avec tous les détails
mock_session = {
    'id': 'test_session_123',
    'customer_details': {
        'email': 'lakhdarberache@gmail.com'
    },
    'metadata': {
        'format': 'pdf',
        'bookType': 'blackwhite',
        'pages': '2',  # Seulement 2 pages pour test rapide !
        'theme': 'Animals, Nature, Wildlife',
        'topic': 'Cartoon',
        'difficulty': 'Easy',
        'colors': '["red", "blue", "green"]'
    }
}

pdf_path = generate_complete_book(mock_session, preview_image_base64=None)

if pdf_path:
    print("\n" + "=" * 80)
    print("✅ TEST RÉUSSI !")
    print("=" * 80)
    print(f"\n📄 PDF créé : {pdf_path}")
    print("📧 Email avec PDF envoyé à : lakhdarberache@gmail.com")
    print("\n🎉 Le système fonctionne parfaitement !")
    print("\n📬 Vérifie tes emails :")
    print("   1. Email de confirmation (reçu il y a ~2 min)")
    print("   2. Email avec PDF (viens d'arriver)")
    print("=" * 80)
else:
    print("\n" + "=" * 80)
    print("❌ TEST ÉCHOUÉ")
    print("=" * 80)
    print("Vérifie les logs ci-dessus pour voir l'erreur")
    sys.exit(1)
