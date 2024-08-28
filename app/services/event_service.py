from datetime import datetime

from utils.logger import log

from app.db.models.event import Event
from app.repositories.event_repository import (EventFullyJoin,
                                               EventFullyJoinSequence)
from app.schemas.event_schemas import (EventFullyJoinedSchema, EventGetSchema,
                                       EventPostSchema, PaginatedEventsSchema)
from app.schemas.general import Pagination
from app.schemas.status_history_schemas import StstusHistoryPost
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
    async def find_one(self, **filter) -> EventGetSchema | None:
        try:
            event : Event | None = await self.repository_manager.event_repo.find_one(filter)

            if not event:
                return None
            
            return EventGetSchema.model_validate(event)
        except Exception as er:
            log.error(f"Some error while finding event: {er}")

    @with_repository_manager
    async def get_event_joined(self, **filter_by) -> EventFullyJoinedSchema | None: 
        try:
            joined_event_row: EventFullyJoin = await self.repository_manager.event_repo.get_event_joined(**filter_by)
            if joined_event_row is None:
                log.info(f"Event with id {filter_by} not found")
                return 1
                # return None

            event, priority, system, first_status, last_status = joined_event_row

            return EventFullyJoinedSchema(
                description=event.description,
                priority=priority.title,
                system=system.title,
                last_status=last_status.title,
                creted_at=first_status.created_at,
                updated_at=last_status.created_at,
                id=event.id,
                priority_id=event.priority_id,
                system_id=event.system_id,
            )
        
        except Exception as er:
            log.error(er)

    @with_repository_manager
    async def get_events_joined_pagination_filters(self, pagination: Pagination, **filter_by) -> PaginatedEventsSchema | None:
        try:
            events_ids: list[int] = await self.repository_manager.event_repo.get_filtered_ids_with_pagination(pagination.per_page, pagination.page, **filter_by)
            count: int = await self.repository_manager.event_repo.get_count()
            if events_ids == []:
                return PaginatedEventsSchema(
                    per_page=pagination.per_page,
                    page=pagination.page,
                    total_count=count,
                    filtered=0,
                    events=[]
                )
            else:
                joined_events: EventFullyJoinSequence = await self.repository_manager.event_repo.get_filtered_events_with_pagination(events_ids)
                events: list[EventFullyJoinedSchema] = [
                    EventFullyJoinedSchema(
                        description=event.description,
                        priority=priority.title,
                        system=system.title,
                        last_status=last_status.title,
                        creted_at=first_status_history.created_at,
                        updated_at=last_status_history.created_at,
                        id=event.id,
                        priority_id=event.priority_id,
                        system_id=event.system_id,
                    )
                    for event, priority, system, first_status, first_status_history, last_status, last_status_history in joined_events
                ]

                return PaginatedEventsSchema(
                    per_page=pagination.per_page,
                    page=pagination.page,
                    total_count=count,
                    filtered=events.__len__(),
                    events=events
                ) 
        except Exception as er:
            log.error(f"Some error while finding event: {er}")