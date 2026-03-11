from __future__ import annotations
from fastapi import APIRouter,Request,Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from src.util.dependency import get_db_session,get_current_owner
from src.util.service import *
from src.core.config import limiter
from src.core.exceptions import *
from src.database import models
from src.authenticaton.auth import *

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class AdminPayload(BaseModel):
    name: str
    username: str
    email: str|None
    password: str

class AdminUpdatePayload(BaseModel):
    name: str|None
    username: str|None
    email: str|None
    password: str|None

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
def get_all_admins(request:Request, db_session:Session = Depends(get_db_session),
                   current_owner = Depends(get_current_owner)):
    try:
        db_admins = db_session.query(models.ADMIN).filter(models.ADMIN.owner_id==current_owner.id).all()
        if not db_admins:
            logger.error('Admin not found')
        return db_admins
    except DatabaseError:
        logger.error('Admin not found')
        raise DatabaseError()

@router.post('/admins')
def add_admin(request:Request, payload: AdminPayload, db_session:Session = Depends(get_db_session),
              current_owner = Depends(get_current_owner)):

    #Checks if the admin already existed
    admin = db_session.query(models.ADMIN).filter(models.ADMIN.owner_id==current_owner.id).filter((models.ADMIN.email==payload.email) | (models.ADMIN.username==payload.username)).first()
    if admin:
        logger.info('Admin creation failed')
        raise AlreadyExistsError(f'Admin: {admin.name}')
    try:
        new_admin = models.ADMIN (
            name = payload.name,
            username = payload.username,
            email = payload.email,
            password = hash_password(payload.password),
            owner = current_owner
        )
        db_session.add(new_admin)
        db_session.commit()
        logger.info('Admin creation successful')
        return {"message":"Admin Creation Successful"}
    except DatabaseError:
        db_session.rollback()
        logger.info('Admin creation failed')
        raise DatabaseError()
    
@router.patch('/admins/{admin_id}')
def update_admin(request:Request,admin_id:str, payload: AdminUpdatePayload, db_session:Session = Depends(get_db_session),
                 current_owner = Depends(get_current_owner) ):
    admin = get_admin_by_id(admin_id,db_session,current_owner)
    if payload.name == None and payload.username == None and payload.email == None and payload.password == None:
        logger.info('Need atleast one data to update')
        raise ValueError()
    
    if payload.name:
        admin.name = payload.name
    if payload.username:
        admin.username = payload.username
    if payload.email:
        admin.email = payload.email
    if payload.password:
        new_password = hash_password(payload.password)
        admin.password = new_password
    try:
        db_session.commit()
        db_session.refresh(admin)
        logger.info('Admin update successful')
    except DatabaseError:
        db_session.rollback()
        logger.info('Admin update failed')
        raise DatabaseError()

@router.delete('/admins/{admin_id}')
def delete_admin(request:Request, admin_id:str, db_session:Session = Depends(get_db_session),
                 current_owner = Depends(get_current_owner)):
    admin = get_admin_by_id(admin_id,db_session,current_owner)
    try:
        db_session.delete(admin)
        db_session.commit()
        logger.info('Admin deletion successful')
    except DatabaseError:
        db_session.rollback()
        logger.info('Admin deletion failed')
        raise DatabaseError()
    