from fastapi import WebSocket, WebSocketDisconnect

from app.utils.logger import log
from app.ws.websocket_manager import websocket_manager


async def websocket_handler(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    log.info(websocket.headers)
    try:
        while True:
            data = await websocket.receive_json()
            command = data.get("command")
            log.info(command)
            match command:
                case "command1":
                    # Handle command1
                    await websocket.send_text("Command1 executed")

    except WebSocketDisconnect:
        log.info(websocket.headers)
        pass
    except Exception as e:
        # Handle other exceptions
        log.error(f"Error: {e}")
    finally:
        websocket_manager.disconnect(websocket)