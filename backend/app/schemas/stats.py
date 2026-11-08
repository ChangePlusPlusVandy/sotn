from datetime import date

from pydantic import BaseModel

from app.models.inquiry import InquiryRole, InquiryStatus
from app.models.region import Region


class DayCount(BaseModel):
    date: date
    count: int


class RoleCount(BaseModel):
    role: InquiryRole
    count: int


class RegionCount(BaseModel):
    region: Region | None
    count: int


class StatusCount(BaseModel):
    status: InquiryStatus
    count: int


class AdminStats(BaseModel):
    new_today: int
    awaiting_contact: int
    total: int
    by_day: list[DayCount]
    by_role: list[RoleCount]
    by_region: list[RegionCount]
    by_status: list[StatusCount]
