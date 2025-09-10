from datetime import datetime
from ..app import db

class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="submitted")  # submitted, in_review, shortlisted, rejected, hired
    cover_letter = db.Column(db.Text, nullable=True)
    resume_path = db.Column(db.String(255), nullable=True)

    user = db.relationship("User", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")

    __table_args__ = (
        db.UniqueConstraint("user_id", "job_id", name="uq_user_job_once"),
    )
