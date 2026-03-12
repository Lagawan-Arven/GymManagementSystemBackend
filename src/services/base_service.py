from fastapi import HTTPException,status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from uuid import UUID

from src.utils.logger import log_action

class BaseService:
    ''' Base Service that handles CRUD Operations '''
    def __init__(self,repo):
        self.repo = repo

    def get_list(self,owner_id:UUID|None=None, page:int = 0, size:int = 10):
        objects = self.repo.list(owner_id,page,size)
        return objects

    def add_object(self,payload,unique_check,resource_name="object",admin_id:str|None=None,owner_id:UUID|None=None):
        #Check if the object already existed
        existing_object = unique_check(payload,owner_id)
        if existing_object:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'{resource_name} already existed')
        
        if isinstance(payload,dict):
            data = payload
        else:
            data = payload.model_dump()
       
        if owner_id:
            data['owner_id'] = owner_id
        if admin_id:
            data['admin_id'] = admin_id
        new_object = self.repo.model(**data)

        self.repo.create(new_object)
        try:
            self.repo.db.commit()
            self.repo.db.refresh(new_object)
            log_action(owner_id if owner_id else None,'added',resource_name,new_object.id)
            return new_object
        
        except IntegrityError:
            self.repo.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,detail=f"{resource_name} with this email already exists")
        except SQLAlchemyError:
            self.repo.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f'Database error while creating {resource_name}')

    def update_object(self, object_id, update_data, owner_id:UUID|None = None, resource_name="object"):
        if owner_id:  
            object = self.repo.get(object_id,owner_id)
        object = self.repo.get(object_id)   
        if not object:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{resource_name} not found')
        
        if isinstance(update_data,dict):
            data = update_data
        else:
            data = update_data.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='No fields provided')
        
        self.repo.update(object,data)
        try:
            self.repo.db.commit()
            self.repo.db.refresh(object)
            log_action(owner_id,'updated',resource_name,object_id)
            return object
        except SQLAlchemyError:
            self.repo.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f'Database error while updating {resource_name}')
        
    def delete_object(self,object_id,owner_id:UUID|None = None,resource_name="object"):
        if not owner_id:
            object = self.repo.get(object_id)
        if owner_id:  
            object = self.repo.get(object_id,owner_id)
        if not object:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{resource_name} not found')
        
        self.repo.soft_delete(object)
        try:
            self.repo.db.commit()
            self.repo.db.refresh(object)
            log_action(owner_id if owner_id else None,'deleted',resource_name,object_id)
            return object
        except SQLAlchemyError:
            self.repo.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f'Database error while deleting a {resource_name}')