"""
global models
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, func


class TimestampMixin:
    """Adding created_at and updated_at fields to the model."""

    created_at = Column(
        DateTime(timezone=True),
        index=True,
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
        onupdate=datetime.now,
    )
