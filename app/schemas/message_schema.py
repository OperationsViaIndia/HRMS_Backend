from pydantic import BaseModel
from typing import Optional

class SendMessageSchema(BaseModel):
    sender_id: str
    receiver_id: str
    content: Optional[str] = None
