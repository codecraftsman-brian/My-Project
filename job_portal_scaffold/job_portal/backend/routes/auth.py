import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import Email
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from ..app import db
from ..models.user import User
from ..utils.auth_utils import hash_password, verify_password
from ..utils.tokens import generate_email_token, verify_email_token
from ..utils.email_utils import send_email

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
csrf = CSRFProtect()

class RegisterForm(FlaskForm):
    name = StringField("Full Name", [validators.DataRequired(), validators.Length(max=120)])
    email = StringField("Email", [validators.DataRequired(), Email(), validators.Length(max=255)])
    phone = StringField("Phone", [validators.Optional(), validators.Length(max=50)])
    address = StringField("Address", [validators.Optional(), validators.Length(max=255)])
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=8, max=255)])

class LoginForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired(), Email()])
    password = PasswordField("Password", [validators.DataRequired()])

@auth_bp.record_once
def setup(state):
    csrf.init_app(state.app)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))
        user = User(
            name=form.name.data.strip(),
            email=form.email.data.lower(),
            phone=form.phone.data.strip() if form.phone.data else None,
            address=form.address.data.strip() if form.address.data else None,
            password_hash=hash_password(form.password.data),
        )
        db.session.add(user)
        db.session.commit()
        token = generate_email_token(user.email)
        verify_link = url_for("auth.verify_email", token=token, _external=True)
        send_email(
            to=user.email,
            subject="Verify your email",
            html_body=render_template("emails/verify.html", verify_link=verify_link, name=user.name),
            text_body=f"Hi {user.name}, verify your email: {verify_link}",
        )
        flash("Account created! Please check your email to verify your account.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth_register.html", form=form)

@auth_bp.route("/verify/<token>")
def verify_email(token):
    try:
        email = verify_email_token(token)
    except Exception:
        flash("Invalid or expired verification link.", "danger")
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(email=email.lower()).first()
    if not user:
        flash("Account not found.", "danger")
    else:
        user.email_verified = True
        db.session.commit()
        flash("Email verified! You can now apply for jobs.", "success")
    return redirect(url_for("jobs.list_jobs"))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if not user or not verify_password(user.password_hash, form.password.data):
            flash("Invalid credentials.", "danger")
            return redirect(url_for("auth.login"))
        login_user(user, remember=True)
        flash("Welcome back!", "success")
        return redirect(url_for("jobs.list_jobs"))
    return render_template("auth_login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("jobs.list_jobs"))
