import requests
import os
import json
import time
from datetime import datetime, timedelta
from services.encryption_service import EncryptionService

class TikTokAPIService:
    def __init__(self, encryption_service=None):
        self.api_base_url = "https://open.tiktokapis.com/v2"
        self.client_key = os.environ.get('TIKTOK_CLIENT_KEY')
        self.client_secret = os.environ.get('TIKTOK_CLIENT_SECRET')
        self.redirect_uri = os.environ.get('TIKTOK_REDIRECT_URI')
        self.encryption_service = encryption_service or EncryptionService()
    
    def get_auth_url(self):
        """Get the TikTok OAuth authorization URL"""
        scope = "user.info.basic,video.upload,video.publish"
        auth_url = f"https://www.tiktok.com/auth/authorize/"
        params = {
            "client_key": self.client_key,
            "scope": scope,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "state": "state"  # Should be a random state for security
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{auth_url}?{query_string}"
    
    def exchange_code_for_token(self, code):
        """Exchange authorization code for access token"""
        url = f"{self.api_base_url}/oauth/token/"
        data = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            # Calculate token expiry time
            expires_in = token_data.get('expires_in', 86400)  # Default to 24 hours
            token_expiry = datetime.utcnow() + timedelta(seconds=expires_in)
            
            return {
                'access_token': token_data.get('access_token'),
                'refresh_token': token_data.get('refresh_token'),
                'token_expiry': token_expiry
            }
        else:
            error_msg = f"Failed to exchange code for token: {response.status_code} - {response.text}"
            raise Exception(error_msg)
    
    def refresh_access_token(self, refresh_token):
        """Refresh an expired access token"""
        url = f"{self.api_base_url}/oauth/token/"
        data = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            # Calculate token expiry time
            expires_in = token_data.get('expires_in', 86400)  # Default to 24 hours
            token_expiry = datetime.utcnow() + timedelta(seconds=expires_in)
            
            return {
                'access_token': token_data.get('access_token'),
                'refresh_token': token_data.get('refresh_token'),
                'token_expiry': token_expiry
            }
        else:
            error_msg = f"Failed to refresh token: {response.status_code} - {response.text}"
            raise Exception(error_msg)
    
    def get_user_info(self, access_token):
        """Get the user's TikTok information"""
        url = f"{self.api_base_url}/user/info/"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = f"Failed to get user info: {response.status_code} - {response.text}"
            raise Exception(error_msg)
    
    def upload_video(self, access_token, video_file_path):
        """Upload a video to TikTok"""
        url = f"{self.api_base_url}/video/upload/"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        with open(video_file_path, 'rb') as video_file:
            files = {'video': video_file}
            response = requests.post(url, headers=headers, files=files)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('data', {}).get('video_id')
        else:
            error_msg = f"Failed to upload video: {response.status_code} - {response.text}"
            raise Exception(error_msg)
    
    def publish_video(self, access_token, video_id, caption):
        """Publish a previously uploaded video"""
        url = f"{self.api_base_url}/video/publish/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "video_id": video_id,
            "text": caption,
            "privacy_level": "public",
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('data', {}).get('post_id')
        else:
            error_msg = f"Failed to publish video: {response.status_code} - {response.text}"
            raise Exception(error_msg)
    
    def check_video_status(self, access_token, post_id):
        """Check the status of a published video"""
        url = f"{self.api_base_url}/post/info/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "post_id": post_id
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = f"Failed to check video status: {response.status_code} - {response.text}"
            raise Exception(error_msg)