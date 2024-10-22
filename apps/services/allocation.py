from pydantic import BaseModel
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime, date
from apps.models.allocation import Allocation
from apps.database.mongodb import get_mongo_collection
from apps.database.config import DBCollections


class AllocationService:
    def __init__(self):
        self.collection = get_mongo_collection(DBCollections.ALLOCATION)
        self.employee_collection = get_mongo_collection(DBCollections.EMPLOYEE)  # Employee/Driver collection
        self.vehicle_collection = get_mongo_collection(DBCollections.VEHICLE)  # Vehicle collection

    def create_allocation(self, allocation_request: Allocation):
        # Convert vehicle_id to ObjectId if it's a string
        try:
            vehicle_id = ObjectId(allocation_request.vehicle_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid vehicle ID format")

        # Check if the vehicle exists
        vehicle = self.vehicle_collection.find_one({"_id": vehicle_id})
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")

        # Check if the same vehicle is already allocated to the same employee
        existing_allocation = self.collection.find_one(
            {"employee_id": allocation_request.employee_id, "vehicle_id": allocation_request.vehicle_id}
        )

        if existing_allocation:
            raise HTTPException(status_code=400, detail="Vehicle is already allocated to this employee.")

        # Check if the same vehicle is already allocated to the same employee
        existing_allocation = self.collection.find_one(
            {"employee_id": allocation_request.employee_id, "vehicle_id": allocation_request.vehicle_id}
        )

        if existing_allocation:
            raise HTTPException(status_code=400, detail="Vehicle is already allocated to this employee.")

        # Convert allocation_date from date to datetime
        new_allocation = allocation_request.dict()
        if isinstance(allocation_request.allocation_date, date):
            new_allocation["allocation_date"] = datetime.combine(
                allocation_request.allocation_date, datetime.min.time()
            )

        # Create the allocation in MongoDB
        result = self.collection.insert_one(new_allocation)
        if result.inserted_id:
            return {"message": "Allocation created successfully", "allocation_id": str(result.inserted_id)}
        raise HTTPException(status_code=500, detail="Failed to create allocation")

    def get_allocations(self):
        allocations = list(self.collection.find())
        enriched_allocations = []

        for allocation in allocations:
            # Convert allocation_date from datetime to date
            if isinstance(allocation.get("allocation_date"), datetime):
                allocation["allocation_date"] = allocation["allocation_date"].date()

            # Convert ObjectId fields to strings
            allocation["_id"] = str(allocation["_id"])
            allocation["employee_id"] = str(allocation["employee_id"])
            allocation["vehicle_id"] = str(allocation["vehicle_id"])

            # Fetch the vehicle details
            vehicle = self.vehicle_collection.find_one({"_id": ObjectId(allocation["vehicle_id"])})
            if vehicle:
                allocation["vehicle_info"] = {
                    "make": vehicle.get("make"),
                    "model": vehicle.get("model"),
                    "year": vehicle.get("year"),
                }
            else:
                allocation["vehicle_info"] = None

            # Fetch the employee/driver details
            employee = self.employee_collection.find_one({"_id": ObjectId(allocation["employee_id"])})
            if employee:
                allocation["employee_info"] = {
                    "name": employee.get("name"),
                    "role": employee.get("role"),
                    "driver": employee.get("driver"),
                }
            else:
                allocation["employee_info"] = None

            # Add the enriched allocation to the result list
            enriched_allocations.append(allocation)

        return enriched_allocations

    def get_allocation_by_id(self, allocation_id: str):
        # Fetch allocation by ID and convert datetime to date
        allocation = self.collection.find_one({"_id": ObjectId(allocation_id)})
        if not allocation:
            raise HTTPException(status_code=404, detail="Allocation not found")

        if isinstance(allocation.get("allocation_date"), datetime):
            allocation["allocation_date"] = allocation["allocation_date"].date()
        return allocation

    def update_allocation(self, allocation_id: str, allocation_request: Allocation):
        # Fetch the existing allocation
        existing_allocation = self.collection.find_one({"_id": ObjectId(allocation_id)})
        if not existing_allocation:
            raise HTTPException(status_code=404, detail="Allocation not found")

        # Validate if the allocation date has already passed
        if existing_allocation.get("allocation_date") < datetime.combine(date.today(), datetime.min.time()):
            raise HTTPException(status_code=400, detail="Cannot update allocation after the allocation date")

        # Convert allocation_date from date to datetime if necessary
        update_data = allocation_request.dict()
        if isinstance(allocation_request.allocation_date, date):
            update_data["allocation_date"] = datetime.combine(allocation_request.allocation_date, datetime.min.time())

        # Proceed with the update if the date is valid
        update_result = self.collection.update_one({"_id": ObjectId(allocation_id)}, {"$set": update_data})

        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Allocation not found or no changes made")

        return {"message": "Allocation updated successfully"}

    def delete_allocation(self, allocation_id: str):
        # Delete the allocation by ID
        delete_result = self.collection.delete_one({"_id": ObjectId(allocation_id)})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Allocation not found")

        return {"message": "Allocation deleted successfully"}
