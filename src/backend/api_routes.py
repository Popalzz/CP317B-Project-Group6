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
