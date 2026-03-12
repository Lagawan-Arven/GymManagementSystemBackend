from fastapi import APIRouter,Depends,Request

from src.core.dependencies import get_current_owner,get_logs_service
from src.services import LogsService
from src.core.config import limiter

router = APIRouter()

@router.get('/logs')
@limiter.limit('10/minute')
def get_sessions(request: Request, owner = Depends(get_current_owner),service: LogsService = Depends(get_logs_service)):
    return service.get_list(owner.id)

@router.post('/logs')
@limiter.limit('10/minute')
def add_session(request: Request, payload,owner = Depends(get_current_owner), service: LogsService = Depends(get_logs_service)):
    service.add_object(payload)

