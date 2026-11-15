import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, str_enum
from app.models.region import Region


class InquiryRole(enum.StrEnum):
    ATHLETE = "athlete"
    VOLUNTEER = "volunteer"
    PARTNER = "partner"
    DONOR = "donor"
    # Add the correct values


class InquiryStatus(enum.StrEnum):
    NEW = "new"
    NEEDS_REVIEW = "needs_review"
    ASSIGNED = "assigned"
    CONTACTED = "contacted"
    REFERRED = "referred"
    CLOSED = "closed"


# Statuses that mean staff have not contacted the submitter yet.
AWAITING_CONTACT_STATUSES = (
    InquiryStatus.NEW,
    InquiryStatus.NEEDS_REVIEW,
    InquiryStatus.ASSIGNED,
)


class Inquiry(Base):
    __tablename__ = "inquiries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    role: Mapped[InquiryRole] = mapped_column(str_enum(InquiryRole))
    status: Mapped[InquiryStatus] = mapped_column(
        str_enum(InquiryStatus), default=InquiryStatus.NEW
    )
    contact_name: Mapped[str] = mapped_column(String(200))
    contact_email: Mapped[str | None] = mapped_column(String(320))
    contact_phone: Mapped[str | None] = mapped_column(String(32))
    zip_code: Mapped[str] = mapped_column(String(10))
    # Nullable until the intake form starts collecting region on every submission.
    region: Mapped[Region | None] = mapped_column(str_enum(Region), nullable=True)

    # Role-specific form fields; the approved field list per role is still TBD (PRD INT-02).
    answers: Mapped[dict] = mapped_column(JSONB, default=dict)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
