import uuid
from datetime import date, datetime
from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    StringConstraints,
    field_validator,
)

from app.models.follow_up import FollowUpStatus
from app.schemas.resource import Description, Title, reject_nul

StaffId = Annotated[
    str, StringConstraints(min_length=1, max_length=64), AfterValidator(reject_nul)
]


class FollowUpCreate(BaseModel):
    """created_by_staff_id is set by the server; assignee defaults to the current staff member."""

    title: Title
    details: Description | None = None
    due_on: date
    assignee_staff_id: StaffId | None = None


class FollowUpRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    inquiry_id: uuid.UUID
    title: str
    details: str | None
    created_by_staff_id: str
    assignee_staff_id: str
    due_on: date
    status: FollowUpStatus
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class FollowUpUpdate(BaseModel):
    """Partial update: only fields present in the request body are changed."""

    title: Title | None = None
    details: Description | None = None
    due_on: date | None = None
    assignee_staff_id: StaffId | None = None
    status: FollowUpStatus | None = None

    @field_validator("title", "due_on", "assignee_staff_id", "status")
    @classmethod
    def not_null(cls, value):
        # Omitting these fields is fine; explicitly sending null is not.
        if value is None:
            raise ValueError("cannot be null")
        return value
