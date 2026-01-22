from fastapi import APIRouter, Depends

from app.security.api_key import validate_api_key
from app.services.stats_service import get_stats

router = APIRouter(prefix="/stats", tags=["stats"], dependencies=[Depends(validate_api_key)])


@router.get("")
def stats():
    return get_stats()
