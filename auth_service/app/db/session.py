from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from auth_service import settings, logger


async_engine = create_async_engine(
    settings.DATABASE_URI,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
    pool_size=settings.DB_POOL_SIZE,
    pool_recycle=settings.DB_POOL_RECYCLE,
    max_overflow=settings.DB_POOL_OVERFLOW,
    connect_args={"server_settings": {"jit": "off"}},
    echo=settings.LOG_RAW_SQL_QUERIES,
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_context_session():
    """
    Асинхронный контекстный менеджер для работы с сессией базы данных.
    Создает новую сессию, отдает, а затем гарантируемо закрывает сессию после завершения работы,
    даже в случае возникновения исключений. В случае исключений выполняет откат транзакции.

    Yields:
        SQLAlchemy AsyncSession: Асинхронная сессия для работы с базой данных.
    Raises:
        Exception: Любое исключение, возникшее при работе с сессией, будет залогировано,
                   после чего будет выполнен откат транзакции.
    """

    session = async_session()
    try:
        yield session
    except Exception as e:
        logger.error("Ошибка при работе с сессией: %s", e, exc_info=True)
        await session.rollback()
    finally:
        await session.close()
