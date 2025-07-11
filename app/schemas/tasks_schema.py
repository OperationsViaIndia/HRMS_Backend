from pydantic import BaseModel
from datetime import date
from typing import Optional

class TasksRequestSchema(BaseModel):
    date: date
    description: str


