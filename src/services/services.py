from src.authenticaton.auth import hash_password
from src.services.base_service import BaseService
from src.repositories import OwnerRepo,AdminRepo,MemberRepo,SessionRepo,PaymentnRepo,LogRepo

class MemberService(BaseService):
    ''' Handles CRUD and other operations for the Member '''
    def __init__(self, repo: MemberRepo):
        super().__init__(repo)

    def add_member(self,payload,admin_id,owner_id):
        return self.add_object(payload, unique_check=lambda p, oid: self.repo.get_by_email(p.email,oid), resource_name='member',
                               admin_id=admin_id, owner_id=owner_id)
    
    def update_member(self,member_id,payload,owner_id,admin_id):
        data = payload.model_dump()
        data['updated_by'] = admin_id
        return self.update_object(member_id,data,owner_id,resource_name='member')

class AdminService(BaseService):
    ''' Handles CRUD and other operations for the Admin '''
    def __init__(self, repo: AdminRepo):
        super().__init__(repo)

    def add_admin(self,payload,owner_id):
        data = payload.model_dump()
        data['password'] = hash_password(data['password'])

        return self.add_object(data, unique_check=lambda p, oid: self.repo.get_by_username_or_email(p['username'],p['email'],oid),
                               resource_name='admin',owner_id=owner_id)

class OwnerService(BaseService):
    ''' Handles CRUD and other operations for the Owner '''
    def __init__(self, repo: OwnerRepo):
        super().__init__(repo)

    def add_owner(self,payload):
        data = payload.model_dump()
        data['password'] = hash_password(data['password'])

        # both p['username'] for now, change to p['email'] later
        return self.add_object(data, unique_check=lambda p,oid: self.repo.get_by_username_or_email(p['username'],p['username']),
                               resource_name='owner')
    
class SessionService(BaseService):
    ''' Handles CRUD and other operations for the Session '''
    def __init__(self, repo: SessionRepo):
        super().__init__(repo)

class PaymentService(BaseService):
    ''' Handles CRUD and other operations for the Payment '''
    def __init__(self, repo: PaymentnRepo):
        super().__init__(repo)
    
class LogsService(BaseService):
    ''' Handles CRUD and other operations for the Logs '''
    def __init__(self, repo: LogRepo):
        super().__init__(repo)
    
    