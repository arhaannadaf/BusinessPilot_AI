from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import(
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.core.config.settings import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800,
    pool_pre_ping=True,
    future=True
)
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
    )

async def get_db() -> AsyncGenerator[AsyncSession,None]:
    async with SessionLocal() as session:
        yield session


