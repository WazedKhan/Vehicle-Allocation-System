from pydantic import BaseModel, constr

from typing import Optional
from bson import ObjectId


class EmployeeCreateRequest(BaseModel):
    name: constr(min_length=1, max_length=100)  # type: ignore
    role: constr(min_length=1, max_length=50)  # type: ignore
    driver: bool


class EmployeeUpdateRequest(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    driver: Optional[bool] = None  # Optional field for update


# Helper function to convert MongoDB ObjectId to string
def object_id_to_str(obj_id: ObjectId) -> str:
    return str(obj_id)
