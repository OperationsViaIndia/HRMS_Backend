from flask import request
from app.schemas.attendance_schema import PunchInSchema, PunchOutSchema
from app.services.attendance_service import (
    punch_in, punch_out, get_my_attendance,
    get_all_attendance, get_punch_status
)
from app.utils.response_wrapper import success_response, error_response
from app.middlewares.auth import authenticate, authorize


@authenticate()
@authorize(['ADMIN', 'EMPLOYEE'])
def punch_in_controller():
    try:
        data = PunchInSchema(**request.get_json()).dict()
        device_info = data.get("device_info")
        result = punch_in(request.user['id'], data['latitude'], data['longitude'], device_info)
        return success_response('Punched in', result)
    except KeyError as e:
        return error_response(str(e), 404)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
@authorize(['ADMIN', 'EMPLOYEE'])
def punch_out_controller():
    try:
        data = PunchOutSchema(**request.get_json()).dict()
        device_info = data.get("device_info")
        result = punch_out(request.user['id'], data['latitude'], data['longitude'], device_info)
        return success_response('Punched out', result)
    except KeyError as e:
        return error_response(str(e), 404)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
@authorize(['ADMIN', 'EMPLOYEE'])
def get_my_attendance_controller():
    try:
        result = get_my_attendance(request.user['id'])
        return success_response('My attendance', result)
    except KeyError as e:
        return error_response(str(e), 404)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def get_all_attendance_controller():
    try:
        role = request.args.get('role', 'ALL').upper()
        result = get_all_attendance(role)
        return success_response(f'Attendance for role: {role}', result)
    except KeyError as e:
        return error_response(str(e), 404)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
@authorize(['ADMIN', 'EMPLOYEE'])
def get_punch_status_controller():
    try:
        status = get_punch_status(request.user['id'])
        return success_response('Punch status', status)
    except KeyError as e:
        return error_response(str(e), 404)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)

