from flask import request
from app.schemas.client_schema import ClientCreateSchema, ClientUpdateSchema
from app.services.client_service import create_client, update_client, delete_client, get_all_clients
from app.utils.response_wrapper import success_response, error_response
from app.middlewares.auth import authenticate, authorize

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def create_client_controller():
    try:
        data = request.get_json()
        validated = ClientCreateSchema(**data)
        client = create_client(validated.dict())
        return success_response("Client created", {"id": client.id}, 201)
    except Exception as e:
        return error_response(str(e), 500)

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def update_client_controller(client_id):
    try:
        data = request.get_json()
        validated = ClientUpdateSchema(**data)
        client = update_client(client_id, validated.dict())
        return success_response("Client updated", {"id": client.id})
    except Exception as e:
        return error_response(str(e), 500)

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def delete_client_controller(client_id):
    try:
        delete_client(client_id)
        print("$$$$$$$$$$$$$",client_id)
        return success_response("Client deleted")
    except Exception as e:
        return error_response(str(e), 500)

@authenticate()
@authorize(['SUPER_ADMIN', 'ADMIN'])
def list_clients_controller():
    try:
        return success_response("Clients list", get_all_clients())
    except Exception as e:
        return error_response(str(e), 500)
