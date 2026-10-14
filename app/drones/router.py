from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_session
from app.drones.models import Drone
from app.drones.schemas import DroneCreate, DroneRead, DroneUpdate
from app.users.models import User

router = APIRouter(prefix="/drones", tags=["drones"])


@router.post("", status_code=201)
def post_drone(
    data: DroneCreate, session: Annotated[Session, Depends(get_session)]
) -> DroneRead:
    owner = session.get(User, data.owner_id)
    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    drone = Drone(name=data.name, owner_id=data.owner_id)
    session.add(drone)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise

    session.refresh(drone)

    response = DroneRead.model_validate(drone)
    return response


@router.get("", status_code=200)
def get_drones(session: Annotated[Session, Depends(get_session)]) -> list[DroneRead]:
    statement = select(Drone).order_by(Drone.id)
    drones = session.scalars(statement).all()
    response: list[DroneRead] = []

    for drone in drones:
        response.append(DroneRead.model_validate(drone))

    return response


@router.get("/{drone_id}")
def get_drone(
    session: Annotated[Session, Depends(get_session)], drone_id: int
) -> DroneRead:
    drone = session.get(Drone, drone_id)
    if drone is None:
        raise HTTPException(status_code=404, detail="Drone not found")

    return DroneRead.model_validate(drone)


@router.patch("/{drone_id}")
def patch_drone(
    session: Annotated[Session, Depends(get_session)], drone_id: int, data: DroneUpdate
) -> DroneRead:
    drone = session.get(Drone, drone_id)
    if drone is None:
        raise HTTPException(status_code=404, detail="Drone not found")

    changes = data.model_dump(exclude_unset=True)

    if None in changes.values():
        raise HTTPException(status_code=422, detail="Updated fields cannot be null")

    if "name" in changes:
        drone.name = changes["name"]
    if "owner_id" in changes:
        owner = session.get(User, data.owner_id)
        if owner is None:
            raise HTTPException(status_code=404, detail="Owner not found")
        drone.owner_id = changes["owner_id"]

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise

    response = DroneRead.model_validate(drone)
    return response


@router.delete("/{drone_id}", status_code=204)
def delete_drone(
    session: Annotated[Session, Depends(get_session)], drone_id: int
) -> None:
    drone = session.get(Drone, drone_id)
    if drone is None:
        raise HTTPException(status_code=404, detail="Drone not found")
    session.delete(drone)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise
