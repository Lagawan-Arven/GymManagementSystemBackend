from sqlalchemy.orm import Session
from uuid import UUID

class BaseRepo:
    '''Base repository use for all repo'''
    def __init__(self, db:Session, model):
        self.db = db
        self.model = model

    def get(self,object_id,owner_id: UUID|None = None):
        query = self.db.query(self.model).filter(self.model.isDeleted==False)
        if owner_id:
            query = query.filter(self.model.owner_id==owner_id)
        return query.filter(self.model.id==object_id).first()
        
    def list(self,owner_id: UUID|None = None,offset:int=0, limit:int =10):
        query = self.db.query(self.model).filter(self.model.isDeleted==False)
        if owner_id:
            query = query.filter(self.model.owner_id==owner_id)
        return query.offset(offset).limit(limit).all()

    def create(self,obj):
        self.db.add(obj)
        return obj
    
    def update(self, db_obj, update_data: dict):
        for field,value in update_data.items():
            setattr(db_obj,field,value)
        return db_obj

    def soft_delete(self,db_obj):
        db_obj.isDeleted = True
        return db_obj
    
class BaseUserRepo(BaseRepo):
    '''Base repo use for user's repo'''
    def __init__(self, db,model):
        super().__init__(db, model)

    def get_by_email(self,email,owner_id: UUID|None = None):
        query = self.db.query(self.model).filter(self.model.isDeleted==False)
        if owner_id:
            query = query.filter(self.model.owner_id==owner_id)
        return query.filter(self.model.email==email).first()
    
    def get_by_username(self,username, owner_id: UUID|None = None):
        query = self.db.query(self.model).filter(self.model.isDeleted==False)
        if owner_id:
            query = query.filter(self.model.owner_id==owner_id)
        return query.filter(self.model.username==username).first()

    def get_by_username_or_email(self,username,email, owner_id: UUID|None = None):
        query = self.db.query(self.model).filter(self.model.isDeleted==False)
        if owner_id:
            query = query.filter(self.model.owner_id==owner_id)
        return query.filter((self.model.username==username) | (self.model.email==email)).first()