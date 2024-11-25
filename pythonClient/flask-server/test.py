from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# In-memory storage for tokens (use a database in production)
user_tokens = {}

# Endpoint to register token
@app.route('/register-token', methods=['POST'])
def register_token():
    data = request.json
    token = data.get('token')
    user_id = data.get('userId')

    if not token or not user_id:
        return jsonify({"error": "Invalid data"}), 400

    # Store token
    user_tokens[user_id] = token
    return jsonify({"message": "Token registered successfully"}), 200

# Endpoint to send notifications
@app.route('/send-notification', methods=['POST'])
def send_notification():
    data = request.json
    user_id = data.get('userId')
    message_title = data.get('title', "Default Title")
    message_body = data.get('body', "Default Body")

    # Get user's Expo token
    expo_token = user_tokens.get(user_id)
    if not expo_token:
        return jsonify({"error": "User not found"}), 404

    # Send notification via Expo Push Notification Service
    headers = {
        "Authorization": f"Bearer YOUR_EXPO_ACCESS_TOKEN",
        "Content-Type": "application/json",
    }
    payload = {
        "to": expo_token,
        "title": message_title,
        "body": message_body,
    }

    response = requests.post(
        "https://exp.host/--/api/v2/push/send", json=payload, headers=headers
    )

    if response.status_code == 200:
        return jsonify({"message": "Notification sent successfully"}), 200
    else:
        return jsonify({"error": response.json()}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200)
