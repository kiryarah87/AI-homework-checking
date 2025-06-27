from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from auth_service import settings, logger


async_engine = create_async_engine(
    pool_pre_ping=settings.DB_POOL_PRE_PING,
    pool_size=settings.DB_POOL_SIZE,
    pool_recycle=settings.DB_POOL_RECYCLE,
    max_overflow=settings.DB_POOL_OVERFLOW,
    connect_args={"server_settings": {"jit": "off"}}
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_context_session():
    session = async_session()
    try:
        yield session
    except Exception as e:
        logger.error("Ошибка при работе с сессией: %s", e, exc_info=True)
        await session.rollback()
    finally:
        await session.close()
