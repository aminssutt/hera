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
    """Add a decorative title page using frontpage.png"""
    try:
        # Path to frontpage image
        frontpage_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'frontpage.png')
        
        # If frontpage doesn't exist, try alternative path
        if not os.path.exists(frontpage_path):
            frontpage_path = os.path.join(os.path.dirname(__file__), '..', 'public', 'images', 'frontpage.png')
        
        if not os.path.exists(frontpage_path):
            print(f"⚠️ Warning: frontpage.png not found, creating text-based title page")
            # Fallback to simple text title page
            canvas_obj.setFillColorRGB(0.91, 0.57, 0.78)  # Hera pink
            canvas_obj.rect(0, 0, width, height, fill=True, stroke=False)
            canvas_obj.setFillColorRGB(1, 1, 1)
            canvas_obj.setFont("Helvetica-Bold", 56)
            canvas_obj.drawCentredString(width / 2, height / 2, "HERA")
            canvas_obj.setFont("Helvetica", 20)
            canvas_obj.drawCentredString(width / 2, height / 2 - 50, "Your Personalized Coloring Book")
        else:
            # Use frontpage.png as cover
            print(f"✅ Using frontpage.png as cover: {frontpage_path}")
            
            # Open and resize frontpage to fit page
            pil_img = Image.open(frontpage_path)
            
            # Convert to RGB if necessary
            if pil_img.mode != 'RGB':
                pil_img = pil_img.convert('RGB')
            
            # Calculate dimensions to fit page while maintaining aspect ratio
            img_width, img_height = pil_img.size
            aspect_ratio = img_width / img_height
            
            # Scale to fill entire page
            if aspect_ratio > width / height:
                # Image is wider - fit to height
                new_height = height
                new_width = height * aspect_ratio
                x = (width - new_width) / 2
                y = 0
            else:
                # Image is taller - fit to width
                new_width = width
                new_height = width / aspect_ratio
                x = 0
                y = (height - new_height) / 2
            
            # Convert PIL image to ImageReader for reportlab
            img_buffer = io.BytesIO()
            pil_img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            img_reader = ImageReader(img_buffer)
            
            # Draw frontpage as full cover
            canvas_obj.drawImage(img_reader, x, y, width=new_width, height=new_height)
        
        # Start new page for actual coloring content
        canvas_obj.showPage()
        
    except Exception as e:
        print(f"❌ Error adding title page: {str(e)}")
        import traceback
        traceback.print_exc()


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
