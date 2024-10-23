from typing import Optional

from pydantic import BaseModel

from bson import ObjectId


# Driver Pydantic model
class DriverCreateRequest(BaseModel):
    name: str
    role: str
    driver: bool = True  # Default to True to indicate that this is a driver


class DriverUpdateRequest(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    driver: Optional[bool] = None  # Optional field for update


# Helper function to convert MongoDB ObjectId to string
def object_id_to_str(obj_id: ObjectId) -> str:
    return str(obj_id)
