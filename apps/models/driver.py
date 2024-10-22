from pydantic import BaseModel


class Driver(BaseModel):
    id: int
    name: str
