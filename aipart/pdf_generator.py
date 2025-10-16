import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import io
import requests


def create_coloring_book_pdf(images, output_path, book_details):
    """
    Create a PDF coloring book from a list of images
    
    Args:
        images (list): List of image paths or PIL Image objects
        output_path (str): Path where the PDF will be saved
        book_details (dict): Dictionary containing book information
    """
    try:
        # Use A4 page size (good for coloring books)
        page_width, page_height = A4
        
        # Create PDF
        c = canvas.Canvas(output_path, pagesize=A4)
        
        # Add title page
        add_title_page(c, book_details, page_width, page_height)
        
        # Add each coloring page
        for idx, img in enumerate(images):
            print(f"Adding page {idx + 1}/{len(images)} to PDF...")
            
            # Convert to PIL Image if it's a path
            if isinstance(img, str):
                pil_img = Image.open(img)
            else:
                pil_img = img
            
            # Convert to RGB if necessary
            if pil_img.mode != 'RGB':
                pil_img = pil_img.convert('RGB')
            
            # Calculate dimensions to fit page while maintaining aspect ratio
            img_width, img_height = pil_img.size
            aspect_ratio = img_width / img_height
            
            # Add generous padding around images (1 inch on all sides)
            padding = 72  # 1 inch padding
            max_width = page_width - (2 * padding)
            max_height = page_height - (2 * padding)
            
            # Calculate new dimensions while maintaining aspect ratio
            if aspect_ratio > 1:
                # Landscape orientation
                new_width = min(max_width, img_width)
                new_height = new_width / aspect_ratio
                # If height exceeds max, recalculate based on height
                if new_height > max_height:
                    new_height = max_height
                    new_width = new_height * aspect_ratio
            else:
                # Portrait orientation
                new_height = min(max_height, img_height)
                new_width = new_height * aspect_ratio
                # If width exceeds max, recalculate based on width
                if new_width > max_width:
                    new_width = max_width
                    new_height = new_width / aspect_ratio
            
            # Center the image on the page
            x = (page_width - new_width) / 2
            y = (page_height - new_height) / 2
            
            # Convert PIL image to ImageReader for reportlab
            img_buffer = io.BytesIO()
            pil_img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            img_reader = ImageReader(img_buffer)
            
            # Draw image on PDF
            c.drawImage(img_reader, x, y, width=new_width, height=new_height)
            
            # Add page number at bottom
            c.setFont("Helvetica", 10)
            c.drawCentredString(page_width / 2, 20, f"Page {idx + 1}")
            
            # Start new page (except for last image)
            if idx < len(images) - 1:
                c.showPage()
        
        # Save PDF
        c.save()
        print(f"PDF successfully created: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")
        return False


