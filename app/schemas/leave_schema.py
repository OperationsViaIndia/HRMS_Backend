
from pydantic import BaseModel
from datetime import date
from enum import Enum

class LeaveType(str, Enum):
    SICK = 'SICK'
    CASUAL = 'CASUAL'

class LeaveRequestSchema(BaseModel):
    type: LeaveType
    from_date: date
    to_date: date
    reason: str
