"""REST-1 order status service scaffold.

Owner suggestion: Omar.
"""

ALLOWED_STATUSES = ["Accepted", "Preparing", "Ready", "On the way", "Delivered"]


def is_valid_transition(current_status: str, new_status: str) -> bool:
    """Return True only for a valid forward status transition.

    TODO:
    - Reject unknown statuses.
    - Decide whether skipping stages is allowed.
    - Decide whether any status can move backwards.
    """
    raise NotImplementedError


def update_order_status(order_id, new_status: str, actor_id=None):
    """Update one order's status.

    TODO:
    - Load the order.
    - Verify the actor is allowed to update it.
    - Validate the transition.
    - Save the new status and timestamp.
    - Return the updated order/status.
    """
    raise NotImplementedError
