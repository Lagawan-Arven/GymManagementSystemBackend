from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
import os

from src.core.config import ENV
from src.database.db_config import db_session
from src.core.exceptions import *
from src.database import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login_test")
admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

def get_db_session():
    session = db_session()
    try:
        yield session
    finally:
        session.close()

def get_current_owner(access_token: str = Depends(oauth2_scheme),
                     db_session: Session = Depends(get_db_session)):
    try:
        payload = jwt.decode(token=access_token,key=SECRET_KEY,algorithms=[ALGORITHM])
        owner_id = payload.get('id')
    except:
        raise InvalidTokenError()
    
    db_owner = db_session.get(models.OWNER,owner_id)
    if not db_owner:
            raise NotFoundError('Owner')
    return db_owner

def get_current_admin(access_token: str = Depends(admin_oauth2_scheme),
                      db_session: Session = Depends(get_db_session)):
    try:
        payload = jwt.decode(token=access_token,key=SECRET_KEY,algorithms=[ALGORITHM])
        admin_id = payload.get('id')
    except:
        raise InvalidTokenError()
    
    db_admin = db_session.get(models.ADMIN,admin_id)
    if not db_admin:
            raise NotFoundError('Owner')
    return db_admin
