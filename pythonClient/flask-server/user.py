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

user_bp = Blueprint("user",__name__)
CORS(user_bp)

# Connect to MongoDB
client = MongoClient(os.environ.get("MONGO_DB"))
maps_key = os.environ.get("GOOGLE_MAP_API")

db = client.lift
CORS(user_bp)


# Collections
hubs = db.hubs
orders = db.orders
staffs = db.staffs
deliveries = db.deliveries
users = db.users

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

# Get all users
@user_bp.route('/users', methods=['GET'])
@cross_origin()
def get_all_users():
    all_users = users.find()
    return parse_json(all_users), 200

# Get user by id
@user_bp.route('/user', methods=['GET'])
@cross_origin()
def get_user():
    user_id = request.args.get('id')
    user = users.find_one({'_id': ObjectId(user_id)})
    return parse_json(user), 200

@user_bp.route('/user', methods=['POST'])
@cross_origin()
def create_user():
    data = request.json
    result = users.insert_one(data)
    return parse_json({'insertedId': result.inserted_id}), 201

@user_bp.route('/user', methods=['PUT'])
@cross_origin()
def update_user():
    user_id = request.args.get('id')
    data = request.json
    result = users.update_one({'_id': ObjectId(user_id)}, {'$set': data})
    return parse_json({'matched_count': result.matched_count, 'modified_count': result.modified_count}), 200

@user_bp.route('/user', methods=['DELETE'])
@cross_origin()
def delete_user():
    user_id = request.args.get('id')
    if not ObjectId.is_valid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400

    user_object_id = ObjectId(user_id)

    # If no links exist, delete the user
    result = users.delete_one({"_id": user_object_id})
    if result.deleted_count == 1:
        return jsonify({"message": "User deleted successfully",
                        "status":"success"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

#  Get users by number rows
@user_bp.route('/user/row', methods=['GET'])
@cross_origin()
def get_user_by_row_num():
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 8

    res = list(
            users.find()
            .skip(number_row)
            .limit(limit)
        )

    return parse_json(res), 200

# Search from all user 
@user_bp.route('/users/search', methods=['GET'])
@cross_origin()
def search_from_all_user():
    search_str = request.args.get('search', default='', type=str)

    query = {
                "$or": 
                [
                    {"username": {"$regex": search_str, "$options": "i"}},
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})

    res = list(
            users.find(query)
        )

    return parse_json(res), 200


# Search user and display from number rows
@user_bp.route('/user/search', methods=['GET'])
@cross_origin()
def search_user_by_row_num():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 8

    query = {
                "$or": 
                [
                    {"username": {"$regex": search_str, "$options": "i"}},
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})

    res = list(
            users.find(query)
            .skip(number_row)
            .limit(limit)
        )

    return parse_json(res), 200

# Count all user
@user_bp.route('/users/count', methods=['GET'])
@cross_origin()
def count_user():
    res = users.count_documents({})
    return jsonify({"count": res}), 200

# Count user and display from number rows
@user_bp.route('/user/search/count', methods=['GET'])
@cross_origin()
def count_user_by_row_num():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 8

    query = {
                "$or": 
                [
                    {"username": {"$regex": search_str, "$options": "i"}},
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})

    res = list(
            users.find(query)
            .skip(number_row)
            .limit(limit)
        ).count({})

    return jsonify({"count": res}), 200
