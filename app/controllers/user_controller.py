import os
import uuid
from flask import request, current_app
from pydantic import ValidationError
from app.services.user_service import (
    create_user, get_user_by_email, get_user_by_phone, get_user_by_id,
    get_users_by_role, update_user, delete_user, toggle_user_status,
    get_user_salaries, get_admin_employee_users, get_full_user_details,
    get_users_exclude_self,get_next_birthdays
)
from app.utils.response_wrapper import success_response, error_response
from app.utils.jwt_utils import sign_access_token, sign_refresh_token
from app.utils.password_utils import verify_password
from app.schemas.user_schema import UserRegisterSchema
from app.middlewares.auth import authenticate, authorize
from app.models.client import Client
from app.utils.user_formatter import format_user,format_users
from app.utils.cloudinary_uploader import upload_to_cloudinary


def register():
    try:
        data = request.form.to_dict()
        role = data.get('role')
        if not role:
            return error_response("Role is required", 400)

        validated_data = UserRegisterSchema(**data)

        if get_user_by_email(validated_data.email):
            return error_response("Email already exists.", 400)
        if get_user_by_phone(validated_data.phone):
            return error_response("Phone number already exists.", 400)

        assigned_clients = []
        if role == 'EMPLOYEE':
            client_ids = request.form.getlist('clients[]')
            if not client_ids:
                return error_response("At least one client must be assigned for EMPLOYEE", 400)
            for cid in client_ids:
                client = Client.query.get(cid)
                if not client:
                    return error_response(f"Client ID {cid} not found", 404)
                assigned_clients.append(client)
        elif role not in ['ADMIN', 'SUPER_ADMIN']:
            return error_response(f"Invalid role: {role}", 400)

        
        photo_file = request.files.get('photo')
        photo_path = None
        if photo_file:
            photo_path = upload_to_cloudinary(photo_file, folder='user')

       
        user_data = validated_data.dict()
        user_data["photo"] = photo_path

        user = create_user(user_data, assigned_clients)
        return success_response("User registered successfully", format_user(user), 201)

    except ValidationError as ve:
        return error_response(str(ve), 400)
    except Exception as e:
        return error_response(str(e), 500)


def login():
    try:
        data = request.get_json()
        user = get_user_by_phone(data['phone'])

        if not user or not verify_password(data['password'], user.password):
            return error_response('Invalid credentials', 401)
        if not user.is_active:
            return error_response('User is deactivated.', 403)

        access_token = sign_access_token({"id": user.id, "role": user.role.value})
        refresh_token = sign_refresh_token({"id": user.id})

        return success_response('Login successful', {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": format_user(user)
        })

    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
def get_logged_in_user():
    try:
        user = get_user_by_id(request.user['id'])
        return success_response('User fetched', {"user": format_user(user)})
    except KeyError as ke:
        return error_response(str(ke), 404)
    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def get_users_by_role_controller(role):
    try:
        users = get_users_by_role(role)
        return success_response('Users fetched', format_users(users))
    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def update_user_controller(id):
    try:
        updated = update_user(id, request.form, request.files)
        return success_response('User updated', {"id": updated.id})
    except KeyError as ke:
        return error_response(str(ke), 404)
    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def delete_user_controller(id):
    try:
        delete_user(id)
        return success_response('User deleted')
    except KeyError as ke:
        return error_response(str(ke), 404)
    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def toggle_user_status_controller(id):
    try:
        updated = toggle_user_status(id)
        return success_response('User status toggled', {
            "id": updated.id,
            "is_active": updated.is_active
        })
    except KeyError as ke:
        return error_response(str(ke), 404)
    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def get_user_salaries_controller(role):
    try:
        data = get_user_salaries(role)
        return success_response(f"Salaries for {role}", data)
    except ValueError as ve:
        return error_response(str(ve), 400)
    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def list_admin_employee_controller(role):
    try:
        role_filter = role.upper()
        if role_filter not in ['ADMIN', 'EMPLOYEE', 'ALL']:
            return error_response("Invalid role filter. Use ADMIN, EMPLOYEE, or ALL", 400)
        users = get_admin_employee_users(role_filter)
        return success_response("Filtered user list", format_users(users))
    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def get_full_user_details_controller(user_id):
    try:
        result = get_full_user_details(user_id)
        return success_response("User full details fetched", result)
    except KeyError as ke:
        return error_response(str(ke), 404)
    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
def get_other_users_list(role):
    try:
        current_user_id = request.user['id']
        users = get_users_exclude_self(role, current_user_id)
        return success_response(f"Users list excluding self with filter: {role}", format_users(users))
    except Exception as e:
        return error_response(str(e), 500)
@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN', 'EMPLOYEE'])
def get_next_birthdays_controller():
    try:
        birthdays = get_next_birthdays()
        return success_response(
            "Next upcoming birthday(s)",
            birthdays
        )
    except Exception as e:
        return error_response(str(e), 500)

