from datetime import date
from pydantic import BaseModel


class Allocation(BaseModel):
    employee_id: int
    vehicle_id: int
    driver_id: int
    allocation_date: date
