import os
import uuid
from flask import current_app
from flask_socketio import emit, join_room, leave_room
from app.extensions import db, socketio
from app.models.message import Message
from app.models.user import User

@socketio.on('join')
def on_join(data):
    user_id = data['user_id']
    room = data['room'] 
    join_room(room)
    emit('status', {'msg': f'User {user_id} joined room {room}'}, room=room)

@socketio.on('leave')
def on_leave(data):
    user_id = data['user_id']
    room = data['room']
    leave_room(room)
    emit('status', {'msg': f'User {user_id} left room {room}'}, room=room)

@socketio.on('send_message')
def handle_send_message(data):
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    content = data.get('content')
    file_data = data.get('file')  # For file sharing via REST only; socket won't handle binary easily here.

    # If you want file upload, better to POST it via your REST API, then send socket message.

    msg = Message(
        id=str(uuid.uuid4()),
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content
    )
    db.session.add(msg)
    db.session.commit()

    room = generate_room_name(sender_id, receiver_id)
    emit('new_message', {
        'id': msg.id,
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'content': content,
        'file_url': msg.file_url,
        'created_at': msg.created_at.isoformat()
    }, room=room)

def generate_room_name(user1, user2):
    # Simple way: always sort ids for consistency
    return '-'.join(sorted([user1, user2]))