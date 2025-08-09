
from flask import request
from app.schemas.reimbursement_schema import ReimbursementRequestSchema
from app.services.reimbursement_service import request_reimbursement, list_reimbursements, approve_reimbursement,list_pending_reimbursements
from app.utils.response_wrapper import success_response, error_response
from app.middlewares.auth import authenticate, authorize

import os

UPLOAD_FOLDER = 'uploads/bills'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@authenticate()
@authorize(['EMPLOYEE', 'ADMIN'])
def create_reimbursement():
    try:
        data = ReimbursementRequestSchema(**request.form).dict()
        file = request.files.get('bill')  
        reimb = request_reimbursement(request.user['id'], data, file)

        return success_response('Reimbursement requested', {
            'id': reimb.id,
            'status': reimb.status.value
        })
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN', 'EMPLOYEE'])
def get_all_reimbursements():
    try:
        items = list_reimbursements(request.user)
        result = [{
            'id': i.id,
            'amount': i.amount,
            'reason': i.reason,
            'bill': i.bill,
            'status': i.status.value,
            "created_at":i.created_at
        } for i in items]
        return success_response('Reimbursements fetched', result)
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['ADMIN', 'SUPER_ADMIN'])
def approve(id):
    try:
        reimb = approve_reimbursement(id, request.get_json()['status'])
        return success_response('Reimbursement status updated', {
            'id': reimb.id,
            'status': reimb.status.value
        })
    except Exception as e:
        return error_response(str(e), 400)
@authenticate()
@authorize(['ADMIN', 'SUPER_ADMIN'])
def get_pending_reimbursements():
    try:
        results = list_pending_reimbursements()
        data = []
        for reimb, user in results:
            data.append({
                'id': reimb.id,
                'user_id': user.id,
                'name': user.name,
                'designation': user.designation,
                'amount': reimb.amount,
                'reason': reimb.reason,
                'bill': reimb.bill,
                'status': reimb.status.value,
                "photo":user.photo,
                "created_at":reimb.created_at
            })
        return success_response('Pending reimbursements fetched', data)
    except Exception as e:
        return error_response(str(e), 400)
