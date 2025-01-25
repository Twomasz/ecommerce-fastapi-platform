import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_list_orders(test_client):
    response = await test_client.get("/orders/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

@pytest.mark.asyncio
async def test_get_order(test_client):
    order_id = 1  # get order from 'setup_test_db' fixture
    response = await test_client.get(f"/orders/id/{order_id}")
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.json()

@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_place_order(test_client):
    # use the data from 'setup_test_db' fixture
    order_data = {
        "user_id": 1,
        "items": [
            {"product_id": 1, "quantity": 1},
            {"product_id": 2, "quantity": 1}
        ]
    }
    response = await test_client.post("/orders/place_order", json=order_data)
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.json()


@pytest.mark.asyncio
@pytest.mark.order(2)
async def test_get_order_history(test_client):
    user_id = 1  # get user from 'setup_test_db' fixture
    response = await test_client.get(f"/orders/history/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0