"""
Book generation orchestrator - Generates complete coloring books from user selections
"""
import os
import json
import base64
from datetime import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pdf_generator import create_coloring_book_pdf, combine_bw_and_colored
from email_service import send_pdf_email
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Google Imagen API configuration
API_KEY = os.getenv('GOOGLE_API_KEY')
client = genai.Client(api_key=API_KEY)

# Configure folders
GENERATED_FOLDER = 'generated_images'
PDF_FOLDER = 'generated_pdfs'

if not os.path.exists(GENERATED_FOLDER):
    os.makedirs(GENERATED_FOLDER)
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)


def build_prompt(theme, topic, difficulty, is_colored=False, colors=None):
    """Build a prompt for AI generation"""
    
    # Theme text
    if isinstance(theme, list):
        theme_text = " and ".join(theme)
    else:
        theme_text = theme
    
    # Difficulty mapping
    difficulty_map = {
        'Easy': 'simple, large shapes with minimal details, perfect for young children',
        'Medium': 'moderate details with medium complexity, suitable for kids 6-10',
        'Hard': 'intricate details and complex patterns, challenging for older kids'
    }
    difficulty_desc = difficulty_map.get(difficulty, difficulty_map['Easy'])
    
    # Style mapping
    style_map = {
        'Ghibli': 'Studio Ghibli inspired, whimsical and magical',
        'Cartoon': 'fun cartoon style with bold outlines',
        'Minimal': 'minimalist clean line art style',
        'Comic': 'comic book style with dynamic compositions',
        'Detailed': 'highly detailed and intricate patterns',
        'Magical': 'magical and fantastical with sparkles and stars'
    }
    style_desc = style_map.get(topic, style_map['Cartoon'])
    
    if is_colored:
        # Colored version prompt
        color_desc = ""
        if colors and len(colors) > 0:
            color_desc = f" Use primarily these colors: {', '.join(colors)}."
        
        prompt = f"""Create a fully colored illustration for a children's coloring book reference page.
Theme: {theme_text}. Art style: {style_desc}. Complexity: {difficulty_desc}.
This is a colored reference example showing how the page could look when finished.{color_desc}
The image should be vibrant, child-friendly, and inspiring. Make it beautiful and fun!"""
    else:
        # Black and white coloring page prompt
        prompt = f"""Create a black and white coloring book page for children.
Theme: {theme_text}. Art style: {style_desc}. Complexity: {difficulty_desc}.
IMPORTANT: The image MUST be black and white line art ONLY - clean outlines, no shading, no grayscale.
Perfect for coloring with crayons or markers. High contrast, clear lines, child-friendly design."""
    
    return prompt


def generate_single_page(theme, topic, difficulty, is_colored=False, colors=None, page_num=1):
    """Generate a single coloring book page"""
    try:
        print(f"  🎨 Generating page {page_num} ({'colored' if is_colored else 'B&W'})...")
        
        prompt = build_prompt(theme, topic, difficulty, is_colored, colors)
        
        # Generate image with Google Imagen - note: generate_image (singular)
        response = client.models.generate_image(
            model='imagen-4.0-generate-001',
            prompt=prompt,
            config=types.GenerateImageConfig(
                number_of_images=1,
                safety_filter_level='block_low_and_above',
                person_generation='allow_adult',
                aspect_ratio='1:1',
                output_mime_type='image/png'
            )
        )
        
        if response.generated_images:
            image_data = response.generated_images[0].image.image_bytes
            
            # Save to file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"page_{page_num}_{'colored' if is_colored else 'bw'}_{timestamp}.png"
            filepath = os.path.join(GENERATED_FOLDER, filename)
            
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            print(f"    ✅ Page {page_num} generated: {filename}")
            return filepath
        else:
            print(f"    ❌ Failed to generate page {page_num}")
            return None
            
    except Exception as e:
        print(f"    ❌ Error generating page {page_num}: {str(e)}")
        return None


