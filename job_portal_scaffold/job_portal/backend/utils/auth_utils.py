from flask import abort
from flask_login import current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from functools import wraps

def hash_password(password: str) -> str:
    return generate_password_hash(password).decode("utf-8")

def verify_password(pw_hash: str, password: str) -> bool:
    return check_password_hash(pw_hash, password)

def login_required_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user or not current_user.is_authenticated:
            abort(401)
        return f(*args, **kwargs)
    return wrapper
