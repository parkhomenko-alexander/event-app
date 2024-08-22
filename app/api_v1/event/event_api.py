from fastapi import APIRouter, Request

from app.api_v1.dependencies import UowDep
from app.utils.logger import log

router = APIRouter(
    tags=['Event']
)

@router.get(
    '/', 
)
async def get_events(
    uow: UowDep,
    request: Request,
):  
    log.info("events get")
    return [x**2 for x in range(5)]

@router.post(
    '/',
)
async def create_event(
    uow: UowDep,
    request: Request,
):  
    log.info("events get")
    return {"id": 123}



