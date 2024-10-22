from os import name
from fastapi import FastAPI

from apps.database.mongodb import check_mongodb_connection

from apps.routers import allocation
from apps.routers import employee

app = FastAPI()

app.include_router(allocation.router, prefix="/api/v1/allocation", tags=["allocation"])
app.include_router(employee.router, prefix="/api/v1/employee", tags=["employee"])


@app.get("/")
def root():
    # check mongoDB connection stating of the project
    check_mongodb_connection()
    return {"message": "Vehicle Allocation System"}
