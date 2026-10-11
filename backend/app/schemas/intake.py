import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.inquiry import InquiryRole, InquiryStatus

ZIP_PATTERN = r"^\d{5}(-\d{4})?$"


class IntakeCreate(BaseModel):
    role: InquiryRole
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


class IntakeConfirmation(BaseModel):
    """Returned to the public submitter: a reference, never the submitted details."""

    id: uuid.UUID
    status: InquiryStatus


class IntakeRead(BaseModel):
    """Full record, for staff only."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: InquiryRole
    status: InquiryStatus
    contact_name: str
    contact_email: str | None
    contact_phone: str | None
    zip_code: str
    answers: dict
    created_at: datetime
    updated_at: datetime


class IntakeUpdate(BaseModel):
    """Partial update: only fields present in the request body are changed."""

    status: InquiryStatus | None = None
    contact_name: str | None = Field(default=None, min_length=1, max_length=200)
    contact_email: str | None = Field(default=None, max_length=320)
    contact_phone: str | None = Field(default=None, max_length=32)
    zip_code: str | None = Field(default=None, pattern=ZIP_PATTERN)

    @field_validator("status", "contact_name", "zip_code")
    @classmethod
    def not_null(cls, value):
        # Omitting these fields is fine; explicitly sending null is not.
        if value is None:
            raise ValueError("cannot be null")
        return value
