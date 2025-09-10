import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from wtforms import Form, TextAreaField, FileField, validators
from flask_wtf import FlaskForm
from ..app import db
from ..models.job import Job
from ..models.application import Application
from ..utils.email_utils import send_email

ALLOWED = {"pdf", "doc", "docx"}

applications_bp = Blueprint("applications", __name__, url_prefix="")

class ApplyForm(FlaskForm):
    cover_letter = TextAreaField("Cover Letter", [validators.Optional(), validators.Length(max=5000)])

def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

@applications_bp.route("/apply/<int:job_id>", methods=["GET", "POST"])
@login_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)
    form = ApplyForm()
    if request.method == "POST" and form.validate():
        # Handle resume upload
        resume_path = None
        file = request.files.get("resume")
        if file and file.filename and allowed(file.filename):
            filename = secure_filename(file.filename)
            save_dir = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
            os.makedirs(save_dir, exist_ok=True)
            target = os.path.join(save_dir, f"user{current_user.id}_job{job.id}_{filename}")
            file.save(target)
            resume_path = os.path.abspath(target)

        # Create application
        if Application.query.filter_by(user_id=current_user.id, job_id=job.id).first():
            flash("You have already applied to this job.", "warning")
            return redirect(url_for("jobs.job_detail", job_id=job.id))

        app_obj = Application(user_id=current_user.id, job_id=job.id, cover_letter=form.cover_letter.data, resume_path=resume_path)
        db.session.add(app_obj)
        db.session.commit()

        # Email notifications
        send_email(
            to=current_user.email,
            subject=f"Application received: {job.title}",
            html_body=render_template("emails/app_confirm.html", job=job, name=current_user.name),
            text_body=f"Your application for {job.title} at {job.company or 'the employer'} was received.",
        )

        flash("Application submitted!", "success")
        return redirect(url_for("applications.my_applications"))
    return render_template("apply.html", form=form, job=job)

@applications_bp.route("/my/applications")
@login_required
def my_applications():
    apps = Application.query.filter_by(user_id=current_user.id).order_by(Application.application_date.desc()).all()
    return render_template("my_applications.html", applications=apps)
