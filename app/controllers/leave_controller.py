from flask import request
from app.services.leave_service import request_leave, get_leave_balance, list_leaves, approve_leave,list_user_leaves,list_user_all_leaves
from app.utils.response_wrapper import success_response, error_response
from app.schemas.leave_schema import LeaveRequestSchema
from app.middlewares.auth import authenticate, authorize

@authenticate()
@authorize(['EMPLOYEE', 'ADMIN'])
def apply_leave():
    try:
        data = LeaveRequestSchema(**request.get_json()).dict()
        leave = request_leave(request.user['id'], data)
        return success_response('Leave requested', {
            "id": leave.id,
            "status": leave.status.value
        })
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['EMPLOYEE', 'ADMIN'])
def get_balance():
    try:
        bal = get_leave_balance(request.user['id'])
        return success_response('Balance fetched', bal)
    except Exception as e:
        return error_response(str(e), 400)


@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN', 'EMPLOYEE'])
def get_all_leaves():
    try:
        leaves = list_leaves(request.user)
        result = [{
            "id": l.id,
            "user_id": l.user_id,
            "name": l.user.name if l.user else "Unknown",
            "designation": l.user.designation if l.user else "Unknown",
            "photo":l.user.photo if l.user else "null",
            "type": l.type.value,
            "from_date": l.from_date.isoformat(),
            "to_date": l.to_date.isoformat(),
            "status": l.status.value,
            "reason": l.reason,
            "created_at": l.created_at
        } for l in leaves]
        return success_response('Pending leaves fetched', result)
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def approve(id):
    try:
        leave = approve_leave(id, request.get_json()['status'])
        return success_response('Leave status updated', {
            "id": leave.id,
            "status": leave.status.value
        })
    except Exception as e:
        return error_response(str(e), 400)

    
@authenticate()
@authorize(['EMPLOYEE', 'ADMIN'])
def get_my_leaves():
    try:
        leave_type = request.args.get('type', 'ALL').upper()
        user_id = request.user['id']

        leaves = list_user_leaves(user_id, leave_type)

        result = [{
            "id": l.id,
            "type": l.type.value,
            "from_date": l.from_date.isoformat(),
            "to_date": l.to_date.isoformat(),
            "status": l.status.value,
            "reason": l.reason,
            "created_at": l.created_at.isoformat(),
            "name": l.user.name if l.user else None,
            "photo": l.user.photo if l.user else None
        } for l in leaves]

        return success_response('My leaves fetched', result)
    except Exception as e:
        return error_response(str(e), 400)
@authenticate()
@authorize(['EMPLOYEE', 'ADMIN'])
def get_my_all_leaves():
    try:
        user_id = request.user['id']
        leaves = list_user_all_leaves(user_id)
        print(leaves)
        result = [{
            "id": l.id,
            "type": l.type.value,
            "from_date": l.from_date.isoformat(),
            "to_date": l.to_date.isoformat(),
            "status": l.status.value,
            "reason": l.reason,
            "created_at": l.created_at.isoformat(),
            "name": l.user.name if l.user else None,
            "photo": l.user.photo if l.user else None
        } for l in leaves]
        return success_response('My Leave List', result)
    except Exception as e:
        return error_response(str(e), 400)

