from pydantic import BaseModel, field_validator, validator
from datetime import date

from apps.models import employee
from apps.routers import allocation


class Allocation(BaseModel):
    employee_id: str  # MongoDB ObjectId as string
    vehicle_id: str  # Vehicle ObjectId as string
    allocation_date: date  # Date of allocation


class AllocationCreate(BaseModel):
    employee_id: str
    vehicle_id: str
    allocation_date: date

    @field_validator("allocation_date")
    def check_allocation_date(cls, value):
        if value < date.today():
            raise ValueError("Allocation date can not be in the past")
        else:
            return value
