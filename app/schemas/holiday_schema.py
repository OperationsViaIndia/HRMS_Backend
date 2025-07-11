from pydantic import BaseModel, constr
from typing import Optional
from datetime import date

class CreateHolidaySchema(BaseModel):
    festival_name: str
    date_from: date
    date_to: Optional[date]

class UpdateHolidaySchema(BaseModel):
    festival_name: Optional[str]
    date_from: Optional[date]
    date_to: Optional[date]

