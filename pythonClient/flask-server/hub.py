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

hub_bp = Blueprint("hub",__name__)
CORS(hub_bp)

# Connect to MongoDB
client = MongoClient(os.environ.get("MONGO_DB"))
maps_key      = os.environ.get("GOOGLE_MAP_API")
geocoding_key = os.environ.get("GEO_CODING_API") 

db = client.lift
CORS(hub_bp)


# Collections
hubs = db.hubs
orders = db.orders
staffs = db.staffs
deliveries = db.deliveries

def geocode_address(address):
    url = f'https://api.opencagedata.com/geocode/v1/json?key='+geocoding_key+'&q='+address+'&pretty=1&language=native'
    response = requests.get(url)
    if         response.status_code == 200:
        # return response.json()
        result = parse_json(response.json())
        if             result:
            location = result['results'][0]['geometry']
            return   location[  'lat'  ] ,   location [  'lng'  ]
    return None , None


def get_hub_detail(hubs_list):
    result = []

    for hub in hubs_list:
        hub_id = str(hub["_id"])

        # Query orders related to the current hub
        orders_list = list(orders.find({"hubId": ObjectId(hub_id)}))

        # Count orders by status
        success_orders = sum(1 for order in orders_list if order["deliveryInfo"]["status"] == "success")
        failed_orders = sum(1 for order in orders_list if order["deliveryInfo"]["status"] == "failed")
        in_progress_orders = sum(1 for order in orders_list if order["deliveryInfo"]["status"] == "inProgress")
        pending_orders = sum(1 for order in orders_list if order["deliveryInfo"]["status"] == "pending")
        canceled_orders = sum(1 for order in orders_list if order["deliveryInfo"]["status"] == "canceled")

        # Append hub details with computed data
        result.append({
            "hubId": str(hub_id),
            "name": hub["name"],
            "address": hub["address"],
            "successOrders": success_orders,
            "failedOrders": failed_orders,
            "canceledOrders": canceled_orders,
            "inProgressOrders": in_progress_orders,
            "pendingOrders": pending_orders,
        })
    return result


@hub_bp.route('/address', methods=['GET'])
@cross_origin()
def get_address():
    address = request.args.get('address')
    url = 'https://geocode.maps.co/search?q='+address+'&api_key='+maps_key
    response = requests.get(url)
    if response.status_code == 200:
        return (parse_json(response.json())), 200
    return ({'result':'failed'}), 200

@hub_bp.route('/checkgeo', methods=['GET'])
@cross_origin()
def check():
    response = geocode_address("1600 Amphitheatre Parkway, Mountain View, CA")
    return ({'response': response})

# Helper function to calculate distance between two locations (latitude, longitude)
def calculate_distance(lat1, lon1, lat2, lon2):
    from math import radians, cos, sin, asin, sqrt
    R = 6371  # Radius of the earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    distance = R * c
    return distance

# Get all hubs
@hub_bp.route('/hubs', methods=['GET'])
@cross_origin()
def get_all_hubs():
    all_hubs = hubs.find()
    return parse_json(all_hubs), 200

@hub_bp.route("/hubs/detail", methods=["GET"])
@cross_origin()
def get_hubs_with_details():
    hubs_list = list(hubs.find())
    result = get_hub_detail(hubs_list)
    return parse_json(result), 200


@hub_bp.route('/hub', methods=['GET'])
@cross_origin()
def get_hub():
    hub_id = request.args.get('id')
    hub = hubs.find_one({'_id': ObjectId(hub_id)})
    return parse_json(hub), 200

@hub_bp.route('/hub', methods=['POST'])
@cross_origin()
def create_hub():
    data = request.json
    result = hubs.insert_one(data)
    return parse_json({'insertedId': result.inserted_id}), 201

@hub_bp.route('/hub', methods=['PUT'])
@cross_origin()
def update_hub():
    hub_id = request.args.get('id')
    data = request.json
    result = hubs.update_one({'_id': ObjectId(hub_id)}, {'$set': data})
    return parse_json({'matched_count': result.matched_count, 'modified_count': result.modified_count}), 200

