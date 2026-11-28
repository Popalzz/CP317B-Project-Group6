"""Flask routes for menus, orders, order status and driver deliveries.

Routes:
  GET   /restaurants/<id>/menu         menu items for a restaurant
  GET   /restaurants/<id>/orders       all orders for a restaurant
  POST  /orders                        place an order
  GET   /orders/<id>                   fetch one order
  PATCH /orders/<id>/status            move an order to the next status
  GET   /deliveries/available          Ready orders with no driver (no customer address)
  POST  /orders/<id>/accept-delivery   assign a driver, body {"driver_id": <int>}

POST /orders body:
  {
    "customer_id": 1,
    "restaurant_id": 2,
    "items": [{"item_id": 4, "quantity": 2}],
    "delivery_location": {"latitude": 43.45, "longitude": -80.49}
  }

Not implemented yet: GET /orders/<id>/eta (eta_service.py exists but isn't wired in).
"""

from flask import Blueprint, jsonify, request
from orders.order_service import create_order, get_order, get_orders_for_restaurant, get_available_deliveries, accept_delivery
from menus.menu_service import get_menu
from restaurants import get_restaurant_by_id
from orders.status_service import update_order_status
from distance_utils import calculate_dist
from orders.eta_service import get_order_eta

order_bp = Blueprint("orders", __name__)


@order_bp.route("/orders", methods=["POST"])
def place_order():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing request body"}), 400

    customer_id = data.get("customer_id")
    restaurant_id = data.get("restaurant_id")
    items = data.get("items")
    delivery_location = data.get("delivery_location")

    order = create_order(
        customer_id,
        restaurant_id,
        items,
        delivery_location
    )

    if order is None:
        return jsonify({"error": "Invalid order"}), 400

    return jsonify(order), 201


@order_bp.route("/orders/<int:order_id>", methods=["GET"])
def fetch_order(order_id):
    order = get_order(order_id)

    if order is None:
        return jsonify({"error": "Order not found"}), 404

    return jsonify(order), 200

@order_bp.route("/restaurants/<int:restaurant_id>/menu", methods=["GET"])
def fetch_menu(restaurant_id):
    restaurant = get_restaurant_by_id(restaurant_id)

    if restaurant is None:
        return jsonify({"error": "Restaurant not found"}), 404

    menu = get_menu(restaurant_id)

    if menu is None:
        return jsonify({"error": "Menu not found"}), 404

    items = []

    for item_id, item in menu.items():
        items.append({
            "id": item_id,
            "name": item["name"],
            "price": item["price"],
            "available": item["available"]
        })

    return jsonify({
        "restaurant": {
            "id": restaurant_id,
            "name": restaurant["name"]
        },
        "items": items
    }), 200

@order_bp.route("/orders/<int:order_id>/status", methods=["PATCH"])
def change_order_status(order_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing request body"}), 400

    new_status = data.get("status")

    if not new_status:
        return jsonify({"error": "Missing status"}), 400

    updated_order = update_order_status(order_id, new_status)

    if updated_order is None:
        return jsonify({"error": "Invalid status update"}), 400

    return jsonify(updated_order), 200

@order_bp.route("/restaurants/<int:restaurant_id>/orders", methods=["GET"])
def fetch_restaurant_orders(restaurant_id):
    restaurant = get_restaurant_by_id(restaurant_id)

    if restaurant is None:
        return jsonify({"error": "Restaurant not found"}), 404

    restaurant_orders = get_orders_for_restaurant(restaurant_id)

    return jsonify({
        "restaurant": {
            "id": restaurant_id,
            "name": restaurant["name"]
        },
        "orders": restaurant_orders
    }), 200

@order_bp.route("/deliveries/available", methods=["GET"])
def fetch_available_deliveries():
    deliveries = []

    for order in get_available_deliveries():
        restaurant = get_restaurant_by_id(order["restaurant_id"])
        location = order["delivery_location"]

        distance = None
        if restaurant:
            distance = round(calculate_dist(
                restaurant["latitude"], restaurant["longitude"],
                location["latitude"], location["longitude"],
            ), 1)

        # Deliberately leaves out delivery_location and customer_id.
        # The full order is only returned once a driver accepts it.
        deliveries.append({
            "order_id": order["order_id"],
            "restaurant_id": order["restaurant_id"],
            "restaurant_name": restaurant["name"] if restaurant else None,
            "delivery_distance_km": distance,
            "items": order["items"],
            "status": order["status"],
        })

    return jsonify({"deliveries": deliveries}), 200


@order_bp.route("/orders/<int:order_id>/accept-delivery", methods=["POST"])
def accept_order_delivery(order_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Missing or invalid request body"}), 400

    driver_id = data.get("driver_id")

    if type(driver_id) is not int or driver_id < 1:
        return jsonify({"error": "Invalid driver ID"}), 400

    if get_order(order_id) is None:
        return jsonify({"error": "Order not found"}), 404

    updated_order = accept_delivery(order_id, driver_id)

    if updated_order is None:
        return jsonify({"error": "Delivery is not available"}), 409

    return jsonify(updated_order), 200

@order_bp.route("/orders/<int:order_id>/eta", methods=["GET"])
def fetch_order_eta(order_id):
    eta = get_order_eta(order_id)

    if eta is None:
        return jsonify({"error": "ETA not available"}), 404

    return jsonify(eta), 200