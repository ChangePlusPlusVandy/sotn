import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select

from app.core.auth import get_current_staff
from app.core.db import DbSession
from app.models.inquiry import Inquiry, InquiryRole, InquiryStatus
from app.schemas.common import Page
from app.schemas.inquiry import (
    InquiryConfirmation,
    InquiryCreate,
    InquiryRead,
    InquiryUpdate,
)

# Public routes: no auth, and responses never echo submitted details.
router = APIRouter(prefix="/inquiries", tags=["inquiries"])

# Staff routes: the router-level dependency rejects unauthenticated requests on every route.
admin_router = APIRouter(
    prefix="/admin/inquiries",
    tags=["admin: inquiries"],
    dependencies=[Depends(get_current_staff)],
)


@router.post("", status_code=201, response_model=InquiryConfirmation)
def create_inquiry(body: InquiryCreate, db: DbSession):
    inquiry = Inquiry(**body.model_dump())
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    return inquiry


@admin_router.get("", response_model=Page[InquiryRead])
def list_inquiries(
    db: DbSession,
    status: InquiryStatus | None = None,
    role: InquiryRole | None = None,
    q: Annotated[str | None, Query(description="Search name or email")] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
):
    query = select(Inquiry)
    if status:
        query = query.where(Inquiry.status == status)
    if role:
        query = query.where(Inquiry.role == role)
    if q:
        query = query.where(
            or_(
                Inquiry.contact_name.ilike(f"%{q}%"),
                Inquiry.contact_email.ilike(f"%{q}%"),
            )
        )

    total = db.scalar(select(func.count()).select_from(query.subquery()))
    items = db.scalars(
        query.order_by(Inquiry.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return Page(items=items, total=total, page=page, page_size=page_size)


def get_inquiry_or_404(db: DbSession, inquiry_id: uuid.UUID) -> Inquiry:
    inquiry = db.get(Inquiry, inquiry_id)
    if inquiry is None:
        raise HTTPException(404, "Inquiry not found")
    return inquiry


@admin_router.get("/{inquiry_id}", response_model=InquiryRead)
def get_inquiry(inquiry: Annotated[Inquiry, Depends(get_inquiry_or_404)]):
    return inquiry


@admin_router.patch("/{inquiry_id}", response_model=InquiryRead)
def update_inquiry(
    body: InquiryUpdate,
    db: DbSession,
    inquiry: Annotated[Inquiry, Depends(get_inquiry_or_404)],
):
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(inquiry, field, value)
    if not inquiry.contact_email and not inquiry.contact_phone:
        raise HTTPException(422, "Inquiry must keep an email or phone number")
    db.commit()
    db.refresh(inquiry)
    return inquiry
