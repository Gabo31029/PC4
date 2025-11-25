from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User, Chat, ChatParticipant, Message
from app.utils import hash_password, check_password, save_uploaded_file
from werkzeug.exceptions import BadRequest
import os

api_bp = Blueprint('api', __name__, url_prefix='/api')

def register_routes(app):
    app.register_blueprint(api_bp)

@api_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create user
        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password)
        )
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@api_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password(password, user.password_hash):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/chats', methods=['GET'])
@jwt_required()
def get_chats():
    try:
        user_id = get_jwt_identity()
        
        # Get all chats where user is a participant
        participants = ChatParticipant.query.filter_by(user_id=user_id).all()
        chat_ids = [p.chat_id for p in participants]
        chats = Chat.query.filter(Chat.id.in_(chat_ids)).all()
        
        return jsonify({
            'chats': [chat.to_dict(user_id=user_id) for chat in chats]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/chats', methods=['POST'])
@jwt_required()
def create_chat():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        chat_type = data.get('type', 'direct')  # 'direct' or 'group'
        name = data.get('name')
        participant_ids = data.get('participant_ids', [])
        
        if chat_type == 'group' and not name:
            return jsonify({'error': 'Group name is required'}), 400
        
        if chat_type == 'direct':
            if len(participant_ids) != 1:
                return jsonify({'error': 'Direct chat must have exactly one other participant'}), 400
            
            other_user_id = participant_ids[0]
            if other_user_id == user_id:
                return jsonify({'error': 'Cannot create direct chat with yourself'}), 400
            
            # Check if direct chat already exists
            existing_chats = Chat.query.filter_by(type='direct').all()
            for chat in existing_chats:
                participants = [p.user_id for p in chat.participants]
                if user_id in participants and other_user_id in participants:
                    return jsonify({
                        'message': 'Chat already exists',
                        'chat': chat.to_dict(user_id=user_id)
                    }), 200
        
        # Create chat
        chat = Chat(type=chat_type, name=name)
        db.session.add(chat)
        db.session.flush()
        
        # Add current user as participant
        participant = ChatParticipant(chat_id=chat.id, user_id=user_id)
        db.session.add(participant)
        
        # Add other participants
        for pid in participant_ids:
            if pid != user_id:
                participant = ChatParticipant(chat_id=chat.id, user_id=pid)
                db.session.add(participant)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Chat created successfully',
            'chat': chat.to_dict(user_id=user_id)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/chats/<int:chat_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(chat_id):
    try:
        user_id = get_jwt_identity()
        
        # Verify user is participant
        participant = ChatParticipant.query.filter_by(chat_id=chat_id, user_id=user_id).first()
        if not participant:
            return jsonify({'error': 'Chat not found or access denied'}), 404
        
        # Get messages
        messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.created_at.asc()).all()
        
        return jsonify({
            'messages': [msg.to_dict() for msg in messages]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/chats/<int:chat_id>/messages', methods=['POST'])
@jwt_required()
def send_message(chat_id):
    try:
        user_id = get_jwt_identity()
        
        # Verify user is participant
        participant = ChatParticipant.query.filter_by(chat_id=chat_id, user_id=user_id).first()
        if not participant:
            return jsonify({'error': 'Chat not found or access denied'}), 404
        
        data = request.get_json()
        content = data.get('content')
        message_type = data.get('message_type', 'text')
        file_path = data.get('file_path')
        
        if message_type == 'text' and not content:
            return jsonify({'error': 'Message content is required'}), 400
        
        if message_type in ['audio', 'file'] and not file_path:
            return jsonify({'error': 'File path is required for file/audio messages'}), 400
        
        # Create message
        message = Message(
            chat_id=chat_id,
            user_id=user_id,
            content=content,
            message_type=message_type,
            file_path=file_path
        )
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'message': 'Message sent successfully',
            'data': message.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    try:
        from flask import current_app
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # save_uploaded_file will use current_app.config if params are None
        filename = save_uploaded_file(file)
        if not filename:
            return jsonify({'error': 'Invalid file type'}), 400
        
        return jsonify({
            'file_path': filename,
            'url': f'/api/files/{filename}'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/files/<filename>', methods=['GET'])
@jwt_required()
def get_file(filename):
    try:
        from flask import current_app
        upload_folder = current_app.config['UPLOAD_FOLDER']
        return send_from_directory(upload_folder, filename)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        search = request.args.get('search', '')
        users = User.query.filter(User.username.contains(search)).limit(20).all()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

