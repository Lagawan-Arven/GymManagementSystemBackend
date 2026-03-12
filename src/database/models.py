from sqlalchemy import Column,String,Enum,DateTime,ForeignKey,Boolean
from sqlalchemy.orm import relationship,Mapped,mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from enum import StrEnum
from datetime import datetime,timezone,timedelta
import uuid,shortuuid
from typing import List,Any

Base = declarative_base()

class Action(StrEnum):
    add_member = 'MEMBER-ADDED'
    update_member = 'MEMBER-UPDATED'
    delete_member = 'MEMBER-DELETED'
    add_admin = 'ADMIN-ADDED'
    update_admin = 'ADMIN-UPDATED'
    delete_admin = 'ADMIN-DELETED'
    admin_login = 'ADMIN-LOGIN'
    admin_logout = 'ADMIN-LOGOUT'
    member_session = 'MEMBER-SESSION'
    walkin_session = 'WALKIN-SESSION'
    membership_payment = 'MEMBERSHIP-PAYMENT'
    walkin_paymet = 'WALKIN-PAYMENT'

class SessionType(StrEnum):
    member = 'member'
    walkin = 'walkin'

class PaymentType(StrEnum):
    membership = 'membership'
    walkin = 'walkin'

class PaymentStatus(StrEnum):
    pending = 'pending'
    paid = 'paid'

class MODELBASE(Base):
    __abstract__ = True
    
    added_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc).isoformat(),
                         onupdate=lambda: datetime.now(timezone.utc).isoformat())
                         
    isDeleted:Mapped[bool] = mapped_column(default=False, server_default='false')

#=================================
            #OWNER
#=================================
class OWNER(MODELBASE):
    __tablename__ =  'Owners'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name: Mapped[str]
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    
    admins: Mapped[List["ADMIN"]] = relationship(back_populates='owner')
    members: Mapped[List["MEMBER"]] = relationship(back_populates='owner')
    sessions: Mapped[List["SESSION"]] = relationship(back_populates='owner')
    logs: Mapped[List["LOG"]] = relationship(back_populates='owner')
    payments: Mapped[List["PAYMENT"]] = relationship(back_populates="owner")

#=================================
            #ADMIN
#=================================
class ADMIN(MODELBASE):
    __tablename__ = 'Admins'

    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("Owners.id"),nullable=False)
    id: Mapped[str] = mapped_column(String,primary_key=True,default=lambda: shortuuid.uuid()[:8] ,unique=True,index=True)
    name: Mapped[str]
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    
    owner: Mapped["OWNER"] = relationship(back_populates='admins')
    members: Mapped[List["MEMBER"]] = relationship(back_populates='admin')
    sessions: Mapped[List["SESSION"]] = relationship(back_populates='admin')
    logs: Mapped[List["LOG"]] = relationship(back_populates='admin')
    payments: Mapped[List["PAYMENT"]] = relationship(back_populates="admin")

#=================================
            #MEMBER
#=================================
class MEMBER(MODELBASE):
    __tablename__ = 'Members'

    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("Owners.id"),nullable=False)
    admin_id: Mapped[str] = mapped_column(String,ForeignKey('Admins.id'),nullable=False)
    id: Mapped[str] = mapped_column(String,primary_key=True,default=lambda: shortuuid.uuid()[:8] ,unique=True,index=True)
    name: Mapped[str]
    age: Mapped[int]
    sex: Mapped[str]
    email: Mapped[str]
    contact_number: Mapped[str]
                
    updated_by: Mapped[str] = mapped_column(nullable=True,default=None)            
    renewed_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: Mapped[datetime] = mapped_column(DateTime,default=lambda: datetime.now(timezone.utc).isoformat()
                                                             + timedelta(days=30))
    
    owner: Mapped["OWNER"] = relationship(back_populates='members')
    admin: Mapped["ADMIN"] = relationship(back_populates='members')
    sessions: Mapped[List["SESSION"]] = relationship(back_populates='member')
    logs: Mapped[List["LOG"]] = relationship(back_populates='member')
    payments: Mapped[List["PAYMENT"]] = relationship(back_populates="member")

    @property
    def isActive(self) -> bool:
        return datetime.now(timezone.utc).isoformat() < self.expires_at

    @property
    def days_remaining(self) -> int:
        remaining = self.expires_at - datetime.now(timezone.utc).isoformat()
        return max(remaining.days, 0)

#=================================
            #SESSION
#=================================
class SESSION(MODELBASE):
    __tablename__ = 'Sessions'

    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("Owners.id"),nullable=False)
    admin_id: Mapped[str] = mapped_column(String,ForeignKey('Admins.id'),nullable=False)
    member_id: Mapped[str] = mapped_column(String,ForeignKey('Members.id'),nullable=True)
    id: Mapped[int] = mapped_column(primary_key=True,unique=True,index=True,autoincrement=True)
    type:Mapped[SessionType] = mapped_column(Enum(SessionType))

    owner: Mapped["OWNER"] = relationship(back_populates='sessions')
    admin: Mapped["ADMIN"] = relationship(back_populates='sessions')
    member: Mapped["MEMBER"] = relationship(back_populates='sessions')
    log: Mapped["LOG"] = relationship(back_populates="session")

#=================================
            #PAYMENTS
#=================================
class PAYMENT(Base):
    __tablename__ = 'Payments'

    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("Owners.id"),nullable=False)
    admin_id: Mapped[str] = mapped_column(String,ForeignKey('Admins.id'),nullable=False)
    member_id: Mapped[str] = mapped_column(String,ForeignKey('Members.id'),nullable=True)
    id: Mapped[int] = mapped_column(primary_key=True,unique=True,index=True,autoincrement=True)
    type: Mapped[PaymentType] = mapped_column(Enum(PaymentType))
    notes: Mapped[str] = mapped_column(nullable=True)
    transaction_ref: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus),default=PaymentStatus.paid.value)

    owner: Mapped["OWNER"] = relationship(back_populates='payments')
    admin: Mapped["ADMIN"] = relationship(back_populates='payments')
    member: Mapped["MEMBER"] = relationship(back_populates='payments')
    log: Mapped["LOG"] = relationship(back_populates="payment")

#=================================
            #LOGS
#=================================
class LOG(MODELBASE):
    __tablename__ = 'Logs'

    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("Owners.id"),nullable=False)
    admin_id:Mapped[str] = mapped_column(String,ForeignKey('Admins.id'),nullable=False)
    member_id: Mapped[str] = mapped_column(String,ForeignKey('Members.id'),nullable=True)
    session_id: Mapped[int] = mapped_column(ForeignKey('Sessions.id'),nullable=True)
    payment_id: Mapped[int] = mapped_column(ForeignKey('Payments.id'),nullable=True)
    id: Mapped[int] = mapped_column(primary_key=True,unique=True,index=True,autoincrement=True)
    action: Mapped[Action] = mapped_column(Enum(Action))
    details: Mapped[str]
    
    owner: Mapped["OWNER"] = relationship(back_populates='logs')
    admin: Mapped["ADMIN"] = relationship(back_populates='logs')
    member: Mapped["MEMBER"] = relationship(back_populates='logs')
    session: Mapped["SESSION"] = relationship(back_populates="log")
    payment: Mapped["PAYMENT"] = relationship(back_populates="log")
