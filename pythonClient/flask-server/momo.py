from flask import Flask, request, jsonify, Blueprint
import os
import hmac
import hashlib
from pymongo import MongoClient # type: ignore
from bson.objectid import ObjectId # type: ignore
from bson import json_util # type: ignore
from datetime import datetime
from flask_cors import CORS, cross_origin # type: ignore
from ortools.constraint_solver import routing_enums_pb2 # type: ignore
from ortools.constraint_solver import pywrapcp # type: ignore
import json
import requests  # type: ignore
from flask_cors import CORS, cross_origin # type: ignore

momo_bp = Blueprint("momo",__name__)
CORS(momo_bp)

# Connect to MongoDB
client = MongoClient(os.environ.get("MONGO_DB"))
maps_key = os.environ.get("GOOGLE_MAP_API")

db = client.lift
CORS(momo_bp)

# Momo variables
env_access_key = os.environ.get("MOMO_ACCESS_KEY")
env_secret_key = os.environ.get("MOMO_SECRET_KEY")
env_ipn_url = os.environ.get("IPN_URL")
env_redirect_url = os.environ.get("REDIRECT_URL")
env_payment_code = os.environ.get("PAYMENT_CODE")
env_momo_hostname = os.environ.get('MOMO_HOSTNAME')
env_port = os.environ.get('PORT')

# Collections
hubs = db.hubs
orders = db.orders
staffs = db.staffs
deliveries = db.deliveries

# Helper function to parse JSON
def parse_json(data):
    data = json.loads(json_util.dumps(data))
    if isinstance(data, list):
        for item in data:
            if 'hubId' in item:
                if '$oid' in item.get('hubId', {}):
                    item['hubId'] = str(item['hubId']["$oid"])
            if '_id' in item:
                item['_id'] = str(item['_id']["$oid"])
            if 'insertedId' in item:
                item['insertedId'] = str(item['insertedId']["$oid"])
    else:
        if 'hubId' in data:
            data['hubId'] = str(data['hubId']["$oid"])
        if '_id' in data:
                data['_id'] = str(data['_id']["$oid"])
        if 'insertedId' in data:
                data['insertedId'] = str(data['insertedId']["$oid"])
    return data

latest_order = ""

# Helper Functions
def pay_momo(amount):
    access_key = env_access_key
    secret_key = env_secret_key
    order_info = "Pay your bill in Lift"
    partner_code = "MOMO"
    redirect_url = env_redirect_url
    ipn_url = env_ipn_url
    request_type = "payWithMethod"
    order_id = partner_code + str(int(datetime.now().timestamp() * 1000))
    request_id = order_id
    extra_data = ""
    payment_code = env_payment_code
    order_group_id = ""
    auto_capture = True
    lang = "vi"

    raw_signature = f"accessKey={access_key}&amount={amount}&extraData={extra_data}&ipnUrl={ipn_url}&orderId={order_id}&orderInfo={order_info}&partnerCode={partner_code}&redirectUrl={redirect_url}&requestId={request_id}&requestType={request_type}"

    global latest_order
    latest_order = order_id

    signature = hmac.new(secret_key.encode(), raw_signature.encode(), hashlib.sha256).hexdigest()

    request_body = {
        "partnerCode": partner_code,
        "partnerName": "Test",
        "storeId": "MomoTestStore",
        "requestId": request_id,
        "amount": amount,
        "orderId": order_id,
        "orderInfo": order_info,
        "redirectUrl": redirect_url,
        "ipnUrl": ipn_url,
        "lang": lang,
        "requestType": request_type,
        "autoCapture": auto_capture,
        "extraData": extra_data,
        "orderGroupId": order_group_id,
        "signature": signature,
    }

    url = f"https://{env_momo_hostname}/v2/gateway/api/create"
    response = requests.post(url, json=request_body)

    if response.status_code == 200:
        return response.json().get("payUrl")
    else:
        response.raise_for_status()


def check_transaction(order_id):
    access_key = env_access_key
    secret_key = env_secret_key
    partner_code = "MOMO"
    request_id = order_id
    lang = "vi"

    raw_signature = f"accessKey={access_key}&orderId={order_id}&partnerCode={partner_code}&requestId={request_id}"
    signature = hmac.new(secret_key.encode(), raw_signature.encode(), hashlib.sha256).hexdigest()

    request_body = {
        "partnerCode": partner_code,
        "requestId": request_id,
        "orderId": order_id,
        "lang": lang,
        "signature": signature,
    }

    url = f"https://{env_momo_hostname}/v2/gateway/api/query"
    response = requests.post(url, json=request_body)

    if response.status_code == 200:
        return response.json().get("resultCode")
    else:
        response.raise_for_status()

# Routes
@momo_bp.route("/pay/momo", methods=["POST"])
@cross_origin()
def api_pay():
    amount = request.args.get("amount")
    try:
        pay_url = pay_momo(amount)
        return parse_json({"payUrl": pay_url})
    except Exception as e:
        return parse_json({"error": str(e)}), 500

@momo_bp.route("/pay/momo/check", methods=["POST"])
@cross_origin()
def api_check():
    order_id = request.args.get("orderId")
    try:
        result = check_transaction(order_id)
        return parse_json({"result": result})
    except Exception as e:
        return parse_json({"error": str(e)}), 500

@momo_bp.route("/pay/momo/orderId", methods=["GET"])
@cross_origin()
def api_order_id():
    try:
        return parse_json({"latestOrder": latest_order})
    except Exception as e:
        return parse_json({"error": str(e)}), 500

