import re
import uuid
from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator

# from src.user_notification.schemas import UserNotificationSchema

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class UserSchema(TunedModel):
    id: uuid.UUID
    name: str
    surname: str
    email: EmailStr


class ExtendedUserSchema(UserSchema):
    notifications: list["UserNotificationSchema"]


class UserCreateSchema(TunedModel):
    name: str
    surname: str
    email: EmailStr
    password: str

    @validator("name")
    def validate_name(cls, value: str) -> str:
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Name should contains only letters")
        return value

    @validator("surname")
    def validate_surname(cls, value: str) -> str:
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Surname should contains only letters")
        return value


class UserDeleteSchema(TunedModel):
    id: uuid.UUID


class UserListSchema(TunedModel):
    users: list[UserSchema]


class UserUpdateSchema(TunedModel):
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserNotificationSchema(TunedModel):
    id: uuid.UUID
    user_id: uuid.UUID
    message: str
    created_at: datetime
    updated_at: datetime


class UserNotificationListSchema(TunedModel):
    notifications: list[UserNotificationSchema]


class UserNotificationCreateSchema(TunedModel):
    message: str


ExtendedUserSchema.update_forward_refs()
