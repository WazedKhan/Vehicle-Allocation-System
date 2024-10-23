from pydantic import BaseModel
from datetime import date


class Allocation(BaseModel):
    employee_id: str  # MongoDB ObjectId as string
    vehicle_id: str  # Vehicle ObjectId as string
    allocation_date: date  # Date of allocation
