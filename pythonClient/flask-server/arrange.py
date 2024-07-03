from flask import Flask, request, jsonify, Blueprint # type: ignore
from pymongo import MongoClient # type: ignore
from bson.objectid import ObjectId # type: ignore
from bson import json_util # type: ignore
from datetime import datetime
from ortools.constraint_solver import routing_enums_pb2 # type: ignore
from ortools.constraint_solver import pywrapcp # type: ignore
import json
import requests  # type: ignore
import os

arrange_bp = Blueprint("arrange",__name__)

# Connect to MongoDB
client = MongoClient(os.environ.get("MONGO_DB"))
maps_key = os.environ.get("GOOGLE_MAP_API")
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
    {"_id": ObjectId("66851e166a086a68a695c187"), "value": 1200000, "weight": 50, "hubId": ObjectId("66851d686a086a68a695c186"), "status": "pending", "deliveryAddress": "123 Vo Thi Sau, District 1, HCM City"},
    {"_id": ObjectId("66851e166a086a68a695c188"), "value": 800000, "weight": 30, "hubId": ObjectId("66851d686a086a68a695c187"), "status": "pending", "deliveryAddress": "456 Nguyen Trai, District 2, HCM City"}
]

sample_staff = [
    {"_id": ObjectId("66851d316a086a68a695c185"), "name": "John Doe", "age": 25, "gender": "male", "weight": 70, "motorcycleCapacity": 150, "hubId": ObjectId("66851d686a086a68a695c186")},
    {"_id": ObjectId("66851d316a086a68a695c186"), "name": "Jane Smith", "age": 30, "gender": "female", "weight": 60, "motorcycleCapacity": 100, "hubId": ObjectId("66851d686a086a68a695c187")}
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
            if 'hubId' in item:
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
    # url = f'https://geocode.maps.co/search?q='+address+'&api_key='+maps_key
    response = requests.get(url)
    if response.status_code == 200:
        result = parse_json(response)
        if result:
            location = result[0]
            print("hi")
            return parse_json({"lat": location['lat'], "lon" : location['lon']})
    return parse_json({"response": 'none'})

@arrange_bp.route('/checkgeocode', methods = ["GET"])
def check():
    response= geocode_address("1600 Amphitheatre Parkway, Mountain View, CA")
    return parse_json(response)

# Helper function to calculate distance between two locations (latitude, longitude)
def calculate_distance(lat1, lon1, lat2, lon2):
    # This function calculates the Haversine distance between two points on the Earth
    from math import radians, cos, sin, asin, sqrt
    R = 6371  # Radius of the earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    distance = R * c
    return distance

# Use OR-Tools to calculate the optimal routes
def create_data_model(orders, staff, hub):
    data = {}
    hub_lat, hub_lng = geocode_address(hub['address'])
    data['distance_matrix'] = []
    all_locations = [(hub_lat, hub_lng)] + [geocode_address(order['delivery_address']) for order in orders]
    for loc1 in all_locations:
        distances = []
        for loc2 in all_locations:
            distances.append(calculate_distance(loc1['lat'], loc1['lng'], loc2['lat'], loc2['lng']))
        data['distance_matrix'].append(distances)
    data['numVehicles'] = len(staff)
    data['depot'] = 0
    return data

def solve_vrp(data):
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)
    if not solution:
        return None

    routes = []
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        routes.append(route)
    return routes

# Hubs Endpoints

@arrange_bp.route('/hubs', methods=['GET'])
def get_all_hubs():
    all_hubs = hubs.find()
    return parse_json(all_hubs), 200

@arrange_bp.route('/hub', methods=['GET'])
def get_hub():
    hubId = request.args.get('id')
    hub = hubs.find_one({'_id': ObjectId(hubId)})
    return parse_json(hub), 200

@arrange_bp.route('/hub', methods=['POST'])
def create_hub():
    data = request.json
    result = hubs.insert_one(data)
    return parse_json({'insertedId': result.insertedId}), 201

@arrange_bp.route('/hub', methods=['PUT'])
def update_hub():
    hubId = request.args.get('id')
    data = request.json
    result = hubs.update_one({'_id': ObjectId(hubId)}, {'$set': data})
    return parse_json({'matchedCount': result.matchedCount, 'modifiedCount': result.modifiedCount}), 200

@arrange_bp.route('/hub', methods=['DELETE'])
def delete_hub():
    hubId = request.args.get('id')
    result = hubs.delete_one({'_id': ObjectId(hubId)})
    return parse_json({'deletedCount': result.deletedCount}), 200

# Orders Endpoints

@arrange_bp.route('/orders', methods=['GET'])
def get_all_orders():
    all_orders = orders.find()
    return parse_json(all_orders), 200

