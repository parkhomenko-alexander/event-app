from typing import Sequence, TypeAlias

from sqlalchemy import CTE, Result, Row, Select, Subquery, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.db.models.event import Event
from app.db.models.priority import Priority
from app.db.models.status import Status
from app.db.models.status_history import StatusHistory
from app.db.models.system import System
from app.repositories.abstract_repository import SQLAlchemyRepository

EventFullyJoinTuple: TypeAlias = tuple[Event, Priority, System, StatusHistory, Status, StatusHistory]
EventFullyJoinSequence: TypeAlias = Sequence[Row[EventFullyJoinTuple]]
EventFullyJoin: TypeAlias = Row[EventFullyJoinTuple] | None

class EventRepository(SQLAlchemyRepository[Event]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Event)

    async def get_event_joined(self, event_id: int) -> EventFullyJoin:
        first_stat_hist = aliased(StatusHistory)
        last_stat_hist = aliased(StatusHistory)

        first_stat = aliased(Status)
        last_stat = aliased(Status)


        first_status_subquery: CTE = (
            select(
                first_stat_hist.event_id,
                func.min(first_stat_hist.id).label("first_status_id")
            )
            .filter_by(event_id=event_id)
            .group_by(first_stat_hist.event_id)
            .cte("first_status_subquery")
        )

        last_status_subquery: CTE = (
            select(
                last_stat_hist.event_id,
                func.max(last_stat_hist.id).label("last_status_id")
            )
            .filter_by(event_id=event_id)
            .group_by(last_stat_hist.event_id)
            .cte("last_status_subquery")
        )

        first_status_joined_subq: Select = (
            select(
                Event,
                Priority,
                System,
                first_stat_hist,
                last_stat,
                last_stat_hist
            )
            .select_from(Event)
            .join(first_status_subquery, first_status_subquery.c.event_id == Event.id)
            .join(first_stat_hist, first_stat_hist.id == first_status_subquery.c.first_status_id)
            .join(first_stat, first_stat.id == first_stat_hist.status_id)
            .join(last_status_subquery, last_status_subquery.c.event_id == Event.id)
            .join(last_stat_hist, last_stat_hist.id == last_status_subquery.c.last_status_id)
            .join(last_stat, last_stat.id == last_stat_hist.status_id)
            .join(Priority, Event.priority_id==Priority.id)
            .join(System, Event.system_id==System.id)
        )


        r = await self.async_session.execute(first_status_joined_subq)
        res = r.one_or_none()

        return res

    async def get_filtered_events_with_pagination(self, events_ids: list[int]) -> EventFullyJoinSequence:
        first_status_history = aliased(StatusHistory)
        last_status_history = aliased(StatusHistory)

        first_status = aliased(Status)
        last_status = aliased(Status)
        
        first_statuses_aggregation: Subquery = (
            select(
                func.min(first_status_history.id).label("first_status_id")
            )
            .filter(first_status_history.event_id.in_(events_ids))
            .group_by(first_status_history.event_id)
            .subquery("first_statuses_min_ids")
        )
        # r = await self.async_session.execute(select(first_statuses_aggregation))
        # obj1 = r.all()

        first_status_subquery: Subquery = (
            select(first_status, first_status_history)
            .join(first_statuses_aggregation, first_status_history.id==first_statuses_aggregation.c.first_status_id)
            .join(first_status, first_status_history.status_id == first_status.id)
            .subquery("first_statuses")
        )
        # r = await self.async_session.execute(select(first_status_subquery))
        # obj = r.all()

        last_statuses_aggregation: Subquery = (
            select(
                func.max(last_status_history.id).label("last_status_id")
            )
            .filter(last_status_history.event_id.in_(events_ids))
            .group_by(last_status_history.event_id)
            .subquery()
        )

        last_status_subquery: Subquery = (
            select(last_status, last_status_history)
            .join(last_statuses_aggregation, last_status_history.id==last_statuses_aggregation.c.last_status_id)
            .join(last_status, last_status_history.status_id == last_status.id)
            .subquery("last_statuses")
        )

        # r = await self.async_session.execute(select(last_status_subquery))
        # obj = r.all()
        
        first_status_history = aliased(StatusHistory, first_status_subquery)
        first_status = aliased(Status, first_status_subquery)

        last_status_history = aliased(StatusHistory, last_status_subquery)
        last_status = aliased(Status, last_status_subquery)

        stmt: Select = (
            select(self.model, Priority, System, first_status_history, last_status, last_status_history)
            .join(Priority, Priority.id == self.model.priority_id)
            .join(System, System.id == self.model.system_id)
            .join(first_status_subquery, (first_status_subquery.c.event_id==self.model.id))
            .join(last_status_subquery, last_status_subquery.c.event_id == self.model.id)
        )
        
        query_res: Result[EventFullyJoinTuple] = await self.async_session.execute(stmt)
        return query_res.all()