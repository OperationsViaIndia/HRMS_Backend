from pydantic import BaseModel, Field

class ReimbursementRequestSchema(BaseModel):
    amount: float = Field(..., gt=0)
    reason: str
