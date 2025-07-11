from app import db

user_clients = db.Table(
    'user_clients',
    db.Column('user_id', db.String(36), db.ForeignKey('user.id'), primary_key=True),
    db.Column('client_id', db.String(36), db.ForeignKey('client.id'), primary_key=True)
)
