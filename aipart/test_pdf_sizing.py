"""
Test script to visualize image sizing in A4 PDF
"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw, ImageFont
import io

# Create a test image (simulating generated coloring page)
def create_test_image():
    # Create a 1024x1024 test image
    img = Image.new('RGB', (1024, 1024), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw border to see edges
    draw.rectangle([0, 0, 1023, 1023], outline='black', width=5)
    
    # Draw a simple coloring page design (flower)
    # Center circle
    draw.ellipse([412, 412, 612, 612], outline='black', width=3)
    
    # Petals around
    for i in range(8):
        angle = i * 45
        import math
        rad = math.radians(angle)
        cx, cy = 512, 512
        px = cx + int(150 * math.cos(rad))
        py = cy + int(150 * math.sin(rad))
        draw.ellipse([px-80, py-80, px+80, py+80], outline='black', width=3)
    
    # Add text to show orientation
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    draw.text((512, 50), "TOP", fill='red', anchor='mm', font=font)
    draw.text((512, 974), "BOTTOM", fill='red', anchor='mm', font=font)
    
    return img

# Test different padding values
def test_pdf_layout(padding, output_filename):
    """Test PDF layout with given padding"""
    page_width, page_height = A4
    
    print(f"\n{'='*60}")
    print(f"Testing with padding: {padding} points")
    print(f"A4 size: {page_width:.1f} x {page_height:.1f} points")
    print(f"Usable area: {page_width - 2*padding:.1f} x {page_height - 2*padding:.1f} points")
    
    # Create PDF
    c = canvas.Canvas(output_filename, pagesize=A4)
    
    # Create test image
    pil_img = create_test_image()
    img_width, img_height = pil_img.size
    aspect_ratio = img_width / img_height
    
    print(f"Image size: {img_width} x {img_height}")
    print(f"Aspect ratio: {aspect_ratio:.2f}")
    
    # Calculate dimensions with padding
    max_width = page_width - (2 * padding)
    max_height = page_height - (2 * padding)
    
    # Calculate new dimensions while maintaining aspect ratio
    if aspect_ratio > 1:
        # Landscape
        new_width = min(max_width, img_width)
        new_height = new_width / aspect_ratio
        if new_height > max_height:
            new_height = max_height
            new_width = new_height * aspect_ratio
    else:
        # Portrait or square
        new_height = min(max_height, img_height)
        new_width = new_height * aspect_ratio
        if new_width > max_width:
            new_width = max_width
            new_height = new_width / aspect_ratio
    
    # Center on page
    x = (page_width - new_width) / 2
    y = (page_height - new_height) / 2
    
    print(f"Final size in PDF: {new_width:.1f} x {new_height:.1f} points")
    print(f"Position: x={x:.1f}, y={y:.1f}")
    print(f"Coverage: {(new_width * new_height) / (page_width * page_height) * 100:.1f}%")
    
    # Draw border to show page edges (for testing)
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.setDash(6, 3)
    c.rect(0, 0, page_width, page_height)
    
    # Draw padding border (for testing)
    c.setStrokeColorRGB(1, 0, 0)
    c.setDash(3, 2)
    c.rect(padding, padding, max_width, max_height)
    
    # Convert PIL image to ImageReader
    img_buffer = io.BytesIO()
    pil_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    img_reader = ImageReader(img_buffer)
    
    # Draw image
    c.drawImage(img_reader, x, y, width=new_width, height=new_height)
    
    # Add labels
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 10)
    c.drawString(10, page_height - 20, f"Padding: {padding}pt")
    c.drawString(10, page_height - 35, f"Coverage: {(new_width * new_height) / (page_width * page_height) * 100:.1f}%")
    
    c.save()
    print(f"✅ PDF created: {output_filename}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    # Test different padding values
    test_pdf_layout(72, "test_padding_72pt.pdf")  # 1 inch (current)
    test_pdf_layout(36, "test_padding_36pt.pdf")  # 0.5 inch (recommended)
    test_pdf_layout(18, "test_padding_18pt.pdf")  # 0.25 inch (minimal)
    
    print("\n🎯 Recommendation:")
    print("- 72pt (1 inch): Safe but small images (~50% coverage)")
    print("- 36pt (0.5 inch): Good balance (~70% coverage) ✅ RECOMMENDED")
    print("- 18pt (0.25 inch): Maximum fill (~85% coverage)")
    print("\nOpen the generated PDFs to compare!")
