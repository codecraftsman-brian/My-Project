from datetime import datetime
from ..app import db

class EmailLog(db.Model):
    __tablename__ = "email_logs"
    id = db.Column(db.Integer, primary_key=True)
    to_address = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default="queued")  # queued, sent, failed
    error = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime, nullable=True)
