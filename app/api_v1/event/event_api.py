
from fastapi import APIRouter

from app.api_v1.dependencies import EventServiceDep, PaginationDep
from app.schemas.event_schemas import PaginatedEventsSchema
from app.utils.logger import log

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


# @router.post(
#     '',
# )
# async def create_event(
#     uow: RepositoryTransactionManagerDep,
#     request: Request,
# ):
#     log.info("events get")
#     return {"id": 123}



