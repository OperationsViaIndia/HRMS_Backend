from app import db
from app.models.ticket import Ticket, TicketStatus

def create_ticket(user_id, data):
    ticket = Ticket(
        user_id=user_id,
        title=data['title'],
        description=data['description']
    )
    db.session.add(ticket)
    db.session.commit()
    return ticket

def list_tickets(user):
    if user['role'] == 'EMPLOYEE':
        return Ticket.query.filter_by(user_id=user['id']).all()
    else:
        return Ticket.query.all()

def update_ticket_status(ticket_id, status):
    if status not in ['PENDING', 'APPROVED', 'REJECTED']:
        raise Exception('Invalid status.')
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        raise Exception('Ticket not found.')
    ticket.status = TicketStatus(status)
    db.session.commit()
    return ticket


def list_pending_tickets():
    from app.models.user import User
    return db.session.query(Ticket, User).join(User).filter(Ticket.status == TicketStatus.PENDING).all()
