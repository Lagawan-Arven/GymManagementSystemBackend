from sqlalchemy import Column,String,Integer,Enum,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import StrEnum
from datetime import datetime

Base = declarative_base()

class UserRole(StrEnum):
    USER = 'user'
    COACH = 'coach'
    ADMIN = 'admin'
    OWNER = 'owner'

#=================================
            #USER
#=================================
class USER(Base):
    __tablename__ =  'Users'

    id = Column(Integer,primary_key=True,unique=True,autoincrement=True,index=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    name = Column(String)
    age = Column(Integer)
    sex = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=lambda: datetime.now())


