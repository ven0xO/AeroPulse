from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.users.models import User


def test_create_drone(client: TestClient) -> None:
    response = client.post("/users", json={"email": "test@xyz.com"})
    assert response.status_code == 201

    owner_id = response.json()["id"]
    response = client.post("/drones", json={"name": "test1", "owner_id": owner_id})
    assert response.status_code == 201
    assert response.json()["name"] == "test1"
    assert response.json()["owner_id"] == owner_id
    assert isinstance(response.json()["id"], int)

    response = client.post("/drones", json={"owner_id": owner_id})
    assert response.status_code == 422

    response = client.post("/drones", json={"name": "test3"})
    assert response.status_code == 422

    response = client.post("/drones", json={"name": "test4", "owner_id": "abc"})
    assert response.status_code == 422

    response = client.post("/drones", json={"name": "test5", "owner_id": None})
    assert response.status_code == 422

    response = client.post("/drones", json={"name": None, "owner_id": owner_id})
    assert response.status_code == 422


def test_create_drone_owner_not_found(client: TestClient, db_session: Session) -> None:
    response = client.post("/users", json={"email": "test@xyz.com"})
    assert response.status_code == 201

    owner_id = response.json()["id"]
    owner = db_session.get(User, owner_id)
    assert owner is not None

    db_session.delete(owner)
    db_session.commit()

    response = client.post("/drones", json={"name": "test1", "owner_id": owner_id})
    assert response.status_code == 404
    assert response.json()["detail"] == "Owner not found"
