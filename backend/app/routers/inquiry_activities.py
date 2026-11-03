from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select

from app.core.auth import CurrentStaff, get_current_staff
from app.core.db import DbSession
from app.models.inquiry import Inquiry
from app.models.inquiry_activity import InquiryActivity
from app.routers.inquiries import get_inquiry_or_404
from app.schemas.common import Page
from app.schemas.inquiry_activity import InquiryActivityCreate, InquiryActivityRead

# Staff-only and append-only: no update or delete routes.
router = APIRouter(
    prefix="/admin/inquiries",
    tags=["admin: inquiry activities"],
    dependencies=[Depends(get_current_staff)],
)


@router.post(
    "/{inquiry_id}/activities", status_code=201, response_model=InquiryActivityRead
)
def create_activity(
    body: InquiryActivityCreate,
    db: DbSession,
    staff_id: CurrentStaff,
    inquiry: Annotated[Inquiry, Depends(get_inquiry_or_404)],
):
    """Log a contact attempt on an inquiry. occurred_at defaults to now."""

    activity = InquiryActivity(
        inquiry_id=inquiry.id,
        staff_id=staff_id,  # from the signed-in user, never the request body
        channel=body.channel,
        outcome=body.outcome,
        occurred_at=body.occurred_at or datetime.now(UTC),
        summary=body.summary,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)  # reload server-set values (created_at)
    return activity


@router.get("/{inquiry_id}/activities", response_model=Page[InquiryActivityRead])
def list_activities(
    db: DbSession,
    inquiry: Annotated[Inquiry, Depends(get_inquiry_or_404)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
):
    """List an inquiry's activities, most recent first."""

    query = select(InquiryActivity).where(InquiryActivity.inquiry_id == inquiry.id)
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    items = db.scalars(
        # created_at breaks ties when two activities share an occurred_at
        query.order_by(
            InquiryActivity.occurred_at.desc(), InquiryActivity.created_at.desc()
        )
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return Page(items=items, total=total, page=page, page_size=page_size)
