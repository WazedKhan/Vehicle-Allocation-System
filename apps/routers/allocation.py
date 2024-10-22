from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
from apps.database.mongodb import get_mongo_collection
from apps.models.allocation import Allocation

router = APIRouter()


@router.post("")
def create_allocation(allocation: Allocation):
    collection = get_mongo_collection("allocations")

    # Check if the vehicle is already allocated on the given date
    existing_allocation = collection.find_one(
        {"vehicle_id": allocation.vehicle_id, "allocation_date": allocation.allocation_date}
    )

    if existing_allocation:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for this date")

    # Insert new allocation
    allocation_data = allocation.dict()
    collection.insert_one(allocation_data)
    return {"message": "Allocation created successfully", "allocation": allocation_data}


@router.get("")
def get_all_allocations():
    collection = get_mongo_collection("allocations")
    allocations = list(collection.find())
    return allocations


@router.put("/{allocation_id}")
def update_allocation(allocation_id: str, updated_allocation: Allocation):
    collection = get_mongo_collection("allocations")

    # Fetch and update allocation
    existing_allocation = collection.find_one({"_id": allocation_id})
    if not existing_allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    collection.update_one({"_id": allocation_id}, {"$set": updated_allocation.dict()})
    return {"message": "Allocation updated successfully"}


@router.delete("/{allocation_id}")
def delete_allocation(allocation_id: str):
    collection = get_mongo_collection("allocations")

    existing_allocation = collection.find_one({"_id": allocation_id})
    if not existing_allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    collection.delete_one({"_id": allocation_id})
    return {"message": "Allocation deleted successfully"}
