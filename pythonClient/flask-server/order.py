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
from arrange import parse_json

order_bp = Blueprint("order",__name__)
CORS(order_bp)

# Connect to MongoDB
client = MongoClient(os.environ.get("MONGO_DB"))
maps_key = os.environ.get("GOOGLE_MAP_API")

db = client.lift
CORS(order_bp)

limit = 6

# Collections
hubs = db.hubs
orders = db.orders
staffs = db.staffs
deliveries = db.deliveries

def get_order_detail(orders_list):
    result = []

    for order in orders_list:
        hub_id = str(order["hubId"])
        hub = hubs.find_one({"_id": hub_id})
        hub_name = hub["name"] if hub else "Unknown Hub"

        # Append order details with computed data
        order["hubName"] = hub_name
        result.append(order)

    return result

# Orders Endpoints

## Get all orders
@order_bp.route('/orders', methods=['GET'])
@cross_origin()
def get_all_orders():
    all_orders = orders.find()
    res = get_order_detail(all_orders)
    return parse_json(res), 200

@order_bp.route('/orders/status', methods=['GET'])
@cross_origin()
def get_orders_by_status():
    status = request.args.get('status')
    if not status:
        return jsonify({"error": "status parameter is required"}), 400

    valid_statuses = ["pending", "inProgress", "success", "failed", "canceled"]
    if status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}"}), 400

    orders_list = orders.find({"deliveryInfo.status": status})
    res = get_order_detail(orders_list)
    return parse_json(res), 200

# Search from all hub 
@order_bp.route('/orders/search', methods=['GET'])
@cross_origin()
def search_from_all_orders():
    search_str = request.args.get('search', default='', type=str)

    query = {
        "$or": [
            {"hubName": {"$regex": search_str, "$options": "i"}},
            {"hubId": {"$regex": search_str, "$options": "i"}},
            {"receiverInfo.name": {"$regex": search_str, "$options": "i"}},
            {"senderInfo.name": {"$regex": search_str, "$options": "i"}},
            {"deliveryInfo.deliveryType": {"$regex": search_str, "$options": "i"}},
            {"deliveryInfo.status": {"$regex": search_str, "$options": "i"}},
            {"message": {"$regex": search_str, "$options": "i"}},
            {"payStatus": {"$regex": search_str, "$options": "i"}},
            {"payWith": {"$regex": search_str, "$options": "i"}},
            {"receiverInfo.address": {"$regex": search_str, "$options": "i"}},
            {"senderInfo.address": {"$regex": search_str, "$options": "i"}},
        ]
    }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)}),

    
    res = list(
            orders.find(query)
        )

    result = get_order_detail(res)
    return parse_json(result), 200


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
    
    res = get_order_detail(order_list)
    return parse_json(res), 200

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
    
    res = get_order_detail(order_list)
    return parse_json(res), 200

## Get all orders matches with hubId
@order_bp.route('/orders/hub', methods=['GET'])
@cross_origin()
def get_orders_by_hub_id():
    hub_id = request.args.get('hubId')
    if not hub_id:
        return jsonify({"error": "hub_id parameter is required"}), 400
    
    order_list = orders.find({"hubId": ObjectId(hub_id)})
    res = get_order_detail(order_list)
    return parse_json(res), 200

## Get order by id
@order_bp.route('/order', methods=['GET'])
@cross_origin()
def get_order():
    orderId = request.args.get('id')
    order = orders.find_one({'_id': ObjectId(orderId)})
    res = get_order_detail(order)
    return parse_json(res), 200


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
    

    res = list(
            orders.find()
            .skip(number_row)
            .limit(limit)
        )

    response = get_order_detail(res)
    return parse_json(response), 200

# Search hub and display from number rows
@order_bp.route('/order/search', methods=['GET'])
@cross_origin()
def search_order_by_row_num():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    

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

    response = get_order_detail(res)
    return parse_json(response), 200

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
        ).count({})

    return jsonify({"count": res}), 200

#  Get order by number rows by status
@order_bp.route('/order/row/status', methods=['GET'])
@cross_origin()
def get_order_by_row_num_status():
    status = request.args.get('status')
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    
    if not status:
        return jsonify({"error": "status parameter is required"}), 400

    valid_statuses = ["pending", "inProgress", "success", "failed", "canceled"]
    if status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}"}), 400

    

    res = list(
            orders.find({"deliveryInfo.status": status})
            .skip(number_row)
            .limit(limit)
        )

    response = get_order_detail(res)
    return parse_json(response), 200

# Search hub and display from number rows
@order_bp.route('/order/search/status', methods=['GET'])
@cross_origin()
def search_order_by_row_num_status():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    status = request.args.get('status')
    if not status:
        return jsonify({"error": "status parameter is required"}), 400

    valid_statuses = ["pending", "inProgress", "success", "failed", "canceled"]
    if status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}"}), 400

    

    query = {
                "$or": 
                [
                    {"_id": {"$regex": search_str, "$options": "i"}}
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})    

    orders_list = orders.find({"deliveryInfo.status": status})

    res = list(
            orders_list.find(query)
            .skip(number_row)
            .limit(limit)
        )

    response = get_order_detail(res)
    return parse_json(response), 200

# Count all hub
@order_bp.route('/orders/count/status', methods=['GET'])
@cross_origin()
def count_order_status():
    status = request.args.get('status')
    if not status:
        return jsonify({"error": "status parameter is required"}), 400

    valid_statuses = ["pending", "inProgress", "success", "failed", "canceled"]
    if status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}"}), 400


    res = orders.find({"deliveryInfo.status": status}).count_documents({})
    return jsonify({"count": res}), 200

# Count hub and display from number rows
@order_bp.route('/order/search/count/status', methods=['GET'])
@cross_origin()
def count_order_by_row_num_status():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    status = request.args.get('status')
    if not status:
        return jsonify({"error": "status parameter is required"}), 400

    valid_statuses = ["pending", "inProgress", "success", "failed", "canceled"]
    if status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}"}), 400

    

    query = {
                "$or": 
                [
                    {"_id": {"$regex": search_str, "$options": "i"}}
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})    
    
    orders_list = orders.find({"deliveryInfo.status": status})

    res = list(
            orders_list.find(query)
            .skip(number_row)
            .limit(limit)
        ).count({})

    return jsonify({"count": res}), 200
