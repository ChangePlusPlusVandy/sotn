import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, str_enum
from app.models.inquiry import InquiryRole


class ResourceKind(enum.StrEnum):
    PDF = "pdf"
    VIDEO = "video"
    LINK = "link"


class Resource(Base):
    """A video, PDF or link that staff manage and that appears on /results after intake."""

    __tablename__ = "resources"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    kind: Mapped[ResourceKind] = mapped_column(str_enum(ResourceKind))
    url: Mapped[str] = mapped_column(String(2048))
    # Which inquiry roles this resource is shown to on the public results page.
    audiences: Mapped[list[InquiryRole]] = mapped_column(
        ARRAY(str_enum(InquiryRole)), default=list
    )
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
