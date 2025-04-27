from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)
from .db_config import settings


class DatabaseSessionManager:
    def __init__(self):
        database_url = settings.get_db_url()

        self.engine = create_async_engine(database_url, echo=False)
        self.async_session_maker = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False
        )

    async def close(self):
        await self.engine.dispose()


db_manager = DatabaseSessionManager()
