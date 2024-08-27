from typing import Annotated

from fastapi import Depends, Query

from app.schemas.general import Pagination
from app.services.event_service import EventService
from app.utils.repository_transaction_managaer import (
    AbstractRepositoryTransactionManagaer,
    SqlAlchemyRepositoryTransactionManagaer)

RepositoryTransactionManagerDep = Annotated[
    AbstractRepositoryTransactionManagaer, 
    Depends(SqlAlchemyRepositoryTransactionManagaer)
]

async def get_event_service() -> EventService:
    return EventService(SqlAlchemyRepositoryTransactionManagaer())

EventServiceDep = Annotated[
    EventService,
    Depends(get_event_service)
]

def pagination_dep(per_page: int = Query(20, ge=1, le=100), page: int = Query(1, ge=1),) -> Pagination:
    return Pagination(per_page=per_page, page=page)

PaginationDep = Annotated[
    Pagination,
    Depends(pagination_dep)
]