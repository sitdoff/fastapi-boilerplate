import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from src.models import BaseModel


@pytest.fixture(scope="session")
def postgres_container():
    print("START CONTAINER")
    with PostgresContainer("postgres:16", driver="asyncpg") as container:
        yield container


@pytest.fixture(scope="session")
async def db_engine(postgres_container: PostgresContainer):
    engine: AsyncEngine = create_async_engine(
        url=postgres_container.get_connection_url(),
        poolclass=NullPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)
    yield engine


@pytest.fixture
async def session(db_engine):
    session_factory = async_sessionmaker(
        bind=db_engine,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
