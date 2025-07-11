from app import db
import uuid

class Office(db.Model):
    __tablename__ = 'offices'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    radius_meters = db.Column(db.Float, default=10)

    users = db.relationship('User', back_populates='office', cascade='all, delete')
    attendances = db.relationship('Attendance', back_populates='office', cascade='all, delete')

