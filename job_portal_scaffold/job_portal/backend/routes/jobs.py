from flask import Blueprint, render_template, request
from sqlalchemy import or_
from ..app import db
from ..models.job import Job

jobs_bp = Blueprint("jobs", __name__, url_prefix="")

@jobs_bp.route("/jobs")
def list_jobs():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "")
    location = request.args.get("location", "")
    status = request.args.get("status", "open")

    query = Job.query
    if status:
        query = query.filter_by(status=status)
    if q:
        like = f"%%{q}%%"
        query = query.filter(or_(Job.title.ilike(like), Job.description.ilike(like), Job.company.ilike(like)))
    if category:
        query = query.filter(Job.category == category)
    if location:
        query = query.filter(Job.location == location)

    jobs = query.order_by(Job.posted_date.desc()).all()

    # For filters UI (distinct lists)
    categories = [c[0] for c in db.session.query(Job.category).distinct().all() if c[0]]
    locations = [l[0] for l in db.session.query(Job.location).distinct().all() if l[0]]
    return render_template("jobs_list.html", jobs=jobs, q=q, category=category, location=location, categories=categories, locations=locations)

@jobs_bp.route("/jobs/<int:job_id>")
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template("job_detail.html", job=job)
