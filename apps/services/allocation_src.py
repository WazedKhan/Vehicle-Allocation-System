from pydantic import BaseModel
from fastapi import HTTPException, Query
from bson import ObjectId
from datetime import datetime, date
from apps.models import employee
from apps.models.allocation import AllocationCreate
from apps.database.mongodb import get_mongo_collection
from apps.database.config import DBCollections

from icecream import ic


class AllocationService:
    def __init__(self):
        self.collection = get_mongo_collection(DBCollections.ALLOCATION)
        self.employee_collection = get_mongo_collection(DBCollections.EMPLOYEE)  # Employee/Driver collection
        self.vehicle_collection = get_mongo_collection(DBCollections.VEHICLE)  # Vehicle collection

    def get_employee(self, employee_id: str) -> dict:
        employee = self.employee_collection.find_one({"_id": ObjectId(employee_id)})
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        employee["_id"] = str(employee["_id"])
        return employee

    def get_vehicle(self, vehicle_id: str) -> dict:
        vehicle = self.vehicle_collection.find_one({"_id": ObjectId(vehicle_id)})
        vehicle["_id"] = str(vehicle["_id"])
        return vehicle

    def check_for_same_employee_with_same_vehicle(self, v_id: str, e_id: str) -> bool:
        # check if same employee is already assigned with same vehicle
        result = self.collection.find({"employee._id": ObjectId(e_id), "vehicle._id": ObjectId(v_id)})
        if result:
            raise HTTPException(status_code=400, detail="This employee is already assigned to this vehicle")
        return True

    def create_allocation(self, allocation_request: AllocationCreate):
        employee = self.get_employee(allocation_request.employee_id)
        vehicle = self.get_vehicle(allocation_request.vehicle_id)
        # check if employee is already assigned to this vehicle
        self.check_for_same_employee_with_same_vehicle(
            v_id=allocation_request.employee_id,
            e_id=allocation_request.employee_id,
        )
        allocation_data = {
            "employee": employee,
            "vehicle": vehicle,
            "allocation_date": str(allocation_request.allocation_date),
        }
        # Insert allocation data into MongoDB and retrieve the inserted ID
        result = self.collection.insert_one(allocation_data)

        # Retrieve the full document to return as a dictionary
        allocation = self.collection.find_one({"_id": result.inserted_id})

        # Convert ObjectId to string for JSON serialization
        allocation["_id"] = str(allocation["_id"])
        return allocation

    def get_allocations(self, vehicle_model: str = None):
        query = {}

        if vehicle_model:
            # Add a filter for vehicle model
            query["vehicle.model"] = vehicle_model
        # Retrieve all allocations and convert the cursor to a list
        ic(query)
        allocations = list(self.collection.find(query).sort("_id", -1))

        # Convert ObjectId to string for each allocation
        for allocation in allocations:
            allocation["_id"] = str(allocation["_id"])

        return allocations
