from flask import Blueprint
from app.controllers import ticket_controller

ticket_bp = Blueprint('ticket_bp', __name__)

ticket_bp.post('/create')(ticket_controller.raise_ticket)
ticket_bp.get('/')(ticket_controller.get_all_tickets)
ticket_bp.put('/<ticket_id>')(ticket_controller.update_status)
ticket_bp.get('/pending')(ticket_controller.get_pending_tickets)
