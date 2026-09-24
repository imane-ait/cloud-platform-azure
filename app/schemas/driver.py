from pydantic import BaseModel


class DriverCreate(BaseModel):
    first_name: str
    last_name: str
    license_number: str


class DriverRead(DriverCreate):
    id: int
    active: bool

    model_config = {"from_attributes": True}
