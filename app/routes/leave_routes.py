
from flask import Blueprint
from app.controllers import leave_controller

leave_bp = Blueprint('leave_bp', __name__)

leave_bp.post('/apply')(leave_controller.apply_leave)
leave_bp.get('/balance')(leave_controller.get_balance)
leave_bp.get('/')(leave_controller.get_all_leaves)
leave_bp.patch('/<id>')(leave_controller.approve)
leave_bp.get('/myLeaves')(leave_controller.get_my_leaves)
leave_bp.get('/myLeaves/all')(leave_controller.get_my_all_leaves)

