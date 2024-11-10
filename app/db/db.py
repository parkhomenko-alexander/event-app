from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (AsyncEngine, async_sessionmaker,
                                    create_async_engine)

from app.settings import config


class Database:
    def __init__(self, url: str, echo: bool = False):
        self.engine: AsyncEngine = create_async_engine(
            url,
            echo=echo,
            poolclass=NullPool
        )
    
        self.async_session_factory: async_sessionmaker = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )
    
    def get_async_sessionmaker(self) -> async_sessionmaker:
        return self.async_session_factory

db: Database = Database(config.get_db_uri(), config.DB_ECHO) 