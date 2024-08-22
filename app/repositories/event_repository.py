from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.event import Event
from app.repositories.abstract_repository import SQLAlchemyRepository


class EventRepository(SQLAlchemyRepository[Event]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Event)

    # async def get_all_joined_rooms(self) -> Sequence[Event]:
    #     stmt = (
    #         select(self.model)
    #         .options(selectinload(self.model.rooms))
    #     )

    #     q_res = await self.async_session.execute(stmt)
    #     res = q_res.unique().scalars().all()
    #     return res