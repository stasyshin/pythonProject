from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker

from app.config.config import Settings


class PostgresClient:
    __async_engine: AsyncEngine | None = None
    __async_session: async_sessionmaker | None = None

    @classmethod
    async def init_engine(cls, config: Settings):
        if not cls.__async_engine:
            connect_args = {"server_settings": {"application_name": "API"}}
            cls.__async_engine = create_async_engine(config.db.postgres_dsn
                                                     )
            await (await cls.__async_engine.connect()).aclose()

    @classmethod
    async def close(cls):
        if cls.__async_engine:
            await cls.__async_engine.dispose()

    @classmethod
    async def get_engine(cls) -> AsyncEngine | None:
        if not cls.__async_engine:
            raise RuntimeError("Postgres connection pool not initialized")
        return cls.__async_engine

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        if not cls.__async_session:
            engine = await cls.get_engine()
            cls.__async_session = async_sessionmaker(engine)
        async with cls.__async_session() as session:
            try:
                yield session
            finally:
                await session.close()

