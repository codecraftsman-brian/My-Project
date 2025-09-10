# Global Careers — Job Portal

A full-stack job contracting portal connecting international job seekers to overseas opportunities.

## Tech Stack
- **Frontend:** HTML5, CSS3 (responsive), vanilla JS
- **Backend:** Flask (Python), Jinja templates, Flask-Login, Flask-WTF, Flask-Mail, Flask-Bcrypt
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **Email:** SMTP via Flask-Mail
- **Security:** CSRF, hashed passwords (bcrypt), session timeout

## Quick Start (Local)

1. **Clone & enter**  
   ```bash
   cd job_portal
   ```

2. **Create & fill env**  
   ```bash
   cp .env.example .env
   # edit .env with your DB and SMTP settings
   ```

3. **Create DB & schema**  
   ```bash
   createdb job_portal
   psql job_portal < database/schema.sql
   ```

4. **Install dependencies**  
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Run**  
   ```bash
   export FLASK_APP=backend/app.py
   python backend/app.py
   # visit http://localhost:8000
   ```

### Default Admin
On first run, an admin is created using `ADMIN_EMAIL` and `ADMIN_PASSWORD` from `.env`.

## Features
- User registration + email verification
- Secure login / logout (session + remember)
- Admin CRUD for jobs
- Job search/filter by keyword, category, location
- Apply to jobs (resume upload + cover letter)
- Application history page
- Email notifications (verification, application confirmation)
- Admin dashboard analytics (apps per job, recent apps)
- Bulk email to all users or applicants to a job
- SEO basics: meta, sitemap.xml, JSON-LD JobPosting

## Security Practices
- Passwords hashed with bcrypt
- CSRF protection via Flask-WTF
- ORM queries (SQL injection resistant)
- Input validation on forms
- Session lifetime configured (6 hours)

## Testing
Add tests under `backend/tests/` (not included by default). Suggested areas:
- Model creation & constraints
- Auth flows (register/login/verify)
- Job CRUD permissions
- Application workflow & email enqueue

## Deployment Notes
- Use `gunicorn` behind Nginx
- Configure `DATABASE_URL` for managed Postgres
- Configure TLS for SMTP and app
- Set `FLASK_ENV=production` and strong `SECRET_KEY`
- Regular DB backups (e.g., `pg_dump`)
- Centralized logging (Gunicorn + app logs)
