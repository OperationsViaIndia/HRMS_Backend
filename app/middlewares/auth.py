from functools import wraps
from flask import request
from app.utils.jwt_utils import verify_token
from app.utils.response_wrapper import error_response

def authenticate():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return error_response('Unauthorized. No token provided.', 401)

            token = auth_header.split(' ')[1]
            try:
                user_data = verify_token(token)
                request.user = user_data  
                return fn(*args, **kwargs)
            except Exception as e:
                return error_response('Invalid or expired token.', 401)

        return wrapper
    return decorator

def authorize(roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not hasattr(request, 'user') or request.user.get('role') not in roles:
                return error_response('Forbidden. Insufficient privileges.', 403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
