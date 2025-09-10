import os
from datetime import timedelta
from flask import Flask, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# Initialize extensions (created here, configured in create_app)
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
bcrypt = Bcrypt()

def create_app():
    load_dotenv(override=False)

    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "..", "frontend"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "frontend"),
    )

    # --- Config ---
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///job_portal.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=6)
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=7)

    # Mail
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "localhost")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", "25"))
    app.config["MAIL_USE_TLS"] = bool(int(os.getenv("MAIL_USE_TLS", "0")))
    app.config["MAIL_USE_SSL"] = bool(int(os.getenv("MAIL_USE_SSL", "0")))
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER", "no-reply@jobportal.local")

    # --- Init extensions ---
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # --- Import models so tables are known ---
    from .models.user import User
    from .models.admin import Admin
    from .models.job import Job
    from .models.application import Application
    from .models.email_log import EmailLog

    # Register the user loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id: str):
        try:
            # SQLAlchemy 2.x style; falls back cleanly if user not found
            return db.session.get(User, int(user_id))
        except Exception:
            return None

    # --- DB bootstrap (create tables, seed admin) ---
    with app.app_context():
        db.create_all()
        from sqlalchemy import select, func
        has_admin = db.session.scalar(select(func.count()).select_from(Admin)) > 0
        if not has_admin:
            admin_email = os.getenv("ADMIN_EMAIL", "admin@jobportal.test")
            admin_pwd = os.getenv("ADMIN_PASSWORD", "Admin123!")
            from .utils.auth_utils import hash_password
            admin = Admin(
                email=admin_email,
                password_hash=hash_password(admin_pwd),
                permissions="superuser",
            )
            db.session.add(admin)
            db.session.commit()

    # --- Blueprints ---
    from .routes.auth import auth_bp
    from .routes.jobs import jobs_bp
    from .routes.applications import applications_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(admin_bp)

    # --- Routes ---
    @app.route("/")
    def landing():
        return render_template("index.html")

    @app.route("/sitemap.xml")
    def sitemap():
        base = request.host_url.rstrip("/")
        static_urls = [f"{base}/", f"{base}/jobs"]
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for u in static_urls:
            xml += f"  <url><loc>{u}</loc></url>\n"
        xml += "</urlset>\n"
        return app.response_class(xml, mimetype="application/xml")

    @app.route("/static/<path:filename>")
    def static_files(filename):
        return send_from_directory(app.static_folder, filename)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
