from orders.order_service import (
    create_order,
    get_order,
    get_orders_for_restaurant,
    orders,
)


def setup_function():
    orders.clear()


def test_create_valid_order():
    order = create_order(
        customer_id=1,
        restaurant_id=1,
        items=[
            {
                "item_id": 1,
                "quantity": 1
            }
        ],
        delivery_location={
            "latitude": 43.4643,
            "longitude": -80.5204
        }
    )

    assert order is not None
    assert order["order_id"] == 1
    assert order["status"] == "Pending"
    assert order["restaurant_id"] == 1


def test_invalid_item():
    order = create_order(
        customer_id=1,
        restaurant_id=1,
        items=[
            {
                "item_id": 999,
                "quantity": 1
            }
        ],
        delivery_location={
            "latitude": 43.4643,
            "longitude": -80.5204
        }
    )

    assert order is None


def test_invalid_quantity():
    order = create_order(
        customer_id=1,
        restaurant_id=1,
        items=[
            {
                "item_id": 1,
                "quantity": 0
            }
        ],
        delivery_location={
            "latitude": 43.4643,
            "longitude": -80.5204
        }
    )

    assert order is None


def test_get_missing_order():
    assert get_order(999) is None


def test_get_orders_for_restaurant():
    create_order(
        customer_id=1,
        restaurant_id=1,
        items=[{"item_id": 1, "quantity": 1}],
        delivery_location={
            "latitude": 43.4643,
            "longitude": -80.5204
        }
    )

    restaurant_orders = get_orders_for_restaurant(1)

    assert len(restaurant_orders) == 1
    assert restaurant_orders[0]["restaurant_id"] == 1
