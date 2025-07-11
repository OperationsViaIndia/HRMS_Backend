from pydantic import BaseModel
from datetime import date
from typing import Optional

class ClientCreateSchema(BaseModel):
    client_name: str
    project_name: str
    start_date: date

class ClientUpdateSchema(BaseModel):
    client_name: Optional[str]
    project_name: Optional[str]
    start_date: Optional[date]
