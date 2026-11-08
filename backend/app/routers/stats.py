from datetime import UTC, date, datetime, timedelta
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import cast, func, literal_column, select
from sqlalchemy.types import Date

from app.core.auth import get_current_staff
from app.core.db import DbSession
from app.models.inquiry import AWAITING_CONTACT_STATUSES, Inquiry
from app.schemas.stats import (
    AdminStats,
    DayCount,
    RegionCount,
    RoleCount,
    StatusCount,
)

# Staff dashboard uses Tennessee local calendar days for "today" and by_day buckets.
TN_TZ = ZoneInfo("America/Chicago")

admin_router = APIRouter(
    prefix="/admin/stats",
    tags=["admin: stats"],
    dependencies=[Depends(get_current_staff)],
)


def _parse_range(
    start: date | None,
    end: date | None,
) -> tuple[date, date]:
    today = datetime.now(TN_TZ).date()
    range_end = end or today
    range_start = start or (range_end - timedelta(days=29))
    if range_start > range_end:
        raise HTTPException(422, "start must be on or before end")
    return range_start, range_end


def _day_bounds(day: date) -> tuple[datetime, datetime]:
    """Inclusive local-day window as UTC timestamps for created_at filters."""
    start = datetime(day.year, day.month, day.day, tzinfo=TN_TZ)
    end = start + timedelta(days=1)
    return start.astimezone(UTC), end.astimezone(UTC)


@admin_router.get("", response_model=AdminStats)
def get_admin_stats(
    db: DbSession,
    start: Annotated[
        date | None,
        Query(description="Range start (inclusive). Defaults to end minus 29 days."),
    ] = None,
    end: Annotated[
        date | None,
        Query(
            description="Range end (inclusive). Defaults to today in America/Chicago."
        ),
    ] = None,
):
    """Dashboard counts for staff. No caching; live COUNT / GROUP BY queries."""

    range_start, range_end = _parse_range(start, end)
    range_start_utc, _ = _day_bounds(range_start)
    _, range_end_utc = _day_bounds(range_end)
    today = datetime.now(TN_TZ).date()
    today_start_utc, today_end_utc = _day_bounds(today)

    new_today = db.scalar(
        select(func.count())
        .select_from(Inquiry)
        .where(
            Inquiry.created_at >= today_start_utc,
            Inquiry.created_at < today_end_utc,
        )
    )
    awaiting_contact = db.scalar(
        select(func.count())
        .select_from(Inquiry)
        .where(Inquiry.status.in_(AWAITING_CONTACT_STATUSES))
    )

    in_range = (
        Inquiry.created_at >= range_start_utc,
        Inquiry.created_at < range_end_utc,
    )

    total = (
        db.scalar(select(func.count()).select_from(Inquiry).where(*in_range)) or 0
    )

    # Bucket by Tennessee local date so charts match staff calendar days.
    # literal_column keeps the timezone name out of bind params so SELECT/GROUP BY match.
    local_day = cast(
        func.timezone(literal_column("'America/Chicago'"), Inquiry.created_at),
        Date,
    ).label("day")
    day_rows = db.execute(
        select(local_day, func.count())
        .where(*in_range)
        .group_by(local_day)
        .order_by(local_day)
    ).all()
    day_counts = {row.day: row[1] for row in day_rows}
    by_day = [
        DayCount(
            date=range_start + timedelta(days=offset),
            count=day_counts.get(range_start + timedelta(days=offset), 0),
        )
        for offset in range((range_end - range_start).days + 1)
    ]

    by_role = [
        RoleCount(role=role, count=count)
        for role, count in db.execute(
            select(Inquiry.role, func.count())
            .where(*in_range)
            .group_by(Inquiry.role)
            .order_by(func.count().desc())
        ).all()
    ]
    by_region = [
        RegionCount(region=region, count=count)
        for region, count in db.execute(
            select(Inquiry.region, func.count())
            .where(*in_range)
            .group_by(Inquiry.region)
            .order_by(func.count().desc())
        ).all()
    ]
    by_status = [
        StatusCount(status=status, count=count)
        for status, count in db.execute(
            select(Inquiry.status, func.count())
            .where(*in_range)
            .group_by(Inquiry.status)
            .order_by(func.count().desc())
        ).all()
    ]

    return AdminStats(
        new_today=new_today or 0,
        awaiting_contact=awaiting_contact or 0,
        total=total,
        by_day=by_day,
        by_role=by_role,
        by_region=by_region,
        by_status=by_status,
    )
