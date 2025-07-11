from app import db
from datetime import datetime
import enum
from app.models.association import user_clients 

class Role(enum.Enum):
    SUPER_ADMIN = 'SUPER_ADMIN'
    ADMIN = 'ADMIN'
    EMPLOYEE = 'EMPLOYEE'

class EmploymentType(enum.Enum):
    FULL_TIME = 'FULL_TIME'
    INTERN = 'INTERN'

class ProbationStatus(enum.Enum):
    IN = 'IN'
    COMPLETED = 'COMPLETED'


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(200))
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    employee_code = db.Column(db.String(20), unique=True)
    role = db.Column(db.Enum(Role), nullable=False)
    designation = db.Column(db.String(100))
    aadhar = db.Column(db.String(20))
    dob = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    doj = db.Column(db.Date)
    employment_type = db.Column(db.Enum(EmploymentType))
    probation_status = db.Column(db.Enum(ProbationStatus))
    probation_salary = db.Column(db.Float)
    full_time_salary = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    office_id = db.Column(db.String(36), db.ForeignKey('offices.id'))
    office = db.relationship('Office', back_populates='users')

    
    clients = db.relationship('Client', secondary=user_clients, back_populates='users')

    leave_status = db.relationship('LeaveStatus', backref='user', lazy=True)
    attendance = db.relationship('Attendance', backref='user', lazy=True)
    reimbursements = db.relationship('Reimbursement', backref='user', lazy=True)
    tasks = db.relationship('Tasks', backref='user', lazy=True)
    tickets = db.relationship('Ticket', backref='user', lazy=True)