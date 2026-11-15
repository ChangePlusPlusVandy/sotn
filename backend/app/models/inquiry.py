import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, str_enum


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


class SubmitterRelationship(enum.StrEnum):
    SELF = "self"
    GUARDIAN = "guardian"
    TEACHER = "teacher"
    CLINICIAN = "clinician"
    OTHER = "other"
    # Placeholder values: the official choices are still being clarified.


class Inquiry(Base):
    __tablename__ = "inquiries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    role: Mapped[InquiryRole] = mapped_column(str_enum(InquiryRole))
    status: Mapped[InquiryStatus] = mapped_column(
        str_enum(InquiryStatus), default=InquiryStatus.NEW
    )
    # Who is filling in the form, and (when it is not the participant) who it is about.
    # server_default keeps rows created before this column existed valid.
    submitter_relationship: Mapped[SubmitterRelationship] = mapped_column(
        str_enum(SubmitterRelationship),
        default=SubmitterRelationship.SELF,
        server_default=SubmitterRelationship.SELF.value,
    )
    participant_name: Mapped[str | None] = mapped_column(String(200))
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
