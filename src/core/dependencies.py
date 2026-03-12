from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
import os

from src.core.config import ENV
from src.database.db_config import db_session
from src.database import models

from src.repositories import OwnerRepo,AdminRepo,MemberRepo,SessionRepo,PaymentRepo,LogRepo
from src.services import AuthService,AdminService,MemberService,OwnerService,SessionService,PaymentService,LogsService

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
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='Invalid token credential')
    
    db_owner = db_session.get(models.OWNER,owner_id)
    if not db_owner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Owner not found')
    return db_owner

def get_current_admin(access_token: str = Depends(admin_oauth2_scheme),
                      db_session: Session = Depends(get_db_session)):
    try:
        payload = jwt.decode(token=access_token,key=SECRET_KEY,algorithms=[ALGORITHM])
        admin_id = payload.get('id')
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='Invalid token credential')
    
    db_admin = db_session.get(models.ADMIN,admin_id)
    if not db_admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Admin not found')
    return db_admin

def get_auth_service(db_session: Session = Depends(get_db_session)):
     repo = OwnerRepo(db_session)
     return AuthService(repo)

def get_owner_service(db_session: Session = Depends(get_db_session)):
     repo = OwnerRepo(db_session)
     return OwnerService(repo)

def get_admin_service(db_session: Session = Depends(get_db_session)):
     repo = AdminRepo(db_session)
     return AdminService(repo)

def get_member_service(db_session: Session = Depends(get_db_session)):
     repo = MemberRepo(db_session)
     return MemberService(repo)

def get_session_service(db_session: Session = Depends(get_db_session)):
     repo = SessionRepo(db_session)
     return SessionService(repo)

def get_payment_service(db_session: Session = Depends(get_db_session)):
     repo = PaymentRepo(db_session)
     return PaymentService(repo)

def get_logs_service(db_session: Session = Depends(get_db_session)):
     repo = LogRepo(db_session)
     return LogsService(repo)

