from apps.database.mongodb import get_mongo_collection

from apps.models.vehicle import Vehicle


class VehicleService:
    @staticmethod
    def create_vehicle(vehicle_data: Vehicle):
        collection = get_mongo_collection("vehicles")
        collection.insert_one(vehicle_data.model_dump())
        return vehicle_data

    @staticmethod
    def get_vehicle_by_id(vehicle_id: int):
        collection = get_mongo_collection("vehicles")
        return collection.find_one({"id": vehicle_id})

    @staticmethod
    def update_vehicle(vehicle_id: int, updated_data: dict):
        collection = get_mongo_collection("vehicles")
        collection.update_one({"id": vehicle_id}, {"$set": updated_data})
        return {"message": "Vehicle updated successfully"}

    @staticmethod
    def delete_vehicle(vehicle_id: int):
        collection = get_mongo_collection("vehicles")
        collection.delete_one({"id": vehicle_id})
        return {"message": "Vehicle deleted successfully"}
