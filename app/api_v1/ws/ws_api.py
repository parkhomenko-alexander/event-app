from fastapi import APIRouter, WebSocket

from app.utils.logger import log
from app.ws.websocket_handlers import websocket_handler

ws_router = APIRouter()

@ws_router.websocket("/")
async def websocket_route(websocket: WebSocket):
    await websocket_handler(websocket) 