import pytest

from orders.eta_service import (
    DEFAULT_PREP_MINUTES,
    estimate_delivery_minutes,
    estimate_travel_minutes,
    get_order_eta,
)
from orders.order_service import create_order, orders


def setup_function():
    orders.clear()


def make_order(latitude, longitude):
    return create_order(
        customer_id=1,
        restaurant_id=1,
        items=[{"item_id": 1, "quantity": 1}],
        delivery_location={
            "latitude": latitude,
            "longitude": longitude
        }
    )


def test_adds_prep_and_travel():
    assert estimate_delivery_minutes(10, 5) == 15


def test_rounds_up():
    assert estimate_delivery_minutes(10, 4.2) == 15


def test_zero_minutes():
    assert estimate_delivery_minutes(0, 0) == 0


def test_negative_time_rejected():
    with pytest.raises(ValueError):
        estimate_delivery_minutes(-1, 5)

    with pytest.raises(ValueError):
        estimate_delivery_minutes(5, -1)


def test_non_number_rejected():
    with pytest.raises(ValueError):
        estimate_delivery_minutes("10", 5)


def test_travel_minutes():
    # 40 km at 40 km/h is one hour
    assert estimate_travel_minutes(40) == 60


def test_eta_same_location_is_prep_time():
    # Customer is at the restaurant, so there is no travel time
    order = make_order(43.4643, -80.5204)

    eta = get_order_eta(order["order_id"])

    assert eta["distance_km"] == 0
    assert eta["eta_minutes"] == DEFAULT_PREP_MINUTES


def test_eta_farther_order_takes_longer():
    near = make_order(43.4643, -80.5204)
    far = make_order(43.3681, -80.4925)

    near_eta = get_order_eta(near["order_id"])
    far_eta = get_order_eta(far["order_id"])

    assert far_eta["eta_minutes"] > near_eta["eta_minutes"]


def test_eta_has_no_driver_location():
    order = make_order(43.4643, -80.5204)

    eta = get_order_eta(order["order_id"])

    assert "driver_location" not in eta
    assert "latitude" not in eta
    assert "longitude" not in eta


def test_eta_missing_order():
    assert get_order_eta(999) is None
