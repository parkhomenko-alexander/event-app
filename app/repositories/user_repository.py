from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.repositories.abstract_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, User)