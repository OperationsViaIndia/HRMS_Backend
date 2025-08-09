from app import db
from app.models.leave import LeaveStatus, LeaveRequestStatus, LeaveType
from app.models.user import User
from sqlalchemy.orm import joinedload
import uuid

MAX_SICK = 6
MAX_CASUAL = 12

def get_day_count(from_date, to_date):
    return (to_date - from_date).days + 1

def request_leave(user_id, data):
    from_date = data['from_date']
    to_date = data['to_date']

    if from_date > to_date:
        raise Exception('from_date must be before or equal to to_date')

    requested_days = get_day_count(from_date, to_date)

    used_leaves = LeaveStatus.query.filter_by(
        user_id=user_id,
        type=LeaveType(data['type']),
        status=LeaveRequestStatus.APPROVED
    ).all()

    used_days = sum(get_day_count(l.from_date, l.to_date) for l in used_leaves)

    max_allowed = MAX_SICK if data['type'] == 'SICK' else MAX_CASUAL

    if used_days + requested_days > max_allowed:
        remaining = max_allowed - used_days
        raise Exception(
            f"Leave limit exceeded. You have only {remaining if remaining > 0 else 0} {data['type']} days left."
        )

    leave = LeaveStatus(
        id=str(uuid.uuid4()),
        user_id=user_id,
        type=LeaveType(data['type']),
        from_date=from_date,
        to_date=to_date,
        reason=data['reason']
    )
    db.session.add(leave)
    db.session.commit()
    return leave

def get_leave_balance(user_id):
    approved = LeaveStatus.query.filter_by(user_id=user_id, status=LeaveRequestStatus.APPROVED).all()

    total_used = 0

    for l in approved:
        days = get_day_count(l.from_date, l.to_date)
        total_used += days

    total_leave = MAX_SICK + MAX_CASUAL

    return {
        'used': total_used,
        'remaining': total_leave - total_used
    }

def list_leaves(user):
    query = LeaveStatus.query.options(joinedload(LeaveStatus.user)) \
        .filter_by(status=LeaveRequestStatus.PENDING)

    if user['role'] == 'EMPLOYEE':
        query = query.filter_by(user_id=user['id'])

    return query.order_by(LeaveStatus.created_at.desc()).all()

def approve_leave(id, status):
    if status not in ['APPROVED', 'REJECTED']:
        raise Exception('Invalid status. Only APPROVED or REJECTED allowed.')
    leave = LeaveStatus.query.get(id)
    if not leave:
        raise Exception('Leave not found.')
    leave.status = LeaveRequestStatus(status)
    db.session.commit()
    return leave

def list_user_leaves(user_id, leave_type='ALL'):
    query = LeaveStatus.query.options(joinedload(LeaveStatus.user)).filter_by(user_id=user_id)

    if leave_type != 'ALL':
        try:
            query = query.filter(LeaveStatus.type == LeaveType(leave_type))
        except ValueError:
            raise Exception('Invalid leave type. Use SICK, CASUAL, or ALL.')

    return query.order_by(LeaveStatus.created_at.desc()).all()


def list_user_all_leaves(user_id):
    print("________________________",user_id)
    query = LeaveStatus.query.options(joinedload(LeaveStatus.user)).filter_by(user_id=user_id)
    return query.order_by(LeaveStatus.created_at.desc()).all()
