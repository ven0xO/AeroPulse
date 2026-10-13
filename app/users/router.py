from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
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

    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        if (
            isinstance(exc.orig, UniqueViolation)
            and exc.orig.diag.constraint_name == "users_email_key"
        ):
            raise HTTPException(
                status_code=409,
                detail="Email is already registered",
            ) from exc
        else:
            raise

    session.refresh(user)

    response = UserRead.model_validate(user)
    return response
