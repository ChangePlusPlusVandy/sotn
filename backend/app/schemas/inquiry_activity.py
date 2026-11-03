import uuid
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.inquiry_activity import ActivityChannel, ActivityOutcome


class InquiryActivityCreate(BaseModel):
    """Logged by staff. The author comes from the signed-in user, not the body."""

    channel: ActivityChannel
    outcome: ActivityOutcome
    occurred_at: datetime | None = None
    summary: str | None = Field(default=None, max_length=500)

    @field_validator("occurred_at")
    @classmethod
    def not_in_future(cls, value):
        # Omitting it is fine (the router uses now); a future time is not.
        if value is None:
            return value
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        if value > datetime.now(UTC):
            raise ValueError("cannot be in the future")
        return value


class InquiryActivityRead(BaseModel):
    """Full record, for staff only."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    inquiry_id: uuid.UUID
    staff_id: str
    channel: ActivityChannel
    outcome: ActivityOutcome
    occurred_at: datetime
    summary: str | None
    created_at: datetime
