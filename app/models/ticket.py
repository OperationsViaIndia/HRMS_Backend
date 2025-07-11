
from app import db
from datetime import datetime
import enum
import uuid

class TicketStatus(enum.Enum):
     PENDING = 'PENDING'
     APPROVED = 'APPROVED'
     REJECTED = 'REJECTED'

class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(TicketStatus), default=TicketStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Ticket {self.id}>"
