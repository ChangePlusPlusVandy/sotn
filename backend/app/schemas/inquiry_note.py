import uuid
from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, StringConstraints

from app.schemas.resource import reject_nul


class InquiryNoteCreate(BaseModel):
    """Request body for a new note. Author comes from the signed-in staff member."""

    model_config = ConfigDict(extra="forbid")

    body: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1, max_length=5000),
        AfterValidator(reject_nul),
    ]


class InquiryNoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    inquiry_id: uuid.UUID
    author_staff_id: str
    body: str
    created_at: datetime
