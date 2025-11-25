import bcrypt
import os
from werkzeug.utils import secure_filename
from flask import current_app
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    """Check if password matches hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def allowed_file(filename, allowed_extensions=None):
    """Check if file extension is allowed"""
    if allowed_extensions is None:
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_file(file, upload_folder=None, allowed_extensions=None):
    """Save uploaded file and return the path"""
    if upload_folder is None:
        upload_folder = current_app.config['UPLOAD_FOLDER']
    if allowed_extensions is None:
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    
    if file and allowed_file(file.filename, allowed_extensions):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        import time
        filename = f"{int(time.time())}_{filename}"
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filename
    return None

def jwt_required_socket(f):
    """Decorator to require JWT for socket events"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            verify_jwt_in_request()
            kwargs['user_id'] = get_jwt_identity()
        except:
            return {'error': 'Authentication required'}, 401
        return f(*args, **kwargs)
    return wrapped

