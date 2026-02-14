from fastapi import APIRouter,Request

from src.core.config import limiter
from src.schemas import auth_schemas
from src.core import exceptions
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

sample_users = [{"name":"arven","age":22,"sex":"male","email":"sample@email.com","password":"1234"}]

#=================================
            #SIGNUP USER
#=================================
@router.post("/signup")
@limiter.limit('10/minute')
def signup_user(request: Request, data: auth_schemas.SignupPayload):
    
    sample_users.append(data)
    return {"message":"Signup success"}

#=================================
            #SIGNIN USER
#=================================
@router.post("/signin")
@limiter.limit('10/minute')
def signin_user(request: Request, payload: auth_schemas.SigninPayload):

    for user in sample_users:
        if payload.email == user["email"]: 
            if payload.password == user['password']:
                logger.info('Sign in successful')
                return user
            else:
                raise exceptions.PasswordIncorrectError()
    
    raise exceptions.NotFoundError("User")