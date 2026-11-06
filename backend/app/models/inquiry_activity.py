import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, str_enum


# How the staff member reached out
class ActivityChannel(enum.StrEnum):
    PHONE = "phone"
    EMAIL = "email"
    TEXT = "text"
    IN_PERSON = "in_person"
    OTHER = "other"


# What happend when they reached out
class ActivityOutcome(enum.StrEnum):
    REACHED = "reached"
    LEFT_MESSAGE = "left_message"
    NO_RESPONSE = "no_response"
    WRONG_CONTACT = "wrong_contact"


# The table: one row per logged contact attempt
# Formatted by column name, Python type and how the database stores it
# Ex: Column name: staff_id, Python type: Mapped[str], Database stores: mapped_column(String(64))
class InquiryActivity(Base):
    """A logged contact attempt (call, email, text, etc.) on an inquiry.

    Created by the "Log touch" button in triage. Staff-only and append-only:
    activities are never edited or deleted.

    Attributes:
        staff_id: The signed-in staff member who logged it.
        occurred_at: When the contact happened. Can't be in the future or
            before the inquiry was submitted.
        created_at: When the row was saved. Can be later than occurred_at
            if staff log a touch after the fact.
    """

    __tablename__ = "inquiry_activities"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    inquiry_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("inquiries.id"), index=True
    )
    staff_id: Mapped[str] = mapped_column(String(64))
    channel: Mapped[ActivityChannel] = mapped_column(str_enum(ActivityChannel))
    outcome: Mapped[ActivityOutcome] = mapped_column(str_enum(ActivityOutcome))
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )  # when the contact happened
    summary: Mapped[str | None] = mapped_column(String(500))  # optional note
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )  # when the row was saved
