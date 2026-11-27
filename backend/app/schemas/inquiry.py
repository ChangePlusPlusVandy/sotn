import uuid
from datetime import datetime
from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from app.models.inquiry import InquiryRole, InquiryStatus, SubmitterRelationship
from app.schemas.resource import reject_nul

ZIP_PATTERN = r"^\d{5}(-\d{4})?$"

# A blank or whitespace-only name is rejected; send null (or omit it) for "no name".
ParticipantName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=200),
    AfterValidator(reject_nul),
]


class InquiryCreate(BaseModel):
    role: InquiryRole
    submitter_relationship: SubmitterRelationship = SubmitterRelationship.SELF
    participant_name: ParticipantName | None = None
    contact_name: str = Field(min_length=1, max_length=200)
    contact_email: str | None = Field(default=None, max_length=320)
    contact_phone: str | None = Field(default=None, max_length=32)
    zip_code: str = Field(pattern=ZIP_PATTERN)
    answers: dict = {}

    @model_validator(mode="after")
    def require_contact_method(self):
        if not self.contact_email and not self.contact_phone:
            raise ValueError("Provide an email or phone number")
        return self


class InquiryConfirmation(BaseModel):
    """Returned to the public submitter: a reference, never the submitted details."""

    id: uuid.UUID
    status: InquiryStatus


class InquiryRead(BaseModel):
    """Full record, for staff only."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: InquiryRole
    status: InquiryStatus
    submitter_relationship: SubmitterRelationship
    participant_name: str | None
    contact_name: str
    contact_email: str | None
    contact_phone: str | None
    zip_code: str
    answers: dict
    created_at: datetime
    updated_at: datetime


class InquiryUpdate(BaseModel):
    """Partial update: only fields present in the request body are changed."""

    status: InquiryStatus | None = None
    submitter_relationship: SubmitterRelationship | None = None
    # Unlike the fields below, null is allowed here: it clears the participant name.
    participant_name: ParticipantName | None = None
    contact_name: str | None = Field(default=None, min_length=1, max_length=200)
    contact_email: str | None = Field(default=None, max_length=320)
    contact_phone: str | None = Field(default=None, max_length=32)
    zip_code: str | None = Field(default=None, pattern=ZIP_PATTERN)

    @field_validator("status", "submitter_relationship", "contact_name", "zip_code")
    @classmethod
    def not_null(cls, value):
        # Omitting these fields is fine; explicitly sending null is not.
        if value is None:
            raise ValueError("cannot be null")
        return value