@hub_bp.route('/hub', methods=['DELETE'])
@cross_origin()
def delete_hub():
    hub_id = request.args.get('id')
    if not ObjectId.is_valid(hub_id):
        return jsonify({"error": "Invalid hub ID"}), 400

    hub_object_id = ObjectId(hub_id)

    # Check if there are any staff linked to the hub
    staff_count = staffs.count_documents({"hubId": hub_object_id})
    if staff_count > 0:
        return jsonify({
            "error": "Cannot delete hub. Staff are linked to this hub.",
            "status": "failed",
        }), 400

    # Check if there are any orders linked to the hub
    order_count = orders.count_documents({"hubId": hub_object_id})
    if order_count > 0:
        return jsonify({
            "error": "Cannot delete hub. Orders are linked to this hub.",
            "status": "failed",
        }), 400

    # If no links exist, delete the hub
    result = hubs.delete_one({"_id": hub_object_id})
    if result.deleted_count == 1:
        return jsonify({"message": "Hub deleted successfully",
                        "status":"success"}), 200
    else:
        return jsonify({"error": "Hub not found"}), 404

# Get the nearest hub by current address

@hub_bp.route('/hub/near', methods=['GET'])
@cross_origin()
def get_nearest_hub():

    address = request.args.get('address')
    address_lat, address_lon = geocode_address(address)

    distances = []
    allHubs = hubs.find()
    minHub = allHubs[0]
    minAddress = allHubs[0]["address"]
    minHub_lat, minHub_lon = geocode_address(minAddress)
    minDistance = calculate_distance(float(address_lat), float(address_lon), float(minHub_lat), float(minHub_lon))

    for ihub in allHubs:
        ihub_lat, ihub_lon = geocode_address(ihub['address'])
        distance = calculate_distance(float(address_lat), float(address_lon), float(ihub_lat), float(ihub_lon))
        distances.append(distance)
        if(minDistance > distance):
            minDistance = distance
            minHub = ihub

    return parse_json(minHub), 200

# Get hub by number rows
@hub_bp.route('/hub/row', methods=['GET'])
@cross_origin()
def get_hub_by_row_num():
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 5

    res = list(
            hubs.find()
            .skip(number_row)
            .limit(limit)
        )
    
    result = get_hub_detail(res)
    return parse_json(result), 200

# Search from all hub 
@hub_bp.route('/hubs/search', methods=['GET'])
@cross_origin()
def search_from_all_hub():
    search_str = request.args.get('search', default='', type=str)

    query = {
                "$or": 
                [
                    {"name": {"$regex": search_str, "$options": "i"}},
                    {"address": {"$regex": search_str, "$options": "i"}},
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})

    res = list(
            hubs.find(query)
        )

    result = get_hub_detail(res)
    return parse_json(result), 200


# Search hub and display from number rows
@hub_bp.route('/hub/search', methods=['GET'])
@cross_origin()
def search_hub_by_row_num():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 5

    query = {
                "$or": 
                [
                    {"name": {"$regex": search_str, "$options": "i"}},
                    {"address": {"$regex": search_str, "$options": "i"}},
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})

    res = list(
            hubs.find(query)
            .skip(number_row)
            .limit(limit)
        )

    result = get_hub_detail(res)
    return parse_json(result), 200

# Count all hub
@hub_bp.route('/hubs/count', methods=['GET'])
@cross_origin()
def count_hub():
    res = hubs.count_documents({})
    return jsonify({"count": res}), 200

# Count hub and display from number rows
@hub_bp.route('/hub/search/count', methods=['GET'])
@cross_origin()
def count_hub_by_row_num():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 5

    query = {
                "$or": 
                [
                    {"name": {"$regex": search_str, "$options": "i"}},
                    {"address": {"$regex": search_str, "$options": "i"}},
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})

    res = list(
            hubs.find(query)
            .skip(number_row)
            .limit(limit)
        ).count({})

    return jsonify({"count": res}), 200
