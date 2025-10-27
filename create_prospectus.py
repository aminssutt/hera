"""
Generate a professional prospectus/flyer for Hera
Design matches the brand colors (purple theme)
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import os

def create_prospectus():
    """Create a beautiful prospectus for Hera"""
    
    # Create PDF
    filename = "Hera_Prospectus.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Define colors (Hera purple theme)
    purple_dark = colors.HexColor('#6b21a8')  # Dark purple
    purple_main = colors.HexColor('#9333ea')  # Main purple
    purple_light = colors.HexColor('#f3e8ff')  # Light purple background
    text_dark = colors.HexColor('#1f2937')  # Dark gray text
    
    # ===== HEADER SECTION =====
    # Purple gradient background for header
    c.setFillColor(purple_main)
    c.rect(0, height - 8*cm, width, 8*cm, fill=True, stroke=False)
    
    # Title
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 42)
    c.drawCentredString(width/2, height - 3*cm, "Hera")
    
    # Subtitle
    c.setFont("Helvetica", 18)
    c.drawCentredString(width/2, height - 4*cm, "✨ Livres de Coloriage Personnalisés pour Enfants ✨")
    
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 5*cm, "Créez des histoires magiques générées par IA")
    
    # ===== MAIN CONTENT SECTION =====
    y_position = height - 10*cm
    
    # What is Hera?
    c.setFillColor(text_dark)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(3*cm, y_position, "🎨 Qu'est-ce que Hera ?")
    
    y_position -= 1.2*cm
    c.setFont("Helvetica", 12)
    c.setFillColor(text_dark)
    
    text_lines = [
        "Hera transforme l'imagination de vos enfants en magnifiques livres de coloriage personnalisés.",
        "Grâce à l'intelligence artificielle, chaque page est unique et adaptée aux préférences de votre enfant."
    ]
    
    for line in text_lines:
        c.drawString(3*cm, y_position, line)
        y_position -= 0.7*cm
    
    y_position -= 0.5*cm
    
    # How it works
    c.setFont("Helvetica-Bold", 20)
    c.drawString(3*cm, y_position, "⚡ Comment ça marche ?")
    
    y_position -= 1.2*cm
    
    # Steps with emoji and boxes
    steps = [
        ("1️⃣ Choisissez un thème", "Animaux, Nature, Fantaisie, Science, Transport..."),
        ("2️⃣ Sélectionnez un style", "Style Ghibli, Cartoon, Minimal, Détaillé..."),
        ("3️⃣ Personnalisez", "Nombre de pages, difficulté, palette de couleurs"),
        ("4️⃣ Téléchargez", "Recevez votre PDF unique par email en quelques minutes !")
    ]
    
    c.setFont("Helvetica", 11)
    for step_title, step_desc in steps:
        # Light purple box
        c.setFillColor(purple_light)
        c.roundRect(2.5*cm, y_position - 0.5*cm, width - 5*cm, 1*cm, 0.3*cm, fill=True, stroke=False)
        
        # Text
        c.setFillColor(purple_dark)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(3*cm, y_position, step_title)
        
        c.setFillColor(text_dark)
        c.setFont("Helvetica", 10)
        c.drawString(3*cm, y_position - 0.4*cm, step_desc)
        
        y_position -= 1.5*cm
    
    y_position -= 0.5*cm
    
    # Features
    c.setFont("Helvetica-Bold", 20)
    c.drawString(3*cm, y_position, "💜 Pourquoi choisir Hera ?")
    
    y_position -= 1*cm
    c.setFont("Helvetica", 11)
    
    features = [
        "✓ 6 langues disponibles (Français, Anglais, Coréen, Chinois, Japonais, Espagnol)",
        "✓ Illustrations générées par IA de haute qualité",
        "✓ PDF téléchargeable instantanément",
        "✓ Adapté à tous les âges et niveaux de difficulté",
        "✓ Prix accessible : à partir de 9,99€"
    ]
    
    for feature in features:
        c.drawString(3*cm, y_position, feature)
        y_position -= 0.7*cm
    
    # ===== TEST SECTION (Important!) =====
    y_position -= 1*cm
    
    # Yellow/orange box for test instructions
    c.setFillColor(colors.HexColor('#fef3c7'))  # Light yellow
    c.roundRect(2*cm, y_position - 3.5*cm, width - 4*cm, 3.5*cm, 0.4*cm, fill=True, stroke=True)
    
    c.setFillColor(colors.HexColor('#b45309'))  # Orange/brown text
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2.5*cm, y_position - 0.8*cm, "🧪 TESTEZ GRATUITEMENT !")
    
    c.setFillColor(text_dark)
    c.setFont("Helvetica", 11)
    c.drawString(2.5*cm, y_position - 1.5*cm, "Au moment du paiement, utilisez ces coordonnées bancaires de test :")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2.5*cm, y_position - 2.2*cm, "📇 Numéro de carte : 4242 4242 4242 4242")
    c.drawString(2.5*cm, y_position - 2.8*cm, "📅 Date d'expiration : 12/25")
    c.drawString(2.5*cm, y_position - 3.4*cm, "🔒 CVV : 123")
    
    y_position -= 4*cm
    
    c.setFont("Helvetica", 10)
    c.setFillColor(text_dark)
    c.drawString(2.5*cm, y_position, "Ensuite, entrez votre adresse email réelle et un nom pour recevoir votre PDF test !")
    
    # ===== FOOTER WITH QR CODES =====
    y_position = 4*cm
    
    # Divider line
    c.setStrokeColor(purple_main)
    c.setLineWidth(2)
    c.line(2*cm, y_position + 0.5*cm, width - 2*cm, y_position + 0.5*cm)
    
    # QR Code placeholders
    c.setFillColor(purple_dark)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(4*cm, y_position - 0.5*cm, "Scannez pour accéder :")
    
    # Left QR - Website
    c.setFont("Helvetica", 10)
    c.drawString(4*cm, y_position - 3.5*cm, "🌐 Site Web")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(3.5*cm, y_position - 4*cm, "[QR CODE ICI]")
    c.setStrokeColor(purple_main)
    c.setLineWidth(1)
    c.rect(3.5*cm, y_position - 2.8*cm, 2*cm, 2*cm, fill=False, stroke=True)
    
    # Right QR - Instagram
    c.setFont("Helvetica", 10)
    c.drawString(width - 8*cm, y_position - 3.5*cm, "📸 Instagram")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(width - 8.5*cm, y_position - 4*cm, "[QR CODE ICI]")
    c.setStrokeColor(purple_main)
    c.setLineWidth(1)
    c.rect(width - 8.5*cm, y_position - 2.8*cm, 2*cm, 2*cm, fill=False, stroke=True)
    
    # Contact info
    c.setFont("Helvetica", 9)
    c.setFillColor(text_dark)
    c.drawCentredString(width/2, 1.5*cm, "📧 hera.work.noreply@gmail.com")
    c.drawCentredString(width/2, 1*cm, "Made with 💜 by Hera Team")
    
    # Save PDF
    c.save()
    print(f"✅ Prospectus créé : {filename}")
    print(f"📍 Emplacement : {os.path.abspath(filename)}")
    print("\n⚠️  N'oubliez pas d'ajouter vos QR codes aux emplacements marqués !")
    print("    - QR Code site web (en bas à gauche)")
    print("    - QR Code Instagram (en bas à droite)")

if __name__ == "__main__":
    create_prospectus()
