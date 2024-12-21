from flask import Flask, request, jsonify, Blueprint # type: ignore
from pymongo import MongoClient # type: ignore
from bson.objectid import ObjectId # type: ignore
from bson import json_util # type: ignore
from datetime import datetime
from flask_cors import CORS, cross_origin # type: ignore
from ortools.constraint_solver import routing_enums_pb2 # type: ignore
from ortools.constraint_solver import pywrapcp # type: ignore
import json
import requests  # type: ignore
import os
from flask_cors import CORS, cross_origin # type: ignore

order_bp = Blueprint("order",__name__)
CORS(order_bp)

# Connect to MongoDB
client = MongoClient(os.environ.get("MONGO_DB"))
maps_key = os.environ.get("GOOGLE_MAP_API")

db = client.lift
CORS(order_bp)


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

# Orders Endpoints

## Get all orders
@order_bp.route('/orders', methods=['GET'])
@cross_origin()
def get_all_orders():
    all_orders = orders.find()
    return parse_json(all_orders), 200

## Get all orders matches with senderId
@order_bp.route('/orders/sender', methods=['GET'])
@cross_origin()
def get_orders_by_sender_userid():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({"error": "userId parameter is required"}), 400
    
    ordersSender = orders.find({"senderInfo.userId": user_id})
    order_list = []
    for order in ordersSender:
        order_list.append(order)
    
    return parse_json(order_list), 200

## Get all orders matches with receiverId
@order_bp.route('/orders/receiver', methods=['GET'])
@cross_origin()
def get_orders_by_receiver_userid():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({"error": "userId parameter is required"}), 400
    
    orders_receiver = orders.find({"receiverInfo.userId": user_id})
    order_list = []
    for order in orders_receiver:
        order_list.append(order)
    
    return parse_json(order_list), 200

## Get all orders matches with hubId
@order_bp.route('/orders/hub', methods=['GET'])
@cross_origin()
def get_orders_by_hubId():
    hub_id = request.args.get('hubId')
    if not hub_id:
        return jsonify({"error": "hub_id parameter is required"}), 400
    
    order_list = orders.find({"hubId": ObjectId(hub_id)})
    return parse_json(order_list), 200

## Get order by id
@order_bp.route('/order', methods=['GET'])
@cross_origin()
def get_order():
    orderId = request.args.get('id')
    order = orders.find_one({'_id': ObjectId(orderId)})
    return parse_json(order), 200

@order_bp.route('/order', methods=['POST'])
@cross_origin()
def create_order():
    data = request.json
    data['hubId'] = ObjectId(data['hubId'])
    result = orders.insert_one(data)
    return parse_json({'insertedId': result.inserted_id}), 201

@order_bp.route('/order', methods=['PUT'])
@cross_origin()
def update_order():
    orderId = request.args.get('id')
    data = request.json
    if 'hubId' in data:
        data['hubId'] = ObjectId(data['hubId'])
    result = orders.update_one({'_id': ObjectId(orderId)}, {'$set': data})
    return parse_json({'matched_count': result.matched_count, 'modified_count': result.modified_count}), 200

@order_bp.route('/order', methods=['DELETE'])
@cross_origin()
def delete_order():
    orderId = request.args.get('id')
    result = orders.delete_one({'_id': ObjectId(orderId)})
    return parse_json({'deleted_count': result.deleted_count}), 200

# Update pay status of order
@order_bp.route('/order/payStatus', methods=['PUT'])
@cross_origin()
def update_pay_status():
    try:
        new_status = request.args.get("payStatus")
        order_id = request.args.get('id')
        if not new_status:
            return parse_json({"error": "Missing payStatus in request body"}), 400
        
        result = orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"payStatus": new_status}}
        )
        if result.matched_count == 0:
            return parse_json({"message": "Order not found"}), 404

        return parse_json({"message": "Pay status updated successfully"}), 200
    except Exception as e:
        return parse_json({"error": str(e)}), 500

#  Get order by number rows
@order_bp.route('/order/row', methods=['GET'])
@cross_origin()
def get_order_by_row_num():
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 8

    res = list(
            orders.find()
            .skip(number_row)
            .limit(limit)
        )

    return parse_json(res), 200

# Search hub and display from number rows
@order_bp.route('/order/search', methods=['GET'])
@cross_origin()
def search_order_by_row_num():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 8

    query = {
                "$or": 
                [
                    {"_id": {"$regex": search_str, "$options": "i"}}
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})    

    res = list(
            orders.find(query)
            .skip(number_row)
            .limit(limit)
        )

    return parse_json(res), 200

# Count all hub
@order_bp.route('/orders/count', methods=['GET'])
@cross_origin()
def count_order():
    res = orders.count_documents({})
    return jsonify({"count": res}), 200

# Count hub and display from number rows
@order_bp.route('/order/search/count', methods=['GET'])
@cross_origin()
def count_order_by_row_num():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 8

    query = {
                "$or": 
                [
                    {"_id": {"$regex": search_str, "$options": "i"}}
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})    

    res = list(
            orders.find(query)
            .skip(number_row)
            .limit(limit)
        ).count()

    return jsonify({"count": res}), 200
