from app import db
from datetime import datetime

class AppVersion(db.Model):
    __tablename__ = 'app_versions'

    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.Enum('android', 'ios', 'web'), nullable=False) 
    version = db.Column(db.String(20), nullable=False)
    force_update = db.Column(db.Boolean, default=False)
    download_url = db.Column(db.Text)
    release_notes = db.Column(db.Text)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
