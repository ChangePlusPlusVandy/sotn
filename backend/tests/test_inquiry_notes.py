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


def test_create_note_rejects_client_supplied_author(staff_client, db):
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


def test_create_note_rejects_whitespace_only_body(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/notes",
        json={"body": "   \n "},
    )

    assert res.status_code == 422


def test_create_note_strips_surrounding_whitespace(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/notes",
        json={"body": "  Called back \n"},
    )

    assert res.status_code == 201
    assert res.json()["body"] == "Called back"


def test_create_note_enforces_max_length(staff_client, db):
    inquiry = add_inquiry(db)
    url = f"/admin/inquiries/{inquiry.id}/notes"

    assert staff_client.post(url, json={"body": "x" * 5000}).status_code == 201
    assert staff_client.post(url, json={"body": "x" * 5001}).status_code == 422


def test_create_note_rejects_nul_character(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/notes",
        json={"body": "a\x00b"},
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


def test_list_notes_returns_only_that_inquirys_notes(staff_client, db):
    inquiry = add_inquiry(db)
    other_inquiry = add_inquiry(db)
    staff_client.post(f"/admin/inquiries/{inquiry.id}/notes", json={"body": "Mine"})
    staff_client.post(
        f"/admin/inquiries/{other_inquiry.id}/notes", json={"body": "Other"}
    )

    body = staff_client.get(f"/admin/inquiries/{inquiry.id}/notes").json()

    assert body["total"] == 1
    assert [item["body"] for item in body["items"]] == ["Mine"]


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


def test_notes_cannot_be_edited_or_deleted(staff_client, db):
    inquiry = add_inquiry(db)
    note = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/notes", json={"body": "Note"}
    ).json()
    url = f"/admin/inquiries/{inquiry.id}/notes/{note['id']}"

    assert staff_client.patch(url, json={"body": "Changed"}).status_code == 404
    assert staff_client.delete(url).status_code == 404


def test_note_routes_require_auth(client, db):
    inquiry = add_inquiry(db)

    assert (
        client.post(
            f"/admin/inquiries/{inquiry.id}/notes", json={"body": "Note"}
        ).status_code
        == 401
    )
    assert client.get(f"/admin/inquiries/{inquiry.id}/notes").status_code == 401
