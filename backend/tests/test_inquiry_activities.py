from datetime import UTC, datetime, timedelta

from app.models.inquiry import Inquiry
from app.models.inquiry_activity import InquiryActivity

MISSING_ID = "00000000-0000-0000-0000-000000000000"
VALID = {"channel": "phone", "outcome": "left_message"}


def add_inquiry(db, **overrides) -> Inquiry:
    inquiry = Inquiry(
        role="athlete",
        contact_name="Test Person",
        contact_email="test@example.com",
        zip_code="37203",
        **overrides,
    )
    db.add(inquiry)
    db.flush()
    return inquiry


def add_activity(db, inquiry, **overrides) -> InquiryActivity:
    fields = {
        "inquiry_id": inquiry.id,
        "staff_id": "user_other_staff",
        "channel": "email",
        "outcome": "reached",
        "occurred_at": datetime.now(UTC),
        **overrides,
    }
    activity = InquiryActivity(**fields)
    db.add(activity)
    db.flush()
    return activity


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


# --- Auth (401) ---


def test_activity_routes_require_auth(client, db):
    inquiry = add_inquiry(db)
    url = f"/admin/inquiries/{inquiry.id}/activities"

    assert client.post(url, json=VALID).status_code == 401
    assert client.get(url).status_code == 401


# --- Create (201) ---


def test_create_activity(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "summary": "Will try again Thursday"},
    )

    assert res.status_code == 201
    body = res.json()
    assert body["inquiry_id"] == str(inquiry.id)
    assert body["staff_id"] == "user_test_staff"  # from staff_client in conftest.py
    assert body["channel"] == "phone"
    assert body["outcome"] == "left_message"
    assert body["summary"] == "Will try again Thursday"


def test_create_activity_defaults_occurred_at_to_now(staff_client, db):
    inquiry = add_inquiry(db)

    before = datetime.now(UTC)
    res = staff_client.post(f"/admin/inquiries/{inquiry.id}/activities", json=VALID)
    after = datetime.now(UTC)

    assert res.status_code == 201
    assert before <= parse_time(res.json()["occurred_at"]) <= after


def test_create_activity_keeps_past_occurred_at(staff_client, db):
    inquiry = add_inquiry(db, created_at=datetime(2026, 1, 1, tzinfo=UTC))
    past = datetime(2026, 1, 15, 10, 0, tzinfo=UTC)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "occurred_at": past.isoformat()},
    )

    assert res.status_code == 201
    assert parse_time(res.json()["occurred_at"]) == past


def test_create_activity_accepts_occurred_at_equal_to_inquiry_created_at(
    staff_client, db
):
    created_at = datetime(2026, 1, 1, tzinfo=UTC)
    inquiry = add_inquiry(db, created_at=created_at)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "occurred_at": created_at.isoformat()},
    )

    assert res.status_code == 201
    assert parse_time(res.json()["occurred_at"]) == created_at


def test_create_activity_strips_summary_whitespace(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "summary": "  Called back \n"},
    )

    assert res.status_code == 201
    assert res.json()["summary"] == "Called back"


def test_create_activity_stores_blank_summary_as_null(staff_client, db):
    inquiry = add_inquiry(db)
    url = f"/admin/inquiries/{inquiry.id}/activities"

    for blank in ("", "   \n "):
        res = staff_client.post(url, json={**VALID, "summary": blank})

        assert res.status_code == 201
        assert res.json()["summary"] is None


def test_create_activity_accepts_max_length_summary(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "summary": "x" * 500},
    )

    assert res.status_code == 201


# --- Validation (422) ---


def test_create_activity_rejects_client_supplied_staff_id(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "staff_id": "someone_else"},
    )

    assert res.status_code == 422


def test_create_activity_rejects_unknown_field(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "sumary": "Typo in the field name"},
    )

    assert res.status_code == 422


def test_create_activity_rejects_occurred_at_without_timezone(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "occurred_at": "2026-01-15T10:00:00"},
    )

    assert res.status_code == 422


def test_create_activity_rejects_future_occurred_at(staff_client, db):
    inquiry = add_inquiry(db)
    future = datetime.now(UTC) + timedelta(days=1)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "occurred_at": future.isoformat()},
    )

    assert res.status_code == 422


def test_create_activity_rejects_occurred_at_before_inquiry_created_at(
    staff_client, db
):
    created_at = datetime(2026, 1, 1, tzinfo=UTC)
    inquiry = add_inquiry(db, created_at=created_at)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "occurred_at": (created_at - timedelta(seconds=1)).isoformat()},
    )

    assert res.status_code == 422


def test_create_activity_rejects_year_1_occurred_at(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "occurred_at": "0001-01-01T00:00:00+14:00"},
    )

    assert res.status_code == 422


def test_create_activity_rejects_unknown_channel(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "channel": "fax"},
    )

    assert res.status_code == 422


def test_create_activity_rejects_unknown_outcome(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "outcome": "maybe"},
    )

    assert res.status_code == 422


def test_create_activity_rejects_nul_in_summary(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "summary": "a\x00b"},
    )

    assert res.status_code == 422


def test_create_activity_rejects_long_summary(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "summary": "x" * 501},
    )

    assert res.status_code == 422


# --- Not found (404) ---


def test_activity_routes_404_for_missing_inquiry(staff_client):
    url = f"/admin/inquiries/{MISSING_ID}/activities"

    assert staff_client.post(url, json=VALID).status_code == 404
    assert staff_client.get(url).status_code == 404


# --- List ---


def test_list_activities_newest_first(staff_client, db):
    inquiry = add_inquiry(db)
    now = datetime.now(UTC)
    add_activity(db, inquiry, summary="3 days ago", occurred_at=now - timedelta(days=3))
    add_activity(db, inquiry, summary="1 day ago", occurred_at=now - timedelta(days=1))
    add_activity(db, inquiry, summary="2 days ago", occurred_at=now - timedelta(days=2))

    res = staff_client.get(f"/admin/inquiries/{inquiry.id}/activities")

    assert res.status_code == 200
    body = res.json()
    assert body["total"] == 3
    assert [a["summary"] for a in body["items"]] == [
        "1 day ago",
        "2 days ago",
        "3 days ago",
    ]


def test_list_activities_only_returns_this_inquirys(staff_client, db):
    inquiry = add_inquiry(db)
    other = add_inquiry(db)
    add_activity(db, inquiry, summary="mine")
    add_activity(db, other, summary="not mine")

    res = staff_client.get(f"/admin/inquiries/{inquiry.id}/activities")

    assert [a["summary"] for a in res.json()["items"]] == ["mine"]


def test_list_activities_paginates(staff_client, db):
    inquiry = add_inquiry(db)
    for _ in range(3):
        add_activity(db, inquiry)

    body = staff_client.get(
        f"/admin/inquiries/{inquiry.id}/activities",
        params={"page": 2, "page_size": 2},
    ).json()

    assert body["total"] == 3
    assert body["page"] == 2
    assert len(body["items"]) == 1


# --- Append-only ---


def test_activities_cannot_be_edited_or_deleted(staff_client, db):
    inquiry = add_inquiry(db)
    activity = add_activity(db, inquiry)
    url = f"/admin/inquiries/{inquiry.id}/activities/{activity.id}"

    assert staff_client.patch(url, json={"summary": "Changed"}).status_code == 404
    assert staff_client.delete(url).status_code == 404
