from app import db
from app.models.attendance import Attendance
from app.models.user import User
from datetime import datetime, date, timezone
from geopy.distance import geodesic
import uuid
# from pytz import utc
import pytz

IST = pytz.timezone('Asia/Kolkata')


# def to_ist(dt):
#     if dt is None:
#         return None
#     if dt.tzinfo is None:
#         dt = utc.localize(dt)
#     return dt.astimezone(IST).strftime('%Y-%m-%d %H:%M:%S')


def punch_in(user_id, lat, lng):
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
    )
    db.session.add(punch)
    db.session.commit()

    return {
        "id": punch.id,
        "date": str(punch.date),
        "punch_in_time": punch.punch_in_time,
        "punch_out_time": punch.punch_out_time,
    }


def punch_out(user_id, lat, lng):
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
    db.session.commit()

    return {
        "id": att.id,
        "date": str(att.date),
        "punch_in_time": punch_in_time,
        "punch_out_time": att.punch_out_time,
        "total_hours": att.total_hours,
    }


def get_my_attendance(user_id):
    user = User.query.get(user_id)
    if not user:
        raise KeyError("User not found")

    records = Attendance.query.filter_by(user_id=user_id).order_by(Attendance.date.desc()).all()
    return [{
        "id": r.id,
        "date": str(r.date),
        "punch_in_time": r.punch_in_time,
        "punch_out_time": r.punch_out_time,
        "total_hours": r.total_hours,
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
        "photo":r.user.photo,
        "date": str(r.date),
        "punch_in_time": r.punch_in_time,
        "punch_out_time": r.punch_out_time,
        "total_hours": r.total_hours,
    } for r in records]


def get_punch_status(user_id):
    user = User.query.get(user_id)
    if not user:
        raise KeyError("User not found")

    today = datetime.now(IST).date()
    record = Attendance.query.filter_by(user_id=user_id, date=today).first()
    return not record
