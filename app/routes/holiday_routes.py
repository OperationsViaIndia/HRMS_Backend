from flask import Blueprint
from app.controllers import holiday_controller
from app.middlewares.auth import authenticate, authorize

holiday_bp = Blueprint('holiday_bp', __name__)


holiday_bp.post('/add')(authenticate()(authorize(['SUPER_ADMIN', 'ADMIN'])(holiday_controller.add_holiday)))
holiday_bp.get('/list')(authenticate()(authorize(['SUPER_ADMIN', 'ADMIN', 'EMPLOYEE'])(holiday_controller.list_holidays)))
holiday_bp.put('/update/<holiday_id>')(authenticate()(authorize(['SUPER_ADMIN', 'ADMIN'])(holiday_controller.update_holiday)))
holiday_bp.delete('/delete/<holiday_id>')(authenticate()(authorize(['SUPER_ADMIN', 'ADMIN'])(holiday_controller.delete_holiday)))

