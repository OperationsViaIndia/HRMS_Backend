from flask import jsonify

def success_response(message, data=None, status_code=200):
    return jsonify({
        "status": status_code,
        "message": message,
        "data": data
    }), status_code


def error_response(message, status_code=400):
    return jsonify({
        "message": message,
        "status": status_code 
    }), status_code  
