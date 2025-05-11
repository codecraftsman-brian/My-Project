import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_username(username):
    """Validate username format"""
    # Alphanumeric, underscore, dash, 3-50 characters
    pattern = r'^[a-zA-Z0-9_-]{3,50}$'
    return bool(re.match(pattern, username))

def validate_password(password):
    """Validate password strength"""
    # At least 8 characters
    if len(password) < 8:
        return False
    
    # Should have at least one letter and one number
    has_letter = bool(re.search(r'[a-zA-Z]', password))
    has_number = bool(re.search(r'\d', password))
    
    return has_letter and has_number

def validate_datetime(date_string):
    """Validate that a string can be parsed as datetime"""
    try:
        if isinstance(date_string, str):
            datetime.fromisoformat(date_string)
        return True
    except (ValueError, TypeError):
        return False

def validate_scheduled_time(scheduled_time):
    """Validate that scheduled time is in the future"""
    if not validate_datetime(scheduled_time):
        return False
    
    # Parse the datetime
    if isinstance(scheduled_time, str):
        scheduled_time = datetime.fromisoformat(scheduled_time)
    
    # Check if the scheduled time is in the future
    return scheduled_time > datetime.utcnow()

def validate_video_extension(filename):
    """Validate that a file has an allowed video extension"""
    allowed_extensions = {'mp4', 'mov', 'avi'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def validate_caption_length(caption):
    """Validate that a caption is within TikTok's limits"""
    # TikTok typically allows captions up to 2200 characters
    return len(caption) <= 2200