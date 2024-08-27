from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.system import System
from app.repositories.abstract_repository import SQLAlchemyRepository


class SystemRepository(SQLAlchemyRepository[System]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, System)