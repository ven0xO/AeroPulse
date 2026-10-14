from pydantic import BaseModel, ConfigDict


class DroneCreate(BaseModel):
    name: str
    owner_id: int


class DroneRead(BaseModel):
    id: int
    name: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
