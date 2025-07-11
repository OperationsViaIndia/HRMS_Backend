import jwt
import os
from datetime import datetime, timedelta
from flask import current_app

SECRET_KEY = os.getenv('SECRET_KEY') or 'super-secret-key'
ACCESS_TTL = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 15))
REFRESH_TTL = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', 7))

def sign_access_token(payload: dict) -> str:
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def sign_refresh_token(payload: dict) -> str:
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'], options={'verify_exp': False})

