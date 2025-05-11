from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def generate_key():
    """Generate a new encryption key"""
    return Fernet.generate_key()

def derive_key_from_password(password, salt=None):
    """Derive a key from a password and salt"""
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def encrypt_data(data, key):
    """Encrypt data using the provided key"""
    if isinstance(data, str):
        data = data.encode()
    
    f = Fernet(key)
    encrypted_data = f.encrypt(data)
    return encrypted_data

def decrypt_data(encrypted_data, key):
    """Decrypt data using the provided key"""
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    
    try:
        # Try to decode as string, otherwise return bytes
        return decrypted_data.decode()
    except UnicodeDecodeError:
        return decrypted_data