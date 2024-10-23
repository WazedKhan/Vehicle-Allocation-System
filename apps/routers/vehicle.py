# routes/vehicle_routes.py

from fastapi import APIRouter
from apps.services.vehicle import VehicleService
from apps.models.vehicle import VehicleCreateRequest, VehicleUpdateRequest

router = APIRouter()
service = VehicleService()


@router.get("")
async def get_vehicles():
    return await service.get_vehicles()


@router.post("")
async def create_vehicle(vehicle_request: VehicleCreateRequest):
    return await service.create_vehicle(vehicle_request)


@router.get("/{vehicle_id}")
async def vehicle_details(vehicle_id: str):
    return await service.get_vehicle_with_driver(vehicle_id)


@router.put("/{vehicle_id}")
async def update_vehicle(vehicle_id: str, vehicle_request: VehicleUpdateRequest):
    return await service.update_vehicle(vehicle_id, vehicle_request)


@router.delete("/{vehicle_id}")
async def delete_vehicle(vehicle_id: str):
    return await service.delete_vehicle(vehicle_id)
