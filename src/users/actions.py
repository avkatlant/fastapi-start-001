from uuid import UUID

from pydantic import parse_obj_as
from sqlalchemy.ext.asyncio import AsyncSession

from .dals import UserDAL, UserNotificationDAL
from .schemas import (
    ExtendedUserSchema,
    UserCreateSchema,
    UserDeleteSchema,
    UserListSchema,
    UserNotificationCreateSchema,
    UserNotificationListSchema,
    UserNotificationSchema,
    UserSchema,
    UserUpdateSchema,
)


class UserAction:
    @staticmethod
    async def create_new_user(body: UserCreateSchema, session: AsyncSession) -> UserSchema:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
            )
            return UserSchema.from_orm(user)

    @staticmethod
    async def get_all_users(session: AsyncSession) -> UserListSchema:
        async with session.begin():
            user_dal = UserDAL(session)
            users = await user_dal.get_all_users()
            return UserListSchema(users=parse_obj_as(list[UserSchema], users))

    @staticmethod
    async def get_user(user_id: UUID, session: AsyncSession) -> ExtendedUserSchema | None:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user(user_id)
            if user:
                return ExtendedUserSchema.from_orm(user)
            return None

    @staticmethod
    async def delete_user(user_id: UUID, session: AsyncSession) -> UserDeleteSchema | None:
        async with session.begin():
            user_dal = UserDAL(session)
            current_id = await user_dal.delete_user(user_id)
            if current_id is not None:
                return UserDeleteSchema(id=current_id)
            return None

    @staticmethod
    async def put_user(user_id: UUID, data: UserUpdateSchema, session: AsyncSession) -> UserSchema | None:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.put_user(user_id, data.dict())
            if user:
                return UserSchema.from_orm(user)
            return None


class UserNotificationAction:
    @staticmethod
    async def get_user_notifications(user_id: UUID, session: AsyncSession) -> UserNotificationListSchema | None:
        async with session.begin():
            dal = UserNotificationDAL(session)
            notifications = await dal.get_notifications(user_id)
            if notifications:
                return UserNotificationListSchema(
                    notifications=parse_obj_as(list[UserNotificationSchema], notifications)
                )
            return None

    @staticmethod
    async def create_user_notification(
        user_id: UUID, body: UserNotificationCreateSchema, session: AsyncSession
    ) -> UserNotificationSchema:
        async with session.begin():
            dal = UserNotificationDAL(session)
            notification = await dal.create_notification(
                user_id=user_id,
                message=body.message,
            )
            return UserNotificationSchema.from_orm(notification)
