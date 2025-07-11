from flask import Blueprint
from app.controllers import client_controller

client_bp = Blueprint('client_bp', __name__)

client_bp.post('/create')(client_controller.create_client_controller)
client_bp.put('/update/<client_id>')(client_controller.update_client_controller)
client_bp.delete('/delete/<client_id>')(client_controller.delete_client_controller)
client_bp.get('/all')(client_controller.list_clients_controller)
