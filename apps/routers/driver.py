# apps/api/drivers.py

from fastapi import APIRouter
from apps.models.driver import DriverCreateRequest
from apps.services.driver import DriverService

router = APIRouter()
driver_service = DriverService()


@router.get("")
async def get_drivers():
    drivers = await driver_service.get_drivers()
    return drivers


@router.post("")
async def create_driver(driver_request: DriverCreateRequest):
    return await driver_service.create_driver(driver_request)
