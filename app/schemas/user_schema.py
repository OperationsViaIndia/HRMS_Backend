from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import date


class ClientSchema(BaseModel):
    client_name: str
    project_name: str
    start_date: date


class UserRegisterSchema(BaseModel):
    name: str
    phone: constr(min_length=10, max_length=10)
    email: EmailStr
    password: constr(min_length=6)
    role: str  # 'ADMIN', 'EMPLOYEE', 'SUPER_ADMIN'
    designation: Optional[str] = None
    employee_code: Optional[str] = None
    office_id: Optional[str]= None
    aadhar: Optional[str] = None
    dob: Optional[date] = None
    doj: Optional[date] = None
    employment_type: Optional[str] = None  # 'FULL_TIME' or 'INTERN'
    probation_status: Optional[str] = None  # 'IN' or 'COMPLETED'
    probation_salary: Optional[float] = None
    full_time_salary: Optional[float] = None
    
