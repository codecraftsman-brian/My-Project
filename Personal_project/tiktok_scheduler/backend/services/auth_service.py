from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.db = None
        self.jwt = None
        self.User = None
    
    def init_app(self, db, jwt, User):
        """Initialize with dependencies"""
        self.db = db
        self.jwt = jwt
        self.User = User
    
    def register_user(self, username, email, password):
        """Register a new user"""
        if not self.db or not self.User:
            raise ValueError("AuthService not properly initialized")
            
        try:
            # Check if user already exists
            existing_user = self.User.query.filter(
                (self.User.username == username) | (self.User.email == email)
            ).first()
            
            if existing_user:
                if existing_user.username == username:
                    raise ValueError("Username already taken")
                else:
                    raise ValueError("Email already registered")
            
            # Create a new user
            new_user = self.User(
                username=username,
                email=email,
                password=password
            )
            
            # Save to database
            self.db.session.add(new_user)
            self.db.session.commit()
            
            logger.info(f"User registered successfully: {username}")
            return new_user.id
            
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error registering user: {str(e)}")
            raise
    
    def authenticate_user(self, username_or_email, password):
        """Authenticate a user and return JWT token"""
        if not self.db or not self.User or not self.jwt:
            raise ValueError("AuthService not properly initialized")
            
        try:
            # Find the user
            user = self.User.query.filter(
                (self.User.username == username_or_email) | (self.User.email == username_or_email)
            ).first()
            
            if not user or not user.check_password(password):
                raise ValueError("Invalid username/email or password")
            
            # Update last login time
            user.last_login = datetime.utcnow()
            self.db.session.commit()
            
            # Generate JWT token
            from flask_jwt_extended import create_access_token
            access_token = create_access_token(identity=user.id)
            
            logger.info(f"User authenticated successfully: {user.username}")
            return {
                'user': user.to_dict(),
                'access_token': access_token
            }
            
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error authenticating user: {str(e)}")
            raise
    
    def get_user_by_id(self, user_id):
        """Get a user by ID"""
        if not self.User:
            raise ValueError("AuthService not properly initialized")
            
        try:
            user = self.User.query.get(user_id)
            
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            return user
            
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            raise
    
    def change_password(self, user_id, current_password, new_password):
        """Change user's password"""
        if not self.db or not self.User:
            raise ValueError("AuthService not properly initialized")
            
        try:
            user = self.User.query.get(user_id)
            
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            if not user.check_password(current_password):
                raise ValueError("Current password is incorrect")
            
            user.set_password(new_password)
            user.updated_at = datetime.utcnow()
            
            self.db.session.commit()
            
            logger.info(f"Password changed successfully for user: {user.username}")
            return True
            
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error changing password: {str(e)}")
            raise
    
    def delete_user(self, user_id, password):
        """Delete a user account"""
        if not self.db or not self.User:
            raise ValueError("AuthService not properly initialized")
            
        try:
            user = self.User.query.get(user_id)
            
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            if not user.check_password(password):
                raise ValueError("Password is incorrect")
            
            # Delete the user
            self.db.session.delete(user)
            self.db.session.commit()
            
            logger.info(f"User deleted successfully: {user.username}")
            return True
            
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error deleting user: {str(e)}")
            raise

# Create a singleton instance
auth_service = AuthService()