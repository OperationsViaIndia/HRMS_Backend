from flask import Blueprint
from app.controllers.tasks_controller import (
    create_task_controller,
    get_all_tasks_controller,
    get_task_by_id
)

tasks_bp = Blueprint('tasks', __name__)

tasks_bp.route('/create', methods=['POST'])(create_task_controller)
tasks_bp.route('/all', methods=['GET'])(get_all_tasks_controller)
tasks_bp.route('/own', methods=['GET'])(get_task_by_id)
