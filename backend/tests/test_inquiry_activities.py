from datetime import UTC, datetime, timedelta

from app.models.inquiry import Inquiry
from app.models.inquiry_activity import InquiryActivity

MISSING_ID = "00000000-0000-0000-0000-000000000000"
VALID = {"channel": "phone", "outcome": "left_message"}


def add_inquiry(db) -> Inquiry:
    inquiry = Inquiry(
        role="athlete",
        contact_name="Test Person",
        contact_email="test@example.com",
        zip_code="37203",
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
    inquiry = add_inquiry(db)
    past = datetime(2026, 1, 15, 10, 0, tzinfo=UTC)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "occurred_at": past.isoformat()},
    )

    assert res.status_code == 201
    assert parse_time(res.json()["occurred_at"]) == past


def test_create_activity_ignores_staff_id_in_body(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "staff_id": "someone_else"},
    )

    assert res.status_code == 201
    assert res.json()["staff_id"] == "user_test_staff"


# --- Validation (422) ---


def test_create_activity_rejects_future_occurred_at(staff_client, db):
    inquiry = add_inquiry(db)
    future = datetime.now(UTC) + timedelta(days=1)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "occurred_at": future.isoformat()},
    )

    assert res.status_code == 422


def test_create_activity_rejects_unknown_channel(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/activities",
        json={**VALID, "channel": "fax"},
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
