# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import base64
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Initialize Gemini client
client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    symptoms = data.get('symptoms', '')
    
    # Handle image if provided
    image_data = data.get('image')
    contents = [symptoms]
    
    if image_data:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))
        contents.append(image)
    
    # Craft medical prompt
    prompt = f"""
    As a medical AI assistant, analyze these symptoms: {symptoms}
    
    Provide:
    1. Possible conditions (with disclaimer)
    2. Recommended over-the-counter medications
    3. When to see a doctor
    4. Home care suggestions
    
    IMPORTANT: Include a clear disclaimer that this is not medical advice.
    """
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=contents
    )
    
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(port=5000)