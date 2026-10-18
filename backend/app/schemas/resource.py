import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.inquiry import InquiryRole
from app.models.resource import ResourceKind


class ResourceCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    kind: ResourceKind
    url: str = Field(min_length=1, max_length=2048)
    audiences: list[InquiryRole] = []
    is_published: bool = False


class ResourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str | None
    kind: ResourceKind
    url: str
    audiences: list[InquiryRole]
    is_published: bool
    created_at: datetime
    updated_at: datetime


class ResourceUpdate(BaseModel):
    """Partial update: only fields present in the request body are changed."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    kind: ResourceKind | None = None
    url: str | None = Field(default=None, min_length=1, max_length=2048)
    audiences: list[InquiryRole] | None = None
    is_published: bool | None = None

    @field_validator("title", "kind", "url", "audiences", "is_published")
    @classmethod
    def not_null(cls, value):
        # Omitting these fields is fine; explicitly sending null is not.
        if value is None:
            raise ValueError("cannot be null")
        return value
