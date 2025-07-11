from app import db
from app.models.office import Office
import uuid

def create_office(data):
    office = Office(
        id=str(uuid.uuid4()),
        name=data['name'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        radius_meters=data.get('radius_meters', 10)
    )
    db.session.add(office)
    db.session.commit()
    return office

def update_office(office_id, data):
    office = Office.query.get(office_id)
    if not office:
        raise Exception("Office not found")

    if 'name' in data:
        office.name = data['name']
    if 'latitude' in data:
        office.latitude = data['latitude']
    if 'longitude' in data:
        office.longitude = data['longitude']
    if 'radius_meters' in data:
        office.radius_meters = data['radius_meters']

    db.session.commit()
    return office

def delete_office(office_id):
    office = Office.query.get(office_id)
    if not office:
        raise Exception("Office not found")
    db.session.delete(office)
    db.session.commit()

def get_all_offices():
    return Office.query.all()

def get_office_by_id(office_id):
    return Office.query.get(office_id)

def get_office_employees(office_id, role=None):
    office = Office.query.get(office_id)
    if not office:
        raise Exception("Office not found")

    if role:
        
        role = role.upper()
        from app.models.user import Role 
        if role not in Role.__members__:
            raise Exception(f"Invalid role: {role}")

        return [u for u in office.users if u.role.name == role]
    
    return office.users
