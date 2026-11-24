from orders.status_service import is_valid_transition


def test_pending_to_accepted():
    assert is_valid_transition("Pending", "Accepted") is True


def test_accepted_to_preparing():
    assert is_valid_transition("Accepted", "Preparing") is True


def test_preparing_to_ready():
    assert is_valid_transition("Preparing", "Ready") is True


def test_cannot_skip_status():
    assert is_valid_transition("Pending", "Ready") is False


def test_cannot_move_backwards():
    assert is_valid_transition("Preparing", "Accepted") is False


def test_same_status_not_allowed():
    assert is_valid_transition("Accepted", "Accepted") is False


def test_invalid_status():
    assert is_valid_transition("Pending", "Flying") is False
