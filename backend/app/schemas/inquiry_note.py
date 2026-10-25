import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InquiryNoteCreate(BaseModel):
    """Request body for a new note. Author comes from the signed-in staff member."""

    model_config = ConfigDict(extra="forbid")

    body: str = Field(min_length=1)


class InquiryNoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    inquiry_id: uuid.UUID
    author_staff_id: str
    body: str
    created_at: datetime
