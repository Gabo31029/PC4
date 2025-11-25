from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('Message', backref='user', lazy=True)
    chat_participants = db.relationship('ChatParticipant', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Chat(db.Model):
    __tablename__ = 'chats'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # 'direct' or 'group'
    name = db.Column(db.String(100), nullable=True)  # Only for groups
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    participants = db.relationship('ChatParticipant', backref='chat', lazy=True, cascade='all, delete-orphan')
    messages = db.relationship('Message', backref='chat', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, user_id=None):
        data = {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'participants': [p.user.to_dict() for p in self.participants]
        }
        
        # For direct chats, include the other user's info
        if self.type == 'direct' and user_id:
            other_participant = next((p for p in self.participants if p.user_id != user_id), None)
            if other_participant:
                data['other_user'] = other_participant.user.to_dict()
        
        return data

class ChatParticipant(db.Model):
    __tablename__ = 'chat_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('chat_id', 'user_id', name='unique_chat_user'),)

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=True)  # Nullable for file/audio messages
    message_type = db.Column(db.String(20), default='text')  # 'text', 'audio', 'file'
    file_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'content': self.content,
            'message_type': self.message_type,
            'file_path': self.file_path,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

