import uuid

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database import Base
from src.models import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)

    notifications = relationship("UserNotification", back_populates="user")


class UserNotification(TimestampMixin, Base):
    __tablename__ = "user_notification"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), index=True, nullable=False)
    message = Column(String(512), nullable=False, default="")
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="notifications")
