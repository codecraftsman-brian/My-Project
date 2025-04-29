"""
Utility functions for the Telegram Message Scheduler.
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

def ensure_file_exists(file_path, default_content):
    """
    Ensure that a file exists, creating it with default content if necessary.
    
    Args:
        file_path: Path to the file
        default_content: Default content to write if file doesn't exist
    """
    if not os.path.exists(file_path):
        logger.info(f"Creating default file at {file_path}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(default_content, f, indent=4)
            
def allowed_file(filename, allowed_extensions):
    """
    Check if a filename has an allowed extension.
    
    Args:
        filename: The filename to check
        allowed_extensions: Set of allowed file extensions
        
    Returns:
        bool: True if file has an allowed extension, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions