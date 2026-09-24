import pytest

@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_create_vehicle(client):
    response = await client.post("/vehicles/", json={
        "plate": "AA-123-BB",
        "brand": "Renault",
        "model": "Clio"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["plate"] == "AA-123-BB"
    assert data["active"] == True

@pytest.mark.asyncio
async def test_list_vehicles(client):
    await client.post("/vehicles/", json={
        "plate": "AA-123-BB",
        "brand": "Renault",
        "model": "Clio"
    })
    response = await client.get("/vehicles/")
    assert response.status_code == 200
    assert len(response.json()) == 1

@pytest.mark.asyncio
async def test_get_vehicle(client):
    create = await client.post("/vehicles/", json={
        "plate": "AA-123-BB",
        "brand": "Renault",
        "model": "Clio"
    })
    vehicle_id = create.json()["id"]
    response = await client.get(f"/vehicles/{vehicle_id}")
    assert response.status_code == 200
    assert response.json()["id"] == vehicle_id

@pytest.mark.asyncio
async def test_get_vehicle_not_found(client):
    response = await client.get("/vehicles/9999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_vehicle(client):
    create = await client.post("/vehicles/", json={
        "plate": "AA-123-BB",
        "brand": "Renault",
        "model": "Clio"
    })
    vehicle_id = create.json()["id"]
    response = await client.delete(f"/vehicles/{vehicle_id}")
    assert response.status_code == 204
