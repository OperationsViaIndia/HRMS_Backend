from pydantic import BaseModel, Field

class TicketRequestSchema(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
