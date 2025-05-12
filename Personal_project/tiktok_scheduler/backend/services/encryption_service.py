import os
import base64
import logging
from utils.encryption import derive_key_from_password, encrypt_data, decrypt_data

logger = logging.getLogger(__name__)

class EncryptionService:
    def __init__(self):
        self.app = None
        self.master_key = None
    
    def init_app(self, app):
        """Initialize with Flask app context"""
        self.app = app
        
        # Get master key from environment or generate one
        master_key_env = app.config.get('ENCRYPTION_MASTER_KEY') or os.environ.get('ENCRYPTION_MASTER_KEY')
        
        if master_key_env:
            try:
                self.master_key = base64.urlsafe_b64decode(master_key_env)
            except Exception as e:
                logger.error(f"Error decoding master key: {str(e)}")
                self.master_key = None
        
        if not self.master_key:
            # For development only - in production, always use an environment variable
            self.master_key = os.urandom(32)
            logger.warning("Using generated master key. This should only be used for development.")
    
    def encrypt_token(self, token, user_password):
        """Encrypt a token using the user's password"""
        if not self.master_key:
            raise ValueError("Encryption service not properly initialized")
        
        # First derive a key from the user's password
        user_key, salt = derive_key_from_password(user_password)
        
        # Encrypt the token with the user's key
        encrypted_token = encrypt_data(token, user_key)
        
        # Store the salt with the encrypted token
        return base64.urlsafe_b64encode(salt + encrypted_token).decode()
    
    def decrypt_token(self, encrypted_data, user_password):
        """Decrypt a token using the user's password"""
        if not self.master_key:
            raise ValueError("Encryption service not properly initialized")
        
        # Decode the encrypted data
        try:
            raw_data = base64.urlsafe_b64decode(encrypted_data)
            
            # Extract the salt and encrypted token
            salt = raw_data[:16]
            encrypted_token = raw_data[16:]
            
            # Derive the key from the user's password and salt
            user_key, _ = derive_key_from_password(user_password, salt)
            
            # Decrypt the token
            return decrypt_data(encrypted_token, user_key)
        except Exception as e:
            logger.error(f"Error decrypting token: {str(e)}")
            raise ValueError("Failed to decrypt token")
    
    def encrypt_for_storage(self, data):
        """Encrypt data for secure storage using the master key"""
        if not self.master_key:
            raise ValueError("Encryption service not properly initialized")
        
        # Convert the master key to the format expected by Fernet
        key = base64.urlsafe_b64encode(self.master_key)
        
        # Encrypt the data
        try:
            return encrypt_data(data, key).decode()
        except Exception as e:
            logger.error(f"Error encrypting data: {str(e)}")
            raise ValueError("Failed to encrypt data")
    
    def decrypt_from_storage(self, encrypted_data):
        """Decrypt data from secure storage using the master key"""
        if not self.master_key:
            raise ValueError("Encryption service not properly initialized")
        
        # Convert the master key to the format expected by Fernet
        key = base64.urlsafe_b64encode(self.master_key)
        
        # Decrypt the data
        try:
            return decrypt_data(encrypted_data.encode(), key)
        except Exception as e:
            logger.error(f"Error decrypting data: {str(e)}")
            raise ValueError("Failed to decrypt data")

# Create a singleton instance
encryption_service = EncryptionService()