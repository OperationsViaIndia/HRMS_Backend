from app import create_app, db, socketio
import os

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    PORT = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=PORT, allow_unsafe_werkzeug=True)

