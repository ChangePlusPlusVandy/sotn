"""Seed the local database with sample inquiries, programs and resources.

Run from backend/:
    uv run python -m app.seed           # add sample rows that aren't there yet
    uv run python -m app.seed --reset   # delete every row in every table, then seed

Without --reset, existing rows are never changed, including sample rows you edited.
Notes, activities and follow-ups aren't seeded: they need a real staff member's Clerk ID,
so create them through the app.
"""

import argparse
import sys
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import make_url
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import SessionLocal
from app.models import Inquiry, Program, Resource
from app.models.base import Base
from app.models.inquiry import InquiryRole as Role
from app.models.inquiry import InquiryStatus as Status
from app.models.programs import Region
from app.models.resource import ResourceKind as Kind
from app.schemas.inquiry import InquiryCreate
from app.schemas.programs import ProgramCreate
from app.schemas.resource import ResourceCreate

# Sample rows get fixed IDs so a rerun can tell which ones already exist.
SEED_NAMESPACE = uuid.UUID("5e6d0000-0000-4000-8000-000000000000")


def seed_id(kind: str, key: str) -> uuid.UUID:
    return uuid.uuid5(SEED_NAMESPACE, f"{kind}:{key}")


# (name, role, status, zip, email, phone), newest first
INQUIRIES = [
    (
        "Aisha Robinson",
        Role.ATHLETE,
        Status.NEW,
        "37902",
        "aisha.robinson@example.com",
        None,
    ),
    (
        "Ben Carter",
        Role.ATHLETE,
        Status.NEEDS_REVIEW,
        "37203",
        "ben.carter@example.com",
        "615-555-0142",
    ),
    (
        "Chloe Nguyen",
        Role.VOLUNTEER,
        Status.ASSIGNED,
        "38103",
        "chloe.nguyen@example.com",
        None,
    ),
    (
        "Diego Alvarez",
        Role.VOLUNTEER,
        Status.CONTACTED,
        "38501",
        "diego.alvarez@example.com",
        None,
    ),
    (
        "Elena Park",
        Role.PARTNER,
        Status.REFERRED,
        "37402",
        "elena.park@example.com",
        "423-555-0187",
    ),
    ("Frankie Doyle", Role.PARTNER, Status.NEW, "37604", None, "423-555-0110"),
    (
        "Gabby Suarez",
        Role.DONOR,
        Status.CLOSED,
        "37064",
        "gabby.suarez@example.com",
        None,
    ),
    ("Henry Blake", Role.PARTNER, Status.NEW, "38301", "henry.blake@example.com", None),
    ("Iris Chen", Role.ATHLETE, Status.NEW, "38506", "iris.chen@example.com", None),
    (
        "Jonah Weiss",
        Role.VOLUNTEER,
        Status.NEEDS_REVIEW,
        "37421",
        "jonah.weiss@example.com",
        None,
    ),
    (
        "Kaya Patel",
        Role.ATHLETE,
        Status.ASSIGNED,
        "37919",
        "kaya.patel@example.com",
        "865-555-0133",
    ),
    (
        "Liam O'Neill",
        Role.ATHLETE,
        Status.CONTACTED,
        "37211",
        "liam.o.neill@example.com",
        None,
    ),
    ("Maya Brooks", Role.ATHLETE, Status.NEW, "38117", "maya.brooks@example.com", None),
    (
        "Noah Fields",
        Role.VOLUNTEER,
        Status.REFERRED,
        "38583",
        "noah.fields@example.com",
        None,
    ),
    (
        "Olive Ramos",
        Role.PARTNER,
        Status.NEEDS_REVIEW,
        "37343",
        "olive.ramos@example.com",
        None,
    ),
    (
        "Priya Singh",
        Role.PARTNER,
        Status.CLOSED,
        "37620",
        "priya.singh@example.com",
        None,
    ),
    (
        "Quinn Larson",
        Role.DONOR,
        Status.NEW,
        "37027",
        "quinn.larson@example.com",
        "615-555-0199",
    ),
    (
        "Ravi Bhatt",
        Role.PARTNER,
        Status.ASSIGNED,
        "38305",
        "ravi.bhatt@example.com",
        None,
    ),
    ("Sasha Kim", Role.ATHLETE, Status.NEEDS_REVIEW, "38555", None, "931-555-0164"),
    (
        "Tomas Herrera",
        Role.VOLUNTEER,
        Status.CONTACTED,
        "37411",
        "tomas.herrera@example.com",
        None,
    ),
    (
        "Uma Desai",
        Role.ATHLETE,
        Status.REFERRED,
        "37917",
        "uma.desai@example.com",
        None,
    ),
    ("Vera Popov", Role.ATHLETE, Status.NEW, "37013", "vera.popov@example.com", None),
    (
        "Wes Ackerman",
        Role.ATHLETE,
        Status.ASSIGNED,
        "38016",
        "wes.ackerman@example.com",
        None,
    ),
    ("Xio Vega", Role.VOLUNTEER, Status.CLOSED, "38501", "xio.vega@example.com", None),
    (
        "Yasmin Hart",
        Role.VOLUNTEER,
        Status.NEW,
        "37405",
        "yasmin.hart@example.com",
        None,
    ),
    (
        "Zeke Morales",
        Role.PARTNER,
        Status.CONTACTED,
        "37601",
        "zeke.morales@example.com",
        None,
    ),
    (
        "Amelia Ford",
        Role.DONOR,
        Status.NEEDS_REVIEW,
        "37067",
        "amelia.ford@example.com",
        None,
    ),
    (
        "Bruno Hall",
        Role.PARTNER,
        Status.REFERRED,
        "38134",
        "bruno.hall@example.com",
        None,
    ),
    (
        "Cora Yates",
        Role.ATHLETE,
        Status.CONTACTED,
        "38506",
        "cora.yates@example.com",
        None,
    ),
    ("Devi Rao", Role.VOLUNTEER, Status.NEW, "37415", "devi.rao@example.com", None),
]

