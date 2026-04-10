import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import io


# ---------------------------------------------------------------------------
# Low-level streaming helpers
# ---------------------------------------------------------------------------

def open_pdf_canvas(output_path, book_details):
    """
    Open a new PDF canvas and add the title page.
    Returns the canvas object; caller must call finalize_pdf() when done.
    """
    page_width, page_height = A4
    c = canvas.Canvas(output_path, pagesize=A4)
    add_title_page(c, book_details, page_width, page_height)
    return c


def append_image_to_canvas(c, img_path, page_number, delete_after=True):
    """
    Draw one image onto the next PDF page, then optionally delete the source file.
    Call c.showPage() internally so the canvas is ready for the next image.

    Args:
        c: ReportLab Canvas opened by open_pdf_canvas()
        img_path (str): Path to the image file
        page_number (int): 1-based page number shown at the bottom
        delete_after (bool): Delete the image file after writing to PDF
    """
    page_width, page_height = A4
    padding = 36  # 0.5 inch

    pil_img = Image.open(img_path)
    if pil_img.mode != 'RGB':
        pil_img = pil_img.convert('RGB')

    img_w, img_h = pil_img.size
    aspect = img_w / img_h
    max_w = page_width - 2 * padding
    max_h = page_height - 2 * padding

    if aspect > 1:
        new_w = min(max_w, img_w)
        new_h = new_w / aspect
        if new_h > max_h:
            new_h = max_h
            new_w = new_h * aspect
    else:
        new_h = min(max_h, img_h)
        new_w = new_h * aspect
        if new_w > max_w:
            new_w = max_w
            new_h = new_w / aspect

    x = (page_width - new_w) / 2
    y = (page_height - new_h) / 2

    buf = io.BytesIO()
    pil_img.save(buf, format='PNG')
    buf.seek(0)
    pil_img.close()
    del pil_img

    c.drawImage(ImageReader(buf), x, y, width=new_w, height=new_h)
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_width / 2, 20, f"Page {page_number}")
    c.showPage()

    buf.close()

    if delete_after:
        try:
            os.remove(img_path)
        except OSError as e:
            print(f"⚠️ Could not delete temp image {img_path}: {e}")


def finalize_pdf(c, output_path):
    """Save and close the canvas."""
    c.save()
    print(f"✅ PDF saved: {output_path}")


# ---------------------------------------------------------------------------
# Legacy batch helper (kept for backward-compatibility)
# ---------------------------------------------------------------------------

def create_coloring_book_pdf(images, output_path, book_details):
    """
    Create a PDF from a list of image paths.
    Processes one image at a time and deletes each temp file after writing
    to keep memory usage at O(1) images regardless of page count.
    """
    try:
        c = open_pdf_canvas(output_path, book_details)
        for idx, img_path in enumerate(images):
            print(f"Adding page {idx + 1}/{len(images)} to PDF...")
            append_image_to_canvas(c, img_path, page_number=idx + 1, delete_after=False)
        finalize_pdf(c, output_path)
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
