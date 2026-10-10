from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_session
from app.users.models import User
from app.users.schemas import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=201)
def post_user(
    data: UserCreate, session: Annotated[Session, Depends(get_session)]
) -> UserRead:
    user = User(email=data.email)
    session.add(user)
    session.commit()

    session.refresh(user)

    response = UserRead.model_validate(user)
    return response
