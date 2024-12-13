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

hub_bp = Blueprint("hub",__name__)
CORS(hub_bp)

# Connect to MongoDB
client = MongoClient(os.environ.get("MONGO_DB"))
maps_key = os.environ.get("GOOGLE_MAP_API")

db = client.lift
CORS(hub_bp)


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

def geocode_address(address):
    url = f'https://geocode.maps.co/search?q='+address+'&api_key='+maps_key
    response = requests.get(url)
    if response.status_code == 200:
        # return response.json()
        result = parse_json(response.json())
        if result:
            location = result[0]
            return location['lat'], location['lon']
    return None, None

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
    result = hubs.delete_one({'_id': ObjectId(hub_id)})
    return parse_json({'deleted_count': result.deleted_count}), 200

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
    limit = 8

    res = list(
            hubs.find()
            .skip(number_row)
            .limit(limit)
        )

    return parse_json(res), 200

# Search hub and display from number rows
@hub_bp.route('/hub/search', methods=['GET'])
@cross_origin()
def search_hub_by_row_num():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 8

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

    return parse_json(res), 200