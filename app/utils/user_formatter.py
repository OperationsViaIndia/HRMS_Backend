from flask import request

def format_client(client):
    return {
        "id": client.id,
        "client_name": client.client_name,
        "project_name": client.project_name,
        "start_date": client.start_date.isoformat() if client.start_date else None,
    }
def format_user(user):
    return {
        "id": user.id,
        "name": user.name,
        "phone": user.phone,
        "email": user.email,
        "photo": user.photo if user.photo else None,
        "role": user.role.value,
        "designation": user.designation,
        "employee_code": user.employee_code,
        "aadhar": user.aadhar,
        "dob": user.dob.isoformat() if user.dob else None,
        "doj": user.doj.isoformat() if user.doj else None,
        "employment_type": user.employment_type.value if user.employment_type else None,
        "probation_status": user.probation_status.value if user.probation_status else None,
        "probation_salary": user.probation_salary,
        "full_time_salary": user.full_time_salary,
        "current_salary": getattr(user, 'current_salary', None),
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
        "clients": [format_client(client) for client in user.clients] 
    }
def format_users(users):
    return [format_user(user) for user in users]