@arrange_bp.route('/order', methods=['GET'])
def get_order():
    orderId = request.args.get('id')
    order = orders.find_one({'_id': ObjectId(orderId)})
    return parse_json(order), 200

@arrange_bp.route('/order', methods=['POST'])
def create_order():
    data = request.json
    data['hubId'] = ObjectId(data['hubId'])
    result = orders.insert_one(data)
    return parse_json({'insertedId': result.insertedId}), 201

@arrange_bp.route('/order', methods=['PUT'])
def update_order():
    orderId = request.args.get('id')
    data = request.json
    result = orders.update_one({'_id': ObjectId(orderId)}, {'$set': data})
    return parse_json({'matchedCount': result.matchedCount, 'modifiedCount': result.modifiedCount}), 200

@arrange_bp.route('/order', methods=['DELETE'])
def delete_order():
    orderId = request.args.get('id')
    result = orders.delete_one({'_id': ObjectId(orderId)})
    return parse_json({'deletedCount': result.deletedCount}), 200

# Staff Endpoints

@arrange_bp.route('/staffs', methods=['GET'])
def get_all_staff():
    all_staff = staff.find()
    return parse_json(all_staff), 200

@arrange_bp.route('/staff', methods=['GET'])
def get_staff():
    staffId = request.args.get('id')
    staff_member = staff.find_one({'_id': ObjectId(staffId)})
    return parse_json(staff_member), 200

@arrange_bp.route('/staff', methods=['POST'])
def create_staff():
    data = request.json
    data['hubId'] = ObjectId(data['hubId'])
    result = staff.insert_one(data)
    return parse_json({'insertedId': result.insertedId}), 201

@arrange_bp.route('/staff', methods=['PUT'])
def update_staff():
    staffId = request.args.get('id')
    data = request.json
    result = staff.update_one({'_id': ObjectId(staffId)}, {'$set': data})
    return parse_json({'matchedCount': result.matchedCount, 'modifiedCount': result.modifiedCount}), 200

@arrange_bp.route('/staff', methods=['DELETE'])
def delete_staff():
    staffId = request.args.get('id')
    result = staff.delete_one({'_id': ObjectId(staffId)})
    return parse_json({'deletedCount': result.deletedCount}), 200

# Assign endpoints

@arrange_bp.route('/assign', methods=['POST'])
def assign_delivery_tasks():
    hub_id = request.json['hubId']
    hub = hubs.find_one({'_id': ObjectId(hub_id)})
    orders_pending = list(orders.find({'hubId': ObjectId(hub_id), 'status': 'pending'}))
    staff_members = list(staff.find({'hubId': ObjectId(hub_id)}))

    if not hub or not orders_pending or not staff_members:
        return jsonify({'error': 'Invalid data'}), 400

    data = create_data_model(orders_pending, staff_members, hub)
    routes = solve_vrp(data)

    if not routes:
        return jsonify({'error': 'No solution found'}), 400

    assignments = []
    for vehicle_id, route in enumerate(routes):
        staff_member = staff_members[vehicle_id]
        for idx in route[1:]:
            order = orders_pending[idx - 1]
            assignment = {
                'staffId': str(staff_member['_id']),
                'orderId': str(order['_id']),
                'date': datetime.utcnow(),
                'deliverTimes': 0,
                'status': 'pending'
            }
            delivery.insert_one(assignment)
            assignments.append(assignment)

            orders.update_one({'_id': order['_id']}, {'$set': {'status': 'delivering'}})

    return jsonify(parse_json(assignments)), 200

@arrange_bp.route('/transfer/update_status', methods=['POST'])
def update_transfer_status():
    transfer_id = request.json['transferId']
    status = request.json['status']
    transfer = delivery.find_one({'_id': ObjectId(transfer_id)})

    if not transfer:
        return jsonify({'error': 'Transfer not found'}), 400

    if status == 'success':
        delivery.update_one({'_id': ObjectId(transfer_id)}, {'$set': {'status': 'success'}})
        orders.update_one({'_id': ObjectId(transfer['orderId'])}, {'$set': {'status': 'delivered'}})
    elif status == 'failed':
        deliver_times = transfer.get('deliverTimes', 0) + 1
        if deliver_times >= 3:
            delivery.update_one({'_id': ObjectId(transfer_id)}, {'$set': {'status': 'failed'}})
            orders.update_one({'_id': ObjectId(transfer['orderId'])}, {'$set': {'status': 'failed'}})
        else:
            delivery.update_one({'_id': ObjectId(transfer_id)}, {'$set': {'deliverTimes': deliver_times}})

    return jsonify({'status': 'updated'}), 200
