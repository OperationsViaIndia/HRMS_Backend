import uuid
from app import db
from app.models.tasks import Tasks
from app.models.user import User

def create_task(user_id, data):
    task = Tasks(
        id=str(uuid.uuid4()),
        user_id=user_id,
        description=data['description'],
        date=data['date']
    )
    db.session.add(task)
    db.session.commit()
    return task

def get_all_tasks():
    return Tasks.query.all()

def get_all_tasks_id(user_id):
    user = User.query.get(user_id)
    print("User found:", user)
    if not user:
        return None
    print("Tasks found:", user.tasks)
    return user.tasks


