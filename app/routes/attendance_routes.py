from flask import Blueprint
from app.controllers import attendance_controller

attendance_bp = Blueprint('attendance_bp', __name__)

attendance_bp.post('/punchin')(attendance_controller.punch_in_controller)
attendance_bp.post('/punchout')(attendance_controller.punch_out_controller)
attendance_bp.get('/me')(attendance_controller.get_my_attendance_controller)
attendance_bp.get('/all')(attendance_controller.get_all_attendance_controller)
attendance_bp.get('/status')(attendance_controller.get_punch_status_controller)
