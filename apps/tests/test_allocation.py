import pytest
from unittest.mock import MagicMock
from bson import ObjectId
from fastapi import HTTPException
from apps.models.allocation import Allocation
from apps.services.allocation import AllocationService


@pytest.fixture
def allocation_service():
    return AllocationService()

def test_create_allocation_success(allocation_service):
    allocation_request = Allocation(
        employee_id="6717edce01192f03e540d464",
        vehicle_id="671893eb47867a11e095c0c7",
        allocation_date="2024-10-25"
    )

    mock_vehicle = {"_id": ObjectId("671893eb47867a11e095c0c7")}
    allocation_service.vehicle_collection.find_one = MagicMock(return_value=mock_vehicle)
    allocation_service.redis_cache.get = MagicMock(return_value=None)
    allocation_service.redis_cache.set = MagicMock()
    allocation_service.collection.find_one = MagicMock(return_value=None)
    allocation_service.collection.insert_one = MagicMock(return_value=MagicMock(inserted_id=ObjectId("6717edce01192f03e540d464")))

    result = allocation_service.create_allocation(allocation_request)
    assert result == {"message": "Allocation created successfully", "allocation_id": "6717edce01192f03e540d464"}

def test_create_allocation_vehicle_not_found(allocation_service):
    allocation_request = Allocation(
        employee_id="6717edce01192f03e540d464",
        vehicle_id="671893eb47867a11e095c0c7",
        allocation_date="2024-10-25"
    )

    # Mock the vehicle collection to return None, simulating a vehicle not found
    allocation_service.vehicle_collection.find_one = MagicMock(return_value=None)

    # Mock the Redis cache to simulate a cache miss
    allocation_service.redis_cache.get = MagicMock(return_value=None)

    # Mock the existing allocation check to ensure it returns None
    allocation_service.collection.find_one = MagicMock(return_value=None)

    with pytest.raises(HTTPException) as excinfo:
        allocation_service.create_allocation(allocation_request)

    assert excinfo.value.status_code == 404  # Expecting a 404 status code for vehicle not found
    assert excinfo.value.detail == "Vehicle not found"  # Expecting this detail message


def test_get_allocations_success(allocation_service):
    from datetime import datetime  # Add this import

    allocation_data = [
        {
            "_id": ObjectId("6717edce01192f03e540d464"),
            "employee_id": "6717edce01192f03e540d464",
            "vehicle_id": "671893eb47867a11e095c0c7",
            "allocation_date": datetime(2024, 10, 25)
        }
    ]

    allocation_service.collection.find = MagicMock(return_value=allocation_data)

    allocations = allocation_service.get_allocations()
    assert len(allocations) == 1
    assert allocations[0]["_id"] == str(allocation_data[0]["_id"])

def test_get_allocation_by_id_success(allocation_service):
    from datetime import datetime  # Add this import

    allocation_id = "6717edce01192f03e540d464"
    allocation_data = {
        "_id": ObjectId(allocation_id),
        "employee_id": "6717edce01192f03e540d464",
        "vehicle_id": "671893eb47867a11e095c0c7",
        "allocation_date": datetime(2024, 10, 25)
    }

    allocation_service.collection.find_one = MagicMock(return_value=allocation_data)

    allocation = allocation_service.get_allocation_by_id(allocation_id)
    assert str(allocation["_id"]) == str(allocation_data["_id"])

def test_update_allocation_success(allocation_service):
    from datetime import datetime  # Add this import

    allocation_id = "6717edce01192f03e540d464"
    allocation_request = Allocation(
        employee_id="6717edce01192f03e540d464",
        vehicle_id="671893eb47867a11e095c0c7",
        allocation_date="2024-10-25"
    )

    existing_allocation = {
        "_id": ObjectId(allocation_id),
        "employee_id": "6717edce01192f03e540d464",
        "vehicle_id": "671893eb47867a11e095c0c7",
        "allocation_date": datetime(2024, 10, 25)
    }

    allocation_service.collection.find_one = MagicMock(return_value=existing_allocation)
    allocation_service.collection.update_one = MagicMock(return_value=MagicMock(modified_count=1))

    result = allocation_service.update_allocation(allocation_id, allocation_request)
    assert result == {"message": "Allocation updated successfully", "allocation_id": allocation_id}
