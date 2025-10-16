import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import io


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
            
            # Add margins
            margin = 36  # 0.5 inch margin
            max_width = page_width - (2 * margin)
            max_height = page_height - (2 * margin)
            
            if aspect_ratio > 1:
                # Landscape orientation
                new_width = min(max_width, img_width)
                new_height = new_width / aspect_ratio
            else:
                # Portrait orientation
                new_height = min(max_height, img_height)
                new_width = new_height * aspect_ratio
            
            # Center the image
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
        # Background gradient effect (using rectangles)
        canvas_obj.setFillColorRGB(0.91, 0.57, 0.78)  # Hera pink
        canvas_obj.rect(0, 0, width, height, fill=True, stroke=False)
        
        # Title
        canvas_obj.setFillColorRGB(1, 1, 1)  # White text
        canvas_obj.setFont("Helvetica-Bold", 36)
        canvas_obj.drawCentredString(width / 2, height - 150, "My Coloring Book")
        
        # Subtitle
        canvas_obj.setFont("Helvetica", 18)
        theme = book_details.get('theme', 'Custom')
        if isinstance(theme, list):
            theme = ', '.join(theme)
        canvas_obj.drawCentredString(width / 2, height - 200, f"Theme: {theme}")
        
        # Details
        canvas_obj.setFont("Helvetica", 14)
        pages = book_details.get('pages', 24)
        difficulty = book_details.get('difficulty', 'Easy')
        canvas_obj.drawCentredString(width / 2, height - 250, f"{pages} pages • {difficulty} difficulty")
        
        # Footer message
        canvas_obj.setFont("Helvetica-Oblique", 12)
        canvas_obj.drawCentredString(width / 2, 100, "Created with ❤️ by Hera")
        canvas_obj.drawCentredString(width / 2, 80, "Have fun coloring!")
        
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
