# from app import db
# from datetime import datetime

# class Attendance(db.Model):
#     __tablename__ = 'attendance'
#     __table_args__ = (db.UniqueConstraint('user_id', 'date', name='_user_date_uc'),)

#     id = db.Column(db.String(36), primary_key=True)
#     user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
#     office_id = db.Column(db.String(36), db.ForeignKey('offices.id'), nullable=False)
#     date = db.Column(db.Date, default=datetime.utcnow)
#     punch_in_time = db.Column(db.DateTime, nullable=True)
#     punch_out_time = db.Column(db.DateTime, nullable=True)
#     total_hours = db.Column(db.Float, nullable=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # user = db.relationship('User', backref=db.backref('attendances', lazy=True))
#     office = db.relationship('Office', back_populates='attendances')

from app import db
from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')

def now_ist():
    return datetime.now(IST)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    __table_args__ = (db.UniqueConstraint('user_id', 'date', name='_user_date_uc'),)

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    office_id = db.Column(db.String(36), db.ForeignKey('offices.id'), nullable=False)

    date = db.Column(db.Date, default=lambda: now_ist().date())

    punch_in_time = db.Column(db.DateTime, nullable=True)
    punch_out_time = db.Column(db.DateTime, nullable=True)
    total_hours = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=now_ist)
    updated_at = db.Column(db.DateTime(timezone=True), default=now_ist, onupdate=now_ist)

    office = db.relationship('Office', back_populates='attendances')
