from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.account import Account
from models.post import Post
from services.tiktok_api_service import TikTokAPIService
from services.encryption_service import EncryptionService
from app import db
from datetime import datetime, timedelta
import logging

dashboard_bp = Blueprint('dashboard', __name__)
tiktok_api = TikTokAPIService()
encryption_service = EncryptionService()
logger = logging.getLogger(__name__)

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    try:
        user_id = get_jwt_identity()
        
        # Get user accounts
        user_accounts = Account.query.filter_by(user_id=user_id).all()
        account_ids = [account.id for account in user_accounts]
        
        if not account_ids:
            return jsonify({
                'total_posts': 0,
                'scheduled_posts': 0,
                'sent_posts': 0,
                'failed_posts': 0,
                'accounts_count': 0
            }), 200
        
        # Get post counts
        total_posts = Post.query.filter(Post.account_id.in_(account_ids)).count()
        scheduled_posts = Post.query.filter(Post.account_id.in_(account_ids), Post.status == 'scheduled').count()
        sent_posts = Post.query.filter(Post.account_id.in_(account_ids), Post.status == 'sent').count()
        failed_posts = Post.query.filter(Post.account_id.in_(account_ids), Post.status == 'failed').count()
        
        # Get stats for the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        posts_last_30_days = Post.query.filter(
            Post.account_id.in_(account_ids),
            Post.created_at >= thirty_days_ago
        ).count()
        
        sent_last_30_days = Post.query.filter(
            Post.account_id.in_(account_ids),
            Post.status == 'sent',
            Post.updated_at >= thirty_days_ago
        ).count()
        
        return jsonify({
            'total_posts': total_posts,
            'scheduled_posts': scheduled_posts,
            'sent_posts': sent_posts,
            'failed_posts': failed_posts,
            'accounts_count': len(account_ids),
            'posts_last_30_days': posts_last_30_days,
            'sent_last_30_days': sent_last_30_days
        }), 200
        
    except Exception as e:
        logger.error(f"Get stats error: {str(e)}")
        return jsonify({'error': 'An error occurred while retrieving the statistics'}), 500

@dashboard_bp.route('/monthly-stats', methods=['GET'])
@jwt_required()
def get_monthly_stats():
    try:
        user_id = get_jwt_identity()
        
        # Get user accounts
        user_accounts = Account.query.filter_by(user_id=user_id).all()
        account_ids = [account.id for account in user_accounts]
        
        if not account_ids:
            return jsonify({'monthly_stats': []}), 200
        
        # Get the last 12 months
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=365)
        
        monthly_stats = []
        
        for i in range(12):
            month_start = datetime(end_date.year, end_date.month, 1) - timedelta(days=30 * i)
            month_end = datetime(month_start.year, month_start.month + 1, 1) if month_start.month < 12 else datetime(month_start.year + 1, 1, 1)
            
            scheduled_count = Post.query.filter(
                Post.account_id.in_(account_ids),
                Post.created_at >= month_start,
                Post.created_at < month_end
            ).count()
            
            sent_count = Post.query.filter(
                Post.account_id.in_(account_ids),
                Post.status == 'sent',
                Post.updated_at >= month_start,
                Post.updated_at < month_end
            ).count()
            
            failed_count = Post.query.filter(
                Post.account_id.in_(account_ids),
                Post.status == 'failed',
                Post.updated_at >= month_start,
                Post.updated_at < month_end
            ).count()
            
            monthly_stats.append({
                'month': month_start.strftime('%B %Y'),
                'scheduled': scheduled_count,
                'sent': sent_count,
                'failed': failed_count
            })
        
        return jsonify({'monthly_stats': monthly_stats}), 200
        
    except Exception as e:
        logger.error(f"Get monthly stats error: {str(e)}")
        return jsonify({'error': 'An error occurred while retrieving the monthly statistics'}), 500

@dashboard_bp.route('/accounts', methods=['GET'])
@jwt_required()
def get_accounts():
    try:
        user_id = get_jwt_identity()
        
        # Get user accounts
        user_accounts = Account.query.filter_by(user_id=user_id).all()
        accounts_list = [account.to_dict() for account in user_accounts]
        
        return jsonify({'accounts': accounts_list}), 200
        
    except Exception as e:
        logger.error(f"Get accounts error: {str(e)}")
        return jsonify({'error': 'An error occurred while retrieving the accounts'}), 500

@dashboard_bp.route('/failed-posts', methods=['GET'])
@jwt_required()
def get_failed_posts():
    try:
        user_id = get_jwt_identity()
        
        # Get user accounts
        user_accounts = Account.query.filter_by(user_id=user_id).all()
        account_ids = [account.id for account in user_accounts]
        
        if not account_ids:
            return jsonify({'failed_posts': []}), 200
        
        # Get failed posts
        failed_posts = Post.query.filter(
            Post.account_id.in_(account_ids),
            Post.status == 'failed'
        ).all()
        
        posts_list = [post.to_dict() for post in failed_posts]
        
        return jsonify({'failed_posts': posts_list}), 200
        
    except Exception as e:
        logger.error(f"Get failed posts error: {str(e)}")
        return jsonify({'error': 'An error occurred while retrieving the failed posts'}), 500

@dashboard_bp.route('/upcoming-posts', methods=['GET'])
@jwt_required()
def get_upcoming_posts():
    try:
        user_id = get_jwt_identity()
        
        # Get user accounts
        user_accounts = Account.query.filter_by(user_id=user_id).all()
        account_ids = [account.id for account in user_accounts]
        
        if not account_ids:
            return jsonify({'upcoming_posts': []}), 200
        
        # Get upcoming scheduled posts
        now = datetime.utcnow()
        upcoming_posts = Post.query.filter(
            Post.account_id.in_(account_ids),
            Post.status == 'scheduled',
            Post.scheduled_time > now
        ).order_by(Post.scheduled_time).all()
        
        posts_list = [post.to_dict() for post in upcoming_posts]
        
        return jsonify({'upcoming_posts': posts_list}), 200
        
    except Exception as e:
        logger.error(f"Get upcoming posts error: {str(e)}")
        return jsonify({'error': 'An error occurred while retrieving the upcoming posts'}), 500