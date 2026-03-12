from src.database.models import MEMBER,ADMIN,OWNER,SESSION,PAYMENT,LOG
from src.repositories import BaseRepo,BaseUserRepo

class OwnerRepo(BaseUserRepo):
    def __init__(self, db):
        super().__init__(db, OWNER)

class AdminRepo(BaseUserRepo):
    def __init__(self, db):
        super().__init__(db, ADMIN)  

class MemberRepo(BaseRepo):
    def __init__(self, db):
        super().__init__(db, MEMBER)

class SessionRepo(BaseRepo):
    def __init__(self, db):
        super().__init__(db, SESSION)

class PaymentRepo(BaseRepo):
    def __init__(self, db):
        super().__init__(db, PAYMENT)

class LogRepo(BaseRepo):
    def __init__(self, db):
        super().__init__(db, OWNER)