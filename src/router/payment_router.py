from fastapi import APIRouter,Depends,Request

from src.core.dependencies import get_current_owner,get_payment_service
from src.services import PaymentService
from src.core.config import limiter

router = APIRouter()

@router.get('/payments')
@limiter.limit('10/minute')
def get_sessions(request: Request, owner = Depends(get_current_owner), service:PaymentService = Depends(get_payment_service)):
    return service.get_list(owner.id)

@router.post('/payments')
@limiter.limit('10/minute')
def add_session(request: Request,payload, owner = Depends(get_current_owner), service:PaymentService = Depends(get_payment_service)):
    service.add_object(payload)

