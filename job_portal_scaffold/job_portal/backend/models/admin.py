from datetime import datetime
from ..app import db

class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    permissions = db.Column(db.String(50), default="editor")
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
