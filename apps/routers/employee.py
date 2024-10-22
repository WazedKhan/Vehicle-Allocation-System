from fastapi import APIRouter, HTTPException

from apps.database.mongodb import get_mongo_collection

from apps.models.employee import EmployeeCreateRequest, object_id_to_str
from apps.utils.db_helpers import convert_objectids_to_strings

from apps.database.config import DBCollections

router = APIRouter()


@router.get("")
async def get_employees():
    collection = get_mongo_collection(DBCollections.EMPLOYEE)
    employees = list(collection.find())

    # Convert ObjectIds to strings using the utility function
    employees = convert_objectids_to_strings(employees)

    return employees


@router.post("")
async def create_employee(employee_request: EmployeeCreateRequest):
    collection = get_mongo_collection(DBCollections.EMPLOYEE)

    # Create a new employee document using the validated data
    new_employee = employee_request.model_dump()

    # Insert into the collection
    result = collection.insert_one(new_employee)

    if result.inserted_id:
        return {"message": "Employee created successfully", "employee_id": object_id_to_str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to create employee")
