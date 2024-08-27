from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.status_history import StatusHistory
from app.repositories.abstract_repository import SQLAlchemyRepository


class StatusHistoryRepository(SQLAlchemyRepository[StatusHistory]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, StatusHistory)