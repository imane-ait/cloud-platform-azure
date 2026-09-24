from pydantic import BaseModel


class VehicleCreate(BaseModel):
    plate: str
    brand: str
    model: str


class VehicleRead(VehicleCreate):
    id: int
    active: bool

    model_config = {"from_attributes": True}
