import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.inquiry import InquiryRole
from app.models.programs import Region


class ProgramCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    audiences: list[InquiryRole] = Field(default_factory=list)
    regions: list[Region] = Field(default_factory=list)
    contact_email: str | None = Field(default=None, max_length=320)
    is_active: bool = True


class ProgramUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    audiences: list[InquiryRole] | None = None
    regions: list[Region] | None = None
    contact_email: str | None = Field(default=None, max_length=320)
    is_active: bool | None = None


class ProgramAdmin(ProgramCreate):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProgramPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    audiences: list[InquiryRole]
    regions: list[Region]
    is_active: bool
