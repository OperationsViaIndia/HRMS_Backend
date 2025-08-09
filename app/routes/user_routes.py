from flask import Blueprint
from app.controllers import user_controller
from app.middlewares.auth import authenticate, authorize

user_bp = Blueprint('user_bp', __name__)


user_bp.post('/register')(user_controller.register)
user_bp.post('/login')(user_controller.login)


user_bp.get('/profile')(authenticate()(user_controller.get_logged_in_user))
user_bp.get('/data/<role>')(
    authenticate()(authorize(['SUPER_ADMIN', 'ADMIN'])(user_controller.get_users_by_role_controller))
)
user_bp.put('/update/<id>')(
    authenticate()(authorize(['SUPER_ADMIN', 'ADMIN'])(user_controller.update_user_controller))
)
user_bp.delete('/delete/<id>')(
    authenticate()(authorize(['SUPER_ADMIN', 'ADMIN'])(user_controller.delete_user_controller))
)
user_bp.patch('/status/<id>/toggle')(
    authenticate()(authorize(['SUPER_ADMIN', 'ADMIN'])(user_controller.toggle_user_status_controller))
)
user_bp.get('/salaries/<role>')(
    authenticate()(authorize(['SUPER_ADMIN', 'ADMIN'])(user_controller.get_user_salaries_controller))
)
user_bp.get('/all_users/<role>')(
    authenticate()(authorize(['SUPER_ADMIN', 'ADMIN'])(user_controller.list_admin_employee_controller))
)
user_bp.get('/user-details/<user_id>')(
    authenticate()(authorize(['SUPER_ADMIN', 'ADMIN'])(user_controller.get_full_user_details_controller))
)
user_bp.get('/message-users/<role>')( 
    authenticate()(user_controller.get_other_users_list)
)
user_bp.get('/recent-birthdays')(
    authenticate()(authorize(['SUPER_ADMIN', 'ADMIN', 'EMPLOYEE'])(user_controller.get_next_birthdays_controller))
)





