from app import db
from app.models.attendance import Attendance
from app.models.user import User
from datetime import datetime, date, timezone
from geopy.distance import geodesic
import uuid
import pytz
from sqlalchemy import extract, and_
from app.models.client import Client
from app.models.office import Office
from app.models.user import user_clients



IST = pytz.timezone('Asia/Kolkata')

def format_total_hours(hours_float):
    if hours_float is None:
        return None
    hours = int(hours_float)
    minutes = int((hours_float - hours) * 60)
    return f"{hours} {minutes}"


def to_ist_string(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt_ist = dt.astimezone(IST)
    return dt_ist.strftime('%Y-%m-%d %I:%M %p')



def punch_in(user_id, lat, lng, device_info=None):
    user = User.query.get(user_id)
    if not user:
        raise KeyError("User not found")
    if not user.office:
        raise KeyError("User has no office assigned")

    office = user.office
    dist = geodesic((lat, lng), (office.latitude, office.longitude)).meters
    if dist > office.radius_meters:
        raise ValueError(f"You must be within {office.radius_meters} meters of {office.name} to punch in")

    today = datetime.now(IST).date()
    exists = Attendance.query.filter_by(user_id=user_id, date=today).first()
    if exists:
        raise ValueError("Already punched in today")

    punch = Attendance(
        id=str(uuid.uuid4()),
        user_id=user_id,
        office_id=office.id,
        date=today,
        punch_in_time=datetime.now(IST),
        punch_in_device=device_info
    )
    db.session.add(punch)
    db.session.commit()

    return {
    "id": punch.id,
    "date": str(punch.date),
    "punch_in_time": to_ist_string(punch.punch_in_time),
    "punch_out_time": to_ist_string(punch.punch_out_time),
}


def punch_out(user_id, lat, lng, device_info=None):
    user = User.query.get(user_id)
    if not user:
        raise KeyError("User not found")
    if not user.office:
        raise KeyError("User has no office assigned")

    office = user.office
    dist = geodesic((lat, lng), (office.latitude, office.longitude)).meters
    if dist > office.radius_meters:
        raise ValueError(f"You must be within {office.radius_meters} meters of {office.name} to punch out")

    today = datetime.now(IST).date()
    att = Attendance.query.filter_by(user_id=user_id, date=today).first()

    if att is None:
        raise KeyError("No punch-in record found for today")
    if att.punch_in_time is None:
        raise ValueError("Punch-in time missing")
    if att.punch_out_time:
        raise ValueError("Already punched out today")

    now = datetime.now(IST)
    punch_in_time = att.punch_in_time
    if punch_in_time.tzinfo is None:
        punch_in_time = IST.localize(punch_in_time)

    hours = (now - punch_in_time).total_seconds() / 3600

    att.punch_out_time = now
    att.total_hours = round(hours, 2)
    att.punch_out_device = device_info
    db.session.commit()

    return {
    "id": att.id,
    "date": str(att.date),
    "punch_in_time": to_ist_string(punch_in_time),
    "punch_out_time": to_ist_string(att.punch_out_time),
    "total_hours": format_total_hours(att.total_hours),
}



def get_my_attendance(user_id, month, year):
    user = User.query.get(user_id)
    if not user:
        raise KeyError("User not found")

    records = Attendance.query.filter_by(user_id=user_id)\
        .filter(extract('month', Attendance.date) == month)\
        .filter(extract('year', Attendance.date) == year)\
        .order_by(Attendance.date.desc()).all()

    return [{
        "id": r.id,
        "date": str(r.date),
        "punch_in_time": r.punch_in_time,
        "punch_out_time": r.punch_out_time,
        "total_hours": format_total_hours(r.total_hours),
    } for r in records]



def get_all_attendance(role):
    query = Attendance.query.join(User)

    if role != 'ALL':
        query = query.filter(User.role == role)

    records = query.order_by(Attendance.date.desc()).all()

    return [{
    "id": r.id,
    "user_id": r.user_id,
    "user_name": r.user.name,
    "user_role": r.user.role.value,
    "user_designation": r.user.designation,
    "photo": r.user.photo,
    "date": str(r.date),
    "punch_in_time": r.punch_in_time,
    "punch_out_time": r.punch_out_time,
    "total_hours": format_total_hours(r.total_hours),
} for r in records]



def get_punch_status(user_id):
    user = User.query.get(user_id)
    if not user:
        raise KeyError("User not found")

    today = datetime.now(IST).date()
    record = Attendance.query.filter_by(user_id=user_id, date=today).first()

    if record:
        return {
            "punchedIn": record.punch_in_time is not None,
            "punchedOut": record.punch_out_time is not None,
            "punchInTime": record.punch_in_time,
            "punchOutTime": record.punch_out_time,
            "totalHours": format_total_hours(record.total_hours) if record.punch_out_time else None
        }
    else:
        return {
            "punchedIn": False,
            "punchedOut": False,
            "punchInTime": None,
            "punchOutTime": None,
            "totalHours": None
        }


def auto_punch_out_all():
    today = datetime.now(IST).date()
    now = datetime.now(IST)

    records = Attendance.query.filter(
        Attendance.date == today,
        Attendance.punch_in_time.isnot(None),
        Attendance.punch_out_time.is_(None)
    ).all()

    for att in records:
        punch_in_time = att.punch_in_time
        if punch_in_time.tzinfo is None:
            punch_in_time = IST.localize(punch_in_time)

        hours = (now - punch_in_time).total_seconds() / 3600
        att.punch_out_time = now
        att.total_hours = round(hours, 2)

    db.session.commit()
    return f"Auto-punched out {len(records)} users"


def get_all_attendance_filtered(office_id, client_id, month, year, role):
    query = Attendance.query.join(User).join(User.office)

    if client_id != 'ALL':
        query = query.join(User.clients) 

    filters = []

    if office_id != 'ALL':
        filters.append(Attendance.office_id == office_id)

    if client_id != 'ALL':
        filters.append(Client.id == client_id) 

    if month != 'ALL':
        filters.append(extract('month', Attendance.date) == month)

    if year != 'ALL':
        filters.append(extract('year', Attendance.date) == year)

    if role != 'ALL':
        filters.append(User.role == role)

    if filters:
        query = query.filter(and_(*filters))

    records = query.order_by(Attendance.date.desc()).all()

    return [{
        "id": r.id,
        "user_id": r.user_id,
        "user_name": r.user.name,
        "user_role": r.user.role.value if hasattr(r.user.role, 'value') else r.user.role,
        "user_designation": r.user.designation,
        "photo": r.user.photo,
        "office_id": r.office_id,
        "office_name": r.office.name if r.office else None,
        "date": str(r.date),
        "punch_in_time": r.punch_in_time,
        "punch_out_time": r.punch_out_time,
        "total_hours": format_total_hours(r.total_hours),
    } for r in records]
