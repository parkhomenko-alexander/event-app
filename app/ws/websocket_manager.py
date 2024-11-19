from typing import List

from fastapi import WebSocket

from app.schemas.event_schemas import EventFullyJoinedSchema, EventGetSchema


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_event(self, event: EventFullyJoinedSchema):
        for connection in self.active_connections:
            await connection.send_text(event.model_dump_json())
        
    async def is_empty_connections_list(self) -> bool:
        return True if self.active_connections == [] else False

websocket_manager = WebSocketManager()