FIRST_SUBMITTED = datetime(2026, 10, 19, 15, tzinfo=UTC)

ALL_REGIONS = [Region.EAST, Region.MIDDLE, Region.WEST]

PROGRAMS = [
    {
        "name": "Sports Programming",
        "description": "Year-round training and competition in more than 20 Olympic-type sports.",
        "audiences": [Role.ATHLETE],
        "regions": ALL_REGIONS,
        "contact_email": "sports@example.com",
    },
    {
        "name": "Healthy Athletes Screenings",
        "description": "Free health screenings in vision, hearing, dental and more at events.",
        "audiences": [Role.ATHLETE],
        "regions": ALL_REGIONS,
        "contact_email": "health@example.com",
    },
    {
        "name": "Train4Life",
        "description": "Fitness and wellness sessions to build healthy habits between seasons.",
        "audiences": [Role.ATHLETE],
        "regions": [Region.MIDDLE, Region.EAST],
        "contact_email": "fitness@example.com",
    },
    {
        "name": "Inclusive Health Training",
        "description": "Training for health professionals on caring for people with intellectual disabilities.",
        "audiences": [Role.PARTNER, Role.VOLUNTEER],
        "regions": ALL_REGIONS,
        "contact_email": "health@example.com",
    },
    {
        "name": "Unified Champion Schools",
        "description": "Unified sports, inclusive youth leadership and whole-school engagement.",
        "audiences": [Role.ATHLETE, Role.PARTNER],
        "regions": ALL_REGIONS,
        "contact_email": "schools@example.com",
    },
    {
        "name": "Athlete Leadership",
        "description": "Leadership, public speaking and governance roles for athletes.",
        "audiences": [Role.ATHLETE],
        "regions": [Region.MIDDLE],
        "contact_email": "leadership@example.com",
    },
    {
        "name": "Volunteer Engagement",
        "description": "Event-day, ongoing and skilled volunteer roles across the state.",
        "audiences": [Role.VOLUNTEER],
        "regions": ALL_REGIONS,
        "contact_email": "volunteer@example.com",
    },
    {
        "name": "Coach Engagement",
        "description": "Coach certification, training and placement with local programs.",
        "audiences": [Role.VOLUNTEER],
        "regions": ALL_REGIONS,
        "contact_email": "coaches@example.com",
    },
    {
        "name": "Sponsors & Corporate Partners",
        "description": "Event sponsorship and corporate partnership opportunities.",
        "audiences": [Role.DONOR, Role.PARTNER],
        "regions": ALL_REGIONS,
        "contact_email": "partners@example.com",
    },
    {
        "name": "Donors",
        "description": "One-time and recurring giving to support athletes statewide.",
        "audiences": [Role.DONOR],
        "regions": ALL_REGIONS,
        "contact_email": "giving@example.com",
    },
    {
        "name": "Vendors & Community Partners",
        "description": "Venue, vendor and community organization partnerships.",
        "audiences": [Role.PARTNER],
        "regions": [Region.WEST],
        "contact_email": "community@example.com",
        "is_active": False,
    },
]

