import uuid
import os
from app import db
from app.models.holiday import Holiday
from app.utils.cloudinary_uploader import upload_to_cloudinary




def save_holiday(data, file):
    if not file:
        raise Exception("Photo file is required")

    photo_url = upload_to_cloudinary(file, folder='holidays')

    holiday = Holiday(
        id=str(uuid.uuid4()),
        festival_name=data['festival_name'],
        photo=photo_url,
        date_from=data['date_from'],
        date_to=data.get('date_to') or data['date_from'],
    )
    db.session.add(holiday)
    db.session.commit()
    return holiday


def get_all_holidays():
    return Holiday.query.order_by(Holiday.date_from.asc()).all()
def update_holiday_by_id(holiday_id, data, file):
    holiday = Holiday.query.get(holiday_id)
    if not holiday:
        raise Exception("Holiday not found")

    if data.get('festival_name'):
        holiday.festival_name = data['festival_name']
    if data.get('date_from'):
        holiday.date_from = data['date_from']
    if data.get('date_to'):
        holiday.date_to = data['date_to']

    if file:
        photo_url = upload_to_cloudinary(file, folder='holidays')
        holiday.photo = photo_url

    db.session.commit()
    return holiday


def delete_holiday_by_id(holiday_id):
    holiday = Holiday.query.get(holiday_id)
    if not holiday:
        raise Exception("Holiday not found")

    db.session.delete(holiday)
    db.session.commit()
