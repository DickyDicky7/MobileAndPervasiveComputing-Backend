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

staff_bp = Blueprint("staff",__name__)
CORS(staff_bp)

# Connect to MongoDB
client = MongoClient(os.environ.get("MONGO_DB"))
maps_key = os.environ.get("GOOGLE_MAP_API")

db = client.lift
CORS(staff_bp)


# Collections
hubs = db.hubs
orders = db.orders
staffs = db.staffs
deliveries = db.deliveries

# Staff Endpoints

@staff_bp.route('/staffs', methods=['GET'])
@cross_origin()
def get_all_staff():
    all_staff = staffs.find()
    return parse_json(all_staff), 200

@staff_bp.route('/staffs/hub', methods=['GET'])
@cross_origin()
def get_all_staff_by_hub_id():
    hub_id = request.args.get('hubId')
    if not hub_id:
        return jsonify({"error": "hub_id parameter is required"}), 400
    
    all_staff = staffs.find({"hubId": ObjectId(hub_id)})

    return parse_json(all_staff), 200

@staff_bp.route('/staffs/search/hub', methods=['GET'])
@cross_origin()
def search_staff_by_hub_id():
    search_str = request.args.get('search', default='', type=str)
    hub_id = request.args.get('hubId')

    if not hub_id:
        return jsonify({"error": "hub_id parameter is required"}), 400
    
    query = {
            "$and": [
            {"hubId": ObjectId(hub_id)},
            {
                "$or": 
                [
                    {"name": {"$regex": search_str, "$options": "i"}},
                    {"age": {"$regex": search_str, "$options": "i"}},
                    {"gender": {"$regex": search_str, "$options": "i"}},
                    {"motorcycleCapacity": {"$regex": search_str, "$options": "i"}},
                    {"weight": {"$regex": search_str, "$options": "i"}}
                ]
            }
        ]
    }
    if ObjectId.is_valid(search_str):
        query["$and"][1]["$or"].extend([
            {"userId": ObjectId(search_str)},
            {"_id": ObjectId(search_str)}
        ])

    response = list(
            staffs.find(query)
        )

    return parse_json(response), 200


@staff_bp.route('/staff', methods=['GET'])
@cross_origin()
def get_staff():
    staffId = request.args.get('id')
    staff_member = staffs.find_one({'_id': ObjectId(staffId)})
    return parse_json(staff_member), 200

@staff_bp.route('/staff', methods=['POST'])
@cross_origin()
def create_staff():
    data = request.json
    data['hubId'] = ObjectId(data['hubId'])
    result = staffs.insert_one(data)
    return parse_json({'insertedId': result.inserted_id}), 201

@staff_bp.route('/staff', methods=['PUT'])
@cross_origin()
def update_staff():
    staffId = request.args.get('id')
    data = request.json
    if 'hubId' in data:
        data['hubId'] = ObjectId(data['hubId'])
    result = staffs.update_one({'_id': ObjectId(staffId)}, {'$set': data})
    return parse_json({'matched_count': result.matched_count, 'modified_count': result.modified_count}), 200

@staff_bp.route('/staff', methods=['DELETE'])
@cross_origin()
def delete_staff():
    staffId = request.args.get('id')
    result = staffs.delete_one({'_id': ObjectId(staffId)})
    return parse_json({'deleted_count': result.deleted_count}), 200

#  Get staff by number rows
@staff_bp.route('/staff/row', methods=['GET'])
@cross_origin()
def get_staff_by_row_num():
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 8

    res = list(
            staffs.find()
            .skip(number_row)
            .limit(limit)
        )

    return parse_json(res), 200

# Search staff and display from number rows
@staff_bp.route('/staff/search', methods=['GET'])
@cross_origin()
def search_staff_by_row_num():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 8

    query = {
                "$or": 
                [
                    {"name": {"$regex": search_str, "$options": "i"}},
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})

    res = list(
            staffs.find(query)
            .skip(number_row)
            .limit(limit)
        )

    return parse_json(res), 200

# Count all hub
@staff_bp.route('/staffs/count', methods=['GET'])
@cross_origin()
def count_staff():
    res = staffs.count_documents({})
    return jsonify({"count": res}), 200

# Count hub and display from number rows
@staff_bp.route('/staff/search/count', methods=['GET'])
@cross_origin()
def count_order_by_row_num():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 8

    query = {
                "$or": 
                [
                    {"name": {"$regex": search_str, "$options": "i"}},
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})

    res = list(
            staffs.find(query)
            .skip(number_row)
            .limit(limit)
        ).count()

    return jsonify({"count": res}), 200
