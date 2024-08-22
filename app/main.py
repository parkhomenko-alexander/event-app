import threading
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api_v1 import router as router_v1
from app.db import Base, db
from app.utils.kafka_consumer import consume_events
from settings import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db.engine.begin() as async_conn:
        await async_conn.run_sync(Base.metadata.create_all)
    thread = threading.Thread(target=consume_events, daemon=True)
    thread.start()
    yield
    # thread.join()


app = FastAPI(
    lifespan=lifespan,
    root_path=config.APPLICATION_PREFIX_BEHIND_PROXY,
)

 
app.include_router(router=router_v1)
# app.include_router(router=router_v1, prefix=config.api_v1_prefix)


if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        host=config.APPLICATION_HOST, 
        port=config.APPLICATION_PORT, 
        log_level=config.APPLICATION_LOG_LEVEL, 
        reload=config.APPLICATION_DEBUG
    )