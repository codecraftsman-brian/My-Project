# # Initialize the models package
# # Import base model classes
# from .user import User
# from .account import Account
# from .post import Post

# # Import setup functions
# from .user import setup_user_model
# from .account import setup_account_model
# from .post import setup_post_model

# # Function to initialize the database
# def init_db(app):
#     """Initialize database models with the app context"""
#     with app.app_context():
#         from app import db
#         db.create_all()