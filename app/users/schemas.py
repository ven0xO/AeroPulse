from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr


class UserRead(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)
