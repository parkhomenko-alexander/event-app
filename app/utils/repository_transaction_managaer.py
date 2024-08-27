from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db
from app.repositories.event_repository import EventRepository
from app.repositories.priotiry_repository import PriorityRepository
from app.repositories.status_history_repository import StatusHistoryRepository
from app.repositories.status_repository import StatusRepository
from app.repositories.system_repository import SystemRepository
from app.repositories.user_repository import UserRepository


class AbstractRepositoryTransactionManagaer(ABC):
    event_repo: EventRepository
    status_repo: StatusRepository
    priority_repo: PriorityRepository
    system_repo: SystemRepository
    user_repo: UserRepository
    status_history_repo: StatusHistoryRepository


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


class SqlAlchemyRepositoryTransactionManagaer(AbstractRepositoryTransactionManagaer):
    
    def __init__(self):
        self.async_session_factory = db.get_async_sessionmaker()

    async def __aenter__(self):
        self.async_session: AsyncSession = self.async_session_factory()
        
        self.event_repo = EventRepository(self.async_session)
        self.status_repo = StatusRepository(self.async_session)
        self.priority_repo = PriorityRepository(self.async_session)
        self.system_repo = SystemRepository(self.async_session)
        self.user_repo = UserRepository(self.async_session)
        self.status_history_repo = StatusHistoryRepository(self.async_session)
        
    async def __aexit__(self, *args):
        await self.rollback()
        await self.async_session.close()
        
    async def commit(self):
        await self.async_session.commit()

    async def rollback(self):
        await self.async_session.rollback()