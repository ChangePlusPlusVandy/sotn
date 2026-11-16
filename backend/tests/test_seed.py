"""Tests for the local seed script."""

from sqlalchemy import func, select

from app.models import Inquiry, Program, Resource
from app.models.inquiry import InquiryStatus
from app.models.inquiry_note import InquiryNote
from app.seed import INQUIRIES, PROGRAMS, RESOURCES, reset, seed

ALL_ADDED = {
    "inquiries": len(INQUIRIES),
    "programs": len(PROGRAMS),
    "resources": len(RESOURCES),
}
NONE_ADDED = {"inquiries": 0, "programs": 0, "resources": 0}


def count(db, model) -> int:
    return db.scalar(select(func.count()).select_from(model))


def test_seed_adds_every_sample_row(db):
    assert seed(db) == ALL_ADDED
    assert count(db, Inquiry) == len(INQUIRIES)
    assert count(db, Program) == len(PROGRAMS)
    assert count(db, Resource) == len(RESOURCES)


def test_rerun_skips_existing_rows_and_keeps_edits(db):
    seed(db)
    inquiry = db.scalars(
        select(Inquiry).where(Inquiry.contact_name == "Aisha Robinson")
    ).one()
    inquiry.status = InquiryStatus.CLOSED
    db.flush()

    assert seed(db) == NONE_ADDED
    db.refresh(inquiry)
    assert inquiry.status == InquiryStatus.CLOSED


def test_skips_program_whose_name_is_taken(db):
    db.add(Program(name=PROGRAMS[0]["name"], audiences=[], regions=[]))
    db.flush()

    assert seed(db)["programs"] == len(PROGRAMS) - 1
    assert count(db, Program) == len(PROGRAMS)


def test_reset_deletes_every_table(db):
    seed(db)
    inquiry = db.scalars(select(Inquiry)).first()
    db.add(
        InquiryNote(
            inquiry_id=inquiry.id, author_staff_id="user_test", body="Called back"
        )
    )
    db.add(
        Inquiry(
            role="athlete",
            contact_name="Added by hand",
            contact_email="x@example.com",
            zip_code="37203",
        )
    )
    db.flush()

    reset(db)

    for model in (Inquiry, InquiryNote, Program, Resource):
        assert count(db, model) == 0
    assert seed(db) == ALL_ADDED
