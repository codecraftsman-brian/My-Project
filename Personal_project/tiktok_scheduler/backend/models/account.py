# from datetime import datetime

# # Function to get db without circular imports
# def get_db():
#     from app import db
#     return db

# class Account(object):
#     """Account model base class"""
    
#     # These will be initialized when the actual model is created in app.py
#     id = None
#     user_id = None
#     tiktok_username = None
#     account_name = None
#     access_token = None
#     refresh_token = None
#     token_expiry = None
#     is_active = None
#     created_at = None
#     updated_at = None
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'tiktok_username': self.tiktok_username,
#             'account_name': self.account_name,
#             'is_active': self.is_active,
#             'created_at': self.created_at.isoformat() if self.created_at else None,
#             'token_expiry': self.token_expiry.isoformat() if self.token_expiry else None
#         }

# # This will be used when app.py sets up the actual model
# def setup_account_model(db):
#     """Configure the Account model with SQLAlchemy"""
#     class Account(db.Model):
#         __tablename__ = 'accounts'
        
#         id = db.Column(db.Integer, primary_key=True)
#         user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#         tiktok_username = db.Column(db.String(100), nullable=False)
#         account_name = db.Column(db.String(100), nullable=False)
#         access_token = db.Column(db.Text, nullable=True)  # Encrypted
#         refresh_token = db.Column(db.Text, nullable=True)  # Encrypted
#         token_expiry = db.Column(db.DateTime, nullable=True)
#         is_active = db.Column(db.Boolean, default=True)
#         created_at = db.Column(db.DateTime, default=datetime.utcnow)
#         updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
#         # Relationships
#         posts = db.relationship('Post', backref='account', lazy=True, cascade='all, delete-orphan')
        
#         def to_dict(self):
#             return {
#                 'id': self.id,
#                 'user_id': self.user_id,
#                 'tiktok_username': self.tiktok_username,
#                 'account_name': self.account_name,
#                 'is_active': self.is_active,
#                 'created_at': self.created_at.isoformat(),
#                 'token_expiry': self.token_expiry.isoformat() if self.token_expiry else None
#             }
    
#     return Account