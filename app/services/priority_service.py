
from typing import Sequence

from app.db.models.priority import Priority
from app.utils.logger import log
from app.utils.repository_transaction_managaer import \
    AbstractRepositoryTransactionManagaer


class PriorityService():
    def __init__(self, repository_manager: AbstractRepositoryTransactionManagaer):
        self.repository_manager = repository_manager


    @staticmethod
    async def bulk_insert(repository_manager: AbstractRepositoryTransactionManagaer, priorities: list[str]) -> int | None:
        """
        Priorities insert
        """
        async with repository_manager:
            priorities_inserting = [{"title": status} for status in priorities]
            try:
                await repository_manager.priority_repo.bulk_insert(priorities_inserting)
                await repository_manager.commit()
            except Exception as e:
                log.error(f"Some error occurred: {e}")
                return None

            log.info(f"Priorities were inserted")
            return 0


    @staticmethod
    async def find_one(repository_manager: AbstractRepositoryTransactionManagaer, **filters) -> Priority | None:
        async with repository_manager:
            try:
                priority: Priority | None = await repository_manager.priority_repo.find_one(filters)
            except Exception as e:
                log.error(f"Some error occurred: {e}")
                return None
            
            return priority 


    @staticmethod 
    async def get_title_id_mapping(repository_manager: AbstractRepositoryTransactionManagaer) -> dict[str, int] | None:
        async with repository_manager:
            mapping = {}
            try:
                priorities: Sequence[Priority] = await repository_manager.priority_repo.get_all()
                if priorities == []:
                    return None
                for prior in priorities:
                    mapping[prior.title] = prior.id
            except Exception as e:
                log.error(f"Some error occurred while generate priorities mapping: {e}")
                return None
            
            return mapping