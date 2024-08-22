from fastapi import WebSocket

from app.ws.websocket_manager import websocket_manager


async def websocket_handler(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            command = data.get("command")

            

            


    except Exception as e:
        pass
    finally:
        websocket_manager.disconnect(websocket)
