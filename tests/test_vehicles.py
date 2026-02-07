def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_vehicle(client):
    payload = {
        "number": "KL-01-1234",
        "type": "car",
        "owner_name": "Shiyas",
    }

    response = client.post("/api/vehicles", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["number"] == payload["number"]
    assert data["type"] == payload["type"]
    assert data["owner_name"] == payload["owner_name"]
    assert "id" in data


def test_list_vehicles(client):
    payload = {
        "number": "KL-02-9999",
        "type": "bike",
        "owner_name": "Alex",
    }

    client.post("/api/vehicles", json=payload)

    response = client.get("/api/vehicles")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
