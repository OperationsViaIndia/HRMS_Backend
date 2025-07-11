from flask import Blueprint
from app.controllers import reimbursement_controller

reimbursement_bp = Blueprint('reimbursement_bp', __name__)

reimbursement_bp.post('/create')(reimbursement_controller.create_reimbursement)
reimbursement_bp.get('/')(reimbursement_controller.get_all_reimbursements)
reimbursement_bp.patch('/<id>')(reimbursement_controller.approve)
reimbursement_bp.get('/pending')(reimbursement_controller.get_pending_reimbursements)

