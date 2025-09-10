from datetime import datetime
from sqlalchemy.orm import relationship
from ..app import db

class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=True)
    benefits = db.Column(db.Text, nullable=True)
    salary = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(120), nullable=True)
    company = db.Column(db.String(120), nullable=True)
    category = db.Column(db.String(120), nullable=True)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default="open")  # open/closed/draft

    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")

    __table_args__ = (
        db.Index("ix_jobs_category", "category"),
        db.Index("ix_jobs_location", "location"),
        db.Index("ix_jobs_status", "status"),
    )
