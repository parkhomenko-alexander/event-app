
from fastapi import APIRouter, HTTPException

from app.api_v1.dependencies import EventServiceDep, PaginationDep
from app.schemas.event_schemas import PaginatedEventsSchema, RawEventInfoSchema
from app.utils.kafka_producer import create_producer
from app.utils.logger import log
from settings import config

router = APIRouter(
    tags=['Event']
)

@router.get(
    '',
    response_model=PaginatedEventsSchema
)
async def get_events(
    event_service: EventServiceDep,
    pagination: PaginationDep,
):
    try:
        events_with_pagination = await event_service.get_events_joined_pagination_filters(pagination)
        return events_with_pagination
    except Exception as er:
        log.error(f"Error occurred: {er}" )

@router.post(
    '',
    response_model=RawEventInfoSchema
)
async def test_kafka_workflow(
    external_event: RawEventInfoSchema
):
    producer = None
    try:
        producer = await create_producer()
        await producer.send(config.KAFKA_TOPIC_NAME_EVENTS, value=external_event.model_dump())
        return external_event
    except Exception as er:
        log.error(f"Error occurred: {er}")
        raise HTTPException(status_code=500, detail="Failed to send message to Kafka")
    finally:
        if producer:
            await producer.stop()


# @router.post(
#     '',
# )
# async def create_event(
#     uow: RepositoryTransactionManagerDep,
#     request: Request,
# ):
#     log.info("events get")
#     return {"id": 123}



