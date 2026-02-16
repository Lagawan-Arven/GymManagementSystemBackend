from fastapi import Depends
from sqlalchemy.orm import Session

from src.util.dependency import get_db_session
from src.database.models import *
from src.core.exceptions import *

def get_user_by_id(id: int, db_session: Session):
    try:
        db_user = db_session.get(USER,id)
        if not db_user:
            raise NotFoundError('USER')
        return db_user
    except DatabaseError:
        db_session.rollback()
        raise DatabaseError()

def get_user_by_email_or_username(db_session: Session, email:str | None = None, username:str | None = None,):
    if email == None and username == None:
        raise ValueError('missing input')
    
    db_user = db_session.query(USER).filter((USER.email==email) | (USER.username==username)).first()
    if not db_user:
        raise NotFoundError('user')
    
    return db_user

