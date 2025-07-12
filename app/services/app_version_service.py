from app.models.app_version import AppVersion
from app import db

def get_latest_version(platform):
    return AppVersion.query.filter_by(platform=platform).order_by(AppVersion.id.desc()).first()

def add_app_version(data):
    version = AppVersion(
        platform=data['platform'],
        version=data['version'],
        force_update=data.get('force_update', False),
        download_url=data.get('download_url'),
        release_notes=data.get('release_notes')
    )
    db.session.add(version)
    db.session.commit()
    return version
