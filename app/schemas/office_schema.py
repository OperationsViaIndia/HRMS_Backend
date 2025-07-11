from pydantic import BaseModel
from typing import Optional

class OfficeCreateSchema(BaseModel):
    name: str
    latitude: float
    longitude: float
    radius_meters: Optional[float] = 10

class OfficeUpdateSchema(BaseModel):
    name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    radius_meters: Optional[float]
