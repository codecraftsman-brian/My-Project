# Initialize the models package
from app import db

# Import models to make them available when importing the models package
from .user import User
from .account import Account
from .post import Post

# Create tables if they don't exist
def init_db(app):
    with app.app_context():
        db.create_all()