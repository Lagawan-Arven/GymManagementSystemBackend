from __future__ import annotations
from fastapi import APIRouter,Request,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.core.config import limiter
from src.core.exceptions import *
from src.authenticaton.auth import hash_password,verify_password,create_access_token
from src.util.dependency import get_db_session
from src.database import models
from src.util.service import *
import logging,uuid

logger = logging.getLogger(__name__)

router = APIRouter()

class RegisterPayload(BaseModel):
    name: str
    username: str
    email: str
    password: str

class LoginPayload(BaseModel):
    emailUsername: str | None = None
    password: str

class LoginResponse(BaseModel):
    message: str
    status: str = "ok"
    access_token: str | None = None
    token_type: str | None = None
    owner: OwnerOut

    model_config = {
        "from_attributes": True
    }

class Owner(BaseModel):
    id: uuid.UUID
    name: str
    username: str
    email: str

class OwnerOut(Owner):
    model_config = {
        "from_attributes": True
    }

#=================================
            #REGISTER OWNER
#=================================
@router.post("/register")
@limiter.limit('10/minute')
def register_owner(request: Request, data: RegisterPayload, 
                db_session: Session = Depends(get_db_session)):

    #Checks if the owner already existed
    db_owner = db_session.query(models.OWNER).filter((models.OWNER.email==data.email) | (models.OWNER.username==data.username)).first()
    if db_owner:
        logger.info('Owner registration failed')
        return {"message":'Owner registration failed'}
    try:
        new_owner = models.OWNER(
            name = data.name.capitalize(),
            username = data.name.strip(),
            email = data.email,
            password = hash_password(data.password)
        )
        db_session.add(new_owner)
        db_session.commit()
        db_session.refresh(new_owner)
    except DatabaseError:
        db_session.rollback()
        raise DatabaseError()

    logger.info('Owner registration success')
    return {"message":"Registration success","status":"ok"}

#=================================
            #LOGIN OWNER
#=================================
@router.post("/login",response_model=LoginResponse)
@limiter.limit('10/minute')
def login_owner(request: Request, data: LoginPayload,
                db_session:Session = Depends(get_db_session)):

    owner = get_owner_by_email_or_username(db_session, email = data.emailUsername,username=data.emailUsername)
   
    if not verify_password(data.password,owner.password):
        raise PasswordIncorrectError()
    
    access_token = create_access_token({"id":str(owner.id)})

    logger.info('Owner login success')

    return LoginResponse(
        message = "login success",
        access_token=access_token,
        token_type="bearer",
        owner = owner
    ).model_dump()

#=================================
            #LOGIN OWNER TEST
#=================================
@router.post("/login_test",response_model=LoginResponse)
@limiter.limit('10/minute')
def login_owner(request: Request, data: OAuth2PasswordRequestForm = Depends(),
                db_session:Session = Depends(get_db_session)):

    owner = get_owner_by_email_or_username(db_session, email = data.username,username=data.username)
   
    if not verify_password(data.password,owner.password):
        raise PasswordIncorrectError()
    
    access_token = create_access_token({"id":str(owner.id)})

    logger.info('Owner login success')

    return LoginResponse(
        message = "login success",
        access_token=access_token,
        token_type="bearer",
        owner = owner
    ).model_dump()