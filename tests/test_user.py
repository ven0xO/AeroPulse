from fastapi.testclient import TestClient


def test_create_user(client: TestClient) -> None:
    response = client.post("/users", json={"email": "test@xyz.com"})
    assert response.json()["email"] == "test@xyz.com"
    assert isinstance(response.json()["id"], int)
    assert response.status_code == 201

    response = client.post("/users", json={"email": "test@xyz.com"})
    assert response.status_code == 409

    response = client.post("/users", json={"email": "test/xyz.com"})
    assert response.status_code == 422

    response = client.post("/users", json={"email": None})
    assert response.status_code == 422

    response = client.post("/users", json={})
    assert response.status_code == 422
