from __future__ import annotations
from fastapi import APIRouter,Request,Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.core.config import limiter
from src.core.exceptions import *
from src.authenticaton.auth import *
from src.util.dependency import get_db_session
from src.database.models import *
from src.util.service import *
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class SignupPayload(BaseModel):
    name: str
    age: int
    sex: str
    email: str
    password: str

class SigninPayload(BaseModel):
    emailUsername: str | None = None
    password: str

class SigninResponse(BaseModel):
    message: str
    status: str = "ok"
    access_token: str | None = None
    token_type: str | None = None
    user: UserOut

class User(BaseModel):
    id: int
    name: str
    age: int
    sex: str
    username: str
    email: str

class UserOut(User):
    class Config():
        from_attributes = True

#=================================
            #SIGNUP USER
#=================================
@router.post("/signup")
@limiter.limit('10/minute')
def signup_user(request: Request, data: SignupPayload, 
                db_session: Session = Depends(get_db_session)):

    #Checks if the user already existed
    db_user = db_session.query(USER).filter(USER.email==data.email).first()
    if db_user:
        logger.info('User signup failed')
        raise AlreadyExistsError(f'User: {db_user.name}')
    try:
        new_user = USER(
            name = data.name.capitalize(),
            age = data.age,
            sex = data.sex,
            username = data.name.capitalize().strip(),
            email = data.email,
            password = hash_password(data.password)
        )
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
    except DatabaseError:
        DatabaseError()

    logger.info('User signup success')
    return {"message":"Signup success","status":"ok"}

#=================================
            #SIGNIN USER
#=================================
@router.post("/signin",response_model=SigninResponse)
@limiter.limit('10/minute')
def signin_user(request: Request, data: SigninPayload,
                db_session:Session = Depends(get_db_session)):

    user = get_user_by_email_or_username(db_session, email = data.emailUsername,username=data.emailUsername)
   
    if not verify_password(data.password,user.password):
        raise PasswordIncorrectError()
    
    access_token = create_access_token({"id":user.id,"role":user.role})

    logger.info('User signin success')
    return SigninResponse(
        message = "signin success",
        access_token=access_token,
        token_type="bearer",
        user = user
    ).model_dump()