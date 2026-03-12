from __future__ import annotations
from fastapi import APIRouter,Request,Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime

from src.core.dependencies import get_current_owner,get_admin_service
from src.core.config import limiter
from src.services import AdminService

router = APIRouter()

class AdminPayload(BaseModel):
    name: str
    username: str
    email: str|None = None
    password: str

class AdminUpdatePayload(BaseModel):
    name: str|None = None
    username: str|None = None
    email: str|None = None
    password: str|None = None

class AdminOut(BaseModel):
    id: str
    name: str
    username:str
    email: str
    added_at: datetime
    updated_at: datetime
    members:List[MemberOut]
    sessions:List[SessionOut]

    model_config = {
        "from_attributes": True
    }

class MemberOut(BaseModel):
    id:str
    isActive: bool

    model_config = {
        "from_attributes": True
    }

class SessionOut(BaseModel):
    id:int
    type: str

    model_config = {
        "from_attributes": True
    }

@router.get('/admins',response_model=List[AdminOut])
@limiter.limit('10/minute')
def get_admins(request:Request, current_owner = Depends(get_current_owner), 
                   service: AdminService = Depends(get_admin_service)):
    return service.get_list(current_owner.id)

@router.post('/admins')
@limiter.limit('10/minute')
def add_admin(request:Request, payload: AdminPayload, current_owner = Depends(get_current_owner),
              service: AdminService = Depends(get_admin_service)):
    service.add_admin(payload,current_owner.id)
    return {"message":'admin added successfully'}

@router.patch('/admins/{admin_id}')
@limiter.limit('10/minute')
def update_admin(request:Request,admin_id:str, payload: AdminUpdatePayload, current_owner = Depends(get_current_owner),
                 service: AdminService = Depends(get_admin_service)):
    service.update_object(admin_id,payload,current_owner.id)
    return {"message":'admin updated successfully'}

@router.delete('/admins/{admin_id}')
@limiter.limit('10/minute')
def delete_admin(request:Request, admin_id:str, current_owner = Depends(get_current_owner),
                 service: AdminService = Depends(get_admin_service)):
    service.delete_object(admin_id,current_owner.id)
    return {"message":'admin deleted successfully'}