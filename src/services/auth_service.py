from fastapi import HTTPException,status
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from src.repositories import OwnerRepo
from src.services.base_service import BaseService
from src.authenticaton.auth import hash_password,verify_password,create_access_token
from src.utils.logger import log_action

class AuthService(BaseService):
    ''' Handles CRUD and other operations for Auth '''
    def __init__(self, repo: OwnerRepo):
        super().__init__(repo)
        
    def login_owner(self,payload):
        
        owner = self.repo.get_by_username_or_email(payload.username,payload.username)
        if not owner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Owner not found')
        if not verify_password(payload.password,owner.password):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Password is incorrect')
        
        access_token = create_access_token({'id':str(owner.id)})
        log_action('owner','login','owner',owner.id)
        return ({'access_token':access_token,'token_type':'bearer','owner':owner})

   
