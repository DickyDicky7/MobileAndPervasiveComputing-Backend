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

arrange_bp = Blueprint("arrange",__name__)
CORS(arrange_bp)

# Connect to MongoDB
client = MongoClient(os.environ.get("MONGO_DB"))
maps_key      = os.environ.get("GOOGLE_MAP_API")
geocoding_key = os.environ.get("GEO_CODING_API") 

db = client.lift
CORS(arrange_bp)


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
            if 'orderId' in item:
                if '$oid' in item.get('orderId', {}):
                    item['orderId'] = str(item['orderId']["$oid"])
            if 'staffId' in item:
                if '$oid' in item.get('staffId', {}):
                    item['staffId'] = str(item['staffId']["$oid"])
            if 'userId' in item:
                if '$oid' in item.get('userId', {}):
                    item['userId'] = str(item['userId']["$oid"])
            if 'senderId' in item:
                if '$oid' in item.get('senderId', {}):
                    item['senderId'] = str(item['senderId']["$oid"])
            if 'receiverId' in item:
                if '$oid' in item.get('receiverId', {}):
                    item['receiverId'] = str(item['receiverId']["$oid"])
            if '_id' in item:
                item['_id'] = str(item['_id']["$oid"])
            if 'insertedId' in item:
                item['insertedId'] = str(item['insertedId']["$oid"])
            if 'deliveryInfo' in item: item['deliveryInfo'] = parse_json(item['deliveryInfo'])
            if 'receiverInfo' in item: item['receiverInfo'] = parse_json(item['receiverInfo'])
            if 'senderInfo' in item: item['senderInfo'] = parse_json(item['senderInfo'])
                
    else:
        if 'hubId' in data:
            data['hubId'] = str(data['hubId']["$oid"])
        if 'orderId' in data:
            data['orderId'] = str(data['orderId']["$oid"])
        if 'staffId' in data:
            data['staffId'] = str(data['staffId']["$oid"])
        if 'userId' in data:
            data['userId'] = str(data['userId']["$oid"])
        if 'senderId' in data:
            data['senderId'] = str(data['senderId']["$oid"])
        if 'receiverId' in data:
            data['receiverId'] = str(data['receiverId']["$oid"])
        if '_id' in data:
                data['_id'] = str(data['_id']["$oid"])
        if 'insertedId' in data:
                data['insertedId'] = str(data['insertedId']["$oid"])
        if 'deliveryInfo' in data: data['deliveryInfo'] = parse_json(data['deliveryInfo'])
        if 'receiverInfo' in data: data['receiverInfo'] = parse_json(data['receiverInfo'])
        if 'senderInfo' in data: data['senderInfo'] = parse_json(data['senderInfo'])
    return data


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


@arrange_bp.route('/checkgeo', methods=['GET'])
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

# Use OR-Tools to calculate the optimal routes
def create_data_model(orders, staff, hub):
    data = {}
    hub_lat, hub_lon = geocode_address(hub['address'])
    data['distance_matrix'] = []
    all_locations = [(hub_lat, hub_lon)] + [geocode_address(order['receiverInfo']['address']) for order in orders]
    for loc1 in all_locations:
        distances = []
        for loc2 in all_locations:
            distances.append(calculate_distance(float(loc1[0]), float(loc1[1]), float(loc2[0]), float(loc2[1]))) # lat = 0, lon  =1
        data['distance_matrix'].append(distances)
    data['num_vehicles'] = len(staff)
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
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # không có khoảng trống
        300000,  # khoảng cách tối đa của phương tiện
        True,  # bắt đầu từ số 0
        dimension_name)
    
    # def cost_callback(from_index, to_index, vehicle_index):
        # from_node = manager.IndexToNode(from_index)
        # to_node = manager.IndexToNode(to_index)
        # distance = data['distance_matrix'][from_node][to_node]
        # return distance * data['vehicle_costs'][vehicle_index]

    # cost_callback_index = routing.RegisterTransitCallback(cost_callback)
    # routing.SetFixedCostOfAllVehicles(cost_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    # search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    # search_parameters.time_limit.seconds = 30


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



