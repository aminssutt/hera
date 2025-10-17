from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from datetime import datetime
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv
from payment import payment_bp  # Import payment blueprint

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Register payment blueprint
app.register_blueprint(payment_bp)

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
    """Build a detailed prompt from user-selected parameters for kids coloring book pages"""
    themes = params.get('theme', [])
    topic = params.get('topic', 'Cartoon')
    difficulty = params.get('difficulty', 'Easy')
    
    # Build theme description
    theme_text = " and ".join(themes) if isinstance(themes, list) and themes else "general"
    
    # Difficulty mapping to detail level
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
        'Minimal': 'minimalist and clean design',
        'Comic': 'comic book style with dynamic energy',
        'Detailed': 'highly detailed and rich illustration',
        'Magical': 'mystical and enchanting with sparkles and magic elements'
    }
    
    style_desc = style_map.get(topic, 'cartoon style')
    
    # Build the complete prompt for a coloring book page
    prompt = f"Create a black and white coloring book page for children. "
    prompt += f"Theme: {theme_text}. "
    prompt += f"Art style: {style_desc}. "
    prompt += f"Complexity: {difficulty_desc}. "
    prompt += f"The image should be a single page with clear outlines, "
    prompt += f"no shading, pure black lines on white background, perfect for coloring. "
    prompt += f"Kid-friendly, safe, and fun content only."
    
    return prompt

def generate_image_api(prompt):
    """Generate image using Google Imagen API"""
    try:
        print(f"Generating image with prompt: {prompt}")
        
        # Using Imagen 4.0 - note: generate_image (singular) not generate_images
        response = client.models.generate_image(
            model='imagen-4.0-generate-001',
            prompt=prompt,
            config=types.GenerateImageConfig(
                number_of_images=1,
            )
        )
        
        # Get the generated image
        if response.generated_images:
            print("Image generated successfully!")
            return response.generated_images[0].image.image_bytes
        
        print("No image was generated")
        return None
        
    except Exception as e:
        print(f"API Error: {str(e)}")
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

if __name__ == '__main__':
    print("🚀 Starting Hera AI Backend on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
