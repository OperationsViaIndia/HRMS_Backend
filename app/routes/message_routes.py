from flask import Blueprint
from app.controllers import message_controller

message_bp = Blueprint('message_bp', __name__)

message_bp.get('/conversation')(message_controller.get_conversation)
message_bp.post('/upload')(message_controller.upload_message_file)  
