from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_session
from app.drones.models import Drone
from app.drones.schemas import DroneCreate, DroneRead
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
