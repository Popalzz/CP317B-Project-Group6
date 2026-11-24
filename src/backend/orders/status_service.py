"""REST-1 order status service scaffold.

Owner suggestion: Omar.
"""

from orders.order_service import get_order

ALLOWED_STATUSES = [
    "Pending",
    "Accepted",
    "Preparing",
    "Ready",
    "On the way",
    "Delivered"
]


def is_valid_transition(current_status: str, new_status: str) -> bool:
    """Return True only for a valid forward status transition.

    TODO:
    - Reject unknown statuses.
    - Decide whether skipping stages is allowed.
    - Decide whether any status can move backwards.
    """
    if current_status not in ALLOWED_STATUSES:
        return False

    if new_status not in ALLOWED_STATUSES:
        return False

    old_index = ALLOWED_STATUSES.index(current_status)
    new_index = ALLOWED_STATUSES.index(new_status)

    if new_index == old_index + 1:
        return True
    return False


def update_order_status(order_id, new_status: str, actor_id=None):
    """Update one order's status.

    TODO:
    - Load the order.
    - Verify the actor is allowed to update it.
    - Validate the transition.
    - Save the new status and timestamp.
    - Return the updated order/status.
    """

    order = get_order(order_id)

    if order is None:
        return None

    status = order.get("status")

    valid = is_valid_transition(status,new_status)

    if not valid:
        return None

    order["status"] = new_status

    return order