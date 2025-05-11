from app import db
from datetime import datetime

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