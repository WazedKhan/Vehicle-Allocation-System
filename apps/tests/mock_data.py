class MockAllocation:
    def __init__(self, vehicle_id="64db1fd3e5554d431fe5a6b4", employee_id="64db1fd3e5554d431fe5a6b5", allocation_date=None):
        self.vehicle_id = vehicle_id
        self.employee_id = employee_id
        self.allocation_date = allocation_date if allocation_date else date.today()

    def model_dump(self):
        return {
            "vehicle_id": self.vehicle_id,
            "employee_id": self.employee_id,
            "allocation_date": self.allocation_date
        }
