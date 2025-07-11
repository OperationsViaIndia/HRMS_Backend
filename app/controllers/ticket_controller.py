from flask import request
from app.schemas.ticket_schema import TicketRequestSchema
from app.services.ticket_service import create_ticket, list_tickets, update_ticket_status, list_pending_tickets
from app.utils.response_wrapper import success_response, error_response
from app.middlewares.auth import authenticate, authorize

@authenticate()
@authorize(['EMPLOYEE', 'ADMIN'])
def raise_ticket():
    try:
        data = TicketRequestSchema(**request.get_json()).dict()
        ticket = create_ticket(request.user['id'], data)
        return success_response('Ticket created', {
            'id': ticket.id,
            'status': ticket.status.value
        })
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN', 'EMPLOYEE'])
def get_all_tickets():
    try:
        tickets = list_tickets(request.user)
        result = [{
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'status': t.status.value,
        } for t in tickets]
        return success_response('Tickets fetched', result)
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['ADMIN', 'SUPER_ADMIN'])
def update_status(ticket_id):
    try:
        status = request.get_json().get('status')
        ticket = update_ticket_status(ticket_id, status)
        return success_response('Ticket status updated', {
            'id': ticket.id,
            'status': ticket.status.value
        })
    except Exception as e:
        return error_response(str(e), 400)

@authenticate()
@authorize(['ADMIN', 'SUPER_ADMIN'])
def get_pending_tickets():
    try:
        results = list_pending_tickets()
        data = []
        for ticket, user in results:
            data.append({
                'id': ticket.id,
                'user_id': user.id,
                'user_name': user.name,
                'designation': user.designation,
                'title': ticket.title,
                'description': ticket.description,
                'status': ticket.status.value,
                'photo': user.photo
            })
        return success_response('Pending tickets fetched', data)
    except Exception as e:
        return error_response(str(e), 400)
