from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from app.models.inquiry import InquiryStatus
from app.models.region import Region
from tests.test_inquiries import add_inquiry

TN_TZ = ZoneInfo("America/Chicago")


def _at(day: date, hour: int = 12) -> datetime:
    return datetime(day.year, day.month, day.day, hour, tzinfo=TN_TZ)


def test_stats_require_auth(client):
    assert client.get("/admin/stats").status_code == 401


def test_stats_rejects_inverted_range(staff_client):
    res = staff_client.get(
        "/admin/stats",
        params={"start": "2026-10-31", "end": "2026-10-01"},
    )
    assert res.status_code == 422


def test_stats_counts_and_breakdowns(staff_client, db):
    today = datetime.now(TN_TZ).date()
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=7)

    add_inquiry(
        db,
        contact_name="Today Athlete",
        role="athlete",
        status=InquiryStatus.NEW,
        region=Region.MIDDLE,
        created_at=_at(today),
    )
    add_inquiry(
        db,
        contact_name="Yesterday Volunteer",
        role="volunteer",
        status=InquiryStatus.ASSIGNED,
        region=Region.EAST,
        created_at=_at(yesterday),
    )
    add_inquiry(
        db,
        contact_name="Last Week Donor",
        role="donor",
        status=InquiryStatus.CONTACTED,
        region=Region.WEST,
        created_at=_at(last_week),
    )
    add_inquiry(
        db,
        contact_name="No Region Yet",
        role="athlete",
        status=InquiryStatus.NEEDS_REVIEW,
        region=None,
        created_at=_at(today, hour=15),
    )

    res = staff_client.get(
        "/admin/stats",
        params={
            "start": (today - timedelta(days=7)).isoformat(),
            "end": today.isoformat(),
        },
    )

    assert res.status_code == 200
    body = res.json()
    assert body["new_today"] == 2
    assert body["awaiting_contact"] == 3
    assert body["total"] == 4

    by_day = {row["date"]: row["count"] for row in body["by_day"]}
    assert by_day[today.isoformat()] == 2
    assert by_day[yesterday.isoformat()] == 1
    assert by_day[last_week.isoformat()] == 1
    assert len(body["by_day"]) == 8

    by_role = {row["role"]: row["count"] for row in body["by_role"]}
    assert by_role == {"athlete": 2, "volunteer": 1, "donor": 1}

    by_region = {(row["region"]): row["count"] for row in body["by_region"]}
    assert by_region == {"middle": 1, "east": 1, "west": 1, None: 1}

    by_status = {row["status"]: row["count"] for row in body["by_status"]}
    assert by_status == {
        "new": 1,
        "assigned": 1,
        "contacted": 1,
        "needs_review": 1,
    }


def test_stats_default_range_is_last_30_days(staff_client, db):
    today = datetime.now(TN_TZ).date()
    inside = today - timedelta(days=10)
    outside = today - timedelta(days=40)

    add_inquiry(db, contact_name="Inside", created_at=_at(inside))
    add_inquiry(db, contact_name="Outside", created_at=_at(outside))

    body = staff_client.get("/admin/stats").json()

    assert body["total"] == 1
    assert len(body["by_day"]) == 30
    assert body["by_day"][0]["date"] == (today - timedelta(days=29)).isoformat()
    assert body["by_day"][-1]["date"] == today.isoformat()


def test_awaiting_contact_ignores_date_range(staff_client, db):
    today = datetime.now(TN_TZ).date()
    old = today - timedelta(days=60)

    add_inquiry(
        db,
        contact_name="Old New",
        status=InquiryStatus.NEW,
        created_at=_at(old),
    )
    add_inquiry(
        db,
        contact_name="Recent Contacted",
        status=InquiryStatus.CONTACTED,
        created_at=_at(today),
    )

    body = staff_client.get(
        "/admin/stats",
        params={"start": today.isoformat(), "end": today.isoformat()},
    ).json()

    assert body["total"] == 1
    assert body["awaiting_contact"] == 1
