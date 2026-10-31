from datetime import UTC, datetime, timedelta

from app.models.follow_up import FollowUp, FollowUpStatus
from app.models.inquiry import Inquiry
from tests.conftest import TEST_STAFF_ID

MISSING_ID = "00000000-0000-0000-0000-000000000000"


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


def add_follow_up(db, inquiry, **overrides) -> FollowUp:
    fields = {
        "inquiry_id": inquiry.id,
        "title": "Call back",
        "created_by_staff_id": TEST_STAFF_ID,
        "assignee_staff_id": TEST_STAFF_ID,
        "due_at": datetime.now(UTC) + timedelta(days=7),
        **overrides,
    }
    follow_up = FollowUp(**fields)
    db.add(follow_up)
    db.flush()
    return follow_up


def test_create_follow_up(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/follow-ups",
        json={
            "title": "Call back",
            "details": "Ask about tennis",
            "due_at": "2026-11-07T17:00:00Z",
            "assignee_staff_id": "user_other_staff",
        },
    )

    assert res.status_code == 201
    body = res.json()
    assert body["inquiry_id"] == str(inquiry.id)
    assert body["title"] == "Call back"
    assert body["status"] == "not_started"
    assert body["completed_at"] is None
    assert body["created_by_staff_id"] == TEST_STAFF_ID
    assert body["assignee_staff_id"] == "user_other_staff"

    follow_up = db.get(FollowUp, body["id"])
    assert follow_up.details == "Ask about tennis"


def test_create_follow_up_assigns_current_staff_by_default(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.post(
        f"/admin/inquiries/{inquiry.id}/follow-ups",
        json={"title": "Call back", "due_at": "2026-11-07T17:00:00Z"},
    )

    assert res.status_code == 201
    assert res.json()["assignee_staff_id"] == TEST_STAFF_ID


def test_create_follow_up_404_for_missing_inquiry(staff_client):
    res = staff_client.post(
        f"/admin/inquiries/{MISSING_ID}/follow-ups",
        json={"title": "Call back", "due_at": "2026-11-07T17:00:00Z"},
    )
    assert res.status_code == 404


def test_create_follow_up_validates_body(staff_client, db):
    inquiry = add_inquiry(db)
    url = f"/admin/inquiries/{inquiry.id}/follow-ups"

    assert staff_client.post(url, json={"title": "Call back"}).status_code == 422
    assert (
        staff_client.post(
            url, json={"title": "", "due_at": "2026-11-07T17:00:00Z"}
        ).status_code
        == 422
    )


def test_follow_up_routes_require_auth(client, db):
    inquiry = add_inquiry(db)
    follow_up = add_follow_up(db, inquiry)

    assert (
        client.post(f"/admin/inquiries/{inquiry.id}/follow-ups", json={}).status_code
        == 401
    )
    assert client.get("/admin/follow-ups").status_code == 401
    assert client.get(f"/admin/follow-ups/{follow_up.id}").status_code == 401
    assert client.patch(f"/admin/follow-ups/{follow_up.id}", json={}).status_code == 401


def test_list_follow_ups_sorted_by_due_date(staff_client, db):
    inquiry = add_inquiry(db)
    now = datetime.now(UTC)
    add_follow_up(db, inquiry, title="Later", due_at=now + timedelta(days=3))
    add_follow_up(db, inquiry, title="Soonest", due_at=now + timedelta(days=1))
    add_follow_up(db, inquiry, title="Middle", due_at=now + timedelta(days=2))

    res = staff_client.get("/admin/follow-ups")

    assert res.status_code == 200
    assert [f["title"] for f in res.json()["items"]] == ["Soonest", "Middle", "Later"]


def test_list_follow_ups_filters(staff_client, db):
    inquiry = add_inquiry(db)
    other_inquiry = add_inquiry(db)
    add_follow_up(db, inquiry, title="Mine")
    add_follow_up(db, inquiry, title="Theirs", assignee_staff_id="user_other_staff")
    add_follow_up(db, other_inquiry, title="Started", status="in_progress")

    res = staff_client.get("/admin/follow-ups", params={"status": "in_progress"})
    assert [f["title"] for f in res.json()["items"]] == ["Started"]

    res = staff_client.get("/admin/follow-ups", params={"inquiry_id": str(inquiry.id)})
    assert res.json()["total"] == 2

    res = staff_client.get("/admin/follow-ups", params={"assignee": "me"})
    assert {f["title"] for f in res.json()["items"]} == {"Mine", "Started"}


def test_list_follow_ups_overdue_excludes_complete_and_future(staff_client, db):
    inquiry = add_inquiry(db)
    yesterday = datetime.now(UTC) - timedelta(days=1)
    add_follow_up(db, inquiry, title="Overdue", due_at=yesterday)
    add_follow_up(db, inquiry, title="Done", due_at=yesterday, status="complete")
    add_follow_up(db, inquiry, title="Upcoming")

    res = staff_client.get("/admin/follow-ups", params={"overdue": "true"})

    assert [f["title"] for f in res.json()["items"]] == ["Overdue"]


def test_list_follow_ups_paginates(staff_client, db):
    inquiry = add_inquiry(db)
    for n in range(3):
        add_follow_up(db, inquiry, title=f"Follow-up {n}")

    body = staff_client.get(
        "/admin/follow-ups", params={"page": 2, "page_size": 2}
    ).json()

    assert body["total"] == 3
    assert body["page"] == 2
    assert len(body["items"]) == 1


def test_get_follow_up(staff_client, db):
    follow_up = add_follow_up(db, add_inquiry(db), details="Ask about tennis")

    res = staff_client.get(f"/admin/follow-ups/{follow_up.id}")

    assert res.status_code == 200
    assert res.json()["details"] == "Ask about tennis"


def test_get_follow_up_404(staff_client):
    res = staff_client.get(f"/admin/follow-ups/{MISSING_ID}")
    assert res.status_code == 404


def test_update_follow_up_changes_only_sent_fields(staff_client, db):
    follow_up = add_follow_up(db, add_inquiry(db), details="Ask about tennis")

    res = staff_client.patch(
        f"/admin/follow-ups/{follow_up.id}", json={"title": "Email instead"}
    )

    assert res.status_code == 200
    assert res.json()["title"] == "Email instead"
    assert res.json()["details"] == "Ask about tennis"


def test_update_follow_up_rejects_null_required_field(staff_client, db):
    follow_up = add_follow_up(db, add_inquiry(db))

    res = staff_client.patch(f"/admin/follow-ups/{follow_up.id}", json={"title": None})

    assert res.status_code == 422


def test_update_follow_up_404(staff_client):
    res = staff_client.patch(f"/admin/follow-ups/{MISSING_ID}", json={"title": "x"})
    assert res.status_code == 404


def test_completing_sets_completed_at_and_reopening_clears_it(staff_client, db):
    follow_up = add_follow_up(db, add_inquiry(db))
    url = f"/admin/follow-ups/{follow_up.id}"

    res = staff_client.patch(url, json={"status": "complete"})
    completed_at = res.json()["completed_at"]
    assert res.json()["status"] == "complete"
    assert completed_at is not None

    # Editing a complete follow-up keeps its original completion time.
    res = staff_client.patch(url, json={"title": "Called back"})
    assert res.json()["completed_at"] == completed_at

    res = staff_client.patch(url, json={"status": "in_progress"})
    assert res.json()["completed_at"] is None
    assert db.get(FollowUp, follow_up.id).status == FollowUpStatus.IN_PROGRESS
