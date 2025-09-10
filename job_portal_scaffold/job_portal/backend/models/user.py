from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from ..app import db, login_manager

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50))
    address = db.Column(db.String(255))
    cv_path = db.Column(db.String(255))
    email_verified = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