RESOURCES = [
    {
        "title": "Getting started as an athlete",
        "description": "What to expect at your first practice and how to register.",
        "kind": Kind.PDF,
        "url": "https://example.com/resources/athlete-getting-started.pdf",
        "audiences": [Role.ATHLETE],
        "is_published": True,
    },
    {
        "title": "Athlete medical form",
        "description": "Required before an athlete can train or compete.",
        "kind": Kind.PDF,
        "url": "https://example.com/resources/athlete-medical-form.pdf",
        "audiences": [Role.ATHLETE],
        "is_published": True,
    },
    {
        "title": "What is Special Olympics Tennessee?",
        "kind": Kind.VIDEO,
        "url": "https://example.com/resources/about-sotn-video",
        "audiences": [Role.ATHLETE, Role.VOLUNTEER, Role.PARTNER, Role.DONOR],
        "is_published": True,
    },
    {
        "title": "Volunteer orientation",
        "description": "A short overview of volunteer roles and event-day expectations.",
        "kind": Kind.VIDEO,
        "url": "https://example.com/resources/volunteer-orientation-video",
        "audiences": [Role.VOLUNTEER],
        "is_published": True,
    },
    {
        "title": "Protective Behaviors training",
        "description": "Required training for all Class A volunteers.",
        "kind": Kind.LINK,
        "url": "https://example.com/resources/protective-behaviors",
        "audiences": [Role.VOLUNTEER],
        "is_published": True,
    },
    {
        "title": "Partnership overview",
        "kind": Kind.PDF,
        "url": "https://example.com/resources/partnership-overview.pdf",
        "audiences": [Role.PARTNER, Role.DONOR],
        "is_published": True,
    },
    {
        "title": "Ways to give",
        "kind": Kind.LINK,
        "url": "https://example.com/resources/ways-to-give",
        "audiences": [Role.DONOR],
        "is_published": True,
    },
    {
        "title": "Coach certification guide (draft)",
        "description": "Unpublished draft; should not appear on the public results page.",
        "kind": Kind.PDF,
        "url": "https://example.com/resources/coach-certification-draft.pdf",
        "audiences": [Role.VOLUNTEER],
        "is_published": False,
    },
]


def inquiry_rows() -> list[dict]:
    rows = []
    for index, (name, role, status, zip_code, email, phone) in enumerate(INQUIRIES):
        body = InquiryCreate(
            role=role,
            contact_name=name,
            contact_email=email,
            contact_phone=phone,
            zip_code=zip_code,
        )
        submitted = FIRST_SUBMITTED - timedelta(days=index)
        rows.append(
            {
                "id": seed_id("inquiry", name),
                **body.model_dump(),
                "status": status,
                "created_at": submitted,
                "updated_at": submitted,
            }
        )
    return rows


def program_rows() -> list[dict]:
    return [
        {
            "id": seed_id("program", program["name"]),
            **ProgramCreate(**program).model_dump(),
        }
        for program in PROGRAMS
    ]


def resource_rows() -> list[dict]:
    return [
        {
            "id": seed_id("resource", resource["title"]),
            **ResourceCreate(**resource).model_dump(),
        }
        for resource in RESOURCES
    ]


def insert_missing(db: Session, model, rows: list[dict]) -> int:
    """Insert rows, skipping any that conflict with an existing row. Returns how many were added."""
    # No conflict target, so a program whose unique name is already taken is skipped too.
    statement = insert(model).values(rows).on_conflict_do_nothing().returning(model.id)
    return len(db.execute(statement).all())


def seed(db: Session) -> dict[str, int]:
    return {
        "inquiries": insert_missing(db, Inquiry, inquiry_rows()),
        "programs": insert_missing(db, Program, program_rows()),
        "resources": insert_missing(db, Resource, resource_rows()),
    }


def reset(db: Session) -> None:
    """Delete every row in every table, children before parents."""
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--reset",
        action="store_true",
        help="delete every row in every table first, including data you added",
    )
    args = parser.parse_args()

    host = make_url(settings.database_url).host
    if host not in ("localhost", "127.0.0.1"):
        sys.exit(
            f"Refusing to seed {host}: this script is only for the local database."
        )

    totals = {
        "inquiries": len(INQUIRIES),
        "programs": len(PROGRAMS),
        "resources": len(RESOURCES),
    }
    with SessionLocal() as db:
        if args.reset:
            reset(db)
        added = seed(db)
        db.commit()

    if args.reset:
        print("Deleted all existing rows.")
    for table, count in added.items():
        print(
            f"{table}: added {count}, skipped {totals[table] - count} already present"
        )


if __name__ == "__main__":
    main()
