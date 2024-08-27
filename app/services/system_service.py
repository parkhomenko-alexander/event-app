
from typing import Sequence

from app.db.models.system import System
from app.utils.logger import log
from app.utils.repository_transaction_managaer import \
    AbstractRepositoryTransactionManagaer


class SystemService():
    def __init__(self, repository_manager: AbstractRepositoryTransactionManagaer):
        self.repository_manager = repository_manager
    
    @staticmethod
    async def bulk_insert(repository_manager: AbstractRepositoryTransactionManagaer, systems: list[str]) -> int | None:
        """
        Systems insert
        """
        async with repository_manager:
            systems_inserting = [{"title": status} for status in systems]
            try:
                await repository_manager.system_repo.bulk_insert(systems_inserting)
                await repository_manager.commit()
            except Exception as e:
                log.error(f"Some error occurred: {e}")
                return None
            
            log.info(f"Systems were inserted")
            return 0                 
        
    @staticmethod
    async def find_one(repository_manager: AbstractRepositoryTransactionManagaer, **filters) -> System | None:
        async with repository_manager:
            try:
                system: System | None = await repository_manager.system_repo.find_one(filters)
            except Exception as e:
                log.error(f"Some error occurred: {e}")
                return None
            
            return system  

    @staticmethod 
    async def get_title_id_mapping(repository_manager: AbstractRepositoryTransactionManagaer) -> dict[str, int] | None:
        async with repository_manager:
            mapping = {}
            try:
                systems: Sequence[System] = await repository_manager.system_repo.get_all()
                if systems == []:
                    return None
                for system in systems:
                    mapping[system.title] = system.id
            except Exception as e:
                log.error(f"Some error occurred while generate systems mapping: {e}")
                return None
            
            return mapping

