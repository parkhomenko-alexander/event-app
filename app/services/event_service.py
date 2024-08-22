from utils.logger import log

from app.schemas.event_schema import EventPostSchema
from app.services.services_helper import with_uow
from app.utils.unit_of_work import AbstractUnitOfWork


class EventService():
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow
    
    @with_uow
    async def insert(self, event: EventPostSchema) -> int:
        """
        Event inserting
        """
        try:
            event_id = await self.uow.event_repo.insert(event.model_dump())
            await self.uow.commit()
        except Exception as e:
            log.error(f"Some error occurred: {e}")
            return 1
        
        log.info(f"Event was")
        return event_id

    # @with_uow
    # async def bulk_update(self, elements_update: list[BuildingPostSchema]) -> int:
    #     """
    #     Buildings updating
    #     """
    #     elements_data_for_updating = [e.model_dump() for e in elements_update]
    #     try:
    #         await self.uow.buildings_repo.bulk_update_by_external_ids(elements_data_for_updating)
    #         await self.uow.commit()
    #     except Exception as e:
    #         logger.error(f"Some error occurred: {e}")
    #         return 1
        
    #     logger.info(f"Buildings between {elements_update[0].external_id}-{elements_update[-1].external_id} were updated")
    #     return 0                 

    # @with_uow
    # async def get_existing_external_ids(self, ids: list[int]) -> set[int]:
    #     return await self.uow.buildings_repo.get_existing_external_ids(ids)
