import pytest
from fastapi import status

@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_list_users(test_client):
    response = await test_client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    print(response.json())
    assert len(response.json()) > 0

@pytest.mark.asyncio
@pytest.mark.order(2)
async def test_register_user(test_client):
    user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "phone_number": "1234567890"
    }
    response = await test_client.post("/users/register", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "User registered successfully"

@pytest.mark.asyncio
@pytest.mark.order(3)
async def test_get_user(test_client):
    user_id = 3  # firstly registered new user
    response = await test_client.get(f"/users/id/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.json()

@pytest.mark.asyncio
@pytest.mark.order(4)
async def test_update_user(test_client):
    user_id = 3  # update the user that was firstly registered in 'test_register_user'
    user_data = {
        "name": "Updated User",
        "email": "updateduser@example.com",
        "phone_number": "0987654321"
    }
    response = await test_client.put(f"/users/id/{user_id}", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == user_data["name"]


@pytest.mark.asyncio
@pytest.mark.order(5)
async def test_delete_user(test_client):
    user_id = 3  # delete the user that was updated in 'test_update_user'
    response = await test_client.delete(f"/users/id/{user_id}")
    if response.status_code == status.HTTP_200_OK:
        assert response.json()["message"] == "User deleted successfully"
    else:
        assert response.status_code == status.HTTP_404_NOT_FOUND