from app import db
from app.models.association import user_clients


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.String(36), primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)

   
    users = db.relationship('User', secondary=user_clients, back_populates='clients')