import pytest

from app import app
from orders.order_service import orders


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        orders.clear()
        yield client


def place_order(client):
    response = client.post(
        "/orders",
        json={
            "customer_id": 1,
            "restaurant_id": 1,
            "items": [{"item_id": 1, "quantity": 1}],
            "delivery_location": {
                "latitude": 43.4643,
                "longitude": -80.5204,
            },
        },
    )
    return response.get_json()["order_id"]


def set_status(client, order_id, status):
    return client.patch(f"/orders/{order_id}/status", json={"status": status})


def make_ready(client):
    order_id = place_order(client)
    for status in ["Accepted", "Preparing", "Ready"]:
        assert set_status(client, order_id, status).status_code == 200
    return order_id


def test_available_deliveries_empty_when_nothing_ready(client):
    place_order(client)  # still Pending

    response = client.get("/deliveries/available")

    assert response.status_code == 200
    assert response.get_json()["deliveries"] == []


def test_available_deliveries_lists_ready_orders(client):
    order_id = make_ready(client)

    deliveries = client.get("/deliveries/available").get_json()["deliveries"]

    assert len(deliveries) == 1
    assert deliveries[0]["order_id"] == order_id
    assert deliveries[0]["restaurant_name"] == "Pizza Palace"
    assert "delivery_distance_km" in deliveries[0]


def test_available_deliveries_hide_customer_details(client):
    # NFR-2 / DRV-1: drivers must not see the customer's address or id
    # until they accept the delivery.
    make_ready(client)

    delivery = client.get("/deliveries/available").get_json()["deliveries"][0]

    assert "delivery_location" not in delivery
    assert "customer_id" not in delivery


def test_accept_delivery_assigns_driver(client):
    order_id = make_ready(client)

    response = client.post(
        f"/orders/{order_id}/accept-delivery", json={"driver_id": 1}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["driver_id"] == 1
    assert data["delivery_status"] == "Assigned"
    # The full order, including the address, is returned after accepting.
    assert "delivery_location" in data

    # No longer available to other drivers.
    deliveries = client.get("/deliveries/available").get_json()["deliveries"]
    assert deliveries == []


def test_second_driver_cannot_accept_same_delivery(client):
    order_id = make_ready(client)

    client.post(f"/orders/{order_id}/accept-delivery", json={"driver_id": 1})
    response = client.post(
        f"/orders/{order_id}/accept-delivery", json={"driver_id": 2}
    )

    assert response.status_code == 409


def test_cannot_accept_order_that_is_not_ready(client):
    order_id = place_order(client)  # Pending

    response = client.post(
        f"/orders/{order_id}/accept-delivery", json={"driver_id": 1}
    )

    assert response.status_code == 409


def test_accept_delivery_rejects_invalid_driver_id(client):
    order_id = make_ready(client)

    response = client.post(
        f"/orders/{order_id}/accept-delivery", json={"driver_id": 0}
    )

    assert response.status_code == 400


def test_accept_delivery_missing_order(client):
    response = client.post(
        "/orders/999/accept-delivery", json={"driver_id": 1}
    )

    assert response.status_code == 404


def test_full_delivery_flow_reaches_delivered(client):
    order_id = make_ready(client)

    client.post(f"/orders/{order_id}/accept-delivery", json={"driver_id": 1})

    assert set_status(client, order_id, "On the way").status_code == 200
    response = set_status(client, order_id, "Delivered")

    assert response.status_code == 200
    assert response.get_json()["status"] == "Delivered"


def test_eta_route_returns_estimate(client):
    order_id = place_order(client)

    response = client.get(f"/orders/{order_id}/eta")

    assert response.status_code == 200
    data = response.get_json()
    assert data["order_id"] == order_id
    assert data["eta_minutes"] > 0
    assert "driver_location" not in data


def test_eta_route_missing_order(client):
    response = client.get("/orders/999/eta")

    assert response.status_code == 404