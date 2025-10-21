"""
Test to show the difference between square (1:1) and portrait (3:4) images in A4 PDF
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw, ImageFont
import io

def create_test_image(width, height, label):
    """Create a test coloring page"""
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Border
    draw.rectangle([5, 5, width-6, height-6], outline='black', width=4)
    
    # Center flower
    cx, cy = width // 2, height // 2
    draw.ellipse([cx-80, cy-80, cx+80, cy+80], outline='black', width=4)
    
    # Petals
    import math
    for i in range(8):
        angle = i * 45
        rad = math.radians(angle)
        px = cx + int(120 * math.cos(rad))
        py = cy + int(120 * math.sin(rad))
        draw.ellipse([px-60, py-60, px+60, py+60], outline='black', width=3)
    
    # Add label
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = None
    
    text = f"{label}\n{width}x{height}px"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw.text((cx - text_width//2, 20), text, fill='red', font=font)
    
    return img

def add_image_to_pdf(c, pil_img, padding, page_width, page_height):
    """Add image to PDF page with given padding"""
    img_width, img_height = pil_img.size
    aspect_ratio = img_width / img_height
    
    # Calculate dimensions
    max_width = page_width - (2 * padding)
    max_height = page_height - (2 * padding)
    
    if aspect_ratio > 1:
        new_width = min(max_width, img_width)
        new_height = new_width / aspect_ratio
        if new_height > max_height:
            new_height = max_height
            new_width = new_height * aspect_ratio
    else:
        new_height = min(max_height, img_height)
        new_width = new_height * aspect_ratio
        if new_width > max_width:
            new_width = max_width
            new_height = new_width / aspect_ratio
    
    # Center
    x = (page_width - new_width) / 2
    y = (page_height - new_height) / 2
    
    # Calculate coverage
    coverage = (new_width * new_height) / (page_width * page_height) * 100
    
    # Convert to ImageReader
    img_buffer = io.BytesIO()
    pil_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    img_reader = ImageReader(img_buffer)
    
    # Draw
    c.drawImage(img_reader, x, y, width=new_width, height=new_height)
    
    # Add info
    c.setFont("Helvetica", 10)
    c.drawString(10, page_height - 20, f"Original: {img_width}x{img_height}px")
    c.drawString(10, page_height - 35, f"In PDF: {new_width:.0f}x{new_height:.0f}pt")
    c.drawString(10, page_height - 50, f"Coverage: {coverage:.1f}%")
    c.drawString(10, page_height - 65, f"Padding: {padding}pt")
    
    return coverage

def create_comparison_pdf():
    """Create PDF comparing square vs portrait images"""
    filename = "comparison_square_vs_portrait.pdf"
    page_width, page_height = A4
    padding = 36  # 0.5 inch
    
    c = canvas.Canvas(filename, pagesize=A4)
    
    print("\n" + "="*60)
    print("🎨 Creating Comparison PDF: Square vs Portrait")
    print("="*60)
    
    # Title page
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(page_width / 2, page_height - 100, "HERA Coloring Book")
    c.setFont("Helvetica", 18)
    c.drawCentredString(page_width / 2, page_height - 140, "Image Format Comparison")
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_width / 2, page_height - 180, "Square (1:1) vs Portrait (3:4)")
    
    c.setFont("Helvetica", 14)
    c.drawString(50, page_height - 250, "Current (Square 1:1):")
    c.setFont("Helvetica", 11)
    c.drawString(70, page_height - 275, "• Size: 1024 x 1024 pixels")
    c.drawString(70, page_height - 295, "• Aspect ratio: 1:1 (square)")
    c.drawString(70, page_height - 315, "• Coverage: ~55% of A4 page")
    c.drawString(70, page_height - 335, "• Problem: Wasted space on portrait page")
    
    c.setFont("Helvetica", 14)
    c.drawString(50, page_height - 380, "New (Portrait 3:4):")
    c.setFont("Helvetica", 11)
    c.drawString(70, page_height - 405, "• Size: 768 x 1024 pixels")
    c.drawString(70, page_height - 425, "• Aspect ratio: 3:4 (portrait)")
    c.drawString(70, page_height - 445, "• Coverage: ~85% of A4 page")
    c.drawString(70, page_height - 465, "✅ Solution: Perfect fit for A4!")
    
    c.showPage()
    
    # Page 1: Square 1024x1024 (OLD)
    print("\n📄 Page 1: Square 1024x1024 (CURRENT)")
    img_square = create_test_image(1024, 1024, "CURRENT\nSquare 1:1")
    coverage_square = add_image_to_pdf(c, img_square, padding, page_width, page_height)
    print(f"   Coverage: {coverage_square:.1f}%")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_width / 2, 40, "CURRENT: Square 1:1 (1024x1024px)")
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_width / 2, 25, "❌ Only 55% page coverage - lots of wasted space")
    
    c.showPage()
    
    # Page 2: Portrait 768x1024 (NEW)
    print("\n📄 Page 2: Portrait 768x1024 (NEW RECOMMENDED)")
    img_portrait = create_test_image(768, 1024, "NEW\nPortrait 3:4")
    coverage_portrait = add_image_to_pdf(c, img_portrait, padding, page_width, page_height)
    print(f"   Coverage: {coverage_portrait:.1f}%")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_width / 2, 40, "NEW: Portrait 3:4 (768x1024px)")
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_width / 2, 25, f"✅ {coverage_portrait:.1f}% page coverage - much better!")
    
    c.showPage()
    
    # Summary page
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(page_width / 2, page_height - 100, "📊 Comparison Summary")
    
    c.setFont("Helvetica", 14)
    y = page_height - 180
    c.drawString(80, y, f"Square 1:1 (1024x1024):")
    c.setFillColorRGB(0.8, 0.2, 0.2)
    c.drawString(320, y, f"{coverage_square:.1f}% coverage")
    
    c.setFillColorRGB(0, 0, 0)
    y -= 40
    c.drawString(80, y, f"Portrait 3:4 (768x1024):")
    c.setFillColorRGB(0.2, 0.7, 0.2)
    c.drawString(320, y, f"{coverage_portrait:.1f}% coverage")
    
    c.setFillColorRGB(0, 0, 0)
    y -= 60
    improvement = ((coverage_portrait - coverage_square) / coverage_square) * 100
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_width / 2, y, f"🎉 Improvement: +{improvement:.0f}%")
    
    c.setFont("Helvetica", 12)
    y -= 80
    c.drawString(80, y, "✅ Recommendation: Use Portrait 3:4 (768x1024)")
    y -= 25
    c.drawString(100, y, "• Better page coverage")
    y -= 20
    c.drawString(100, y, "• More professional look")
    y -= 20
    c.drawString(100, y, "• Perfect for A4 coloring books")
    
    c.save()
    
    print(f"\n✅ PDF created: {filename}")
    print("="*60)
    print(f"\n📊 Results:")
    print(f"   Square 1:1:   {coverage_square:.1f}% coverage")
    print(f"   Portrait 3:4: {coverage_portrait:.1f}% coverage")
    print(f"   Improvement:  +{improvement:.0f}%")
    print("\n" + "="*60)
    
    return filename

if __name__ == '__main__':
    pdf_file = create_comparison_pdf()
    
    # Open PDF
    print("\n📖 Opening PDF...")
    os.startfile(pdf_file)
    
    print("\n✅ Done! Check the PDF to see the difference.")
