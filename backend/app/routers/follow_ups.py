import uuid
from datetime import UTC, datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select

from app.core.auth import CurrentStaff, get_current_staff
from app.core.db import DbSession
from app.models.follow_up import FollowUp, FollowUpStatus
from app.models.inquiry import Inquiry
from app.routers.inquiries import get_inquiry_or_404
from app.schemas.common import Page
from app.schemas.follow_up import FollowUpCreate, FollowUpRead, FollowUpUpdate

# Follow-ups are created under an inquiry...
inquiry_router = APIRouter(
    prefix="/admin/inquiries",
    tags=["admin: follow-ups"],
    dependencies=[Depends(get_current_staff)],
)

# ...but listed, read, and edited across all inquiries on the follow-ups board
admin_router = APIRouter(
    prefix="/admin/follow-ups",
    tags=["admin: follow-ups"],
    dependencies=[Depends(get_current_staff)],
)


# POST /admin/inquiries/{inquiry_id}/follow-ups:
# assignee_staff_id optional (defaults to the current staff member),
# 404 for a missing inquiry, returns 201
@inquiry_router.post(
    "/{inquiry_id}/follow-ups", status_code=201, response_model=FollowUpRead
)
def create_follow_up(
    body: FollowUpCreate,
    db: DbSession,
    staff_id: CurrentStaff,
    inquiry: Annotated[Inquiry, Depends(get_inquiry_or_404)],
):
    """Create a follow-up on an inquiry. The assignee defaults to the current staff member."""
    follow_up = FollowUp(
        **body.model_dump(exclude={"assignee_staff_id"}),
        inquiry_id=inquiry.id,
        created_by_staff_id=staff_id,
        assignee_staff_id=body.assignee_staff_id or staff_id,
    )
    db.add(follow_up)
    db.commit()
    db.refresh(follow_up)
    return follow_up


# GET /admin/follow-ups:
# filters status, inquiry_id, assignee (me = current staff), overdue=true;
# sorted by due_at, soonest first
@admin_router.get("", response_model=Page[FollowUpRead])
def list_follow_ups(
    db: DbSession,
    staff_id: CurrentStaff,
    status: FollowUpStatus | None = None,
    inquiry_id: uuid.UUID | None = None,
    assignee: Annotated[
        Literal["me"] | None, Query(description="'me' for the current staff member")
    ] = None,
    overdue: Annotated[
        bool, Query(description="Only incomplete follow-ups past their due date")
    ] = False,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
):
    """List follow-ups across all inquiries, soonest due first, with optional filters."""
    query = select(FollowUp)
    if status:
        query = query.where(FollowUp.status == status)
    if inquiry_id:
        query = query.where(FollowUp.inquiry_id == inquiry_id)
    if assignee == "me":
        query = query.where(FollowUp.assignee_staff_id == staff_id)
    if overdue:
        query = query.where(
            FollowUp.due_at < func.now(), FollowUp.status != FollowUpStatus.COMPLETE
        )
    # Counting all matching rows before pagination
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    items = db.scalars(
        query.order_by(FollowUp.due_at.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return Page(items=items, total=total, page=page, page_size=page_size)


# helper for get_follow_up and update_follow_up
def get_follow_up_or_404(db: DbSession, follow_up_id: uuid.UUID) -> FollowUp:
    follow_up = db.get(FollowUp, follow_up_id)
    if follow_up is None:
        raise HTTPException(404, "Follow-up not found")
    return follow_up


# GET /admin/follow-ups/{id}
@admin_router.get("/{follow_up_id}", response_model=FollowUpRead)
def get_follow_up(follow_up: Annotated[FollowUp, Depends(get_follow_up_or_404)]):
    """Get one follow-up."""
    return follow_up


# PATCH /admin/follow-ups/{id}:
# can change title, details, due_at, assignee_staff_id, status
@admin_router.patch("/{follow_up_id}", response_model=FollowUpRead)
def update_follow_up(
    body: FollowUpUpdate,
    db: DbSession,
    follow_up: Annotated[FollowUp, Depends(get_follow_up_or_404)],
):
    """Update only the fields sent in the body. completed_at is set and cleared by the server."""
    was_complete = follow_up.status == FollowUpStatus.COMPLETE
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(follow_up, field, value)

    is_complete = follow_up.status == FollowUpStatus.COMPLETE
    if is_complete and not was_complete:
        follow_up.completed_at = datetime.now(UTC)
    elif was_complete and not is_complete:
        follow_up.completed_at = None

    db.commit()
    db.refresh(follow_up)
    return follow_up
