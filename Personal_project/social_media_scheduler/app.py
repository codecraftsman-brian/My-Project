# Social Media Scheduler Application

import os
import json
from datetime import datetime, timedelta
import time
import threading
import secrets
import logging

# Web Framework
from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# Social Media APIs
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.instagramuser import InstagramUser
from facebook_business.adobjects.adaccount import AdAccount
import requests  # Add this for TikTok API calls
import json     # Add this for handling JSON data


# For background task scheduling
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_scheduler.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scheduler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('social_scheduler')

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class SocialAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(20), nullable=False)  # 'facebook', 'instagram', 'tiktok'
    account_name = db.Column(db.String(100), nullable=False)
    account_id = db.Column(db.String(100), nullable=False)
    access_token = db.Column(db.String(500), nullable=False)
    refresh_token = db.Column(db.String(500), nullable=True)
    token_expiry = db.Column(db.DateTime, nullable=True)
    connected = db.Column(db.Boolean, default=False)
    
class ScheduledPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_account_id = db.Column(db.Integer, db.ForeignKey('social_account.id'), nullable=False)
    caption = db.Column(db.Text, nullable=True)
    media_path = db.Column(db.String(500), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # 'scheduled', 'posted', 'failed'
    error_message = db.Column(db.Text, nullable=True)
    
    social_account = db.relationship('SocialAccount', backref='scheduled_posts')

# Initialize scheduler
jobstores = {
    'default': SQLAlchemyJobStore(url=app.config['SQLALCHEMY_DATABASE_URI'])
}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

# Social Media posting functions
def post_to_facebook(post_id):
    with app.app_context():
        try:
            post = ScheduledPost.query.get(post_id)
            if not post:
                logger.error(f"Post {post_id} not found")
                return
            
            account = SocialAccount.query.get(post.social_account_id)
            if not account or account.platform != 'facebook':
                logger.error(f"Invalid account for post {post_id}")
                return
            
            # In simulation mode for development
            logger.info(f"SIMULATION: Would post to Facebook: {post.caption} (file: {post.media_path})")
            
            # Simulate API delay
            import time
            time.sleep(2)
            
            post.status = 'posted'
            db.session.commit()
            logger.info(f"Successfully simulated posting to Facebook: {post_id}")
            
        except Exception as e:
            post.status = 'failed'
            post.error_message = str(e)
            db.session.commit()
            logger.error(f"Error simulating Facebook post: {str(e)}")

def post_to_instagram(post_id):
    with app.app_context():
        try:
            post = ScheduledPost.query.get(post_id)
            if not post:
                logger.error(f"Post {post_id} not found")
                return
            
            account = SocialAccount.query.get(post.social_account_id)
            if not account or account.platform != 'instagram':
                logger.error(f"Invalid account for post {post_id}")
                return
            
            # In simulation mode for development
            logger.info(f"SIMULATION: Would post to Instagram: {post.caption} (file: {post.media_path})")
            
            # Simulate API delay
            import time
            time.sleep(2)
            
            post.status = 'posted'
            db.session.commit()
            logger.info(f"Successfully simulated posting to Instagram: {post_id}")
            
        except Exception as e:
            post.status = 'failed'
            post.error_message = str(e)
            db.session.commit()
            logger.error(f"Error simulating Instagram post: {str(e)}")

def post_to_tiktok(post_id):
    with app.app_context():
        try:
            post = ScheduledPost.query.get(post_id)
            if not post:
                logger.error(f"Post {post_id} not found")
                return
            
            account = SocialAccount.query.get(post.social_account_id)
            if not account or account.platform != 'tiktok':
                logger.error(f"Invalid account for post {post_id}")
                return
            
            # In simulation mode for development
            logger.info(f"SIMULATION: Would post to TikTok: {post.caption} (file: {post.media_path})")
            
            # Simulate API delay
            import time
            time.sleep(2)
            
            post.status = 'posted'
            db.session.commit()
            logger.info(f"Successfully simulated posting to TikTok: {post_id}")
            
        except Exception as e:
            post.status = 'failed'
            post.error_message = str(e)
            db.session.commit()
            logger.error(f"Error simulating TikTok post: {str(e)}")

# Schedule checking function
def check_and_publish_scheduled_posts():
    with app.app_context():
        # Find posts that are due to be published
        now = datetime.now()
        posts = ScheduledPost.query.filter(
            ScheduledPost.scheduled_time <= now,
            ScheduledPost.status == 'scheduled'
        ).all()
        
        for post in posts:
            account = SocialAccount.query.get(post.social_account_id)
            if not account:
                continue
                
            if account.platform == 'facebook':
                threading.Thread(target=post_to_facebook, args=(post.id,)).start()
            elif account.platform == 'instagram':
                threading.Thread(target=post_to_instagram, args=(post.id,)).start()
            elif account.platform == 'tiktok':
                threading.Thread(target=post_to_tiktok, args=(post.id,)).start()

# Add the scheduler job to check every minute
scheduler.add_job(
    check_and_publish_scheduled_posts,
    'interval',
    minutes=1,
    id='publish_scheduler',
    replace_existing=True
)

# Flask routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    accounts = SocialAccount.query.all()
    posts = ScheduledPost.query.order_by(ScheduledPost.scheduled_time.desc()).all()
    
    return render_template('index.html', accounts=accounts, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/accounts')
def accounts():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    accounts = SocialAccount.query.all()
    return render_template('accounts.html', accounts=accounts)

@app.route('/accounts/add', methods=['GET', 'POST'])
def add_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        platform = request.form.get('platform')
        account_name = request.form.get('account_name')
        account_id = request.form.get('account_id')
        access_token = request.form.get('access_token')
        
        account = SocialAccount(
            platform=platform,
            account_name=account_name,
            account_id=account_id,
            access_token=access_token,
            connected=True
        )
        
        db.session.add(account)
        db.session.commit()
        
        flash(f'Successfully added {platform} account!')
        return redirect(url_for('accounts'))
    
    return render_template('add_account.html')

@app.route('/schedule', methods=['GET', 'POST'])
def schedule_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    accounts = SocialAccount.query.all()
    
    if request.method == 'POST':
        account_id = request.form.get('account_id')
        caption = request.form.get('caption')
        scheduled_date = request.form.get('scheduled_date')
        scheduled_time = request.form.get('scheduled_time')
        
        # Handle file upload
        if 'media' not in request.files:
            flash('No file part')
            return redirect(request.url)
            
        file = request.files['media']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if file:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Parse scheduled datetime
            scheduled_datetime = datetime.strptime(f"{scheduled_date} {scheduled_time}", '%Y-%m-%d %H:%M')
            
            # Create scheduled post
            post = ScheduledPost(
                social_account_id=account_id,
                caption=caption,
                media_path=file_path,
                scheduled_time=scheduled_datetime,
                status='scheduled'
            )
            
            db.session.add(post)
            db.session.commit()
            
            flash('Post scheduled successfully!')
            return redirect(url_for('index'))
    
    return render_template('schedule.html', accounts=accounts)

@app.route('/posts')
def posts():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    status_filter = request.args.get('status', 'all')
    
    if status_filter == 'all':
        posts = ScheduledPost.query.order_by(ScheduledPost.scheduled_time.desc()).all()
    else:
        posts = ScheduledPost.query.filter_by(status=status_filter).order_by(ScheduledPost.scheduled_time.desc()).all()
    
    return render_template('posts.html', posts=posts, status_filter=status_filter)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    post = ScheduledPost.query.get_or_404(post_id)
    
    # Delete the media file
    if os.path.exists(post.media_path):
        os.remove(post.media_path)
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Post deleted successfully!')
    return redirect(url_for('posts'))

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    post = ScheduledPost.query.get_or_404(post_id)
    accounts = SocialAccount.query.all()
    
    if request.method == 'POST':
        account_id = request.form.get('account_id')
        caption = request.form.get('caption')
        scheduled_date = request.form.get('scheduled_date')
        scheduled_time = request.form.get('scheduled_time')
        
        # Update post details
        post.social_account_id = account_id
        post.caption = caption
        
        # Parse scheduled datetime
        scheduled_datetime = datetime.strptime(f"{scheduled_date} {scheduled_time}", '%Y-%m-%d %H:%M')
        post.scheduled_time = scheduled_datetime
        
        # Handle new file upload if provided
        if 'media' in request.files and request.files['media'].filename != '':
            file = request.files['media']
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Delete old media file
            if os.path.exists(post.media_path):
                os.remove(post.media_path)
                
            post.media_path = file_path
        
        db.session.commit()
        flash('Post updated successfully!')
        return redirect(url_for('posts'))
    
    # Format date and time for form
    scheduled_date = post.scheduled_time.strftime('%Y-%m-%d')
    scheduled_time = post.scheduled_time.strftime('%H:%M')
    
    return render_template('edit_post.html', post=post, accounts=accounts, 
                           scheduled_date=scheduled_date, scheduled_time=scheduled_time)

# Initialize database
with app.app_context():
    db.create_all()
    
    # Create a default admin user if none exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('password')  # CHANGE THIS PASSWORD IN PRODUCTION
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)