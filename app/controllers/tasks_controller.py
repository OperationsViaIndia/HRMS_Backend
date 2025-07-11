from flask import request
from app.schemas.tasks_schema import TasksRequestSchema
from app.services.task_service import create_task, get_all_tasks,get_all_tasks_id
from app.utils.response_wrapper import success_response, error_response
from app.middlewares.auth import authenticate, authorize

@authenticate()
@authorize(['EMPLOYEE', 'ADMIN'])
def create_task_controller():
    try:
        data = TasksRequestSchema(**request.json).dict()
        task = create_task(request.user['id'], data)
        return success_response("Task created successfully", {
            "id": task.id,
        })
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN', 'EMPLOYEE'])
def get_all_tasks_controller():
    try:
        tasks = get_all_tasks()
        result = [{
            "id": t.id,
            "user_id": t.user_id,
            "description": t.description,
            "date": t.date.isoformat(),
            "created_at": t.created_at.isoformat(),
            "updated_at": t.updated_at.isoformat()
        } for t in tasks]
        return success_response("Tasks fetched successfully", result)
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['ADMIN', 'EMPLOYEE'])
def get_task_by_id():
    try:
        task = get_all_tasks_id(request.user['id'])

        if not task:
            return error_response("Task not found",404)
        result = [{
            "id": t.id,
            "user_id": t.user_id,
            "description": t.description,
            "date": t.date.isoformat(),
            "created_at": t.created_at.isoformat(),
            "updated_at": t.updated_at.isoformat()
        } for t in task]
        return success_response("Task fetched sucessfully",result)
    except Exception as e:
        return error_response(str(e),500)
    