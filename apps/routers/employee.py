from pydantic import BaseModel
from datetime import date

from fastapi import APIRouter, HTTPException

from apps.database.mongodb import get_mongo_collection

from apps.models.employee import EmployeeCreateRequest, object_id_to_str

router = APIRouter()


@router.get("")
async def get_employees():
    collection = get_mongo_collection("employees")
    employees = list(collection.find())

    # Convert ObjectIds to strings
    for employee in employees:
        employee["_id"] = str(employee["_id"])  # Convert ObjectId to string

    return employees


@router.post("")
async def create_employee(employee_request: EmployeeCreateRequest):
    collection = get_mongo_collection("employees")

    # Create a new employee document
    new_employee = {
        "name": employee_request.name,
        "role": employee_request.role,
        "driver": employee_request.driver,
    }

    # Insert into the collection
    result = collection.insert_one(new_employee)

    if result.inserted_id:
        return {"message": "Employee created successfully", "employee_id": object_id_to_str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to create employee")
