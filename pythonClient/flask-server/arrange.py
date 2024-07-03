from flask import Flask, request, jsonify, Blueprint # type: ignore
from pymongo import MongoClient # type: ignore
from bson.objectid import ObjectId # type: ignore
from bson import json_util # type: ignore
import json
import os

arrange_bp = Blueprint("arrange",__name__)

# Connect to MongoDB
client = MongoClient(os.environ.get("MONGO_DB"))
db = client.lift

# Collections
hubs = db.hubs
orders = db.orders
staff = db.staff
delivery = db.deliveries

# Sample data
sample_hubs = [
    {"_id": ObjectId("66851d686a086a68a695c186"), "name": "Hub 1", "district": "District 1"},
    {"_id": ObjectId("66851d686a086a68a695c187"), "name": "Hub 2", "district": "District 2"}
]

sample_orders = [
    {"_id": ObjectId("66851e166a086a68a695c187"), "value": 1200000, "weight": 50, "hub_id": ObjectId("66851d686a086a68a695c186"), "status": "pending", "delivery_address": "123 Vo Thi Sau, District 1, HCM City"},
    {"_id": ObjectId("66851e166a086a68a695c188"), "value": 800000, "weight": 30, "hub_id": ObjectId("66851d686a086a68a695c187"), "status": "pending", "delivery_address": "456 Nguyen Trai, District 2, HCM City"}
]

sample_staff = [
    {"_id": ObjectId("66851d316a086a68a695c185"), "name": "John Doe", "age": 25, "gender": "male", "weight": 70, "motorcycle_capacity": 150, "hub_id": ObjectId("66851d686a086a68a695c186")},
    {"_id": ObjectId("66851d316a086a68a695c186"), "name": "Jane Smith", "age": 30, "gender": "female", "weight": 60, "motorcycle_capacity": 100, "hub_id": ObjectId("66851d686a086a68a695c187")}
]

# Insert sample data into the collections
@arrange_bp.route('/init', methods=['GET'])
def insert_sample_data():
    # Insert hubs
    hubs.insert_many(sample_hubs)
    
    # Insert orders
    orders.insert_many(sample_orders)
    
    # Insert staff
    staff.insert_many(sample_staff)

    return("Sample data inserted successfully.")


# Helper function to parse JSON
def parse_json(data):
    data = json.loads(json_util.dumps(data))
    if isinstance(data, list):
        for item in data:
            if 'hub_id' in item:
                item['hub_id'] = str(item['hub_id']["$oid"])
            if '_id' in item:
                item['_id'] = str(item['_id']["$oid"])
            if 'inserted_id' in item:
                item['inserted_id'] = str(item['inserted_id']["$oid"])
    else:
        if 'hub_id' in data:
            data['hub_id'] = str(data['hub_id']["$oid"])
        if '_id' in data:
                data['_id'] = str(data['_id']["$oid"])
        if 'inserted_id' in data:
                data['inserted_id'] = str(data['inserted_id']["$oid"])
    return data

# Hubs Endpoints

@arrange_bp.route('/hubs', methods=['GET'])
def get_all_hubs():
    all_hubs = hubs.find()
    return parse_json(all_hubs), 200

@arrange_bp.route('/hub', methods=['GET'])
def get_hub():
    hub_id = request.args.get('id')
    hub = hubs.find_one({'_id': ObjectId(hub_id)})
    return parse_json(hub), 200

@arrange_bp.route('/hub', methods=['POST'])
def create_hub():
    data = request.json
    result = hubs.insert_one(data)
    return parse_json({'inserted_id': result.inserted_id}), 201

@arrange_bp.route('/hub', methods=['PUT'])
def update_hub():
    hub_id = request.args.get('id')
    data = request.json
    result = hubs.update_one({'_id': ObjectId(hub_id)}, {'$set': data})
    return parse_json({'matched_count': result.matched_count, 'modified_count': result.modified_count}), 200

@arrange_bp.route('/hub', methods=['DELETE'])
def delete_hub():
    hub_id = request.args.get('id')
    result = hubs.delete_one({'_id': ObjectId(hub_id)})
    return parse_json({'deleted_count': result.deleted_count}), 200

# Orders Endpoints

@arrange_bp.route('/orders', methods=['GET'])
def get_all_orders():
    all_orders = orders.find()
    return parse_json(all_orders), 200

@arrange_bp.route('/order', methods=['GET'])
def get_order():
    order_id = request.args.get('id')
    order = orders.find_one({'_id': ObjectId(order_id)})
    return parse_json(order), 200

@arrange_bp.route('/order', methods=['POST'])
def create_order():
    data = request.json
    data['hub_id'] = ObjectId(data['hub_id'])
    result = orders.insert_one(data)
    return parse_json({'inserted_id': result.inserted_id}), 201

@arrange_bp.route('/order', methods=['PUT'])
def update_order():
    order_id = request.args.get('id')
    data = request.json
    result = orders.update_one({'_id': ObjectId(order_id)}, {'$set': data})
    return parse_json({'matched_count': result.matched_count, 'modified_count': result.modified_count}), 200

@arrange_bp.route('/order', methods=['DELETE'])
def delete_order():
    order_id = request.args.get('id')
    result = orders.delete_one({'_id': ObjectId(order_id)})
    return parse_json({'deleted_count': result.deleted_count}), 200

# Staff Endpoints

@arrange_bp.route('/staffs', methods=['GET'])
def get_all_staff():
    all_staff = staff.find()
    return parse_json(all_staff), 200

@arrange_bp.route('/staff', methods=['GET'])
def get_staff():
    staff_id = request.args.get('id')
    staff_member = staff.find_one({'_id': ObjectId(staff_id)})
    return parse_json(staff_member), 200

@arrange_bp.route('/staff', methods=['POST'])
def create_staff():
    data = request.json
    data['hub_id'] = ObjectId(data['hub_id'])
    result = staff.insert_one(data)
    return parse_json({'inserted_id': result.inserted_id}), 201

@arrange_bp.route('/staff', methods=['PUT'])
def update_staff():
    staff_id = request.args.get('id')
    data = request.json
    result = staff.update_one({'_id': ObjectId(staff_id)}, {'$set': data})
    return parse_json({'matched_count': result.matched_count, 'modified_count': result.modified_count}), 200

@arrange_bp.route('/staff', methods=['DELETE'])
def delete_staff():
    staff_id = request.args.get('id')
    result = staff.delete_one({'_id': ObjectId(staff_id)})
    return parse_json({'deleted_count': result.deleted_count}), 200

# Assign Delivery Task Endpoint

@arrange_bp.route('/assign', methods=['POST'])
def assign_delivery_task():
    hub_id = request.json['hub_id']
    orders_pending = orders.find({'hub_id': ObjectId(hub_id), 'status': 'pending'})
    staff_members = staff.find({'hub_id': ObjectId(hub_id)})

    assignments = []

    for order in orders_pending:
        for member in staff_members:
            if (order['weight'] <= member['motorcycle_capacity'] and
                    ((member['age'] <= 30 and order['value'] > 1000000) or
                    (member['age'] > 30 and order['value'] <= 1000000))):
                assignments.append({
                    'order_id': order['_id'],
                    'staff_id': member['_id'],
                    'delivery_id': order['hub_id']
                })
                orders.update_one({'_id': order['_id']}, {'$set': {'status': 'assigned'}})
                break

    return parse_json(assignments), 200



# if __name__ == '__main__':
#     app.run(debug=True)
