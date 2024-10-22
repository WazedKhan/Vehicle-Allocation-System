from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from pymongo.collection import Collection
from bson import ObjectId


# Employee Pydantic model
class EmployeeCreateRequest(BaseModel):
    name: str
    role: str
    driver: bool = False  # Optional field to indicate if the employee is a driver


class EmployeeUpdateRequest(BaseModel):
    name: str
    role: str
    driver: bool = False  # Optional field for update


# Helper function to convert MongoDB ObjectId to string
def object_id_to_str(obj_id: ObjectId) -> str:
    return str(obj_id)
