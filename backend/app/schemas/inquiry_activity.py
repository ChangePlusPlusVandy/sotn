import uuid
from datetime import UTC, datetime
from typing import Annotated

from pydantic import (
    AfterValidator,
    AwareDatetime,
    BaseModel,
    ConfigDict,
    StringConstraints,
    field_validator,
)

from app.models.inquiry_activity import ActivityChannel, ActivityOutcome
from app.schemas.resource import reject_nul


class InquiryActivityCreate(BaseModel):
    """Logged by staff. The author comes from the signed-in user, not the body."""

    model_config = ConfigDict(extra="forbid")

    channel: ActivityChannel
    outcome: ActivityOutcome
    # Must include a timezone, so a local time can't be mistaken for UTC.
    occurred_at: AwareDatetime | None = None
    summary: (
        Annotated[
            str,
            StringConstraints(strip_whitespace=True, max_length=500),
            AfterValidator(reject_nul),
        ]
        | None
    ) = None

    @field_validator("occurred_at")
    @classmethod
    def not_in_future(cls, value):
        # Omitting it is fine (the router uses now); a future time is not.
        if value is not None and value > datetime.now(UTC):
            raise ValueError("cannot be in the future")
        return value

    @field_validator("summary")
    @classmethod
    def blank_to_none(cls, value):
        # The summary is optional, so a blank one means there isn't one.
        return value or None


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
