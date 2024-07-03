from flask import Flask, request, jsonify, Blueprint # type: ignore
from transformers import ViTImageProcessor, ViTForImageClassification # type: ignore
from dotenv import load_dotenv # type: ignore
import cohere # type: ignore
import os
from flask_cors import CORS, cross_origin # type: ignore
from PIL import Image # type: ignore
import requests # type: ignore
import pytesseract # type: ignore
from io import BytesIO

load_dotenv()  

co = cohere.Client(os.environ.get("COHERE_API_KEY"))

ai_bp = Blueprint('aimodel', __name__)

CORS(ai_bp)
# Setup ViT model and feature extractor
image_processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

# Set CoHere API key
# os.environ["COHERE_API_KEY"] = 's1v4UzmYNozCzM6gX5NGQmK4Ld1kLTjlB3MphF8t'

def chat_with_cohere(prompt):
    response = co.chat(
        message=prompt
    )
    return str(response.text)

@ai_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "UP"}), 200

@ai_bp.route('/classify-image', methods=['POST','GET'])
def classify_image():
    if request.method == 'GET':                                            
        # return ({'response': 'Please enter your image'})
        # 
        url = 'http://images.cocodataset.org/val2017/000000039769.jpg'
        # response = requests.get(url)
        image = Image.open(requests.get(url, stream=True).raw)

        inputs = image_processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        predicted_result = model.config.id2label[predicted_class_idx]

        return ({'predicted_class': predicted_result})
    url = request.json.get('image_url')
    # url = 'http://images.cocodataset.org/val2017/000000039769.jpg'
    # response = requests.get(url)
    image = Image.open(requests.get(url, stream=True).raw)

    inputs = image_processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    predicted_result = model.config.id2label[predicted_class_idx]

    return ({'predicted_class': predicted_result})

@ai_bp.route('/chat', methods=['POST', 'GET'])
@cross_origin(origins='*')
def chat():
    if request.method == 'GET':                                            
        return ({'response': 'Please enter your question'})                             
    prompt = request.args.get('prompt')
    response = chat_with_cohere(prompt)
    return ({'response': response})

@ai_bp.route('/recommendation', methods=['POST', 'GET'])
@cross_origin(origins='*')
def recommendation():
# pass
# Get the message input from the user
    if request.method == 'GET':                                            
        return ({'response': 'Please enter your type of package'})     
    data = request.get_json()
    category = data["category"]
    prompt = "How to package {category} for logistics company?"

    # Use the API to generate a response
    response = chat_with_cohere(prompt)
    return ({'response': response})

@ai_bp.route('/extract-text-from-image', methods=['POST', 'GET'])
def extract_text_from_image():
    if request.method == 'GET':                                            
        return ({'response': 'Please enter your image'})     
    uploaded_file = request.files['image']
    image = Image.open(uploaded_file)

    extracted_information = pytesseract.image_to_string(image)

    return jsonify({'extracted_text': extracted_information})

# ai_bp.run(host='0.0.0.0', port=8081, debug=True)  # Run the ai_bp on port 8081 with debug mode enabled
