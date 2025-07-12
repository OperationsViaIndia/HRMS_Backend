from flask import Blueprint
from app.controllers.app_version_controller import check_update_controller, add_version_controller

app_version_bp = Blueprint('app_version_bp', __name__)

app_version_bp.route('/check_update', methods=['POST'])(check_update_controller)
app_version_bp.route('/add_version', methods=['POST'])(add_version_controller)