def get_delivery_detail(deliveries_list):
    result = []

    for delivery in deliveries_list:
        hub_id = str(delivery["hubId"])
        staff_id = str(delivery["staffId"])

        # Query hub name
        hub = hubs.find_one({"_id": ObjectId(hub_id)})
        hub_name = hub["name"] if hub else "Unknown"

        # Query staff name
        staff = staffs.find_one({"_id": ObjectId(staff_id)})
        staff_name = staff["name"] if staff else "Unknown"

        # Append delivery details with computed data
        result.append({
            "deliveryId": str(delivery["_id"]),
            "hubId": hub_id,
            "hubName": hub_name,
            "staffId": staff_id,
            "staffName": staff_name,
            "orderId": str(delivery["orderId"]),
            "date": delivery["date"],
            "deliverTimes": delivery["deliverTimes"],
            "status": delivery["status"]
        })

    return result
# Assign endpoints

@arrange_bp.route('/assign', methods=['POST'])
@cross_origin()
def assign_delivery_tasks():
    hub_id = request.json['hubId']
    hub    =    hubs.find_one({'_id': ObjectId(hub_id)})
    orders_pending = list(orders.find({'hubId': ObjectId(hub_id), 'deliveryInfo.status': 'pending'}))
    staff_members  = list(staffs.find({'hubId': ObjectId(hub_id),                                 }))

    if not hub or not orders_pending or not staff_members:
        return jsonify({'error': 'Step 1 wrong'}), 400

    data   = create_data_model(orders_pending, staff_members, hub)
    # print(data)
    
    routes = solve_vrp(data)
    print(routes)
    
    if not routes:
        return jsonify({'error': 'Step 2 wrong'}), 400

    assignments = []
    for vehicle_id, route in enumerate(routes):
        staff_member = staff_members[vehicle_id]
        for idx in  route[1:]:
            order      = orders_pending[idx - 1]
            assignment = {
                'staffId': ObjectId(str(staff_member['_id'])),
                'orderId': ObjectId(str(       order['_id'])),
                  'hubId': ObjectId(str(hub_id             )),
                'date' : datetime.today().strftime("%d-%m-%Y"),
                'deliverTimes':         0,
                      'status': 'pending',
            }
            deliveries .insert_one(assignment)
            assignments.append    (assignment)

            # orders.update_one({'_id': order['_id']}, {'$set': {'deliveryInfo.status': 'inProgress'}})

    return jsonify(parse_json(assignments)), 200

## Update status of order, max 3 times failed

@arrange_bp.route('/delivery/update_status', methods=['POST'])
@cross_origin()
def update_delivery_status():
    delivery_id = request.json['deliveryId']
    status      = request.json[  'status'  ]
    delivery    = deliveries.find_one({'_id': ObjectId(delivery_id)})

    if not delivery:
        return jsonify({'error': 'delivery not found'}), 400

    deliver_times = delivery.get('deliverTimes', 0)
    if   status == 'success'       :
        deliveries.update_one({'_id': ObjectId(delivery_id        )}, {'$set': {             'status': 'success'}})
        orders    .update_one({'_id': ObjectId(delivery['orderId'])}, {'$set': {'deliveryInfo.status': 'success'}})
    elif status ==         'failed':
        deliver_times = delivery.get('deliverTimes', 0) + 1
        if deliver_times >= 3:
            deliveries.update_one({'_id': ObjectId(delivery_id        )}, {'$set': {             'status': 'failed'}})
            orders    .update_one({'_id': ObjectId(delivery['orderId'])}, {'$set': {'deliveryInfo.status': 'failed'}})
        else:
            deliveries.update_one({'_id': ObjectId(delivery_id)}, {'$set': {'deliverTimes': deliver_times}})
    else:
        deliveries.update_one({'_id': ObjectId(delivery_id        )}, {'$set': {             'status': status}})
#       orders    .update_one({'_id': ObjectId(delivery['orderId'])}, {'$set': {'deliveryInfo.status': status}})

    return jsonify({'status': 'updated', 'deliverTimes': deliver_times}), 200

## Get delivery by id

@arrange_bp.route('/delivery/id', methods=['GET'])
@cross_origin()
def get_delivery_by_id():
    delivery_id = request.args.get('deliveryId')
    if not delivery_id:
        return jsonify({"error": "delivery_id parameter is required"}), 400
    
    deliveries_list = deliveries.find({"_id": ObjectId(delivery_id)})
    return parse_json(deliveries_list), 200

