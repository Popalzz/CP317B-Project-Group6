"""Suggested Flask route integration for Sprint 2.

This file is intentionally a scaffold. Copy routes into your existing app.py
or convert this into a Flask Blueprint once the team agrees on structure.
"""

# Suggested endpoints to implement:
#
# GET /restaurants/<restaurant_id>/menu
#   -> calls menu_service.get_menu(...)
#
# POST /orders
#   JSON body example:
#   {
#       "customer_id": 1,
#       "restaurant_id": 2,
#       "items": [{"item_id": 4, "quantity": 2}],
#       "delivery_location": {"lat": 43.45, "lon": -80.49}
#   }
#   -> calls order_service.create_order(...)
#
# GET /orders/<order_id>
#   -> calls order_service.get_order(...)
#
# PATCH /orders/<order_id>/status
#   JSON body: {"status": "Preparing"}
#   -> calls status_service.update_order_status(...)
#
# GET /orders/<order_id>/eta
#   -> calls eta_service.get_order_eta(...)

from flask import Blueprint, jsonify, request
from orders.order_service import create_order, get_order
from menus.menu_service import get_menu
from restaurants import get_restaurant_by_id

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