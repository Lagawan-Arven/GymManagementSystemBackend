from __future__ import annotations
from fastapi import APIRouter,Request,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from src.core.config import limiter
from src.schemas import schemas
from src.core.dependencies import get_current_owner,get_current_admin,get_member_service
from src.services import MemberService

router = APIRouter()

class MemberPayload(BaseModel):
    name: str
    age: int
    sex: str
    email: str
    contact_number: str

class MemberUpdatePayload(BaseModel):
    name: str|None
    age: int|None
    sex: str|None
    email: str|None
    contact_number: str|None

class MemberOut(BaseModel):
    id: str
    name: str
    email: str
    admin: AdminOut
    sessions: List[SessionOut]

    model_config = {
        "from_attributes": True
    }

class AdminOut(BaseModel):
    id:str
    name: str

    model_config = {
        "from_attributes": True
    }

class SessionOut(BaseModel):
    id:int
    type: str

    model_config = {
        "from_attributes": True
    }

@router.get('/members',response_model=List[MemberOut])
def get_members(request:Request, owner = Depends(get_current_owner), admin = Depends(get_current_admin),
                service: MemberService=Depends(get_member_service)):
    return service.get_list(owner.id)

@router.post('/members')
def add_member(request:Request, payload: MemberPayload,owner = Depends(get_current_owner),
            admin = Depends(get_current_admin),service: MemberService=Depends(get_member_service)):
    service.add_member(payload,admin.id)
    return {"message":'Member added successfully'}
    
@router.patch('/members/{member_id}')
def update_member(request:Request,member_id:str, payload: MemberUpdatePayload,
                  owner = Depends(get_current_owner),admin = Depends(get_current_admin),
                  service: MemberService=Depends(get_member_service) ):
    service.update_member(member_id,payload,owner.id,admin.id)   
    return {"message":'Member updated successfully'}     
    
@router.delete('/members/{member_id}')
def delete_member(request:Request, member_id:str,owner = Depends(get_current_owner),
                  admin = Depends(get_current_admin), service: MemberService=Depends(get_member_service)):
    service.delete_object(member_id, owner.id,resource_name='member')
    return {"message":'Member deleted successfully'}
    