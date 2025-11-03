from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from datetime import datetime
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv
import io
from payment import payment_bp  # Import payment blueprint

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS pour permettre les requêtes depuis Vercel et domaine custom
CORS(app, origins=[
    'https://www.herastudio.art',      # Custom domain (www)
    'https://herastudio.art',          # Custom domain (apex)
    'https://hera-seven.vercel.app',   # Production Vercel
    'https://hera-*.vercel.app',       # Preview deployments Vercel
    'http://localhost:3000',           # Dev local
    'http://localhost:5173',           # Vite dev server
    'http://localhost:3001',           # Dev local (alternative port)
], supports_credentials=True)

# Register payment blueprint
app.register_blueprint(payment_bp)

# Start the generation queue worker
from generation_queue import start_queue_worker
start_queue_worker()
print("✅ Generation queue worker initialized")

# Configure upload folder
UPLOAD_FOLDER = 'generated_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Google Imagen API configuration from environment variable
API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")

client = genai.Client(api_key=API_KEY)

def build_prompt(params):
    """Build a detailed, flattened, and negatively reinforced prompt for Imagen 4."""
    themes = params.get('theme', [])
    topic = params.get('topic', 'Cartoon') # Corresponds to Art Style
    difficulty = params.get('difficulty', 'Easy') # Corresponds to Complexity
 
    # 1. Map parameters to descriptive, model-friendly phrases
    # Build theme description
    theme_text = " and ".join(themes) if isinstance(themes, list) and themes else "a general topic"
 
    # Difficulty mapping to detail level
    difficulty_map = {
        'Easy': 'simple, large shapes with minimal details, perfect for young children',
        'Medium': 'moderate details with medium complexity',
        'Hard': 'intricate details and complex patterns, challenging for older kids'
    }
    difficulty_desc = difficulty_map.get(difficulty, difficulty_map['Easy'])
    # Style mapping
    style_map = {
        'Ghibli': 'Studio Ghibli inspired, whimsical and magical style',
        'Cartoon': 'fun cartoon style with bold outlines',
        'Minimal': 'minimalist and clean design, highly simplified',
        'Comic': 'comic book illustration style with dynamic energy',
        'Detailed': 'highly detailed and rich illustration style',
        'Magical': 'mystical and enchanting style with stars and magic elements'
    }
    style_desc = style_map.get(topic, 'cartoon style')
 
    # 2. Flatten and Assemble the Final Prompt
    # Part A: The Critical Negative Instruction (placed first for emphasis)
    prompt_negative_critical = "CRITICAL: A clean line art illustration with ABSOLUTELY NO TEXT, NO WORDS, NO LETTERS, NO NUMBERS, NO TYPOGRAPHY, NO CODE, NO METADATA, NO WATERMARKS. "
    # Part B: The Descriptive, Flattened Prompt
    prompt_description = (
        f"Create a black and white coloring book page for children, illustrating **{theme_text}**. "
        f"The art style is a **{style_desc}**. "
        f"The composition is **{difficulty_desc}**. "
        f"The entire image must be black and white line art ONLY, with clear, high-contrast, black outlines on a pure white background, and NO shading, NO grayscale. "
        f"Perfect for coloring with crayons."
    )
    # Part C: Reiterate Negative Constraints (for final reinforcement)
    prompt_negative_reinforcement = "IMPORTANT: Only generate the drawing. Do not include any form of text, keywords, theme names, or numbers anywhere in the image."
    # Combine all parts
    final_prompt = f"{prompt_negative_critical}{prompt_description} {prompt_negative_reinforcement}"
    return final_prompt

def generate_image_api(prompt):
    """Generate image using Gemini 2.5 Flash Image"""
    print(f"Generating image with prompt: {prompt}")
    
    try:
        print("🎨 Generating with Gemini 2.5 Flash Image...")
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=[prompt]
        )
        
        # Extract image from response parts
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                print("✅ Image generated successfully with Gemini 2.5 Flash Image!")
                # Return the raw image bytes
                return part.inline_data.data
        
        print("❌ No image found in response")
        return None
    
    except Exception as e:
        error_str = str(e)
        print(f"❌ Gemini 2.5 Flash Image failed: {error_str[:200]}")
        import traceback
        traceback.print_exc()
        return None

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Hera AI Backend is running'})

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        params = request.json
        print(f"Received params: {params}")
        
        # Build the prompt
        prompt = build_prompt(params)
        print(f"Generated prompt: {prompt}")
        
        # Generate image using Google Imagen API
        image_data = generate_image_api(prompt)
        
        if image_data is None:
            return jsonify({'error': 'Failed to generate image'}), 500
        
        # Save the image
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'coloring_page_{timestamp}.png'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        # Convert to base64 for display
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'image': f'data:image/png;base64,{image_base64}',
            'filename': filename
        })
    
    except Exception as e:
        print(f"Error in generate: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download(filename):
    """Download generated image"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)

@app.route('/api/queue-status', methods=['GET'])
def queue_status():
    """Get current generation queue status"""
    from generation_queue import get_queue_status
    status = get_queue_status()
    return jsonify({
        'success': True,
        'queue': status
    })

if __name__ == '__main__':
    print("🚀 Starting Hera AI Backend on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
