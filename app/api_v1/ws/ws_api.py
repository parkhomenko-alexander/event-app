from fastapi import APIRouter, WebSocket

from app.ws.websocket_handlers import websocket_handler

router = APIRouter(
    tags=['ws-api'],
    prefix="/ws"
)

@router.websocket("/")
async def websocket_route(websocket: WebSocket):
    await websocket_handler(websocket)