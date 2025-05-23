from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self):
        self.app = None
        self.db = None
        self.scheduler = None
        self.Post = None
        self.Account = None
        self.encryption_service = None
        self.tiktok_api_service = None
    
    def init_app(self, app, db, scheduler, models, services):
        """Initialize with Flask app context and dependencies"""
        self.app = app
        self.db = db
        self.scheduler = scheduler
        self.Post = models['Post']
        self.Account = models['Account']
        self.encryption_service = services['encryption_service']
        self.tiktok_api_service = services['tiktok_api_service']
        
        # Schedule the job to run every minute to check for posts to publish
        self.scheduler.add_job(
            self.process_scheduled_posts,
            'interval',
            minutes=1,
            id='process_scheduled_posts',
            replace_existing=True
        )
    
    def schedule_post(self, user_id, account_id, video_path, caption, scheduled_time):
        """Schedule a new post"""
        if not self.db or not self.Post:
            raise ValueError("SchedulerService not properly initialized")
            
        try:
            # Create a new post record
            new_post = self.Post(
                account_id=account_id,
                video_path=video_path,
                caption=caption,
                scheduled_time=scheduled_time,
                status='scheduled'
            )
            
            # Save to database
            self.db.session.add(new_post)
            self.db.session.commit()
            
            logger.info(f"Post scheduled successfully with ID: {new_post.id}")
            return new_post.id
            
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error scheduling post: {str(e)}")
            raise
    
    def reschedule_post(self, post_id, new_scheduled_time):
        """Reschedule an existing post"""
        if not self.db or not self.Post:
            raise ValueError("SchedulerService not properly initialized")
            
        try:
            post = self.Post.query.get(post_id)
            
            if not post:
                raise ValueError(f"Post with ID {post_id} not found")
            
            if post.status != 'scheduled':
                raise ValueError(f"Cannot reschedule post with status '{post.status}'")
            
            post.scheduled_time = new_scheduled_time
            post.updated_at = datetime.utcnow()
            
            self.db.session.commit()
            
            logger.info(f"Post {post_id} rescheduled successfully to {new_scheduled_time}")
            return True
            
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error rescheduling post: {str(e)}")
            raise
    
    def update_post(self, post_id, video_path=None, caption=None):
        """Update an existing post's content"""
        if not self.db or not self.Post:
            raise ValueError("SchedulerService not properly initialized")
            
        try:
            post = self.Post.query.get(post_id)
            
            if not post:
                raise ValueError(f"Post with ID {post_id} not found")
            
            if post.status != 'scheduled':
                raise ValueError(f"Cannot update post with status '{post.status}'")
            
            if video_path is not None:
                post.video_path = video_path
            
            if caption is not None:
                post.caption = caption
            
            post.updated_at = datetime.utcnow()
            
            self.db.session.commit()
            
            logger.info(f"Post {post_id} updated successfully")
            return True
            
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error updating post: {str(e)}")
            raise
    
    def cancel_post(self, post_id):
        """Cancel a scheduled post"""
        if not self.db or not self.Post:
            raise ValueError("SchedulerService not properly initialized")
            
        try:
            post = self.Post.query.get(post_id)
            
            if not post:
                raise ValueError(f"Post with ID {post_id} not found")
            
            if post.status != 'scheduled':
                raise ValueError(f"Cannot cancel post with status '{post.status}'")
            
            # Delete the post
            self.db.session.delete(post)
            self.db.session.commit()
            
            logger.info(f"Post {post_id} cancelled successfully")
            return True
            
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error cancelling post: {str(e)}")
            raise
    
    def process_scheduled_posts(self):
        """Process all scheduled posts that are due for publishing"""
        if not self.app or not self.db or not self.Post:
            logger.error("SchedulerService not properly initialized")
            return
            
        with self.app.app_context():
            try:
                # Get all scheduled posts that are due
                now = datetime.utcnow()
                posts_to_process = self.Post.query.filter(
                    self.Post.status == 'scheduled',
                    self.Post.scheduled_time <= now
                ).all()
                
                logger.info(f"Processing {len(posts_to_process)} scheduled posts")
                
                for post in posts_to_process:
                    self.publish_post(post.id)
                    
            except Exception as e:
                logger.error(f"Error processing scheduled posts: {str(e)}")
    
    def publish_post(self, post_id):
        """Publish a specific post to TikTok"""
        if not self.app or not self.db or not self.Post or not self.Account:
            logger.error("SchedulerService not properly initialized")
            return False
            
        with self.app.app_context():
            try:
                post = self.Post.query.get(post_id)
                
                if not post:
                    raise ValueError(f"Post with ID {post_id} not found")
                
                # Get the account information
                account = self.Account.query.get(post.account_id)
                
                if not account:
                    raise ValueError(f"Account with ID {post.account_id} not found")
                
                # Check if token is expired and refresh if needed
                if account.token_expiry and account.token_expiry <= datetime.utcnow():
                    # Decrypt the refresh token
                    refresh_token = self.encryption_service.decrypt_from_storage(account.refresh_token)
                    
                    # Refresh the token
                    token_data = self.tiktok_api_service.refresh_access_token(refresh_token)
                    
                    # Update the account with new token information
                    account.access_token = self.encryption_service.encrypt_for_storage(token_data['access_token'])
                    account.refresh_token = self.encryption_service.encrypt_for_storage(token_data['refresh_token'])
                    account.token_expiry = token_data['token_expiry']
                    
                    self.db.session.commit()
                
                # Decrypt the access token
                access_token = self.encryption_service.decrypt_from_storage(account.access_token)
                
                # Upload the video
                video_id = self.tiktok_api_service.upload_video(access_token, post.video_path)
                
                # Publish the video
                post_id_tiktok = self.tiktok_api_service.publish_video(access_token, video_id, post.caption)
                
                # Update the post status
                post.status = 'sent'
                post.tiktok_post_id = post_id_tiktok
                post.updated_at = datetime.utcnow()
                
                self.db.session.commit()
                
                logger.info(f"Post {post_id} published successfully to TikTok with ID: {post_id_tiktok}")
                return True
                
            except Exception as e:
                try:
                    # Update the post status to failed
                    post = self.Post.query.get(post_id)
                    
                    if post:
                        post.status = 'failed'
                        post.error_message = str(e)
                        post.updated_at = datetime.utcnow()
                        
                        self.db.session.commit()
                    
                    logger.error(f"Failed to publish post {post_id}: {str(e)}")
                except:
                    logger.error(f"Failed to update post status for {post_id}")
                
                return False

# Create a singleton instance
scheduler_service = SchedulerService()