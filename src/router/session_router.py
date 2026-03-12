from fastapi import APIRouter,Depends,Request

from src.core.dependencies import get_current_owner,get_session_service
from src.services import SessionService
from src.core.config import limiter

router = APIRouter()

@router.get('/sessions')
@limiter.limit('10/minute')
def get_sessions(request: Request, owner = Depends(get_current_owner), service:SessionService = Depends(get_session_service)):
    return service.get_list(owner.id)

@router.post('/sessions')
@limiter.limit('10/minute')
def add_session(request: Request,payload, owner = Depends(get_current_owner), service:SessionService = Depends(get_session_service)):
    service.add_object(payload)
    return {"message":"session added successfully"}
