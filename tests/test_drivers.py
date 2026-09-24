import pytest

@pytest.mark.asyncio
async def test_create_driver(client):
    response = await client.post("/drivers/", json={
        "first_name": "Jean",
        "last_name": "Dupont",
        "license_number": "123456"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["license_number"] == "123456"
    assert data["active"] == True

@pytest.mark.asyncio
async def test_list_drivers(client):
    await client.post("/drivers/", json={
        "first_name": "Jean",
        "last_name": "Dupont",
        "license_number": "123456"
    })
    response = await client.get("/drivers/")
    assert response.status_code == 200
    assert len(response.json()) == 1

@pytest.mark.asyncio
async def test_get_driver(client):
    create = await client.post("/drivers/", json={
        "first_name": "Jean",
        "last_name": "Dupont",
        "license_number": "123456"
    })
    driver_id = create.json()["id"]
    response = await client.get(f"/drivers/{driver_id}")
    assert response.status_code == 200
    assert response.json()["id"] == driver_id

@pytest.mark.asyncio
async def test_get_driver_not_found(client):
    response = await client.get("/drivers/9999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_driver(client):
    create = await client.post("/drivers/", json={
        "first_name": "Jean",
        "last_name": "Dupont",
        "license_number": "123456"
    })
    driver_id = create.json()["id"]
    response = await client.delete(f"/drivers/{driver_id}")
    assert response.status_code == 204
