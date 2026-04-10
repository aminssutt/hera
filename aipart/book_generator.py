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
from pdf_generator import open_pdf_canvas, append_image_to_canvas, finalize_pdf
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
The image should be vibrant, child-friendly, and inspiring. Make it beautiful and fun!
IMPORTANT: NO TEXT, NO WORDS, NO LETTERS - only illustrations and drawings."""
    else:
        # Black and white coloring page prompt
        prompt = f"""Create a black and white coloring book page for children.
Theme: {theme_text}. Art style: {style_desc}. Complexity: {difficulty_desc}.
IMPORTANT: The image MUST be black and white line art ONLY - clean outlines, no shading, no grayscale.
Perfect for coloring with crayons or markers. High contrast, clear lines, child-friendly design.
CRITICAL: NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS - only pure line art illustrations."""
    
    return prompt


def generate_single_page(theme, topic, difficulty, is_colored=False, colors=None, page_num=1, source_image_path=None):
    """Generate a single coloring book page or color an existing B&W page"""
    try:
        if is_colored and source_image_path:
            # COLORIER une image B&W existante avec Gemini 2.5 Flash
            print(f"  � Coloring page {page_num} with Gemini 2.5 Flash...")
            
            # Ouvrir l'image B&W source
            bw_image = Image.open(source_image_path)
            
            # Construire le prompt de coloration
            color_list = ', '.join(colors) if colors else 'vibrant child-friendly colors'
            coloring_prompt = (
                f"Color in this black and white coloring book illustration neatly using the following colors: {color_list}. "
                "Do not change the line art. Stay within the lines. Use flat, solid colors without shading or texture. "
                "Make it bright, fun, and perfect for kids!"
            )
            
            # Appeler Gemini 2.5 Flash pour colorier
            response = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[coloring_prompt, bw_image]
            )
            
            # Extraire l'image colorée
            colored_image = None
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    colored_image = Image.open(io.BytesIO(part.inline_data.data))
                    break
            
            if colored_image:
                # Sauvegarder l'image colorée
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"page_{page_num}_colored_{timestamp}.png"
                filepath = os.path.join(GENERATED_FOLDER, filename)
                colored_image.save(filepath)
                print(f"    ✅ Page {page_num} colored: {filename}")
                return filepath
            else:
                print(f"    ❌ Failed to color page {page_num}")
                return None
        
        else:
            # GÉNÉRER une nouvelle page B&W avec Gemini 2.5 Flash Image
            print(f"  🎨 Generating B&W page {page_num} with Gemini 2.5 Flash Image...")
            
            prompt = build_prompt(theme, topic, difficulty, is_colored=False, colors=None)
            
            try:
                # Generate image with Gemini 2.5 Flash Image
                response = client.models.generate_content(
                    model='gemini-2.5-flash-image',
                    contents=[prompt]
                )
                
                # Extract image from response parts
                generated_image = None
                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        generated_image = Image.open(io.BytesIO(part.inline_data.data))
                        break
                
                if generated_image:
                    # Save the generated image
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"page_{page_num}_bw_{timestamp}.png"
                    filepath = os.path.join(GENERATED_FOLDER, filename)
                    generated_image.save(filepath)
                    print(f"    ✅ Page {page_num} generated: {filename}")
                    return filepath
                else:
                    print(f"    ❌ No image found in response for page {page_num}")
                    return None
                    
            except Exception as e:
                print(f"    ❌ Failed to generate page {page_num}: {str(e)[:200]}")
                import traceback
                traceback.print_exc()
                return None
            
            # if response.generated_images:
            #     image_data = response.generated_images[0].image.image_bytes
                
            #     # Save to file
            #     timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            #     filename = f"page_{page_num}_bw_{timestamp}.png"
            #     filepath = os.path.join(GENERATED_FOLDER, filename)
                
            #     with open(filepath, 'wb') as f:
            #         f.write(image_data)
                
            #     print(f"    ✅ B&W page {page_num} generated: {filename}")
            #     return filepath
            # else:
            #     print(f"    ❌ Failed to generate page {page_num}")
            #     return None
            
    except Exception as e:
        print(f"    ❌ Error generating page {page_num}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def generate_complete_book(session_data, preview_image_base64=None):
    """
    Generate a complete coloring book based on payment session data.

    Uses a streaming approach: each page is generated, written to the PDF
    canvas, and its temp file deleted before moving to the next page.
    This keeps RAM usage at O(1) images regardless of page count.

    Args:
        session_data: Stripe session object or dict with metadata
        preview_image_base64: IGNORED – all pages are regenerated fresh

    Returns:
        str: Path to generated PDF, or None if failed
    """
    try:
        # ── Extract metadata ──────────────────────────────────────────────
        metadata = session_data.get('metadata', {})
        customer_email = session_data.get('customer_details', {}).get('email')

        format_type = metadata.get('format', 'pdf')
        book_type   = metadata.get('bookType', 'blackwhite')
        total_pages = int(metadata.get('pages', 24))
        raw_theme   = metadata.get('theme', 'Custom')
        theme       = raw_theme.split(',') if ',' in raw_theme else [raw_theme]
        topic       = metadata.get('topic', 'Cartoon')
        difficulty  = metadata.get('difficulty', 'Easy')

        try:
            colors = json.loads(metadata.get('colors', '[]'))
        except Exception:
            colors = []

        print(f"\n{'='*60}")
        print(f"📚 Starting book generation for {customer_email}")
        print(f"   Format: {format_type} | Type: {book_type} | Pages: {total_pages}")
        print(f"   Theme: {', '.join(theme)} | Style: {topic} | Difficulty: {difficulty}")
        print(f"{'='*60}\n")

        # ── Prepare output paths ──────────────────────────────────────────
        timestamp    = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"coloring_book_{timestamp}.pdf"
        pdf_path     = os.path.join(PDF_FOLDER, pdf_filename)

        book_details = {
            'theme'     : theme if isinstance(theme, str) else ', '.join(theme),
            'style'     : topic,
            'pages'     : total_pages,
            'difficulty': difficulty,
            'book_type' : book_type,
            'format'    : format_type,
        }

        # ── Open canvas once (title page already added) ───────────────────
        c        = open_pdf_canvas(pdf_path, book_details)
        pdf_page = 0  # tracks pages written to canvas

        if book_type == 'blackwhite':
            # ── B&W: generate → write → delete → next ────────────────────
            print(f"🖤 Generating {total_pages} B&W pages (streaming)...")
            for i in range(total_pages):
                page_num = i + 1
                img_path = generate_single_page(
                    theme, topic, difficulty, is_colored=False, page_num=page_num
                )
                if img_path:
                    pdf_page += 1
                    append_image_to_canvas(c, img_path, page_number=pdf_page, delete_after=True)
                    print(f"   ✅ Page {page_num}/{total_pages} written to PDF (temp file deleted)")
                else:
                    print(f"   ⚠️  Page {page_num} generation failed – skipping")

        else:
            # ── Colored: for each slot generate B&W, color it, write both,
            #    delete both – only 2 images in RAM at a time ──────────────
            num_slots = total_pages // 2
            print(f"🌈 Generating {num_slots} B&W + {num_slots} colored pages (streaming)...")
            for i in range(num_slots):
                page_num = i + 1

                # Step A – generate the B&W version
                bw_path = generate_single_page(
                    theme, topic, difficulty, is_colored=False, page_num=page_num
                )
                if not bw_path:
                    print(f"   ⚠️  B&W page {page_num} failed – skipping slot")
                    continue

                # Step B – color it (pass the B&W file as source)
                colored_path = generate_single_page(
                    theme, topic, difficulty,
                    is_colored=True,
                    colors=colors,
                    page_num=page_num,
                    source_image_path=bw_path,
                )

                # Step C – write B&W page to PDF, delete temp file
                pdf_page += 1
                append_image_to_canvas(c, bw_path, page_number=pdf_page, delete_after=True)

                # Step D – write colored page to PDF, delete temp file
                if colored_path:
                    pdf_page += 1
                    append_image_to_canvas(c, colored_path, page_number=pdf_page, delete_after=True)

                print(f"   ✅ Slot {page_num}/{num_slots} written to PDF (temp files deleted)")

        # ── Save PDF ──────────────────────────────────────────────────────
        if pdf_page == 0:
            print("❌ No pages were generated – aborting PDF")
            return None

        finalize_pdf(c, pdf_path)
        size_mb = os.path.getsize(pdf_path) / 1024 / 1024
        print(f"✅ PDF created: {pdf_path}  ({size_mb:.2f} MB, {pdf_page} pages)\n")

        print(f"\n{'='*60}")
        print(f"🎉 Book generation complete for {customer_email}!")
        print(f"{'='*60}\n")

        return pdf_path

    except Exception as e:
        print(f"❌ Error in book generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
