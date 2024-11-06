from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


def get_engine(database_url: str = None):
    if database_url is None:
        database_url = settings.DATABASE_URL
    return create_async_engine(
        database_url,
        echo=False,
        future=True,
    )


def get_sessionmaker(engine):
    return sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )


def get_db(sessionmaker):
    async def _get_db():
        async with sessionmaker() as session:
            yield session

    return _get_db


engine = get_engine()
AsyncSessionLocal = get_sessionmaker(engine)
get_db = get_db(AsyncSessionLocal)
