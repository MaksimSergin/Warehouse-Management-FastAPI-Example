import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import create_app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings

DATABASE_URL_TEST = settings.DATABASE_URL_TEST

engine_test = create_async_engine(
    DATABASE_URL_TEST,
    echo=False,
    future=True,
)

AsyncSessionLocal_test = sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def db_session():
    async with AsyncSessionLocal_test() as session:
        yield session


@pytest.fixture(scope="function")
async def app(db_session):
    settings.DATABASE_URL = settings.DATABASE_URL_TEST

    app = create_app()

    async def override_get_db():
        async with AsyncSessionLocal_test() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture(scope="function")
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
