from flask import request
from app.schemas.office_schema import OfficeCreateSchema, OfficeUpdateSchema
from app.services import office_service
from app.utils.response_wrapper import success_response, error_response
from pydantic import ValidationError
from app.middlewares.auth import authenticate, authorize

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def create_office_controller():
    try:
        data = OfficeCreateSchema(**request.get_json()).dict()
        office = office_service.create_office(data)
        return success_response('Office created', {
            "id": office.id,
            "name": office.name,
            "latitude": office.latitude,
            "longitude": office.longitude,
            "radius_meters": office.radius_meters
        })
    except ValidationError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def update_office_controller(office_id):
    try:
        data = OfficeUpdateSchema(**request.get_json()).dict(exclude_unset=True)
        office = office_service.update_office(office_id, data)
        return success_response('Office updated', {
            "id": office.id,
            "name": office.name,
            "latitude": office.latitude,
            "longitude": office.longitude,
            "radius_meters": office.radius_meters
        })
    except ValidationError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def delete_office_controller(office_id):
    try:
        office_service.delete_office(office_id)
        return success_response('Office deleted', {})
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def get_all_offices_controller():
    try:
        offices = office_service.get_all_offices()
        return success_response('All offices', [{
            "id": o.id,
            "name": o.name,
            "latitude": o.latitude,
            "longitude": o.longitude,
            "radius_meters": o.radius_meters
        } for o in offices])
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def get_office_by_id_controller(office_id):
    try:
        o = office_service.get_office_by_id(office_id)
        if not o:
            return error_response("Office not found", 404)
        return success_response('Office details', {
            "id": o.id,
            "name": o.name,
            "latitude": o.latitude,
            "longitude": o.longitude,
            "radius_meters": o.radius_meters
        })
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def get_office_employees_controller(office_id):
    try:
        role = request.args.get('role') 
        employees = office_service.get_office_employees(office_id, role)
        return success_response('Office employees', [{
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "phone": u.phone,
            "role": u.role.name  
        } for u in employees])
    except Exception as e:
        return error_response(str(e), 400)
