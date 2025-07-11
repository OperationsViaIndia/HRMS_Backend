from app import db
from datetime import datetime

class Holiday(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    festival_name = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(200), nullable=False)
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
