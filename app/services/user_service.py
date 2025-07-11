from app import db
from app.models.user import User
from app.utils.password_utils import hash_password
from app.models.user import Role, ProbationStatus, EmploymentType
from app.models.client import Client
from app.models.office import Office
from app.utils.user_formatter import format_user
from app.utils.client_formatter import format_clients
from app.utils.office_formatter import format_office
from app.models.attendance import Attendance
from app.models.leave import LeaveStatus
from app.models.reimbursement import Reimbursement
import uuid
import os
from werkzeug.utils import secure_filename
from flask import current_app
from app.models.message import Message
from sqlalchemy import or_
from datetime import datetime, timedelta
from app.utils.cloudinary_uploader import upload_to_cloudinary
from app.models.tasks import Tasks
from app.models.ticket import Ticket

def create_user(data, assigned_clients):
    office_id = data.get('office_id')

    if data['role'] == 'EMPLOYEE' and not office_id:
        raise ValueError("office_id required for EMPLOYEE")

    office = None
    if office_id:
        office = Office.query.get(office_id)
        if not office:
            raise KeyError("Office not found")

    user = User(
        id=str(uuid.uuid4()),
        name=data['name'],
        phone=data['phone'],
        email=data['email'],
        password=hash_password(data['password']),
        role=Role(data['role']),
        designation=data.get('designation'),
        aadhar=data.get('aadhar'),
        dob=data.get('dob'),
        employee_code=data.get('employee_code'),
        doj=data.get('doj'),
        employment_type=EmploymentType(data['employment_type']) if data.get('employment_type') else None,
        probation_status=ProbationStatus(data['probation_status']) if data.get('probation_status') else None,
        probation_salary=data.get('probation_salary'),
        full_time_salary=data.get('full_time_salary'),
        office_id=office.id if office else None,
        photo=data.get('photo')
    )

    user.clients.extend(assigned_clients)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_phone(phone):
    return User.query.filter_by(phone=phone).first()


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        raise KeyError("User not found")
    current_salary = None
    if user.probation_status == ProbationStatus.IN:
        current_salary = user.probation_salary
    elif user.probation_status == ProbationStatus.COMPLETED:
        current_salary = user.full_time_salary

    
    user.current_salary = current_salary
    user.employee_code = user.employee_code 

    return user



def get_users_by_role(role):
    try:
        return User.query.filter_by(role=Role(role)).all()
    except ValueError:
        raise ValueError("Invalid role provided")


def update_user(user_id, form_data, files_data):
    user = User.query.get(user_id)
    if not user:
        raise KeyError('User not found')

    allowed_fields = [
        'name', 'phone', 'email', 'designation', 'aadhar',
        'dob', 'doj', 'employment_type', 'probation_status',
        'probation_salary', 'full_time_salary', 'role', 'employee_code'
    ]

    for key in allowed_fields:
        value = form_data.get(key)
        if value is not None and value != '':
            setattr(user, key, value)

    office_id = form_data.get('office_id')
    if office_id is not None:
        office_id = office_id.strip()
        if office_id == '':
            user.office_id = None
        else:
            office = Office.query.get(office_id)
            if not office:
                raise KeyError('Office not found')
            user.office_id = office.id

    
    if 'photo' in files_data:
        photo = files_data['photo']
        photo_url = upload_to_cloudinary(photo, folder='user')  
        user.photo = photo_url

    db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        raise KeyError('User not found')

    super_admin = User.query.filter_by(role='SUPER_ADMIN').first()
    if not super_admin:
        raise KeyError('No SUPER_ADMIN user found')

    
    user.clients.clear()


    Tasks.query.filter_by(user_id=user_id).delete()
    Ticket.query.filter_by(user_id=user_id).delete()

    Attendance.query.filter_by(user_id=user_id).delete()
    LeaveStatus.query.filter_by(user_id=user_id).delete()
    Reimbursement.query.filter_by(user_id=user_id).delete()
    Message.query.filter(
        or_(Message.sender_id == user_id, Message.receiver_id == user_id)
    ).delete(synchronize_session=False)

    db.session.delete(user)
    db.session.commit()


def toggle_user_status(user_id):
    user = User.query.get(user_id)
    if not user:
        raise KeyError('User not found')

    user.is_active = not user.is_active
    db.session.commit()
    return user


