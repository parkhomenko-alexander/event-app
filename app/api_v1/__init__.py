from fastapi import APIRouter

from .event.event_api import router as event_router
from .ws.ws_api import ws_router as ws_router

router = APIRouter()
router.include_router(router=event_router, prefix='/event')
router.include_router(router=ws_router, prefix="/ws")