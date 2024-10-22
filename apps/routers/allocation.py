from fastapi import APIRouter
from typing import List
from apps.models.allocation import Allocation
from apps.services.allocation import AllocationService

router = APIRouter()

# Initialize the allocation service
allocation_service = AllocationService()


# Create a new allocation
@router.post("", response_model=dict)
def create_allocation(allocation_request: Allocation):
    result = allocation_service.create_allocation(allocation_request)
    return result


# Get all allocations
@router.get("", response_model=List[Allocation])
def get_allocations():
    print("fucl:", allocation_service.get_allocations())
    return allocation_service.get_allocations()


# Get a specific allocation by ID
@router.get("/{allocation_id}", response_model=Allocation)
def get_allocation_by_id(allocation_id: str):
    return allocation_service.get_allocation_by_id(allocation_id)


# Update an allocation
@router.put("/{allocation_id}", response_model=dict)
def update_allocation(allocation_id: str, allocation_request: Allocation):
    result = allocation_service.update_allocation(allocation_id, allocation_request)
    return result


# Delete an allocation
@router.delete("/{allocation_id}", response_model=dict)
def delete_allocation(allocation_id: str):
    result = allocation_service.delete_allocation(allocation_id)
    return result
