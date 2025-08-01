from pydantic import BaseModel

class PunchInSchema(BaseModel):
    latitude: float
    longitude: float
    device_info: str 

class PunchOutSchema(BaseModel):
    latitude: float
    longitude: float
    device_info: str 