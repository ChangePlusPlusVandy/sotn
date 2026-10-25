import uuid
from datetime import UTC, datetime

from app.models.inquiry_note import InquiryNote
from tests.conftest import TEST_STAFF_ID
from tests.test_inquiries import add_inquiry

MISSING_INQUIRY_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")


def test_create_note_returns_201_with_signed_in_author(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/notes",
        json={"body": "Called, left voicemail"},
    )

    assert res.status_code == 201
    body = res.json()
    assert body["inquiry_id"] == str(inquiry.id)
    assert body["author_staff_id"] == TEST_STAFF_ID
    assert body["body"] == "Called, left voicemail"
    assert "id" in body
    assert "created_at" in body


def test_create_note_ignores_client_supplied_author(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/notes",
        json={"body": "Note", "author_staff_id": "user_someone_else"},
    )

    assert res.status_code == 422


def test_create_note_rejects_empty_body(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/notes",
        json={"body": ""},
    )

    assert res.status_code == 422


def test_create_note_404_for_missing_inquiry(staff_client):
    res = staff_client.post(
        f"/admin/inquiries/{MISSING_INQUIRY_ID}/notes",
        json={"body": "Note"},
    )

    assert res.status_code == 404


def test_list_notes_newest_first(staff_client, db):
    inquiry = add_inquiry(db)
    db.add_all(
        [
            InquiryNote(
                inquiry_id=inquiry.id,
                author_staff_id=TEST_STAFF_ID,
                body="First",
                created_at=datetime(2026, 1, 1, tzinfo=UTC),
            ),
            InquiryNote(
                inquiry_id=inquiry.id,
                author_staff_id=TEST_STAFF_ID,
                body="Second",
                created_at=datetime(2026, 1, 2, tzinfo=UTC),
            ),
        ]
    )
    db.flush()

    res = staff_client.get(f"/admin/inquiries/{inquiry.id}/notes")

    assert res.status_code == 200
    body = res.json()
    assert body["total"] == 2
    assert [item["body"] for item in body["items"]] == ["Second", "First"]


def test_list_notes_paginates(staff_client, db):
    inquiry = add_inquiry(db)
    for n in range(3):
        staff_client.post(
            f"/admin/inquiries/{inquiry.id}/notes", json={"body": f"Note {n}"}
        )

    body = staff_client.get(
        f"/admin/inquiries/{inquiry.id}/notes",
        params={"page": 2, "page_size": 2},
    ).json()

    assert body["total"] == 3
    assert body["page"] == 2
    assert len(body["items"]) == 1


def test_list_notes_404_for_missing_inquiry(staff_client):
    res = staff_client.get(f"/admin/inquiries/{MISSING_INQUIRY_ID}/notes")
    assert res.status_code == 404


def test_note_routes_require_auth(client, db):
    inquiry = add_inquiry(db)

    assert (
        client.post(
            f"/admin/inquiries/{inquiry.id}/notes", json={"body": "Note"}
        ).status_code
        == 401
    )
    assert client.get(f"/admin/inquiries/{inquiry.id}/notes").status_code == 401
