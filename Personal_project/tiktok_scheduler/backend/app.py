from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///tiktok_scheduler.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 hours
app.config['TIKTOK_CLIENT_KEY'] = os.environ.get('TIKTOK_CLIENT_KEY')
app.config['TIKTOK_CLIENT_SECRET'] = os.environ.get('TIKTOK_CLIENT_SECRET')
app.config['TIKTOK_REDIRECT_URI'] = os.environ.get('TIKTOK_REDIRECT_URI')
app.config['ENCRYPTION_MASTER_KEY'] = os.environ.get('ENCRYPTION_MASTER_KEY')

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Define models directly in app.py to avoid circular imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    accounts = db.relationship('Account', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tiktok_username = db.Column(db.String(100), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    access_token = db.Column(db.Text, nullable=True)  # Encrypted
    refresh_token = db.Column(db.Text, nullable=True)  # Encrypted
    token_expiry = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='account', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tiktok_username': self.tiktok_username,
            'account_name': self.account_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'token_expiry': self.token_expiry.isoformat() if self.token_expiry else None
        }

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    video_path = db.Column(db.String(255), nullable=True)  # Local path or URL to video
    caption = db.Column(db.Text, nullable=True)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, sent, failed
    error_message = db.Column(db.Text, nullable=True)
    tiktok_post_id = db.Column(db.String(100), nullable=True)  # ID of the post on TikTok
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'caption': self.caption,
            'scheduled_time': self.scheduled_time.isoformat(),
            'status': self.status,
            'error_message': self.error_message,
            'tiktok_post_id': self.tiktok_post_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Package models in a dictionary for easy access
models = {
    'User': User,
    'Account': Account,
    'Post': Post
}

# Initialize services
from services import auth_service, encryption_service, scheduler_service, tiktok_api_service, init_app as init_services

# Initialize services with dependencies
services = init_services(app, db, jwt, scheduler, models)

# Create and register blueprints
from flask import Blueprint

# Create blueprints
auth_bp = Blueprint('auth', __name__)
scheduler_bp = Blueprint('scheduler', __name__)
dashboard_bp = Blueprint('dashboard', __name__)

# Import route registration functions
from routes.auth_routes import register_auth_routes
from routes.scheduler_routes import register_scheduler_routes
from routes.dashboard_routes import register_dashboard_routes

# Register routes with blueprints
register_auth_routes(auth_bp, services, models)
register_scheduler_routes(scheduler_bp, services, models)
register_dashboard_routes(dashboard_bp, services, models)

# Register blueprints with app
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(scheduler_bp, url_prefix='/api/scheduler')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Ensure all tables are created
    with app.app_context():
        db.create_all()
    
    # Run the app
    app.run(debug=True)