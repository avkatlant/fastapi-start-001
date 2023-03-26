"""
Data Access Layer.
Сдесь пишутся запросы в БД.
"""
from typing import Any, cast
from uuid import UUID

from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import User, UserNotification


class UserDAL:
    """Data Access Layer for operating user info."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, name: str, surname: str, email: str) -> User:
        new_user = User(name=name, surname=surname, email=email)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def get_all_users(self) -> list[User]:
        q = select(User).where(User.is_active == True)  # noqa
        users = (await self.db_session.execute(q)).scalars().all()
        return list(users)

    async def get_user(self, user_id: UUID) -> User | None:
        user = await self.db_session.get(User, user_id, options=[selectinload(User.notifications)])
        return user

    async def delete_user(self, user_id: UUID) -> UUID | None:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))  # noqa
            .values(is_active=False)
            .returning(User.id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row:
            return cast(UUID, deleted_user_id_row[0])
        return None

    async def put_user(self, user_id: UUID, data: dict[str, Any]) -> User | None:
        user = await self.db_session.get(User, user_id)
        if user:
            for key in data:
                if data[key]:
                    setattr(user, key, data[key])
            self.db_session.add(user)
            await self.db_session.flush()
        return user


class UserNotificationDAL:
    """Data Access Layer for operating User Notification info."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_notifications(self, user_id: UUID) -> list[UserNotification]:
        q = select(UserNotification).where(UserNotification.user_id == user_id)
        notifications = (await self.db_session.execute(q)).scalars().all()
        return list(notifications)

    async def create_notification(self, user_id: UUID, message: str) -> UserNotification:
        new_notification = UserNotification(user_id=user_id, message=message)
        self.db_session.add(new_notification)
        await self.db_session.flush()
        return new_notification
