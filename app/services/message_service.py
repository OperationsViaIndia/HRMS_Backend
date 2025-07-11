from app.models.message import Message
from app import db
import uuid

def save_message(sender_id, receiver_id, content, file_url=None):
    msg = Message(
        id=str(uuid.uuid4()),
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        file_url=file_url
    )
    db.session.add(msg)
    db.session.commit()
    return msg

def get_conversation_between(user1, user2):
    return Message.query.filter(
        ((Message.sender_id == user1) & (Message.receiver_id == user2)) |
        ((Message.sender_id == user2) & (Message.receiver_id == user1))
    ).order_by(Message.created_at).all()
