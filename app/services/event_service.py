from datetime import datetime

from utils.logger import log

from app.db.models.event import Event
from app.repositories.event_repository import EventFullyJoinSequence
from app.schemas.event_schema import (EventFullyJoined, EventGetSchema,
                                      EventPostSchema, PaginatedEvents)
from app.schemas.general import Pagination
from app.schemas.status_history_schema import StstusHistoryPost
from app.services.services_helper import with_repository_manager
from app.utils.repository_transaction_managaer import \
    AbstractRepositoryTransactionManagaer


class EventService():
    def __init__(self, repository_manager: AbstractRepositoryTransactionManagaer):
        self.repository_manager = repository_manager
    
    @with_repository_manager
    async def insert(self, event: EventPostSchema, user_id: int | None, status_id: int, created: str) -> int | None:
        """
        Event inserting
        """
        try:
            event_id = await self.repository_manager.event_repo.insert(event.model_dump())
            dt = datetime.fromisoformat(created)
            start_status_history_record = StstusHistoryPost(
                created_at=dt,
                user_id=user_id,
                event_id=event_id,
                status_id=status_id,
            )
            status_id = await self.repository_manager.status_history_repo.insert(start_status_history_record.model_dump())
            await self.repository_manager.commit()
        except Exception as e:
            log.error(f"Some error occurred: {e}")
            return None
        
        log.info(f"Event was created")
        return event_id
    
    @with_repository_manager
    async def find_one(self, **filter: int) -> EventGetSchema | None:
        try:
            event : Event | None = await self.repository_manager.event_repo.find_one(filter)

            if not event:
                return None
            
            return EventGetSchema.model_validate(event)
        except Exception as er:
            log.error(f"Some error while finding event: {er}")

    @with_repository_manager
    async def get_events_pagination_filters(self, pagination: Pagination, **filter_by) -> PaginatedEvents | None:
        try:
            events_fully_joined: EventFullyJoinSequence = await self.repository_manager.event_repo.get_filtered_with_last_status(pagination.per_page, pagination.page, **filter_by)
            count: int = await self.repository_manager.event_repo.get_count()
            if events_fully_joined == []:
                return PaginatedEvents(
                    per_page=pagination.per_page,
                    page=pagination.page,
                    total_count=count,
                    filtered=0,
                    events=[]
                )
            else:
                events: list[EventFullyJoined] = [
                    EventFullyJoined(
                        description=event.description,
                        status=status_history.status,
                        priority=priority.name,
                        system=system.name,

                        id=event.id,
                        priority_id=event.priority_id,
                        system_id=event.system_id,
                    )
                    for event, status_history, priority, system in events_fully_joined
                ]

                return PaginatedEvents(
                    per_page=pagination.per_page,
                    page=pagination.page,
                    total_count=count,
                    filtered=events.__len__(),
                    events=events
                ) 
        except Exception as er:
            log.error(f"Some error while finding event: {er}")