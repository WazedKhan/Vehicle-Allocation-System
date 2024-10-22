from fastapi import HTTPException
from apps.database.mongodb import get_mongo_collection
from apps.models.vehicle import VehicleCreateRequest, VehicleUpdateRequest, Vehicle
from apps.models.driver import DriverCreateRequest
from apps.database.config import DBCollections
from bson import ObjectId


class VehicleService:
    def __init__(self):
        self.collection = get_mongo_collection(DBCollections.VEHICLE)

    async def get_vehicles(self):
        vehicles = list(self.collection.find())
        return [Vehicle(**vehicle) for vehicle in vehicles]  # Convert to Vehicle model

    async def create_vehicle(self, vehicle_request: VehicleCreateRequest):
        new_vehicle = vehicle_request.model_dump()

        result = await self.collection.insert_one(new_vehicle)
        if result.inserted_id:
            return {"message": "Vehicle created successfully", "vehicle_id": str(result.inserted_id)}
        raise HTTPException(status_code=500, detail="Failed to create vehicle")

    async def update_vehicle(self, vehicle_id: str, vehicle_request: VehicleUpdateRequest):
        update_data = vehicle_request.model_dump(exclude_unset=True)  # Only update provided fields
        result = await self.collection.update_one({"_id": ObjectId(vehicle_id)}, {"$set": update_data})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Vehicle not found or no update performed")

        return {"message": "Vehicle updated successfully"}

    async def delete_vehicle(self, vehicle_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(vehicle_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Vehicle not found")

        return {"message": "Vehicle deleted successfully"}

    async def get_vehicle_with_driver(self, vehicle_id: str):
        # Fetch the vehicle by vehicle_id
        vehicle_collection = get_mongo_collection(DBCollections.VEHICLE)
        vehicle = vehicle_collection.find_one({"_id": ObjectId(vehicle_id)})

        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")

        # Convert ObjectId to string for the vehicle ID
        vehicle["_id"] = str(vehicle["_id"])

        # Fetch the driver details using assigned_driver_id
        if "assigned_driver_id" in vehicle and vehicle["assigned_driver_id"]:
            driver_collection = get_mongo_collection(DBCollections.EMPLOYEE)

            # Ensure the assigned_driver_id is an ObjectId
            assigned_driver_id = ObjectId(vehicle["assigned_driver_id"])

            # Query the driver by ObjectId and check if driver is True
            driver = driver_collection.find_one({"_id": assigned_driver_id, "driver": True})

            if driver:
                # Convert driver data into a structured format
                vehicle["assigned_driver"] = DriverCreateRequest(
                    **driver
                ).model_dump()  # Convert to Pydantic model and then to dict
                vehicle["assigned_driver"]["id"] = str(driver["_id"])  # Add driver ID as a string
            else:
                vehicle["assigned_driver"] = None  # No driver found

        return vehicle
