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

# Staff Endpoints

@staff_bp.route('/staffs', methods=['GET'])
@cross_origin()
def get_all_staff():
    all_staff = staffs.find()
    return parse_json(all_staff), 200

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
