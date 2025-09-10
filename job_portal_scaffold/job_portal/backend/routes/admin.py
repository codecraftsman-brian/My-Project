from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from wtforms import Form, StringField, TextAreaField, SelectField, validators
from flask_wtf import FlaskForm
from ..app import db
from ..models.admin import Admin
from ..models.job import Job
from ..models.application import Application
from ..models.user import User
from ..utils.auth_utils import hash_password
from ..utils.email_utils import send_email

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_guard():
    # Simple placeholder: first admin-only protection can be improved by actual admin sessions
    # In production, use a separate admin auth or role-based system.
    pass

class JobForm(FlaskForm):
    title = StringField("Title", [validators.DataRequired(), validators.Length(max=150)])
    description = TextAreaField("Description", [validators.DataRequired()])
    requirements = TextAreaField("Requirements", [validators.Optional()])
    benefits = TextAreaField("Benefits", [validators.Optional()])
    salary = StringField("Salary", [validators.Optional(), validators.Length(max=100)])
    location = StringField("Location", [validators.Optional(), validators.Length(max=120)])
    company = StringField("Company", [validators.Optional(), validators.Length(max=120)])
    category = StringField("Category", [validators.Optional(), validators.Length(max=120)])
    status = SelectField("Status", choices=[("open","Open"),("closed","Closed"),("draft","Draft")], default="open")

@admin_bp.route("/dashboard")
@login_required
def dashboard():
    # Basic analytics
    total_jobs = Job.query.count()
    total_apps = Application.query.count()
    apps_per_job = db.session.query(Job.title, db.func.count(Application.id)).join(Application, isouter=True).group_by(Job.id).all()
    users_count = User.query.count()
    recent_apps = Application.query.order_by(Application.application_date.desc()).limit(10).all()
    return render_template("admin/dashboard.html", total_jobs=total_jobs, total_apps=total_apps, users_count=users_count, apps_per_job=apps_per_job, recent_apps=recent_apps)

@admin_bp.route("/jobs")
@login_required
def jobs_list():
    jobs = Job.query.order_by(Job.posted_date.desc()).all()
    return render_template("admin/jobs.html", jobs=jobs)

@admin_bp.route("/jobs/create", methods=["GET","POST"])
@login_required
def jobs_create():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(**{f.name: f.data for f in form})
        db.session.add(job)
        db.session.commit()
        flash("Job created.", "success")
        return redirect(url_for("admin.jobs_list"))
    return render_template("admin/job_form.html", form=form, action="Create")

@admin_bp.route("/jobs/<int:job_id>/edit", methods=["GET","POST"])
@login_required
def jobs_edit(job_id):
    job = Job.query.get_or_404(job_id)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        for f in form:
            if f.name in {"csrf_token"}: continue
            setattr(job, f.name, f.data)
        db.session.commit()
        flash("Job updated.", "success")
        return redirect(url_for("admin.jobs_list"))
    return render_template("admin/job_form.html", form=form, action="Edit")

@admin_bp.route("/jobs/<int:job_id>/delete", methods=["POST"])
@login_required
def jobs_delete(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash("Job deleted.", "info")
    return redirect(url_for("admin.jobs_list"))

@admin_bp.route("/users")
@login_required
def users_list():
    users = User.query.order_by(User.created_date.desc()).all()
    return render_template("admin/users.html", users=users)

@admin_bp.route("/applications")
@login_required
def apps_list():
    apps = Application.query.order_by(Application.application_date.desc()).all()
    return render_template("admin/applications.html", applications=apps)

@admin_bp.route("/email/bulk", methods=["GET", "POST"])
@login_required
def email_bulk():
    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        body = request.form.get("body", "")
        job_id = request.form.get("job_id")
        recipients = []
        if job_id:
            job = Job.query.get(job_id)
            if job:
                for app in job.applications:
                    recipients.append(app.user.email)
        else:
            recipients = [u.email for u in User.query.all()]
        sent = 0
        for to in set(recipients):
            status = send_email(to, subject, body, body)
            if status == "sent":
                sent += 1
        flash(f"Bulk email queued to {sent} recipients.", "success")
        return redirect(url_for("admin.dashboard"))
    jobs = Job.query.order_by(Job.posted_date.desc()).all()
    return render_template("admin/email_bulk.html", jobs=jobs)