def generate_complete_book(session_data, preview_image_base64=None):
    """
    Generate a complete coloring book based on payment session data
    
    Args:
        session_data (dict): Payment session with metadata
        preview_image_base64 (str): IGNORED - we regenerate all pages fresh
    
    Returns:
        str: Path to generated PDF, or None if failed
    """
    try:
        # Extract metadata
        metadata = session_data.get('metadata', {})
        customer_email = session_data.get('customer_details', {}).get('email')
        
        format_type = metadata.get('format', 'pdf')
        book_type = metadata.get('bookType', 'blackwhite')
        total_pages = int(metadata.get('pages', 24))
        theme = metadata.get('theme', '').split(',') if ',' in metadata.get('theme', '') else [metadata.get('theme', 'Custom')]
        topic = metadata.get('topic', 'Cartoon')
        difficulty = metadata.get('difficulty', 'Easy')
        
        try:
            colors = json.loads(metadata.get('colors', '[]'))
        except:
            colors = []
        
        print(f"\n{'='*60}")
        print(f"📚 Starting book generation for {customer_email}")
        print(f"   Format: {format_type} | Type: {book_type} | Total Pages: {total_pages}")
        print(f"   Theme: {', '.join(theme)} | Style: {topic} | Difficulty: {difficulty}")
        print(f"   🎨 Generating ALL {total_pages} pages fresh (no preview reuse)")
        print(f"{'='*60}\n")
        
        bw_images = []
        colored_images = []
        
        # Generate all pages fresh (ignoring preview)
        if book_type == 'blackwhite':
            # Black & white only: generate all total_pages B&W pages
            print(f"🖤 Generating {total_pages} black & white pages...")
            for i in range(total_pages):
                page_num = i + 1
                img_path = generate_single_page(theme, topic, difficulty, is_colored=False, page_num=page_num)
                if img_path:
                    bw_images.append(img_path)
        
        else:
            # Colored edition: half B&W, half colored
            bw_count = total_pages // 2
            colored_count = total_pages // 2
            
            print(f"🖤 Generating {bw_count} black & white pages...")
            for i in range(bw_count):
                page_num = i + 1
                img_path = generate_single_page(theme, topic, difficulty, is_colored=False, page_num=page_num)
                if img_path:
                    bw_images.append(img_path)
            
            print(f"🌈 Generating {colored_count} colored pages...")
            for i in range(colored_count):
                page_num = bw_count + i + 1
                img_path = generate_single_page(theme, topic, difficulty, is_colored=True, colors=colors, page_num=page_num)
                if img_path:
                    colored_images.append(img_path)
        
        # Generate PDF
        print(f"\n📄 Compiling PDF...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"coloring_book_{timestamp}.pdf"
        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
        
        book_details = {
            'theme': theme if isinstance(theme, str) else ', '.join(theme),
            'style': topic,
            'pages': total_pages,
            'difficulty': difficulty,
            'book_type': book_type,
            'format': format_type
        }
        
        if book_type == 'colored' and colored_images:
            # Interleave B&W and colored
            success = combine_bw_and_colored(bw_images, colored_images, pdf_path, book_details)
        else:
            # Just B&W pages
            success = create_coloring_book_pdf(bw_images, pdf_path, book_details)
        
        if success:
            print(f"✅ PDF created successfully: {pdf_path}")
            print(f"   File size: {os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB\n")
            
            # Send email with PDF
            print(f"📧 Sending email to {customer_email}...")
            email_sent = send_pdf_email(customer_email, pdf_path, book_details)
            
            if email_sent:
                print(f"✅ Email sent successfully!")
            else:
                print(f"⚠️ Email failed, but PDF is saved at: {pdf_path}")
            
            print(f"\n{'='*60}")
            print(f"🎉 Book generation complete for {customer_email}!")
            print(f"{'='*60}\n")
            
            return pdf_path
        else:
            print(f"❌ Failed to create PDF")
            return None
            
    except Exception as e:
        print(f"❌ Error in book generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
