import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

transport = ASGITransport(app=app)
client = AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio(loop_scope="function")
async def test_create_product():
    product_data = {
        "name": "Test Product",
        "description": "A product for testing",
        "price": 99.99,
        "quantity": 50
    }
    response = await client.post("/api/v1/products/", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["quantity"] == product_data["quantity"]
    assert "id" in data


@pytest.mark.asyncio(loop_scope="function")
async def test_create_duplicate_product():
    product_data = {
        "name": "Unique Product",
        "description": "First instance",
        "price": 49.99,
        "quantity": 20
    }
    response = await client.post("/api/v1/products/", json=product_data)
    assert response.status_code == 201

    product_data_duplicate = {
        "name": "Unique Product",
        "description": "Duplicate instance",
        "price": 59.99,
        "quantity": 30
    }
    response = await client.post("/api/v1/products/", json=product_data_duplicate)
    assert response.status_code == 400
    assert response.json()["detail"] == "Product already exists."


@pytest.mark.asyncio(loop_scope="function")
async def test_read_products():
    products = [
        {"name": "Product 1", "description": "Desc 1", "price": 10.0, "quantity": 100},
        {"name": "Product 2", "description": "Desc 2", "price": 20.0, "quantity": 200},
    ]
    for product in products:
        await client.post("/api/v1/products/", json=product)

    response = await client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert any(p["name"] == "Product 1" for p in data)
    assert any(p["name"] == "Product 2" for p in data)


@pytest.mark.asyncio(loop_scope="function")
async def test_read_product():
    product_data = {
        "name": "Single Product",
        "description": "A single product",
        "price": 15.0,
        "quantity": 150
    }
    create_response = await client.post("/api/v1/products/", json=product_data)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == product_data["name"]


@pytest.mark.asyncio(loop_scope="function")
async def test_read_nonexistent_product():
    response = await client.get("/api/v1/products/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product with id 9999 does not exist."


@pytest.mark.asyncio(loop_scope="function")
async def test_update_product():
    product_data = {
        "name": "Update Product",
        "description": "Before update",
        "price": 30.0,
        "quantity": 300
    }
    create_response = await client.post("/api/v1/products/", json=product_data)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    update_data = {
        "description": "After update",
        "price": 35.0
    }
    response = await client.put(f"/api/v1/products/{product_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == update_data["description"]
    assert data["price"] == update_data["price"]
    assert data["name"] == product_data["name"]


@pytest.mark.asyncio(loop_scope="function")
async def test_update_nonexistent_product():
    update_data = {
        "description": "Nonexistent update",
        "price": 40.0
    }
    response = await client.put("/api/v1/products/9999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Product with id 9999 does not exist."


@pytest.mark.asyncio(loop_scope="function")
async def test_delete_product():
    product_data = {
        "name": "Delete Product",
        "description": "To be deleted",
        "price": 25.0,
        "quantity": 250
    }
    create_response = await client.post("/api/v1/products/", json=product_data)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == 204

    get_response = await client.get(f"/api/v1/products/{product_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio(loop_scope="function")
async def test_delete_nonexistent_product():
    response = await client.delete("/api/v1/products/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product with id 9999 does not exist."
