from app import db
from app.models.client import Client
import uuid

def create_client(data):
    client = Client(
        id=str(uuid.uuid4()),
        client_name=data['client_name'],
        project_name=data['project_name'],
        start_date=data['start_date']
    )
    db.session.add(client)
    db.session.commit()
    return client

def update_client(client_id, data):
    client = Client.query.get(client_id)
    if not client:
        raise Exception("Client not found")

    if data.get('client_name'):
        client.client_name = data['client_name']
    if data.get('project_name'):
        client.project_name = data['project_name']
    if data.get('start_date'):
        client.start_date = data['start_date']

    db.session.commit()
    return client

def delete_client(client_id):
    client = Client.query.get(client_id)
    print("!!!!!!!!!!!!!!1",client)
    if not client:
        raise Exception("Client not found")
    db.session.delete(client)
    db.session.commit()

def get_all_clients():
    clients = Client.query.all()
    return [{
        "id": c.id,
        "client_name": c.client_name,
        "project_name": c.project_name,
        "start_date": c.start_date.isoformat()
    } for c in clients]
