import enum

from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def str_enum(enum_cls: type[enum.StrEnum]) -> Enum:
    """Column type for a StrEnum. Use this for every enum column."""
    # native_enum=False stores enums as VARCHAR, so adding a value later needs no ALTER TYPE.
    # values_callable stores the values ("athlete") the API uses, not the names ("ATHLETE").
    return Enum(
        enum_cls,
        native_enum=False,
        length=32,
        values_callable=lambda cls: [member.value for member in cls],
    )
