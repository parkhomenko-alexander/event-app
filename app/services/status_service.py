
from typing import Sequence

from app.db.models.status import Status
from app.utils.logger import log
from app.utils.repository_transaction_managaer import \
    AbstractRepositoryTransactionManagaer


class StatusService():
    def __init__(self, repository_manager: AbstractRepositoryTransactionManagaer):
        self.repository_manager = repository_manager

    @staticmethod
    async def bulk_insert(repository_manager: AbstractRepositoryTransactionManagaer, statuses: list[str]) -> int | None:
        """
        Statuses insert
        """
        async with repository_manager:
            statuses_inserting = [{"title": status} for status in statuses]
            try:
                await repository_manager.status_repo.bulk_insert(statuses_inserting)
                await repository_manager.commit()
            except Exception as e:
                log.error(f"Some error occurred: {e}")
                return None
            
            log.info(f"Statuses were inserted")
            return 0

    @staticmethod
    async def find_one(repository_manager: AbstractRepositoryTransactionManagaer, **filters) -> Status | None:
        async with repository_manager:
            try:
                status: Status | None = await repository_manager.status_repo.find_one(filters)
            except Exception as e:
                log.error(f"Some error occurred: {e}")
                return None
            return status

    @staticmethod 
    async def get_title_id_mapping(repository_manager: AbstractRepositoryTransactionManagaer) -> dict[str, int] | None:
        async with repository_manager:
            mapping = {}
            try:
                statuses: Sequence[Status] = await repository_manager.status_repo.get_all()
                if statuses == []:
                    return None
                for status in statuses:
                    mapping[status.title] = status.id
            except Exception as e:
                log.error(f"Some error occurred while generate mapping: {e}")
                return None
            return mapping
