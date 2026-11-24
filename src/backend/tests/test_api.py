import pytest

from app import app
from orders.order_service import orders


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        orders.clear()
        yield client


def test_get_restaurants(client):
    response = client.get(
        "/restaurants?lat=43.4643&lon=-80.5204"
    )

    assert response.status_code == 200


def test_create_order(client):
    response = client.post(
        "/orders",
        json={
            "customer_id": 1,
            "restaurant_id": 1,
            "items": [
                {
                    "item_id": 1,
                    "quantity": 1
                }
            ],
            "delivery_location": {
                "latitude": 43.4643,
                "longitude": -80.5204
            }
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["status"] == "Pending"
    assert data["total"] == 14.99


def test_create_invalid_order(client):
    response = client.post(
        "/orders",
        json={
            "customer_id": 1,
            "restaurant_id": 1,
            "items": [
                {
                    "item_id": 999,
                    "quantity": 1
                }
            ],
            "delivery_location": {
                "latitude": 43.4643,
                "longitude": -80.5204
            }
        }
    )

    assert response.status_code == 400


def test_missing_order(client):
    response = client.get("/orders/999")

    assert response.status_code == 404


def test_update_order_status(client):
    create_response = client.post(
        "/orders",
        json={
            "customer_id": 1,
            "restaurant_id": 1,
            "items": [
                {
                    "item_id": 1,
                    "quantity": 1
                }
            ],
            "delivery_location": {
                "latitude": 43.4643,
                "longitude": -80.5204
            }
        }
    )

    order_id = create_response.get_json()["order_id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json={
            "status": "Accepted"
        }
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "Accepted"


def test_invalid_status_transition(client):
    create_response = client.post(
        "/orders",
        json={
            "customer_id": 1,
            "restaurant_id": 1,
            "items": [{"item_id": 1, "quantity": 1}],
            "delivery_location": {
                "latitude": 43.4643,
                "longitude": -80.5204
            }
        }
    )

    order_id = create_response.get_json()["order_id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json={
            "status": "Delivered"
        }
    )

    assert response.status_code == 400
