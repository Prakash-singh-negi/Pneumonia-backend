from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the trained model
model = load_model("Pneumonia_binary_classification.keras")

# Create uploads folder if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Preprocess image to match training pipeline
def preprocess(img_path):
    # Load as grayscale to match training (1 channel)
    img = image.load_img(img_path, target_size=(256, 256), color_mode='grayscale')
    
    # Convert to numpy array
    img = image.img_to_array(img)  # Shape: (256, 256, 1)
    
    # Add batch dimension for prediction (1, 256, 256, 1)
    img = np.expand_dims(img, axis=0)
    
    # Normalize pixel values (0-1)
    img = img / 255.0
    
    return img

@app.route('/')
def home():
    return "✅ Pneumonia Detection API is running."

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    # Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Preprocess and predict
    img = preprocess(filepath)
    prediction = model.predict(img)[0][0]

    # Output: Pneumonia or Normal
    result = "Pneumonia" if prediction > 0.5 else "Normal"

    return jsonify({'prediction': result})

if __name__ == "__main__":
    # Run locally (Docker/Gunicorn will override in production)
    app.run(host="0.0.0.0", port=8080)
