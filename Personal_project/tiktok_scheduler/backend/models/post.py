# from datetime import datetime

# # Function to get db without circular imports
# def get_db():
#     from app import db
#     return db

# class Post(object):
#     """Post model base class"""
    
#     # These will be initialized when the actual model is created in app.py
#     id = None
#     account_id = None
#     video_path = None
#     caption = None
#     scheduled_time = None
#     status = None
#     error_message = None
#     tiktok_post_id = None
#     created_at = None
#     updated_at = None
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'account_id': self.account_id,
#             'caption': self.caption,
#             'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
#             'status': self.status,
#             'error_message': self.error_message,
#             'tiktok_post_id': self.tiktok_post_id,
#             'created_at': self.created_at.isoformat() if self.created_at else None,
#             'updated_at': self.updated_at.isoformat() if self.updated_at else None
#         }

# # This will be used when app.py sets up the actual model
# def setup_post_model(db):
#     """Configure the Post model with SQLAlchemy"""
#     class Post(db.Model):
#         __tablename__ = 'posts'
        
#         id = db.Column(db.Integer, primary_key=True)
#         account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
#         video_path = db.Column(db.String(255), nullable=True)  # Local path or URL to video
#         caption = db.Column(db.Text, nullable=True)
#         scheduled_time = db.Column(db.DateTime, nullable=False)
#         status = db.Column(db.String(20), default='scheduled')  # scheduled, sent, failed
#         error_message = db.Column(db.Text, nullable=True)
#         tiktok_post_id = db.Column(db.String(100), nullable=True)  # ID of the post on TikTok
#         created_at = db.Column(db.DateTime, default=datetime.utcnow)
#         updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
#         def to_dict(self):
#             return {
#                 'id': self.id,
#                 'account_id': self.account_id,
#                 'caption': self.caption,
#                 'scheduled_time': self.scheduled_time.isoformat(),
#                 'status': self.status,
#                 'error_message': self.error_message,
#                 'tiktok_post_id': self.tiktok_post_id,
#                 'created_at': self.created_at.isoformat(),
#                 'updated_at': self.updated_at.isoformat()
#             }
    
#     return Post