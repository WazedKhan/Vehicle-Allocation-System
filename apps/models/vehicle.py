from pydantic import BaseModel


class Vehicle(BaseModel):
    id: int
    name: str
    driver_id: int
