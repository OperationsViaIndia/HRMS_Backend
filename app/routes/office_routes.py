from flask import Blueprint
from app.controllers import office_controller

office_bp = Blueprint('office_bp', __name__)

office_bp.post('/create')(office_controller.create_office_controller)
office_bp.put('/update/<office_id>')(office_controller.update_office_controller)
office_bp.delete('/delete/<office_id>')(office_controller.delete_office_controller)
office_bp.get('/all')(office_controller.get_all_offices_controller)
office_bp.get('/getById/<office_id>')(office_controller.get_office_by_id_controller)
office_bp.get('/allEmployee/<office_id>/employees')(office_controller.get_office_employees_controller)
