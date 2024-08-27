import asyncio
import threading
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api_v1 import router as router_v1
from app.api_v1.ws.ws_api import ws_router
from app.db import Base, db
from app.db.initial_data import init_db
from app.utils.kafka_consumer import consume_events
from app.utils.logger import log
from settings import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db.engine.begin() as async_conn:
        await async_conn.run_sync(Base.metadata.create_all)
    await init_db()

    # Start the Kafka consumer
    consumer_task = asyncio.create_task(consume_events())
    yield
    # Shutdown Kafka consumer
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass
    except Exception as er:
        log.error("xczxcz") 



app = FastAPI(
    lifespan=lifespan, 
    root_path=config.APPLICATION_PREFIX_BEHIND_PROXY,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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