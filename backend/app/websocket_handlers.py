from flask_socketio import emit, join_room, leave_room
from flask import request
from flask_jwt_extended import decode_token
from app import db, socketio
from app.models import Chat, Message, ChatParticipant, User
from datetime import datetime
import json

# Store connected users: {user_id: socket_id}
connected_users = {}

def register_socket_handlers(socketio):
    
    @socketio.on('connect')
    def handle_connect(auth):
        """Handle client connection"""
        try:
            token = auth.get('token') if auth else None
            if not token:
                return False
            
            decoded = decode_token(token)
            user_id = decoded['sub']
            
            # Store connection
            connected_users[user_id] = request.sid
            
            # Join user's personal room
            join_room(f"user_{user_id}")
            
            # Notify others that user is online
            socketio.emit('user_online', {'user_id': user_id}, room=None, include_self=False)
            
            print(f"User {user_id} connected: {request.sid}")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        try:
            # Find user by socket_id
            user_id = None
            for uid, sid in connected_users.items():
                if sid == request.sid:
                    user_id = uid
                    break
            
            if user_id:
                del connected_users[user_id]
                socketio.emit('user_offline', {'user_id': user_id}, room=None, include_self=False)
                print(f"User {user_id} disconnected")
        except Exception as e:
            print(f"Disconnect error: {e}")
    
    @socketio.on('join_chat')
    def handle_join_chat(data):
        """Join a chat room"""
        try:
            token = data.get('token')
            if not token:
                emit('error', {'message': 'Authentication required'})
                return
            
            decoded = decode_token(token)
            user_id = decoded['sub']
            chat_id = data.get('chat_id')
            
            # Verify user is participant
            participant = ChatParticipant.query.filter_by(chat_id=chat_id, user_id=user_id).first()
            if not participant:
                emit('error', {'message': 'Access denied'})
                return
            
            join_room(f"chat_{chat_id}")
            emit('joined_chat', {'chat_id': chat_id})
            print(f"User {user_id} joined chat {chat_id}")
        except Exception as e:
            emit('error', {'message': str(e)})
    
    @socketio.on('leave_chat')
    def handle_leave_chat(data):
        """Leave a chat room"""
        try:
            chat_id = data.get('chat_id')
            leave_room(f"chat_{chat_id}")
            emit('left_chat', {'chat_id': chat_id})
        except Exception as e:
            emit('error', {'message': str(e)})
    
    @socketio.on('send_message')
    def handle_send_message(data):
        """Handle new message"""
        try:
            token = data.get('token')
            if not token:
                emit('error', {'message': 'Authentication required'})
                return
            
            decoded = decode_token(token)
            user_id = decoded['sub']
            chat_id = data.get('chat_id')
            content = data.get('content')
            message_type = data.get('message_type', 'text')
            file_path = data.get('file_path')
            
            # Verify user is participant
            participant = ChatParticipant.query.filter_by(chat_id=chat_id, user_id=user_id).first()
            if not participant:
                emit('error', {'message': 'Access denied'})
                return
            
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
            
            # Emit to all participants in the chat room
            message_data = message.to_dict()
            socketio.emit('new_message', message_data, room=f"chat_{chat_id}")
            
            print(f"Message sent in chat {chat_id} by user {user_id}")
        except Exception as e:
            db.session.rollback()
            emit('error', {'message': str(e)})
    
    @socketio.on('call_offer')
    def handle_call_offer(data):
        """Handle WebRTC call offer"""
        try:
            token = data.get('token')
            if not token:
                emit('error', {'message': 'Authentication required'})
                return
            
            decoded = decode_token(token)
            caller_id = decoded['sub']
            chat_id = data.get('chat_id')
            offer = data.get('offer')
            
            # Verify caller is participant
            participant = ChatParticipant.query.filter_by(chat_id=chat_id, user_id=caller_id).first()
            if not participant:
                emit('error', {'message': 'Access denied'})
                return
            
            # Get other participants
            participants = ChatParticipant.query.filter_by(chat_id=chat_id).filter(ChatParticipant.user_id != caller_id).all()
            
            # Send offer to other participants
            for p in participants:
                socketio.emit('call_offer', {
                    'chat_id': chat_id,
                    'caller_id': caller_id,
                    'offer': offer
                }, room=f"user_{p.user_id}")
            
            print(f"Call offer from user {caller_id} in chat {chat_id}")
        except Exception as e:
            emit('error', {'message': str(e)})
    
    @socketio.on('call_answer')
    def handle_call_answer(data):
        """Handle WebRTC call answer"""
        try:
            token = data.get('token')
            if not token:
                emit('error', {'message': 'Authentication required'})
                return
            
            decoded = decode_token(token)
            answerer_id = decoded['sub']
            chat_id = data.get('chat_id')
            caller_id = data.get('caller_id')
            answer = data.get('answer')
            
            # Send answer to caller
            socketio.emit('call_answer', {
                'chat_id': chat_id,
                'answerer_id': answerer_id,
                'answer': answer
            }, room=f"user_{caller_id}")
            
            print(f"Call answer from user {answerer_id} to caller {caller_id}")
        except Exception as e:
            emit('error', {'message': str(e)})
    
    @socketio.on('ice_candidate')
    def handle_ice_candidate(data):
        """Handle WebRTC ICE candidate"""
        try:
            token = data.get('token')
            if not token:
                emit('error', {'message': 'Authentication required'})
                return
            
            decoded = decode_token(token)
            sender_id = decoded['sub']
            chat_id = data.get('chat_id')
            target_id = data.get('target_id')
            candidate = data.get('candidate')
            
            # Send ICE candidate to target
            socketio.emit('ice_candidate', {
                'chat_id': chat_id,
                'sender_id': sender_id,
                'candidate': candidate
            }, room=f"user_{target_id}")
        except Exception as e:
            emit('error', {'message': str(e)})
    
    @socketio.on('call_end')
    def handle_call_end(data):
        """Handle call end"""
        try:
            token = data.get('token')
            if not token:
                emit('error', {'message': 'Authentication required'})
                return
            
            decoded = decode_token(token)
            user_id = decoded['sub']
            chat_id = data.get('chat_id')
            
            # Get all participants
            participants = ChatParticipant.query.filter_by(chat_id=chat_id).all()
            
            # Notify all participants
            for p in participants:
                if p.user_id != user_id:
                    socketio.emit('call_end', {
                        'chat_id': chat_id,
                        'ended_by': user_id
                    }, room=f"user_{p.user_id}")
            
            print(f"Call ended by user {user_id} in chat {chat_id}")
        except Exception as e:
            emit('error', {'message': str(e)})
    
    @socketio.on('get_online_users')
    def handle_get_online_users(data):
        """Get list of online users"""
        try:
            token = data.get('token')
            if not token:
                emit('error', {'message': 'Authentication required'})
                return
            
            decoded = decode_token(token)
            user_id = decoded['sub']
            
            # Get all online user IDs
            online_user_ids = list(connected_users.keys())
            
            emit('online_users', {'user_ids': online_user_ids})
        except Exception as e:
            emit('error', {'message': str(e)})

