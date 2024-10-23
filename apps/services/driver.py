from fastapi import HTTPException

from apps.database.config import DBCollections
from apps.database.mongodb import get_mongo_collection

from apps.models.driver import DriverCreateRequest, object_id_to_str

from apps.utils.db_helpers import convert_objectids_to_strings


class DriverService:
    def __init__(self):
        self.collection = get_mongo_collection(DBCollections.EMPLOYEE)

    async def get_drivers(self):
        drivers = list(self.collection.find({"driver": True}))
        # Convert ObjectIds to strings
        return convert_objectids_to_strings(drivers)

    async def create_driver(self, driver_request: DriverCreateRequest):
        # Create a new driver document using the validated data
        new_driver = driver_request.model_dump()

        # Insert into the collection
        result = self.collection.insert_one(new_driver)

        if result.inserted_id:
            return {"message": "Driver created successfully", "driver_id": object_id_to_str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Failed to create driver")
