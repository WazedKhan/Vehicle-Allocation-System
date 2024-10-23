from typing import Optional
from pydantic import BaseModel


class Vehicle(BaseModel):
    make: str
    model: str
    year: int


class VehicleCreateRequest(BaseModel):
    make: str  # Manufacturer of the vehicle
    model: str  # Specific model of the vehicle
    year: int  # Year the vehicle was manufactured
    assigned_driver_id: str  # Accepting string here for assigned driver ID


class VehicleUpdateRequest(BaseModel):
    make: Optional[str]
    model: Optional[str]
    year: Optional[int]
    assigned_driver_id: Optional[str]  # Optional string for updates
