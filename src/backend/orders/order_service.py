"""ORD-1 order placement service scaffold.
"""
from distance_utils import calculate_dist
from restaurants import get_restaurant_by_id
from menus.menu_service import get_menu, get_menu_item

orders = {

}


def calculate_order_total(restaurant_id: int,items: list) -> float | None:
    """Calculate the order subtotal from validated line items.

    Each item should contain a unit price and quantity.

    TODO:
    - Reject invalid/negative quantities.
    - Avoid trusting a client-supplied total.
    - Decide how taxes/delivery fees are handled for this sprint.
    """
    total = 0

    for order_item in items:
        if not isinstance(order_item, dict):
            return None
        item_id = order_item.get("item_id")
        quantity = order_item.get("quantity")

        if not isinstance(item_id, int) or item_id < 1:
            return None

        if not isinstance(quantity, int) or quantity < 1:
            return None

        item = get_menu_item(restaurant_id, item_id)

        if not item:
            return None

        price = item.get("price")

        if not isinstance(price, (int, float)):
            return None

        total = total + (price * quantity)
    
    return total






def validate_order(restaurant_id: int, items: list, delivery_location: dict):
    """Validate an order before it is created.

    TODO:
    - Require at least one item.
    - Confirm all items belong to the chosen restaurant.
    - Confirm requested items are available.
    - Re-check the 35 km delivery rule using existing distance logic.
    - Return a useful validation result/errors.
    """

    if restaurant_id is None:
        return False
    rest = get_restaurant_by_id(restaurant_id)

    if not rest:
        return False
    
    if items == None or not items:
        return False

    if delivery_location is None:
        return False

    if not isinstance(delivery_location, dict):
        return False

    latitude = delivery_location.get("latitude")
    longitude = delivery_location.get("longitude")

    if latitude is None or longitude is None:
        return False

    if not isinstance(latitude, (int, float)):
        return False

    if not isinstance(longitude, (int, float)):
        return False

    if latitude < -90 or latitude > 90:
        return False

    if longitude < -180 or longitude > 180:
        return False

    dist = calculate_dist(latitude, longitude, rest["latitude"], rest["longitude"])

    if dist > 35:
        return False

    rest_menu = get_menu(restaurant_id)

    if rest_menu is None:
        return False

    if not isinstance(items, list) or not items:
        return False
    
    for item in items:
        if not isinstance(item, dict):
            return False
        item_id = item.get("item_id")
        quantity = item.get("quantity")

        if not isinstance(item_id, int) or item_id < 1:
            return False

        if not isinstance(quantity, int) or quantity < 1:
            return False

        menu_item = get_menu_item(restaurant_id, item_id)

        if not menu_item:
            return False

        if not menu_item["available"]:
            return False

    return True




def create_order(customer_id, restaurant_id: int, items: list, delivery_location: dict):
    """Create and persist a new order after validation.

    Suggested initial status: 'Accepted' or 'Pending' (team should choose one).

    TODO:
    - Call validate_order.
    - Calculate totals server-side.
    - Generate unique order ID.
    - Store only the payment outcome/reference if payment is mocked.
    - Persist order and return confirmation data.
    """

    valid = validate_order(restaurant_id, items, delivery_location)

    if not valid:
        return None

    total = calculate_order_total(restaurant_id, items)

    if total is None:
        return None

    if not orders:
        new_ord_id = 1
    else:
        new_ord_id = max(orders) + 1

    new_order = {
        "order_id": new_ord_id,
        "customer_id": customer_id,
        "restaurant_id": restaurant_id,
        "items": items,
        "delivery_location": delivery_location,
        "total": total,
        "status": "Pending",
        "driver_id": None,
        "delivery_status": "Unassigned"
    }

    orders[new_ord_id] = new_order
    
    return new_order

    
    
def get_orders_for_restaurant(restaurant_id):

    rest_ord = []
    for ord in orders.values():
        if ord["restaurant_id"] == restaurant_id:
            rest_ord.append(ord)

    return rest_ord
    



def get_order(order_id):
    """Return order details by ID.

    TODO:
    - Load order.
    - Later add authorization so customers only see their own orders and
      restaurant staff only see orders for their restaurant.
    """

    if not isinstance(order_id, int) or order_id < 1:
        return None

    order = orders.get(order_id)

    if order is None:
        return None

    return order

def get_available_deliveries():
    deliveries = []

    for order in orders.values():
        if order["status"] == "Ready" and order["driver_id"] is None:
            deliveries.append(order)
    return deliveries

def accept_delivery(order_id, driver_id):
    order = get_order(order_id)

    if order is None:
        return None

    if type(driver_id) is not int or driver_id < 1:
        return None

    if order["status"] != "Ready":
        return None
    if order["driver_id"] is not None:
        return None

    order["driver_id"] = driver_id
    order["delivery_status"] = "Assigned"

    return order