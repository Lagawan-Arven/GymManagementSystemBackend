from __future__ import annotations
from fastapi import APIRouter,Request,Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from src.core.config import limiter
from src.core.dependencies import get_auth_service,get_owner_service
from src.services import AuthService,OwnerService
import uuid

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
    message: str | None = None
    access_token: str | None = None
    token_type: str | None = None
    owner: OwnerOut | None = None

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
def register_owner(request: Request, payload: RegisterPayload, service: OwnerService = Depends(get_owner_service)):

    service.add_owner(payload)
    return {"message":"Owner Registration Successful"}

#=================================
            #LOGIN OWNER
#=================================
@router.post("/login",response_model=LoginResponse)
@limiter.limit('10/minute')
def login_owner(request: Request, data: LoginPayload, service: AuthService = Depends(get_auth_service)):

    return service.login_owner(data)
    

#=================================
            #LOGIN OWNER TEST
#=================================
@router.post("/login_test",response_model=LoginResponse)
@limiter.limit('10/minute')
def login_owner(request: Request, data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):

    return service.login_owner(data)