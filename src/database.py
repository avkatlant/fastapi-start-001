import logging
from typing import AsyncGenerator, cast

from sqlalchemy import MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import get_app_settings

logger = logging.getLogger(__name__)


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata_obj = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


class Base(DeclarativeBase):
    metadata = metadata_obj


# class SessionManager:
#     def __init__(self) -> None:
#         self.settings = get_app_settings()
#         self.async_engine = create_async_engine(self.settings.DATABASE_URL, future=True, echo=True)
#         self.async_session = sessionmaker(
#             bind=self.async_engine,
#             class_=AsyncSession,
#             expire_on_commit=False,
#         )

#     def __new__(cls) -> "SessionManager":
#         if not hasattr(cls, "instance"):
#             cls.instance = super().__new__(cls)
#         return cls.instance

#     def get_session(self) -> AsyncSession:
#         return cast(AsyncSession, self.async_session())


# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     try:
#         async_session = SessionManager().get_session()
#         yield async_session
#     except SQLAlchemyError as exc:
#         await async_session.rollback()
#         logger.error("Get sqlalchemy error")
#         raise exc
#     finally:
#         await async_session.close()


settings = get_app_settings()
async_engine = create_async_engine(settings.DATABASE_URL, future=True, echo=settings.SQL_SHOW_QUERY)
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        session = async_session()
        yield session
    except SQLAlchemyError as exc:
        await session.rollback()
        logger.error("Get sqlalchemy error")
        raise exc
    finally:
        await session.close()
