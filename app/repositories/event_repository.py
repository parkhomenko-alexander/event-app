from typing import Sequence, TypeAlias

from sqlalchemy import Result, Row, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.event import Event
from app.db.models.priority import Priority
from app.db.models.status_history import StatusHistory
from app.db.models.system import System
from app.repositories.abstract_repository import SQLAlchemyRepository

EventFullyJoinRow: TypeAlias = tuple[Event, StatusHistory, Priority, System]
EventFullyJoinSequence: TypeAlias = Sequence[Row[EventFullyJoinRow]]

class EventRepository(SQLAlchemyRepository[Event]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Event)

    async def get_filtered_with_last_status(self, per_page: int = 20, page: int = 1, **filter_by):
        offset: int = per_page * (page - 1)

        stmt: Select = (
            select(self.model, StatusHistory, Priority, System).
            filter_by(**filter_by).
            offset(offset).
            limit(per_page).
            join(StatusHistory, StatusHistory.event_id==self.model.id).
            join(Priority, Priority.id==self.model.priority_id).
            join(System, System.id==self.model.system_id)
        )

        query_res: Result[EventFullyJoinRow] = await self.async_session.execute(stmt)
        res: EventFullyJoinSequence = query_res.all()

        return res