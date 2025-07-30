from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)
CORS(app)

model = load_model("Pneumonia_binary_classification.keras")

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def preprocess(img_path):
    img = image.load_img(img_path, target_size=(256, 256))  # Adjust if needed
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255.0
    return img

@app.route('/')
def home():
    return "Pneumonia Detection API is running."

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    img = preprocess(filepath)
    prediction = model.predict(img)[0][0]
    result = "Pneumonia" if prediction > 0.5 else "Normal"

    return jsonify({'prediction': result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
