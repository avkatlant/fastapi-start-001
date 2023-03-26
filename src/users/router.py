from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db

from .actions import UserAction, UserNotificationAction
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

user_router = APIRouter()


@user_router.post("/", status_code=201, response_model=UserSchema)
async def create_user(body: UserCreateSchema, db: AsyncSession = Depends(get_db)) -> UserSchema:
    return await UserAction.create_new_user(body, db)


@user_router.get("/", response_model=UserListSchema)
async def get_all_users(db: AsyncSession = Depends(get_db)) -> UserListSchema:
    return await UserAction.get_all_users(db)


@user_router.get("/{user_id}", response_model=ExtendedUserSchema)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ExtendedUserSchema:
    user = await UserAction.get_user(user_id, db)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@user_router.delete("/{user_id}", response_model=UserDeleteSchema)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> UserDeleteSchema:
    user = await UserAction.delete_user(user_id, db)
    if user:
        return user
    raise HTTPException(status_code=204)


@user_router.put("/{user_id}", response_model=UserSchema)
async def put_user(user_id: UUID, data: UserUpdateSchema, db: AsyncSession = Depends(get_db)) -> UserSchema:
    user = await UserAction.put_user(user_id, data, db)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


user_notification_router = APIRouter()


@user_notification_router.get("/{user_id}/notifications", response_model=UserNotificationListSchema)
async def get_user_notifications(user_id: UUID, db: AsyncSession = Depends(get_db)) -> UserNotificationListSchema:
    user = await UserAction.get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    notifications = await UserNotificationAction.get_user_notifications(user_id, db)
    if notifications:
        return notifications
    raise HTTPException(status_code=404, detail="Notifications not found")


@user_notification_router.post("/{user_id}/notifications", status_code=201, response_model=UserNotificationSchema)
async def create_user_notification(
    user_id: UUID, body: UserNotificationCreateSchema, db: AsyncSession = Depends(get_db)
) -> UserNotificationSchema:
    user = await UserAction.get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await UserNotificationAction.create_user_notification(user_id, body, db)
