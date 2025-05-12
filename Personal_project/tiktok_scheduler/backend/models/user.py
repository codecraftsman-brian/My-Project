# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash

# # Function to get db without circular imports
# def get_db():
#     from app import db
#     return db

# class User(object):
#     """User model base class"""
    
#     # These will be initialized when the actual model is created in app.py
#     id = None
#     username = None
#     email = None
#     password_hash = None
#     created_at = None
#     updated_at = None
#     last_login = None
    
#     def __init__(self, username, email, password):
#         self.username = username
#         self.email = email
#         self.set_password(password)
    
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
    
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'username': self.username,
#             'email': self.email,
#             'created_at': self.created_at.isoformat() if self.created_at else None,
#             'last_login': self.last_login.isoformat() if self.last_login else None
#         }

# # This will be used when app.py sets up the actual model
# def setup_user_model(db):
#     """Configure the User model with SQLAlchemy"""
#     class User(db.Model):
#         __tablename__ = 'users'
        
#         id = db.Column(db.Integer, primary_key=True)
#         username = db.Column(db.String(100), unique=True, nullable=False)
#         email = db.Column(db.String(100), unique=True, nullable=False)
#         password_hash = db.Column(db.String(200), nullable=False)
#         created_at = db.Column(db.DateTime, default=datetime.utcnow)
#         updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#         last_login = db.Column(db.DateTime, nullable=True)
        
#         # Relationships
#         accounts = db.relationship('Account', backref='user', lazy=True, cascade='all, delete-orphan')
        
#         def __init__(self, username, email, password):
#             self.username = username
#             self.email = email
#             self.set_password(password)
        
#         def set_password(self, password):
#             self.password_hash = generate_password_hash(password)
        
#         def check_password(self, password):
#             return check_password_hash(self.password_hash, password)
        
#         def to_dict(self):
#             return {
#                 'id': self.id,
#                 'username': self.username,
#                 'email': self.email,
#                 'created_at': self.created_at.isoformat(),
#                 'last_login': self.last_login.isoformat() if self.last_login else None
#             }
    
#     return User