def add_title_page(canvas_obj, book_details, width, height):
    """Add a decorative title page to the coloring book"""
    try:
        # Try to use Fredoka font (like the website)
        try:
            # Download Fredoka font from Google Fonts if not already cached
            font_cache_path = 'fredoka.ttf'
            if not os.path.exists(font_cache_path):
                font_url = 'https://github.com/googlefonts/fredoka/raw/main/fonts/ttf/Fredoka-SemiBold.ttf'
                response = requests.get(font_url, timeout=5)
                if response.status_code == 200:
                    with open(font_cache_path, 'wb') as f:
                        f.write(response.content)
            
            if os.path.exists(font_cache_path):
                pdfmetrics.registerFont(TTFont('Fredoka', font_cache_path))
                title_font = 'Fredoka'
            else:
                title_font = 'Helvetica-Bold'
        except:
            title_font = 'Helvetica-Bold'
        
        # Background - Elegant gradient effect
        # Top gradient (pink)
        canvas_obj.setFillColorRGB(0.91, 0.57, 0.78)  # Hera pink #E891C7
        canvas_obj.rect(0, height * 0.6, width, height * 0.4, fill=True, stroke=False)
        
        # Bottom gradient (lighter pink)
        canvas_obj.setFillColorRGB(0.98, 0.89, 0.95)  # Light pink
        canvas_obj.rect(0, 0, width, height * 0.6, fill=True, stroke=False)
        
        # Add decorative circles
        canvas_obj.setFillColorRGB(1, 1, 1, alpha=0.2)
        canvas_obj.circle(width * 0.15, height * 0.85, 60, fill=True, stroke=False)
        canvas_obj.circle(width * 0.85, height * 0.20, 80, fill=True, stroke=False)
        
        # HERA logo/title
        canvas_obj.setFillColorRGB(1, 1, 1)  # White text
        canvas_obj.setFont(title_font, 56)
        canvas_obj.drawCentredString(width / 2, height - 120, "HERA")
        
        # Tagline
        canvas_obj.setFont("Helvetica-Oblique", 14)
        canvas_obj.setFillColorRGB(1, 1, 1, alpha=0.9)
        canvas_obj.drawCentredString(width / 2, height - 150, "Your personalized coloring book")
        
        # Decorative line
        canvas_obj.setStrokeColorRGB(1, 1, 1)
        canvas_obj.setLineWidth(2)
        canvas_obj.line(width * 0.35, height - 170, width * 0.65, height - 170)
        
        # Book Details Section
        y_position = height - 240
        
        # Theme
        canvas_obj.setFillColorRGB(0.3, 0.3, 0.3)  # Dark gray
        canvas_obj.setFont("Helvetica-Bold", 16)
        canvas_obj.drawCentredString(width / 2, y_position, "📚 Your Book Details")
        
        y_position -= 35
        canvas_obj.setFont("Helvetica", 12)
        
        # Theme
        theme = book_details.get('theme', 'Custom')
        if isinstance(theme, list):
            theme = ', '.join(theme)
        canvas_obj.setFont("Helvetica-Bold", 11)
        canvas_obj.drawString(width * 0.25, y_position, "Theme:")
        canvas_obj.setFont("Helvetica", 11)
        canvas_obj.drawString(width * 0.40, y_position, theme)
        
        y_position -= 25
        
        # Style
        style = book_details.get('style', 'Cartoon')
        canvas_obj.setFont("Helvetica-Bold", 11)
        canvas_obj.drawString(width * 0.25, y_position, "Style:")
        canvas_obj.setFont("Helvetica", 11)
        canvas_obj.drawString(width * 0.40, y_position, style)
        
        y_position -= 25
        
        # Difficulty
        difficulty = book_details.get('difficulty', 'Easy')
        canvas_obj.setFont("Helvetica-Bold", 11)
        canvas_obj.drawString(width * 0.25, y_position, "Difficulty:")
        canvas_obj.setFont("Helvetica", 11)
        canvas_obj.drawString(width * 0.40, y_position, difficulty)
        
        y_position -= 25
        
        # Number of pages
        pages = book_details.get('pages', 24)
        book_type = book_details.get('book_type', 'blackwhite')
        if book_type == 'colored':
            pages_text = f"{pages} colored pages"
        elif book_type == 'both':
            pages_text = f"{pages} pages (B&W + Colored)"
        else:
            pages_text = f"{pages} black & white pages"
        
        canvas_obj.setFont("Helvetica-Bold", 11)
        canvas_obj.drawString(width * 0.25, y_position, "Pages:")
        canvas_obj.setFont("Helvetica", 11)
        canvas_obj.drawString(width * 0.40, y_position, pages_text)
        
        y_position -= 25
        
        # Format
        format_type = book_details.get('format', 'pdf')
        canvas_obj.setFont("Helvetica-Bold", 11)
        canvas_obj.drawString(width * 0.25, y_position, "Format:")
        canvas_obj.setFont("Helvetica", 11)
        canvas_obj.drawString(width * 0.40, y_position, format_type.upper())
        
        # Description box
        y_position -= 60
        canvas_obj.setFillColorRGB(0.91, 0.57, 0.78, alpha=0.15)  # Light pink background
        canvas_obj.roundRect(width * 0.15, y_position - 80, width * 0.7, 100, 10, fill=True, stroke=False)
        
        canvas_obj.setFillColorRGB(0.3, 0.3, 0.3)
        canvas_obj.setFont("Helvetica-Oblique", 11)
        
        description_lines = [
            "✨ Each page is uniquely generated by AI",
            "🎨 Perfect for relaxation and creativity",
            "💝 Made with love, just for you"
        ]
        
        y_desc = y_position - 30
        for line in description_lines:
            canvas_obj.drawCentredString(width / 2, y_desc, line)
            y_desc -= 25
        
        # Footer message
        canvas_obj.setFillColorRGB(0.91, 0.57, 0.78)
        canvas_obj.setFont("Helvetica-Bold", 12)
        canvas_obj.drawCentredString(width / 2, 80, "🖍️ Happy Coloring! 🖍️")
        
        canvas_obj.setFillColorRGB(0.5, 0.5, 0.5)
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.drawCentredString(width / 2, 50, "www.hera-coloring.com • Created with AI")
        
        # Start new page for actual content
        canvas_obj.showPage()
        
    except Exception as e:
        print(f"Error adding title page: {str(e)}")


def combine_bw_and_colored(bw_images, colored_images, output_path, book_details):
    """
    Create a PDF with alternating B&W and colored pages
    
    Args:
        bw_images (list): List of black & white image paths
        colored_images (list): List of colored image paths
        output_path (str): Path where the PDF will be saved
        book_details (dict): Dictionary containing book information
    """
    try:
        # Interleave B&W and colored images
        all_images = []
        for i in range(max(len(bw_images), len(colored_images))):
            if i < len(bw_images):
                all_images.append(bw_images[i])
            if i < len(colored_images):
                all_images.append(colored_images[i])
        
        # Create PDF with all images
        return create_coloring_book_pdf(all_images, output_path, book_details)
        
    except Exception as e:
        print(f"Error combining images: {str(e)}")
        return False
