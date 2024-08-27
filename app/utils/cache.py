from app.services.status_service import StatusService


async def initiate_event_cache():
    cache: dict[str, dict]
    statuses =  StatusService