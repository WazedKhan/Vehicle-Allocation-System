from pydantic import BaseModel

from bson import ObjectId


class Vehicle(BaseModel):
    id: int
    make: str  # Manufacturer or brand of the vehicle
    model: str  # Specific model of the vehicle
    year: int  # Year the vehicle was manufactured
    assigned_driver_id: ObjectId  # Reference to the driver assigned to this vehicle
