from sqlalchemy.orm import Session

from src.database import models
from src.core.exceptions import *

def get_owner_by_id(id: int, db_session: Session):
    db_owner = db_session.get(models.OWNER,id)
    if not db_owner:
        raise NotFoundError('OWNER')
    return db_owner

def get_owner_by_email_or_username(db_session: Session, email:str | None = None, username:str | None = None,):
    if email == None and username == None:
        raise ValueError('missing input')
    
    db_owner = db_session.query(models.OWNER).filter((models.OWNER.email==email) | (models.OWNER.username==username)).first()
    if not db_owner:
        raise NotFoundError('owner')
    return db_owner

def get_admin_by_id(id: int, db_session: Session, current_owner: models.OWNER):
    db_admin = db_session.query(models.ADMIN).filter(models.ADMIN.owner_id==current_owner.id).filter(models.ADMIN.id==id).first()
    if not db_admin:
        raise NotFoundError('ADMIN')
    return db_admin

    
def get_admin_by_email_or_username(db_session: Session, email:str | None = None, username:str | None = None,):
    if email == None and username == None:
        raise ValueError('missing input')
    
    db_admin = db_session.query(models.ADMIN).filter((models.ADMIN.email==email) | (models.ADMIN.username==username)).first()
    if not db_admin:
        raise NotFoundError('user')
    return db_admin

def get_member_by_id(id: int, db_session: Session, current_owner: models.OWNER):
    db_member = db_session.query(models.MEMBER).filter(models.MEMBER.owner_id==current_owner.id).filter(models.MEMBER.id==id).first()
    if not db_member:
        raise NotFoundError('ADMIN')
    return db_member
