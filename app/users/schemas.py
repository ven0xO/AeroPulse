from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    email: str


class UserRead(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)
