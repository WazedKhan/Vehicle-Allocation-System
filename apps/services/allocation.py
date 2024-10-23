from pydantic import BaseModel
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime, date
from apps.models.allocation import Allocation
from apps.database.mongodb import get_mongo_collection
from apps.database.config import DBCollections

from apps.cache.redis_cache import RedisCache
from apps.cache.cache_keys import VEHICLE_CACHE_KEY, EMPLOYEE_CACHE_KEY


class AllocationService:
    def __init__(self):
        self.collection = get_mongo_collection(DBCollections.ALLOCATION)
        self.employee_collection = get_mongo_collection(DBCollections.EMPLOYEE)  # Employee/Driver collection
        self.vehicle_collection = get_mongo_collection(DBCollections.VEHICLE)  # Vehicle collection

        # Initialize RedisCache
        self.redis_cache = RedisCache()

    def create_allocation(self, allocation_request: Allocation):
        try:
            vehicle_id = ObjectId(allocation_request.vehicle_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid vehicle ID format")

        vehicle_cache_key = f"{VEHICLE_CACHE_KEY}{vehicle_id}"
        vehicle = self.redis_cache.get(vehicle_cache_key)

        if not vehicle:
            vehicle = self.vehicle_collection.find_one({"_id": vehicle_id})
            if vehicle:
                self.redis_cache.set(vehicle_cache_key, vehicle)
            else:
                raise HTTPException(status_code=404, detail="Vehicle not found")

        existing_allocation = self.collection.find_one({"vehicle_id": allocation_request.vehicle_id})
        if existing_allocation and existing_allocation["employee_id"] != allocation_request.employee_id:
            raise HTTPException(status_code=400, detail="Vehicle is already allocated to another employee.")

        if existing_allocation and existing_allocation["employee_id"] == allocation_request.employee_id:
            raise HTTPException(status_code=400, detail="Vehicle is already allocated to this employee.")

        # check if employee already has a vehicle assigned to him
        already_has_vehicle= self.collection.find_one({"employee_id": allocation_request.employee_id})
        if already_has_vehicle:
            raise HTTPException(status_code=400, detail="Another vehicle is already allocated to this employee.")

        new_allocation = allocation_request.model_dump()
        if isinstance(allocation_request.allocation_date, date):
            new_allocation["allocation_date"] = datetime.combine(
                allocation_request.allocation_date, datetime.min.time()
            )

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

            # Check Redis cache for the vehicle information
            vehicle_cache_key = f"{VEHICLE_CACHE_KEY}{allocation['vehicle_id']}"
            vehicle = self.redis_cache.get(vehicle_cache_key)

            if not vehicle:
                vehicle = self.vehicle_collection.find_one({"_id": ObjectId(allocation["vehicle_id"])})
                if vehicle:
                    self.redis_cache.set(vehicle_cache_key, vehicle)

            # Add vehicle info to the allocation
            if vehicle:
                allocation["vehicle_info"] = {
                    "id": str(vehicle.get("_id")),
                    "make": vehicle.get("make"),
                    "model": vehicle.get("model"),
                    "year": vehicle.get("year"),
                }
            else:
                allocation["vehicle_info"] = None

            # Check Redis cache for the employee information
            employee_cache_key = f"{EMPLOYEE_CACHE_KEY}{allocation['employee_id']}"
            employee = self.redis_cache.get(employee_cache_key)

            if not employee:
                employee = self.employee_collection.find_one({"_id": ObjectId(allocation["employee_id"])})
                if employee:
                    self.redis_cache.set(employee_cache_key, employee)

            # Add employee info to the allocation
            if employee:
                allocation["employee_info"] = {
                    "id": str(employee.get("_id")),
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
        allocation_date = existing_allocation.get("allocation_date")
        if isinstance(allocation_date, str):  # If it's a string, convert to datetime
            allocation_date = datetime.fromisoformat(allocation_date)

        if allocation_date < datetime.combine(date.today(), datetime.min.time()):
            raise HTTPException(status_code=400, detail="Cannot update allocation after the allocation date")

        # Convert allocation_date from date to datetime if necessary
        update_data = allocation_request.model_dump()
        if isinstance(allocation_request.allocation_date, date):
            update_data["allocation_date"] = datetime.combine(allocation_request.allocation_date, datetime.min.time())

        # Proceed with the update if the date is valid
        update_result = self.collection.update_one({"_id": ObjectId(allocation_id)}, {"$set": update_data})

        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Allocation not found or no changes made")

        return {"message": "Allocation updated successfully", "allocation_id": allocation_id}

    def delete_allocation(self, allocation_id: str):
        # Delete the allocation by ID
        delete_result = self.collection.delete_one({"_id": ObjectId(allocation_id)})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Allocation not found")

        return {"message": "Allocation deleted successfully"}
