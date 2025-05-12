from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Configure uploads
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def register_scheduler_routes(bp, services, models):
    """Register routes with blueprint"""
    scheduler_service = services['scheduler_service']
    tiktok_api_service = services['tiktok_api_service']
    Account = models['Account']
    Post = models['Post']
    
    @bp.route('/schedule', methods=['POST'])
    @jwt_required()
    def schedule_post():
        try:
            user_id = get_jwt_identity()
            
            # Validate request data
            if 'account_id' not in request.form:
                return jsonify({'error': 'Account ID is required'}), 400
                
            if 'scheduled_time' not in request.form:
                return jsonify({'error': 'Scheduled time is required'}), 400
                
            if 'video' not in request.files:
                return jsonify({'error': 'Video file is required'}), 400
            
            # Get data from request
            account_id = request.form['account_id']
            scheduled_time = datetime.fromisoformat(request.form['scheduled_time'])
            caption = request.form.get('caption', '')
            video_file = request.files['video']
            
            # Check if the account belongs to the user
            account = Account.query.filter_by(id=account_id, user_id=user_id).first()
            if not account:
                return jsonify({'error': 'Account not found or does not belong to the user'}), 404
            
            # Validate video file
            if video_file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
                
            if not allowed_file(video_file.filename):
                return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
            
            # Save the video file
            filename = secure_filename(f"{user_id}_{account_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{video_file.filename}")
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            video_file.save(file_path)
            
            # Schedule the post
            post_id = scheduler_service.schedule_post(
                user_id=user_id,
                account_id=account_id,
                video_path=file_path,
                caption=caption,
                scheduled_time=scheduled_time
            )
            
            return jsonify({
                'message': 'Post scheduled successfully',
                'post_id': post_id
            }), 201
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Schedule post error: {str(e)}")
            return jsonify({'error': 'An error occurred while scheduling the post'}), 500

    @bp.route('/reschedule/<int:post_id>', methods=['PUT'])
    @jwt_required()
    def reschedule_post(post_id):
        try:
            user_id = get_jwt_identity()
            
            # Validate request data
            if 'scheduled_time' not in request.json:
                return jsonify({'error': 'Scheduled time is required'}), 400
            
            # Get data from request
            scheduled_time = datetime.fromisoformat(request.json['scheduled_time'])
            
            # Check if the post belongs to the user
            post = Post.query.get(post_id)
            if not post:
                return jsonify({'error': 'Post not found'}), 404
                
            account = Account.query.filter_by(id=post.account_id, user_id=user_id).first()
            if not account:
                return jsonify({'error': 'Post does not belong to the user'}), 403
            
            # Reschedule the post
            scheduler_service.reschedule_post(
                post_id=post_id,
                new_scheduled_time=scheduled_time
            )
            
            return jsonify({
                'message': 'Post rescheduled successfully'
            }), 200
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Reschedule post error: {str(e)}")
            return jsonify({'error': 'An error occurred while rescheduling the post'}), 500

    @bp.route('/update/<int:post_id>', methods=['PUT'])
    @jwt_required()
    def update_post(post_id):
        try:
            user_id = get_jwt_identity()  # Add this line
            
            # Check if the post belongs to the user
            post = Post.query.get(post_id)
            if not post:
                return jsonify({'error': 'Post not found'}), 404
                
            account = Account.query.filter_by(id=post.account_id, user_id=user_id).first()
            if not account:
                return jsonify({'error': 'Post does not belong to the user'}), 403
            
            # Get data from request
            caption = request.form.get('caption')
            video_file = request.files.get('video')
            
            # Update video if provided
            file_path = None
            if video_file and video_file.filename != '':
                if not allowed_file(video_file.filename):
                    return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
                    
                # Save the new video file
                filename = secure_filename(f"{user_id}_{account.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{video_file.filename}")
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                video_file.save(file_path)
            
            # Update the post
            scheduler_service.update_post(
                post_id=post_id,
                video_path=file_path,
                caption=caption
            )
            
            return jsonify({
                'message': 'Post updated successfully'
            }), 200
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Update post error: {str(e)}")
            return jsonify({'error': 'An error occurred while updating the post'}), 500

    @bp.route('/cancel/<int:post_id>', methods=['DELETE'])
    @jwt_required()
    def cancel_post(post_id):
        try:
            user_id = get_jwt_identity()
            # Check if the post belongs to the user
            post = Post.query.get(post_id)
            if not post:
                return jsonify({'error': 'Post not found'}), 404
                
            account = Account.query.filter_by(id=post.account_id, user_id=user_id).first()
            if not account:
                return jsonify({'error': 'Post does not belong to the user'}), 403
            
            # Cancel the post
            scheduler_service.cancel_post(post_id=post_id)
            
            return jsonify({
                'message': 'Post cancelled successfully'
            }), 200
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Cancel post error: {str(e)}")
            return jsonify({'error': 'An error occurred while cancelling the post'}), 500

    @bp.route('/posts', methods=['GET'])
    @jwt_required()
    def get_posts():
        try:
            user_id = get_jwt_identity()
            # Get query parameters
            status = request.args.get('status')
            account_id = request.args.get('account_id')
            
            # Get user accounts
            user_accounts = Account.query.filter_by(user_id=user_id).all()
            account_ids = [account.id for account in user_accounts]
            
            if not account_ids:
                return jsonify({'posts': []}), 200
            
            # Build the query
            query = Post.query.filter(Post.account_id.in_(account_ids))
            
            if status:
                query = query.filter_by(status=status)
                
            if account_id:
                query = query.filter_by(account_id=account_id)
            
            # Get the posts
            posts = query.all()
            posts_list = [post.to_dict() for post in posts]
            
            return jsonify({'posts': posts_list}), 200
            
        except Exception as e:
            logger.error(f"Get posts error: {str(e)}")
            return jsonify({'error': 'An error occurred while retrieving the posts'}), 500