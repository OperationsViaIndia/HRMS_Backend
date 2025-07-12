from flask import request
from app.services.app_version_service import get_latest_version, add_app_version
from app.utils.response_wrapper import success_response, error_response

def check_update_controller():
    try:
        data = request.get_json()
        platform = data.get('platform')
        current_version = data.get('version')

        if not platform or not current_version:
            return error_response("Platform and version are required", 400)

        latest = get_latest_version(platform)
        if not latest:
            return success_response("No update available", {"update_available": False})

        update_available = latest.version != current_version

        return success_response("Version check complete", {
            "update_available": update_available,
            "force_update": latest.force_update,
            "download_url": latest.download_url,
            "latest_version": latest.version,
            "release_notes": latest.release_notes,
        })

    except Exception as e:
        return error_response(str(e), 500)


def add_version_controller():
    try:
        data = request.get_json()
        required_fields = ['platform', 'version']
        for field in required_fields:
            if field not in data:
                return error_response(f"{field} is required", 400)

        version = add_app_version(data)

        return success_response("App version added", {
            "id": version.id,
            "platform": version.platform,
            "version": version.version
        })

    except Exception as e:
        return error_response(str(e), 500)