def get_user_salaries(role):
    allowed_roles = [Role.EMPLOYEE, Role.ADMIN]

    if role.upper() == "ALL":
        users = User.query.filter(User.role.in_(allowed_roles), User.is_active.is_(True)).all()
    else:
        try:
            role_enum = Role(role.upper())
            if role_enum not in allowed_roles:
                raise ValueError("Access denied: Only EMPLOYEE and ADMIN roles are allowed.")
            users = User.query.filter_by(role=role_enum, is_active=True).all()
        except ValueError:
            raise ValueError("Invalid role provided.")

    salaries = []
    total = 0
    for u in users:
       
        current_salary = None
        if u.probation_status == ProbationStatus.IN:
            current_salary = u.probation_salary
        elif u.probation_status == ProbationStatus.COMPLETED:
            current_salary = u.full_time_salary

        salaries.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "phone": u.phone,
            "designation": u.designation,
            "role": u.role.value,
            "photo": u.photo,
            "probation_status": u.probation_status.name if u.probation_status else None,
            "probation_salary": u.probation_salary,
            "full_time_salary": u.full_time_salary,
            "currentSalary": current_salary
        })
        total += current_salary or 0

    return {
        "users": salaries,
        "totalMonthlySalary": total
    }


def get_admin_employee_users(role_filter):
    if role_filter == 'ALL':
        users = User.query.filter(User.role.in_([Role.ADMIN, Role.EMPLOYEE])).all()
    else:
        users = User.query.filter_by(role=Role(role_filter)).all()
    return users


def get_full_user_details(user_id):
    user = User.query.get(user_id)
    if not user:
        raise KeyError("User not found")

    user_data = format_user(user)
    office = user.office
    user_data["office"] = format_office(office) if office else None
    user_data["clients"] = format_clients(user.clients) if user.clients else []

    user_data["leaves"] = [
        {
            "id": leave.id,
            "type": leave.type.value,
            "status": leave.status.value,
            "from": leave.from_date.isoformat(),
            "to": leave.to_date.isoformat(),
            "reason": leave.reason,
        } for leave in getattr(user, 'leave_status', [])
    ]

    user_data["attendance"] = [
        {
            "id": att.id,
            "date": att.date.isoformat(),
            "punch_in": att.punch_in_time.isoformat() if att.punch_in_time else None,
            "punch_out": att.punch_out_time.isoformat() if att.punch_out_time else None,
            "total_hours": att.total_hours
        } for att in getattr(user, 'attendance', [])
    ]

    user_data["reimbursements"] = [
        {
            "id": r.id,
            "reason": r.reason,
            "amount": r.amount,
            "bill": r.bill,
            "status": r.status.value,
            "date": r.created_at.isoformat()
        } for r in getattr(user, 'reimbursements', [])
    ]
    user_data["tasks"] = [
        {
            "id": task.id,
            "description": task.description,
            "date": task.date.isoformat(),
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        } for task in getattr(user, 'tasks', [])
    ]
    user_data["tickets"] = [
        {
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "status": ticket.status.value,
            "created_at": ticket.created_at.isoformat(),
            "updated_at": ticket.updated_at.isoformat()
        } for ticket in getattr(user, 'tickets', [])
    ]
    return user_data


def get_users_exclude_self(role_filter, current_user_id):
    allowed_roles = [Role.SUPER_ADMIN, Role.ADMIN, Role.EMPLOYEE]

    query = User.query.filter(User.id != current_user_id)

    if role_filter.upper() != 'ALL':
        try:
            role = Role(role_filter.upper())
        except ValueError:
            raise ValueError("Invalid role filter.")
        if role not in allowed_roles:
            raise ValueError("Invalid role filter.")
        query = query.filter(User.role == role)
    else:
        query = query.filter(User.role.in_(allowed_roles))

    return query.all()
def get_next_birthdays():
    today = datetime.utcnow().date()

    users = User.query.filter(User.dob.isnot(None), User.is_active == True).all()

    upcoming = []

    for user in users:
        dob = user.dob
        next_birthday = dob.replace(year=today.year)

        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)

        days_until_birthday = (next_birthday - today).days

        upcoming.append({
            "id": user.id,
            "name": user.name,
            "dob": dob.isoformat(),
            "photo": user.photo,
            "next_birthday": next_birthday,
            "days_until_birthday": days_until_birthday
        })

    
    upcoming.sort(key=lambda x: x['days_until_birthday'])

    if not upcoming:
        return []

    nearest_days = upcoming[0]['days_until_birthday']

    
    nearest_birthdays = [u for u in upcoming if u['days_until_birthday'] == nearest_days]

    for u in nearest_birthdays:
        u.pop('days_until_birthday')
        u['next_birthday'] = u['next_birthday'].isoformat()

    return nearest_birthdays

    