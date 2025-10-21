"""
Generate a test PDF with real image sizing and open it
"""
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw, ImageFont
import io
import subprocess
import platform

def create_coloring_page():
    """Create a realistic coloring page (flower design)"""
    # Create 1024x1024 image
    img = Image.new('RGB', (1024, 1024), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw a flower with petals
    # Center circle
    draw.ellipse([412, 412, 612, 612], outline='black', width=4)
    
    # 8 petals around center
    import math
    for i in range(8):
        angle = i * 45
        rad = math.radians(angle)
        cx, cy = 512, 512
        px = cx + int(180 * math.cos(rad))
        py = cy + int(180 * math.sin(rad))
        draw.ellipse([px-100, py-100, px+100, py+100], outline='black', width=4)
    
    # Add some inner details
    for i in range(12):
        angle = i * 30
        rad = math.radians(angle)
        cx, cy = 512, 512
        px = cx + int(70 * math.cos(rad))
        py = cy + int(70 * math.sin(rad))
        draw.ellipse([px-15, py-15, px+15, py+15], outline='black', width=3)
    
    # Add leaf at bottom
    draw.ellipse([470, 650, 554, 850], outline='black', width=4)
    draw.line((512, 612, 512, 750), fill='black', width=4)
    
    return img

def create_test_pdf(padding_value, filename):
    """Create test PDF with given padding"""
    page_width, page_height = A4
    
    print(f"\n{'='*60}")
    print(f"📄 Creating PDF: {filename}")
    print(f"   Padding: {padding_value}pt ({padding_value/72:.2f} inch)")
    
    # Create PDF
    c = canvas.Canvas(filename, pagesize=A4)
    
    # Add title page info
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(page_width / 2, page_height - 50, "HERA Coloring Book")
    c.setFont("Helvetica", 14)
    c.drawCentredString(page_width / 2, page_height - 80, f"Test PDF - Padding: {padding_value}pt")
    c.showPage()
    
    # Create coloring page
    pil_img = create_coloring_page()
    img_width, img_height = pil_img.size
    aspect_ratio = img_width / img_height
    
    # Calculate dimensions with padding
    max_width = page_width - (2 * padding_value)
    max_height = page_height - (2 * padding_value)
    
    # Calculate new dimensions
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
    
    # Center on page
    x = (page_width - new_width) / 2
    y = (page_height - new_height) / 2
    
    coverage = (new_width * new_height) / (page_width * page_height) * 100
    
    print(f"   Image size: {new_width:.1f} x {new_height:.1f}pt")
    print(f"   Coverage: {coverage:.1f}%")
    
    # Convert to ImageReader
    img_buffer = io.BytesIO()
    pil_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    img_reader = ImageReader(img_buffer)
    
    # Draw image
    c.drawImage(img_reader, x, y, width=new_width, height=new_height)
    
    # Add page number
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_width / 2, 20, "Page 1")
    
    # Add another page for comparison
    c.showPage()
    
    # Second page with different design
    pil_img2 = create_coloring_page()  # Same for now
    img_buffer2 = io.BytesIO()
    pil_img2.save(img_buffer2, format='PNG')
    img_buffer2.seek(0)
    img_reader2 = ImageReader(img_buffer2)
    
    c.drawImage(img_reader2, x, y, width=new_width, height=new_height)
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_width / 2, 20, "Page 2")
    
    c.save()
    print(f"✅ PDF created: {filename}")
    print(f"{'='*60}\n")
    
    return filename

def open_pdf(filepath):
    """Open PDF with default viewer"""
    abs_path = os.path.abspath(filepath)
    
    try:
        if platform.system() == 'Windows':
            os.startfile(abs_path)
            print(f"📖 Opening PDF in default viewer...")
        elif platform.system() == 'Darwin':  # macOS
            subprocess.call(['open', abs_path])
        else:  # Linux
            subprocess.call(['xdg-open', abs_path])
        
        return True
    except Exception as e:
        print(f"❌ Could not open PDF automatically: {e}")
        print(f"   Please open manually: {abs_path}")
        return False

if __name__ == '__main__':
    print("\n🎨 HERA PDF Test Generator\n")
    
    # Generate PDFs with different paddings
    pdfs = []
    
    # Old padding (72pt)
    pdf1 = create_test_pdf(72, "test_old_padding_72pt.pdf")
    pdfs.append(("Old (1 inch)", pdf1))
    
    # New recommended padding (36pt)
    pdf2 = create_test_pdf(36, "test_new_padding_36pt.pdf")
    pdfs.append(("New (0.5 inch)", pdf2))
    
    # Minimal padding (18pt)
    pdf3 = create_test_pdf(18, "test_minimal_padding_18pt.pdf")
    pdfs.append(("Minimal (0.25 inch)", pdf3))
    
    print("\n📊 Comparison:")
    print("  1. Old (72pt)     - Conservative, small images")
    print("  2. New (36pt)     - Balanced, good coverage ✅ RECOMMENDED")
    print("  3. Minimal (18pt) - Maximum fill, less margin")
    
    # Ask which to open
    print("\n" + "="*60)
    choice = input("Which PDF do you want to open? (1/2/3 or 'all'): ").strip().lower()
    
    if choice == 'all':
        for name, path in pdfs:
            print(f"\n📖 Opening {name}...")
            open_pdf(path)
    elif choice in ['1', '2', '3']:
        idx = int(choice) - 1
        name, path = pdfs[idx]
        print(f"\n📖 Opening {name}...")
        open_pdf(path)
    else:
        # Default: open the recommended one
        print(f"\n📖 Opening recommended (36pt)...")
        open_pdf(pdfs[1][1])
    
    print("\n✅ Done! Check the PDFs to compare.")
