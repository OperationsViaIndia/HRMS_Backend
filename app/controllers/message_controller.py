from flask import request, current_app
from app.utils.response_wrapper import success_response, error_response
from app.models.message import Message
from app.middlewares.auth import authenticate
from app.services.message_service import save_message, get_conversation_between  
from app import sockets 
import os
import uuid

@authenticate()
def get_conversation():
    try:
        user_id = request.user['id']
        other_user_id = request.args.get('user_id')
        if not other_user_id:
            return error_response("user_id is required", 400)

        messages = get_conversation_between(user_id, other_user_id) 

        result = [{
            "id": m.id,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
            "content": m.content,
            "file_url": m.file_url,
            "created_at": m.created_at.isoformat()
        } for m in messages]

        return success_response("Conversation fetched", result)

    except Exception as e:
        return error_response(str(e), 500)


@authenticate()
def upload_message_file():
    try:
        sender_id = request.user['id']
        receiver_id = request.form.get('receiver_id')
        if not receiver_id:
            return error_response("receiver_id is required", 400)

        file = request.files.get('file')
        if not file:
            return error_response("No file uploaded", 400)

        upload_folder = os.path.join(current_app.root_path, '..', 'uploads', 'messages')
        os.makedirs(upload_folder, exist_ok=True)

        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file.save(os.path.join(upload_folder, filename))

        file_url = f"/uploads/messages/{filename}"

        msg = save_message(sender_id, receiver_id, content=None, file_url=file_url)  

        room = generate_room_name(sender_id, receiver_id)
        sockets.emit('new_message', {
            "id": msg.id,
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "content": None,
            "file_url": file_url,
            "created_at": msg.created_at.isoformat()
        }, room=room)

        return success_response("File sent", {
            "id": msg.id,
            "file_url": file_url
        })

    except Exception as e:
        return error_response(str(e), 500)


def generate_room_name(user1, user2):
    return '-'.join(sorted([user1, user2]))
