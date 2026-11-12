"""ORD-1 order placement service scaffold.
"""
from app import calculate_dist


def calculate_order_total(items: list) -> float:
    """Calculate the order subtotal from validated line items.

    Each item should contain a unit price and quantity.

    TODO:
    - Reject invalid/negative quantities.
    - Avoid trusting a client-supplied total.
    - Decide how taxes/delivery fees are handled for this sprint.
    """
    

    raise NotImplementedError



def validate_order(restaurant_id: int, items: list, delivery_location: dict):
    """Validate an order before it is created.

    TODO:
    - Require at least one item.
    - Confirm all items belong to the chosen restaurant.
    - Confirm requested items are available.
    - Re-check the 35 km delivery rule using existing distance logic.
    - Return a useful validation result/errors.
    """

    if restaurant_id == None:
            return False
    
    if items == None:
            return False
    
    for item in items:
        if item > 10:
            return False

    dist = calculate_dist(delivery_location.lat ,delivery_location.lon, )

    raise NotImplementedError


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

    

    raise NotImplementedError


def get_order(order_id):
    """Return order details by ID.

    TODO:
    - Load order.
    - Later add authorization so customers only see their own orders and
      restaurant staff only see orders for their restaurant.
    """
    raise NotImplementedError
