from jose import jwt
import os

from src.core.config import ENV

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(claims=to_encode,key=SECRET_KEY,algorithm=ALGORITHM)