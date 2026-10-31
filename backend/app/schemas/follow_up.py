import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.follow_up import FollowUpStatus


class FollowUpCreate(BaseModel):
    """created_by_staff_id is set by the server; assignee defaults to the current staff member."""

    title: str = Field(min_length=1, max_length=200)
    details: str | None = None
    due_at: datetime
    assignee_staff_id: str | None = Field(default=None, min_length=1, max_length=64)


class FollowUpRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    inquiry_id: uuid.UUID
    title: str
    details: str | None
    created_by_staff_id: str
    assignee_staff_id: str
    due_at: datetime
    status: FollowUpStatus
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class FollowUpUpdate(BaseModel):
    """Partial update: only fields present in the request body are changed."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    details: str | None = None
    due_at: datetime | None = None
    assignee_staff_id: str | None = Field(default=None, min_length=1, max_length=64)
    status: FollowUpStatus | None = None

    @field_validator("title", "due_at", "assignee_staff_id", "status")
    @classmethod
    def not_null(cls, value):
        # Omitting these fields is fine; explicitly sending null is not.
        if value is None:
            raise ValueError("cannot be null")
        return value
