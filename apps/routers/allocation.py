from fastapi import APIRouter, Query
from typing import List
from apps.models.allocation import Allocation, AllocationCreate
from apps.services.allocation_src import AllocationService

router = APIRouter()

# Initialize the allocation service
allocation_service = AllocationService()


# Create a new allocation
@router.post("", response_model=dict)
def create_allocation(allocation_request: AllocationCreate):
    result = allocation_service.create_allocation(allocation_request)
    return result


# Get all allocations
@router.get("", response_model=list)
def get_allocations(vehicle_model: str = Query(None, description="Filter allocations by vehicle model")):
    return allocation_service.get_allocations(vehicle_model)


# Get a specific allocation by ID
@router.get("/{allocation_id}", response_model=Allocation)
def get_allocation_by_id(allocation_id: str):
    return allocation_service.get_allocation_by_id(allocation_id)


# Update an allocation
@router.patch("/{allocation_id}", response_model=dict)
def update_allocation(allocation_id: str, allocation_request: Allocation):
    result = allocation_service.update_allocation(allocation_id, allocation_request)
    return result


# Delete an allocation
@router.delete("/{allocation_id}", response_model=dict)
def delete_allocation(allocation_id: str):
    result = allocation_service.delete_allocation(allocation_id)
    return result
