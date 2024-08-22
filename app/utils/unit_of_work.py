from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db
from app.repositories.event_repository import EventRepository


class AbstractUnitOfWork(ABC):
    event_repo: EventRepository


    @abstractmethod
    def __init__(self, *args):
        raise NotImplementedError
    
    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    
    def __init__(self):
        self.async_session_factory = db.get_async_sessionmaker()

    async def __aenter__(self):
        self.async_session: AsyncSession = self.async_session_factory()
        
        self.event_repo = EventRepository(self.async_session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.async_session.close()
        
    async def commit(self):
        await self.async_session.commit()

    async def rollback(self):
        await self.async_session.rollback()