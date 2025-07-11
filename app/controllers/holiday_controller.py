from flask import request
from app.utils.response_wrapper import success_response, error_response
from app.services.holiday_service import save_holiday, get_all_holidays,delete_holiday_by_id,update_holiday_by_id
from app.schemas.holiday_schema import CreateHolidaySchema,UpdateHolidaySchema
from pydantic import ValidationError

def add_holiday():
    try:
        form = request.form.to_dict()
        file = request.files.get('photo')

        data = CreateHolidaySchema(**form).dict()
        holiday = save_holiday(data, file)

        return success_response("Holiday added successfully", {
            "id": holiday.id,
            "festival_name": holiday.festival_name,
           "photo": holiday.photo 
        })
    except ValidationError as ve:
        return error_response(str(ve), 400)
    except Exception as e:
        return error_response(str(e), 500)


def list_holidays():
    try:
        holidays = get_all_holidays()
        result = [
            {
                "id": h.id,
                "festival_name": h.festival_name,
                "photo": h.photo,
                "date_from": h.date_from.isoformat(),
                "date_to": h.date_to.isoformat() if h.date_to else None
            } for h in holidays
        ]
        return success_response("Holiday list fetched successfully", result)
    except Exception as e:
        return error_response(str(e), 500)
def update_holiday(holiday_id):
    try:
        form = request.form.to_dict()
        file = request.files.get('photo')

        data = UpdateHolidaySchema(**form).dict()
        holiday = update_holiday_by_id(holiday_id, data, file)

        return success_response("Holiday updated successfully", {
            "id": holiday.id,
            "festival_name": holiday.festival_name,
            "photo": holiday.photo,
            "date_from": holiday.date_from.isoformat(),
            "date_to": holiday.date_to.isoformat() if holiday.date_to else None
        })
    except ValidationError as ve:
        return error_response(str(ve), 400)
    except Exception as e:
        return error_response(str(e), 500)


def delete_holiday(holiday_id):
    try:
        delete_holiday_by_id(holiday_id)
        return success_response("Holiday deleted successfully")
    except Exception as e:
        return error_response(str(e), 500)