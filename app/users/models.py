from typing import TYPE_CHECKING

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.drones.models import Drone


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    drones: Mapped[list["Drone"]] = relationship(back_populates="owner")
