from enum import Enum
from typing import Any


class ExtendedEnum(Enum):
    @classmethod
    def to_list(cls) -> list[Any]:
        """Returns a list of all the enum values."""
        return list(map(lambda c: c.value, cls))

    @classmethod
    def to_dict(cls) -> dict[Any, Any]:
        """Returns a dictionary representation of the enum."""
        return {e.name: e.value for e in cls}
