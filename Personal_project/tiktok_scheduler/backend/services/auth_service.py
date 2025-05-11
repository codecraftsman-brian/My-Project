from models.user import User
from app import db, jwt
from datetime import datetime
from flask_jwt_extended import create_access_token
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def register_user(self, username, email, password):
        """Register a new user"""
        try:
            # Check if user already exists
            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                if existing_user.username == username:
                    raise ValueError("Username already taken")
                else:
                    raise ValueError("Email already registered")
            
            # Create a new user
            new_user = User(
                username=username,
                email=email,
                password=password
            )
            
            # Save to database
            db.session.add(new_user)
            db.session.commit()
            
            logger.info(f"User registered successfully: {username}")
            return new_user.id
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error registering user: {str(e)}")
            raise
    
    def authenticate_user(self, username_or_email, password):
        """Authenticate a user and return JWT token"""
        try:
            # Find the user
            user = User.query.filter(
                (User.username == username_or_email) | (User.email == username_or_email)
            ).first()
            
            if not user or not user.check_password(password):
                raise ValueError("Invalid username/email or password")
            
            # Update last login time
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Generate JWT token
            access_token = create_access_token(identity=user.id)
            
            logger.info(f"User authenticated successfully: {user.username}")
            return {
                'user': user.to_dict(),
                'access_token': access_token
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error authenticating user: {str(e)}")
            raise
    
    def get_user_by_id(self, user_id):
        """Get a user by ID"""
        try:
            user = User.query.get(user_id)
            
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            return user
            
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            raise
    
    def change_password(self, user_id, current_password, new_password):
        """Change user's password"""
        try:
            user = User.query.get(user_id)
            
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            if not user.check_password(current_password):
                raise ValueError("Current password is incorrect")
            
            user.set_password(new_password)
            user.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            logger.info(f"Password changed successfully for user: {user.username}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error changing password: {str(e)}")
            raise
    
    def delete_user(self, user_id, password):
        """Delete a user account"""
        try:
            user = User.query.get(user_id)
            
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            if not user.check_password(password):
                raise ValueError("Password is incorrect")
            
            # Delete the user
            db.session.delete(user)
            db.session.commit()
            
            logger.info(f"User deleted successfully: {user.username}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting user: {str(e)}")
            raise