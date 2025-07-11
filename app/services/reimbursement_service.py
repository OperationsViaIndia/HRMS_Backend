from app import db
from app.models.reimbursement import Reimbursement, ReimbursementStatus
from app.models.user import User
import uuid
import os
from app.utils.cloudinary_uploader import upload_to_cloudinary

MAX_AMOUNT_WITHOUT_BILL = 100

def request_reimbursement(user_id, data, file):
    if data['amount'] > MAX_AMOUNT_WITHOUT_BILL and file is None:
        raise Exception('Bill required for amount > 100')

    bill_url = upload_to_cloudinary(file, folder='bills') if file else None

    reimb = Reimbursement(
        id=str(uuid.uuid4()),
        user_id=user_id,
        amount=data['amount'],
        reason=data['reason'],
        bill=bill_url  
    )
    db.session.add(reimb)
    db.session.commit()
    return reimb

def list_reimbursements(user):
    if user['role'] == 'EMPLOYEE':
        return Reimbursement.query.filter_by(user_id=user['id']).all()
    else:
        return Reimbursement.query.all()

def approve_reimbursement(id, status):
    if status not in ['APPROVED', 'REJECTED']:
        raise Exception('Invalid status.')
    reimb = Reimbursement.query.get(id)
    if not reimb:
        raise Exception('Reimbursement not found.')
    reimb.status = ReimbursementStatus(status)
    db.session.commit()
    return reimb

def list_pending_reimbursements():
    return db.session.query(Reimbursement, User).join(User).filter(Reimbursement.status == ReimbursementStatus.PENDING).all()
