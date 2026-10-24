import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, str_enum
from app.models.inquiry import InquiryRole


class Region(enum.StrEnum):
    EAST = "east"
    MIDDLE = "middle"
    WEST = "west"


class Program(Base):
    __tablename__ = "programs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        unique=True,
    )

    description: Mapped[str | None] = mapped_column(Text)

    audiences: Mapped[list[InquiryRole]] = mapped_column(
        ARRAY(str_enum(InquiryRole))
    )

    regions: Mapped[list[Region]] = mapped_column(
        ARRAY(str_enum(Region))
    )

    contact_email: Mapped[str | None] = mapped_column(
        String(320)
    )

    is_active: Mapped[bool] = mapped_column(
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
