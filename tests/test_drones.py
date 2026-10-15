from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.drones.models import Drone
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


def test_get_drones_empty(client: TestClient) -> None:
    response = client.get("/drones")
    assert response.status_code == 200
    assert response.json() == []


def test_get_drones(client: TestClient, db_session: Session) -> None:
    response = client.post("/users", json={"email": "test@xyz.com"})
    assert response.status_code == 201

    owner_id = response.json()["id"]
    owner = db_session.get(User, owner_id)
    assert owner is not None

    response = client.post("/drones", json={"name": "test1", "owner_id": owner_id})
    assert response.status_code == 201
    first_drone = response.json()

    response = client.post("/drones", json={"name": "test2", "owner_id": owner_id})
    assert response.status_code == 201
    second_drone = response.json()

    response = client.get("/drones")
    assert response.status_code == 200
    assert response.json() == [first_drone, second_drone]


def test_get_drone(client: TestClient, db_session: Session) -> None:
    response = client.post("/users", json={"email": "test@xyz.com"})
    assert response.status_code == 201

    owner_id = response.json()["id"]
    owner = db_session.get(User, owner_id)
    assert owner is not None

    response = client.post("/drones", json={"name": "test1", "owner_id": owner_id})
    assert response.status_code == 201
    created_drone = response.json()
    drone_id = created_drone["id"]

    response = client.get(f"/drones/{drone_id}")
    assert response.status_code == 200
    assert response.json() == created_drone

    drone = db_session.get(Drone, drone_id)
    assert drone is not None
    db_session.delete(drone)
    db_session.commit()

    response = client.get(f"/drones/{drone_id}")
    assert response.status_code == 404

    response = client.get("/drones/abc")
    assert response.status_code == 422


def test_patch_drone(client: TestClient, db_session: Session) -> None:
    response = client.post("/users", json={"email": "test@xyz.com"})
    assert response.status_code == 201

    owner_id = response.json()["id"]
    owner = db_session.get(User, owner_id)
    assert owner is not None

    response = client.post("/drones", json={"name": "test1", "owner_id": owner_id})
    assert response.status_code == 201
    created_drone = response.json()
    drone_id = created_drone["id"]

    response = client.patch(f"/drones/{drone_id}", json={"name": "new_test1"})
    assert response.status_code == 200
    assert response.json() == {
        "id": drone_id,
        "name": "new_test1",
        "owner_id": owner_id,
    }
    patched_drone = db_session.get(Drone, drone_id)
    assert patched_drone is not None
    assert patched_drone.name == "new_test1"


def test_patch_drone_owner(client: TestClient, db_session: Session) -> None:
    response = client.post("/users", json={"email": "test@xyz.com"})
    assert response.status_code == 201

    owner_id = response.json()["id"]
    owner = db_session.get(User, owner_id)
    assert owner is not None

    response = client.post("/drones", json={"name": "test1", "owner_id": owner_id})
    assert response.status_code == 201
    created_drone = response.json()
    drone_id = created_drone["id"]

    response = client.post("/users", json={"email": "test2@xyz.com"})
    assert response.status_code == 201
    owner_id2 = response.json()["id"]
    owner2 = db_session.get(User, owner_id2)
    assert owner2 is not None

    response = client.patch(f"/drones/{drone_id}", json={"owner_id": owner_id2})
    assert response.status_code == 200
    assert response.json()["owner_id"] == owner_id2
    assert response.json()["id"] == drone_id
    assert response.json()["name"] == created_drone["name"]

    patched_drone = db_session.get(Drone, drone_id)
    assert patched_drone is not None
    assert patched_drone.owner_id == owner_id2
