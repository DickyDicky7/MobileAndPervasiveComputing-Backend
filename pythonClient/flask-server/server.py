from flask import Flask, request, jsonify
from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image
import requests
import pytesseract
from io import BytesIO

app = Flask("Lift")  # Setting the app name to "Lift"

# Setup ViT model and feature extractor
feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

# Set CoHere API key
os.environ["COHERE_API_KEY"] = 's1v4UzmYNozCzM6gX5NGQmK4Ld1kLTjlB3MphF8t'

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "UP"}), 200

@app.route('/classify-image', methods=['POST'])
def classify_image():
    url = request.json.get('image_url')
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    inputs = feature_extractor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    predicted_result = model.config.id2label[predicted_class_idx]

    return jsonify({'predicted_class': predicted_result})

@app.route('/recommendation', methods=['POST'])
def recommendation():
    category = request.json.get('category')
    prompt = f"How to package {category} for logistics company?"

    # Execute CoHere API command or any other relevant logic here

    return jsonify({'recommendation': f"Recommendations for {category} packaging"})

@app.route('/extract-text-from-image', methods=['POST'])
def extract_text_from_image():
    uploaded_file = request.files['image']
    image = Image.open(uploaded_file)

    extracted_information = pytesseract.image_to_string(image)

    return jsonify({'extracted_text': extracted_information})

app.run(port=8081, debug=True)  # Run the app on port 8081 with debug mode enabled
