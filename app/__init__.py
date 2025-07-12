from flask import Flask, jsonify, send_from_directory, current_app 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from pydantic import ValidationError
import logging
from logging.handlers import RotatingFileHandler
import os
from .extensions import db, socketio


migrate = Migrate()





def create_app():
    from app.config import Config
    from app.utils.app_error import AppError 
    from app.models.user import User
    from app.models.client import Client
    from app.routes.user_routes import user_bp
    from app.routes.holiday_routes import holiday_bp
    from app.routes.leave_routes import leave_bp
    from app.routes.reimbursement_routes import reimbursement_bp
    from app.routes.attendance_routes import attendance_bp
    from app.routes.office_routes import office_bp
    from app.routes.client_routes import client_bp
    from app.routes.message_routes import message_bp
    from flask_socketio import SocketIO
    from app.routes.tasks_routes import tasks_bp
    from app.routes.ticket_router import ticket_bp
    from app.routes.app_version_routes import app_version_bp




    app = Flask(__name__)
    app.config.from_object(Config)

   
    db.init_app(app)
    migrate.init_app(app, db)

   
    CORS(app)
    socketio.init_app(app)
    if __name__ == "__main__":
     socketio.run(app, debug=True)

  
    app.register_blueprint(user_bp, url_prefix="/api/auth")
    app.register_blueprint(holiday_bp, url_prefix="/api/holiday")
    app.register_blueprint(leave_bp, url_prefix="/api/leave")
    app.register_blueprint(reimbursement_bp, url_prefix="/api/reimbursement")
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(office_bp,url_prefix='/api/office')
    app.register_blueprint(client_bp, url_prefix="/api/client")
    app.register_blueprint(message_bp, url_prefix='/api/message')
    app.register_blueprint(tasks_bp, url_prefix='/api/task')
    app.register_blueprint(ticket_bp, url_prefix='/api/tickets')
    app.register_blueprint(app_version_bp, url_prefix='/api/app')

    configure_logging(app)

  
    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(error):
        app.logger.error(f"Validation error: {error}")
        return jsonify({
            "status": "error",
            "message": "Validation failed",
            "details": error.errors()
        }), 400

   
    @app.errorhandler(AppError)
    def handle_app_error(error):
        app.logger.error(f"App error: {error}")
        return jsonify({
            "status": "error",
            "message": str(error)
        }), getattr(error, 'code', 500)

   
    @app.route("/api/health")
    def health():
        return {"status": "ok"}, 200
    # @app.route('/uploads/holidays/<path:filename>')
    # def uploaded_file(filename):
    #  uploads_dir = os.path.join(current_app.root_path, '..', 'uploads', 'holidays')
    #  uploads_dir = os.path.abspath(uploads_dir)
    #  return send_from_directory(uploads_dir, filename)


    
    # @app.route('/uploads/messages/<path:filename>')
    # def uploaded_message_file(filename):
    #  uploads_dir = os.path.join(current_app.root_path, '..', 'uploads', 'messages')
    #  uploads_dir = os.path.abspath(uploads_dir)
    #  return send_from_directory(uploads_dir, filename)

    
    # @app.route('/uploads/user/<path:filename>')
    # def uploaded_user_file(filename):
    #     uploads_dir = os.path.join(current_app.root_path, '..', 'uploads', 'user')
    #     uploads_dir = os.path.abspath(uploads_dir)
    #     return send_from_directory(uploads_dir, filename)

  


    return app

def configure_logging(app):
    """Set up logging: console + rotating file."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "app.log")

    file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=5)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    ))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s"
    ))

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
