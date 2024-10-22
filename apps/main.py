from os import name
from fastapi import FastAPI

from apps.database.mongodb import check_mongodb_connection

from apps.routers import allocation, employee, driver, vehicle

app = FastAPI()

app.include_router(allocation.router, prefix="/api/v1/allocation", tags=["allocation"])
app.include_router(employee.router, prefix="/api/v1/employee", tags=["employee"])
app.include_router(driver.router, prefix="/api/v1/driver", tags=["driver"])
app.include_router(vehicle.router, prefix="/api/v1/vehicle", tags=["vehicle"])


@app.get("/")
def root():
    # check mongoDB connection stating of the project
    check_mongodb_connection()
    return {"message": "Vehicle Allocation System"}