## Get all delivery
@arrange_bp.route('/deliveries', methods=['GET'])
@cross_origin()
def get_all_deliveries():
    all_orders = deliveries.find()
    return parse_json(all_orders), 200

@arrange_bp.route('/deliveries/status', methods=['GET'])
@cross_origin()
def get_deliveries_by_status():
    status = request.args.get('status')
    if not status:
        return jsonify({"error": "status parameter is required"}), 400

    valid_statuses = ["pending", "inProgress", "success", "failed", "canceled"]
    if status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}"}), 400

    deliveries_list = deliveries.find({"status": status})
    res = get_delivery_detail(parse_json(deliveries_list))
    return parse_json(res), 200

## Get all delivery matches with hubId
@arrange_bp.route('/deliveries/hub', methods=['GET'])
@cross_origin()
def get_deliveries_by_hub_id():
    hub_id = request.args.get('hubId')
    if not hub_id:
        return jsonify({"error": "hub_id parameter is required"}), 400
    
    delivery_list = deliveries.find({"hubId": ObjectId(hub_id)})
    order_list = []
    for order in delivery_list:
        order_list.append(order)
    return parse_json( {'list': parse_json(order_list) , 'count': len(order_list)}), 200

@arrange_bp.route('/deliveries/status/hub', methods=['GET'])
@cross_origin()
def get_deliveries_by_status_by_hub_id():
    status = request.args.get('status')
    hub_id = request.args.get('hubId')
    if not hub_id:
        return jsonify({"error": "hub_id parameter is required"}), 400
    if not status:
        return jsonify({"error": "status parameter is required"}), 400

    valid_statuses = ["pending", "inProgress", "success", "failed", "canceled"]
    if status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}"}), 400

    deliveries_list = deliveries.find({
        "$and": [
            {"hubId": ObjectId(hub_id)},
            {"status": status}
        ]
    })

    res = get_delivery_detail(parse_json(deliveries_list))
    return parse_json(res), 200


## Get all delivery matches with staffId
@arrange_bp.route('/deliveries/staff', methods=['GET'])
@cross_origin()
def get_deliveries_by_staffId():
    staff_id = request.args.get('staffId')
    if not staff_id:
        return jsonify({"error": "staff_id parameter is required"}), 400
    
    delivery_list = deliveries.find({"staffId": ObjectId(staff_id)})
    order_list = []
    for order in delivery_list:
        order_list.append(order)
    return parse_json( {'list': parse_json(order_list) , 'count': len(order_list)}), 200

#  Get deliveries by number rows
@arrange_bp.route('/delivery/row', methods=['GET'])
@cross_origin()
def get_deliveries_by_row_num():
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 8

    res = list(
            deliveries.find()
            .skip(number_row)
            .limit(limit)
        )

    return parse_json(res), 200

# Search user and display from number rows
@arrange_bp.route('/delivery/search', methods=['GET'])
@cross_origin()
def search_delivery_by_row_num():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 8

    query = {
                "$or": 
                [
                    {"status": {"$regex": search_str, "$options": "i"}},
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})

    res = list(
            deliveries.find(query)
            .skip(number_row)
            .limit(limit)
        )

    return parse_json(res), 200

# Count all hub
@arrange_bp.route('/deliveries/count', methods=['GET'])
@cross_origin()
def count_hub():
    res = deliveries.count_documents({})
    return jsonify({"count": res}), 200

# Count hub and display from number rows
@arrange_bp.route('/delivery/search/count', methods=['GET'])
@cross_origin()
def count_delivery_by_row_num():
    search_str = request.args.get('search', default='', type=str)
    number_row = request.args.get('numberRowIgnore', default=0, type=int)
    limit = 8

    query = {
                "$or": 
                [
                    {"status": {"$regex": search_str, "$options": "i"}},
                ]
            }
    if ObjectId.is_valid(search_str):
        query["$or"].append({"_id": ObjectId(search_str)})

    res = list(
            deliveries.find(query)
            .skip(number_row)
            .limit(limit)
        ).count()

    return jsonify({"count": res}), 200
