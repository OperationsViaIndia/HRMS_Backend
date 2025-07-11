from pydantic import BaseModel

class PunchInSchema(BaseModel):
    latitude: float
    longitude: float

class PunchOutSchema(BaseModel):
    latitude: float
    longitude: float
