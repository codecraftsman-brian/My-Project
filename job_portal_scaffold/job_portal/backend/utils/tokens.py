import os
from itsdangerous import URLSafeTimedSerializer

def get_serializer():
    secret = os.getenv("SECRET_KEY", "dev-key-change-me")
    return URLSafeTimedSerializer(secret_key=secret, salt="email-verify")

def generate_email_token(email: str) -> str:
    s = get_serializer()
    return s.dumps(email)

def verify_email_token(token: str, max_age=60*60*24*3):  # 3 days
    s = get_serializer()
    return s.loads(token, max_age=max_age)
