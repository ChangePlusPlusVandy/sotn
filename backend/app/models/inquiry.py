import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, str_enum


class InquiryRole(enum.StrEnum):
    # Order and labels follow step 2 of the intake form.
    ATHLETE = "athlete"
    UNIFIED_PARTNER = "unified_partner"
    CAREGIVER = "caregiver"  # caregiver, parent, or conservator
    COACH = "coach"
    VOLUNTEER = "volunteer"
    PARTNER = "partner"  # community partner, vendor, or venue
    DONOR = "donor"  # donor, sponsor, or partner
    FIRST_RESPONDER = "first_responder"  # law enforcement or first responder
    EMPLOYMENT = "employment"  # interested in employment or an internship


class InquiryStatus(enum.StrEnum):
    NEW = "new"
    NEEDS_REVIEW = "needs_review"
    ASSIGNED = "assigned"
    CONTACTED = "contacted"
    REFERRED = "referred"
    CLOSED = "closed"


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

    # Role-specific form fields; the approved field list per role is still TBD (PRD INT-02).
    answers: Mapped[dict] = mapped_column(JSONB, default=dict)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
