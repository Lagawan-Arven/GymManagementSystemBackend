from __future__ import annotations
from fastapi import APIRouter,Request,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from src.util.dependency import get_db_session,get_current_owner,get_current_admin
from src.util.service import *
from src.core.config import limiter
from src.core.exceptions import *
from src.database import models
from src.schemas import schemas
from src.authenticaton.auth import hash_password,verify_password,create_access_token

import logging

logger = logging.getLogger(__name__)

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

@router.post("/admin/login")
def admin_login(request: Request, payload: OAuth2PasswordRequestForm, db_session:Session = Depends(get_db_session),
                   current_owner = Depends(get_current_owner)):
    db_admin = db_session.query(models.ADMIN).filter(models.ADMIN.owner_id==current_owner.id).filter(models.ADMIN.username==payload.username).first()
    if not db_admin:
        logger.info('Admin not found')
    if not verify_password(payload.password,db_admin.password):
        logger.info('Incorrect password')
    access_token = create_access_token({'id':db_admin.id})
    logger.info('Admin login successful')
    return {"message":'Admin login successful','access_token':access_token,"token_type":'bearer'}

@router.get('/members',response_model=List[MemberOut])
def get_all_members(request:Request, db_session:Session = Depends(get_db_session),
                   current_owner = Depends(get_current_owner)):
    try:
        db_members = db_session.query(models.MEMBER).filter(models.MEMBER.owner_id==current_owner.id).all()
        if not db_members:
            logger.error('member not found')
        return db_members
    except DatabaseError:
        logger.error('member not found')
        raise DatabaseError()

@router.post('/members')
def add_member(request:Request, payload: MemberPayload, db_session:Session = Depends(get_db_session),
               current_admin = Depends(get_current_admin), current_owner = Depends(get_current_owner)):

    #Checks if the member already existed
    member = db_session.query(models.member).filter(models.MEMBER.owner_id==current_owner.id).filter(models.MEMBER.email==payload.email).first()
    if member:
        logger.info('member creation failed')
        raise AlreadyExistsError(f'member: {member.name}')
    try:
        new_member = models.MEMBER (
            name = payload.name,
            age = payload.age,
            sex = payload.sex,
            email = payload.email,
            contact_number = payload.contact_number,
            owner = current_owner,
            admin = current_admin,
        )
        db_session.add(new_member)
        db_session.commit()
        logger.info('member creation successful')
        return {"message":"member Creation Successful"}
    except DatabaseError:
        db_session.rollback()
        logger.info('member creation failed')
        raise DatabaseError()
    
@router.patch('/members/{member_id}')
def update_member(request:Request,member_id:str, payload: MemberUpdatePayload, db_session:Session = Depends(get_db_session),
                 current_admin = Depends(get_current_admin), current_owner = Depends(get_current_owner) ):
                 
    member = get_member_by_id(member_id,db_session,current_owner)
    if payload.name == None and payload.username == None and payload.email == None and payload.password == None:
        logger.info('Need atleast one data to update')
        raise ValueError()
    
    if payload.name: member.name = payload.name
    if payload.age: member.age = payload.age
    if payload.sex: member.sex = payload.sex
    if payload.email: member.email = payload.email
    if payload.contact_number: member.contact_number = payload.contact_number
   
    try:
        db_session.commit()
        db_session.refresh(member)
        logger.info('member update successful')
    except DatabaseError:
        db_session.rollback()
        logger.info('member update failed')
        raise DatabaseError()

@router.delete('/members/{member_id}')
def delete_member(request:Request, member_id:str, db_session:Session = Depends(get_db_session),
                 current_owner = Depends(get_current_owner)):
    member = get_member_by_id(member_id,db_session,current_owner)
    try:
        db_session.delete(member)
        db_session.commit()
        logger.info('member deletion successful')
    except DatabaseError:
        db_session.rollback()
        logger.info('member deletion failed')
        raise DatabaseError()
    
@router.get('/sessions')
def get_all_sessions(request: Request, db_session: Session = Depends(get_db_session)):
    pass
    