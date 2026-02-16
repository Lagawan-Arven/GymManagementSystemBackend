from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
import os

from src.core.config import ENV
from src.database.db_config import db_session
from src.core.exceptions import *
from src.database.models import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

def get_db_session():
    session = db_session()
    try:
        yield session
    finally:
        session.close()

def get_current_user(access_token: str = Depends(oauth2_scheme),
                     db_session: Session = Depends(get_db_session)):
    try:
        payload = jwt.decode(token=access_token,key=SECRET_KEY,algorithms=[ALGORITHM])
        user_id = int(payload.get('id'))
    except:
        raise InvalidTokenError()
    
    db_user = db_session.get(USER,user_id)
    if not db_user:
            raise NotFoundError('User')
    return db_user