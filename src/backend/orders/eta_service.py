"""ORD-2 delivery estimate service.

Omar, with frontend display by Ervin.
"""
import math

from distance_utils import calculate_dist
from restaurants import get_restaurant_by_id
from orders.order_service import get_order


DEFAULT_PREP_MINUTES = 15
AVERAGE_SPEED_KMH = 40


def estimate_delivery_minutes(preparation_minutes: float, travel_minutes: float) -> int:
    """return estimated delivery time in minutes.

    Prep time and travel time are added together and rounded up
    
    customer is never told the food will arrive sooner than it really will.
    """

    for value in (preparation_minutes, travel_minutes):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("Times must be numbers")

        if not math.isfinite(value) or value < 0:
            raise ValueError("Times must be 0 or more")

    return math.ceil(preparation_minutes + travel_minutes)


def estimate_travel_minutes(distance_km: float) -> float:
    """Convert a distance into travel minutes using the average speed."""
    return distance_km / AVERAGE_SPEED_KMH * 60


def get_order_eta(order_id):
    """rturn ETA information for an existing order.

    uses the ditance between the restaurant and the customers delivery
    location. 
    
    The drivers live location is never returned, so customers
    only see an estimate.
    """
    order = get_order(order_id)

    if order is None:
        return None

    restaurant = get_restaurant_by_id(order["restaurant_id"])

    if restaurant is None:
        return None

    location = order["delivery_location"]

    distance = calculate_dist(
        restaurant["latitude"],
        restaurant["longitude"],
        location["latitude"],
        location["longitude"]
    )

    travel_minutes = estimate_travel_minutes(distance)
    eta_minutes = estimate_delivery_minutes(DEFAULT_PREP_MINUTES, travel_minutes)

    return {
        "order_id": order["order_id"],
        "status": order["status"],
        "distance_km": round(distance, 1),
        "prep_minutes": DEFAULT_PREP_MINUTES,
        "travel_minutes": math.ceil(travel_minutes),
        "eta_minutes": eta_minutes
    }
