
from app import db
from datetime import datetime
import enum

class ReimbursementStatus(enum.Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

class Reimbursement(db.Model):
    __tablename__ = 'reimbursement'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    bill = db.Column(db.String(255), nullable=True)  # file path
    status = db.Column(db.Enum(ReimbursementStatus), default=ReimbursementStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)