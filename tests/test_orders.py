import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

transport = ASGITransport(app=app)
client = AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio(loop_scope="function")
async def test_create_order():
    product_data = {
        "name": "Order Product",
        "description": "Product for order",
        "price": 50.0,
        "quantity": 100
    }
    create_product_response = await client.post("/api/v1/products/", json=product_data)
    assert create_product_response.status_code == 201
    product_id = create_product_response.json()["id"]

    order_data = {
        "items": [
            {"product_id": product_id, "quantity": 2}
        ]
    }
    response = await client.post("/api/v1/orders/", json=order_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "in_progress"
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product_id
    assert data["items"][0]["quantity"] == 2
    assert "id" in data


@pytest.mark.asyncio(loop_scope="function")
async def test_create_order_with_nonexistent_product():
    order_data = {
        "items": [
            {"product_id": 9999, "quantity": 1}
        ]
    }
    response = await client.post("/api/v1/orders/", json=order_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Product with id 9999 does not exist."


@pytest.mark.asyncio(loop_scope="function")
async def test_create_order_with_insufficient_quantity():
    product_data = {
        "name": "Limited Product",
        "description": "Limited stock",
        "price": 30.0,
        "quantity": 5
    }
    create_product_response = await client.post("/api/v1/products/", json=product_data)
    assert create_product_response.status_code == 201
    product_id = create_product_response.json()["id"]

    order_data = {
        "items": [
            {"product_id": product_id, "quantity": 10}
        ]
    }
    response = await client.post("/api/v1/orders/", json=order_data)
    assert response.status_code == 400
    assert response.json()["detail"] == f"Insufficient quantity for product {product_data['name']}."


@pytest.mark.asyncio(loop_scope="function")
async def test_read_orders():
    product1 = {
        "name": "Product A",
        "description": "Desc A",
        "price": 20.0,
        "quantity": 100
    }
    product2 = {
        "name": "Product B",
        "description": "Desc B",
        "price": 40.0,
        "quantity": 200
    }
    response1 = await client.post("/api/v1/products/", json=product1)
    response2 = await client.post("/api/v1/products/", json=product2)
    assert response1.status_code == 201
    assert response2.status_code == 201
    product_id1 = response1.json()["id"]
    product_id2 = response2.json()["id"]

    orders = [
        {"items": [{"product_id": product_id1, "quantity": 1}]},
        {"items": [{"product_id": product_id2, "quantity": 2}]},
    ]
    for order in orders:
        await client.post("/api/v1/orders/", json=order)

    response = await client.get("/api/v1/orders/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert any(order["items"][0]["product_id"] == product_id1 for order in data)
    assert any(order["items"][0]["product_id"] == product_id2 for order in data)


@pytest.mark.asyncio(loop_scope="function")
async def test_read_order():
    product_data = {
        "name": "Specific Product",
        "description": "Specific description",
        "price": 60.0,
        "quantity": 80
    }
    create_product_response = await client.post("/api/v1/products/", json=product_data)
    assert create_product_response.status_code == 201
    product_id = create_product_response.json()["id"]

    order_data = {
        "items": [{"product_id": product_id, "quantity": 3}]
    }
    create_order_response = await client.post("/api/v1/orders/", json=order_data)
    assert create_order_response.status_code == 201
    order_id = create_order_response.json()["id"]

    response = await client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["status"] == "in_progress"
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product_id
    assert data["items"][0]["quantity"] == 3


@pytest.mark.asyncio(loop_scope="function")
async def test_read_nonexistent_order():
    response = await client.get("/api/v1/orders/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found."


@pytest.mark.asyncio(loop_scope="function")
async def test_update_order_status():
    product_data = {
        "name": "Status Product",
        "description": "For status update",
        "price": 70.0,
        "quantity": 60
    }
    create_product_response = await client.post("/api/v1/products/", json=product_data)
    assert create_product_response.status_code == 201
    product_id = create_product_response.json()["id"]

    order_data = {
        "items": [{"product_id": product_id, "quantity": 2}]
    }
    create_order_response = await client.post("/api/v1/orders/", json=order_data)
    assert create_order_response.status_code == 201
    order_id = create_order_response.json()["id"]

    status_update = {"status": "shipped"}
    response = await client.patch(f"/api/v1/orders/{order_id}/status", json=status_update)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["status"] == "shipped"


@pytest.mark.asyncio(loop_scope="function")
async def test_update_status_nonexistent_order():
    status_update = {"status": "delivered"}
    response = await client.patch("/api/v1/orders/9999/status", json=status_update)
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found."


@pytest.mark.asyncio(loop_scope="function")
async def test_update_order_status_invalid_status():
    product_data = {
        "name": "Invalid Status Product",
        "description": "For invalid status",
        "price": 80.0,
        "quantity": 70
    }
    create_product_response = await client.post("/api/v1/products/", json=product_data)
    assert create_product_response.status_code == 201
    product_id = create_product_response.json()["id"]

    order_data = {
        "items": [{"product_id": product_id, "quantity": 1}]
    }
    create_order_response = await client.post("/api/v1/orders/", json=order_data)
    assert create_order_response.status_code == 201
    order_id = create_order_response.json()["id"]

    invalid_status = {"status": "unknown_status"}
    response = await client.patch(f"/api/v1/orders/{order_id}/status", json=invalid_status)
    assert response.status_code == 422
