from flask import Flask
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    # CORS configuration - allow all origins for LAN access
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})
    socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')
    
    # Create uploads directory
    import os
    upload_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Register routes
    from app.routes import register_routes
    register_routes(app)
    
    # Register socket handlers
    from app.websocket_handlers import register_socket_handlers
    register_socket_handlers(socketio)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

