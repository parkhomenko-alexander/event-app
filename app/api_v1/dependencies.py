from typing import Annotated

from fastapi import Depends, Query

from app.schemas.event_schemas import EventsQueryFilters
from app.schemas.general import Pagination
from app.services.event_service import EventService
from app.utils.building_cache import BuildingCache
from app.utils.redis_manager import RedisManager
from app.utils.repository_transaction_managaer import (
    AbstractRepositoryTransactionManagaer,
    SqlAlchemyRepositoryTransactionManagaer)

# async def get_event_service() -> EventService:
#     return EventService(SqlAlchemyRepositoryTransactionManagaer(), RedisManager())

# EventServiceDep = Annotated[
#     EventService,
#     Depends(get_event_service)
# ]

async def get_repository_manager() -> AbstractRepositoryTransactionManagaer:
    return SqlAlchemyRepositoryTransactionManagaer()

async def get_building_cache() -> BuildingCache:
    return BuildingCache()

async def get_event_service(
    repository_manager: AbstractRepositoryTransactionManagaer = Depends(get_repository_manager),
    building_cache: BuildingCache = Depends(get_building_cache)
) -> EventService:
    return EventService(repository_manager, building_cache)

EventServiceDep = Annotated[EventService, Depends(get_event_service)]

def pagination_dep(per_page: int = Query(20, ge=1, le=100), page: int = Query(1, ge=1),) -> Pagination:
    return Pagination(per_page=per_page, page=page)

def  filters_dep(sort_by: str = Query("id"), sort_order: str = Query("desc")):
    return EventsQueryFilters(sort_by=sort_by, sort_order=sort_order) 

PaginationDep = Annotated[
    Pagination,
    Depends(pagination_dep)
]

FiltersDep = Annotated[
    EventsQueryFilters,
    Depends(filters_dep)
]