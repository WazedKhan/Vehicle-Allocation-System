from enum import Enum


class DBCollections(str, Enum):
    EMPLOYEE = "employees"
    ALLOCATION = "allocations"
    VEHICLE = "vehicles"
