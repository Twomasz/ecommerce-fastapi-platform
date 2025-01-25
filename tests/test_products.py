import pytest
from fastapi import status

@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_list_products(test_client):
    response = await test_client.get("/products/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

@pytest.mark.asyncio
@pytest.mark.order(2)
async def test_fill_product(test_client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "category": "Test Category",
        "unit_price": 10.0,
        "quantity": 5
    }
    response = await test_client.post("/products/fill", json=product_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == product_data["name"]

@pytest.mark.asyncio
@pytest.mark.order(3)
async def test_get_product(test_client):
    product_id = 3  # obtained from test_fill_product
    response = await test_client.get(f"/products/id/{product_id}")
    print(response.text)
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.json()

@pytest.mark.asyncio
@pytest.mark.order(4)
async def test_search_products(test_client):
    params = {"name": "Test"}
    response = await test_client.get("/products/search", params=params)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
@pytest.mark.order(5)
async def test_delete_product(test_client):
    product_id = 3  # delete the product is created in test_fill_product
    response = await test_client.delete(f"/products/id/{product_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Product deleted successfully"
