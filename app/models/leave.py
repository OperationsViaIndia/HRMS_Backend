
from app import db
from datetime import datetime
import enum

class LeaveType(enum.Enum):
    SICK = 'SICK'
    CASUAL = 'CASUAL'

class LeaveRequestStatus(enum.Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

class LeaveStatus(db.Model):
    __tablename__ = 'leave'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Enum(LeaveType), nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(LeaveRequestStatus), default=LeaveRequestStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

