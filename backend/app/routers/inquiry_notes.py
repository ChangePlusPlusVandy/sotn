from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select

from app.core.auth import CurrentStaff, get_current_staff
from app.core.db import DbSession
from app.models.inquiry import Inquiry
from app.models.inquiry_note import InquiryNote
from app.routers.inquiries import get_inquiry_or_404
from app.schemas.common import Page
from app.schemas.inquiry_note import InquiryNoteCreate, InquiryNoteRead

admin_router = APIRouter(
    prefix="/admin/inquiries/{inquiry_id}/notes",
    tags=["admin: inquiry notes"],
    dependencies=[Depends(get_current_staff)],
)


@admin_router.post("", status_code=201, response_model=InquiryNoteRead)
def create_note(
    body: InquiryNoteCreate,
    db: DbSession,
    staff_id: CurrentStaff,
    inquiry: Annotated[Inquiry, Depends(get_inquiry_or_404)],
):
    note = InquiryNote(
        inquiry_id=inquiry.id,
        author_staff_id=staff_id,
        body=body.body,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@admin_router.get("", response_model=Page[InquiryNoteRead])
def list_notes(
    db: DbSession,
    inquiry: Annotated[Inquiry, Depends(get_inquiry_or_404)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
):
    query = select(InquiryNote).where(InquiryNote.inquiry_id == inquiry.id)
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    items = db.scalars(
        query.order_by(InquiryNote.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return Page(items=items, total=total, page=page, page_size=page_size)
