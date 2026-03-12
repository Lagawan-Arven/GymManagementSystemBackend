from fastapi import APIRouter,Depends

from src.core.dependencies import get_owner_service
from src.services import OwnerService

router = APIRouter()

@router.get('/owners')
def get_owners(service: OwnerService = Depends(get_owner_service)):
    service.get_list()

