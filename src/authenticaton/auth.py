from jose import jwt
from jose.exceptions import JWTError
from argon2 import PasswordHasher
from argon2.exceptions import *
from src.core.exceptions import *
from datetime import datetime,timedelta
import os

from src.core.config import ENV

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

pwd_hasher = PasswordHasher()

def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=15)
        to_encode.update({"exp":expire})
        return jwt.encode(claims=to_encode,key=SECRET_KEY,algorithm=ALGORITHM)
    except JWTError:
        raise InvalidError('token crendential')

def verify_password(input_pwd: str, hashed_pwd: str):
    try:
        return pwd_hasher.verify(hashed_pwd,input_pwd)
    except VerifyMismatchError:
        raise PasswordIncorrectError()
    except VerificationError:
        raise InvalidError('password hash')

def hash_password(input_pwd: str):
    try:
        return pwd_hasher.hash(input_pwd)
    except HashingError:
        raise InvalidError()