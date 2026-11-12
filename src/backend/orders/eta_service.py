"""ORD-2 delivery estimate scaffold.

Omar, with frontend display by Ervin.
"""


def estimate_delivery_minutes(preparation_minutes: float, travel_minutes: float) -> int:
    """Return a simple estimated delivery time in minutes.

    Sprint 2 can begin with a deterministic estimate. A real maps/routing API
    can be integrated later if the team has time.

    TODO:
    - Validate both values are >= 0.
    - Combine prep and travel time.
    - Decide rounding behavior.
    """
    raise NotImplementedError


def get_order_eta(order_id):
    """Return ETA information for an existing order.

    TODO:
    - Load order and restaurant preparation estimate.
    - Determine travel estimate (mock value or routing provider for Sprint 2).
    - Return ETA without exposing a precise live driver location.
    """
    raise NotImplementedError
