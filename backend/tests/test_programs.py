"""Tests for the Program API."""

import uuid

from app.models.inquiry import InquiryRole
from app.models.programs import Program, Region

VALID_PROGRAM = {
    "name": "Train4Life",
    "description": "Fitness and wellness opportunities",
    "audiences": ["athlete"],
    "regions": ["middle"],
    "contact_email": "staff@example.com",
    "is_active": True,
}


def add_program(db, name: str, **overrides) -> Program:
    """Create a program directly in the test database."""

    fields = {
        "name": name,
        "description": "Sample program",
        "audiences": [InquiryRole.ATHLETE],
        "regions": [Region.MIDDLE],
        "contact_email": "internal@example.com",
        "is_active": True,
        **overrides,
    }

    program = Program(**fields)
    db.add(program)
    db.flush()

    return program


# ----------------------------------------
# POST: Create programs
# ----------------------------------------


def test_create_program_returns_full_admin_record(staff_client, db):
    response = staff_client.post(
        "/admin/programs",
        json=VALID_PROGRAM,
    )

    assert response.status_code == 201, response.text

    body = response.json()

    assert body["name"] == "Train4Life"
    assert body["audiences"] == ["athlete"]
    assert body["regions"] == ["middle"]
    assert body["contact_email"] == "staff@example.com"
    assert body["is_active"] is True
    assert body["created_at"] is not None
    assert body["updated_at"] is not None

    assert (
        db.get(
            Program,
            uuid.UUID(body["id"]),
        )
        is not None
    )


def test_duplicate_name_on_create_returns_409(staff_client, db):
    add_program(db, "Train4Life")

    response = staff_client.post(
        "/admin/programs",
        json=VALID_PROGRAM,
    )

    assert response.status_code == 409


# ----------------------------------------
# GET: Retrieve one program
# ----------------------------------------


def test_get_program_by_id_returns_contact_email(staff_client, db):
    program = add_program(db, "Unified Champion Schools")

    response = staff_client.get(f"/admin/programs/{program.id}")

    assert response.status_code == 200, response.text
    assert response.json()["id"] == str(program.id)
    assert response.json()["contact_email"] == "internal@example.com"


def test_get_nonexistent_program_returns_404(staff_client):
    response = staff_client.get(f"/admin/programs/{uuid.uuid4()}")

    assert response.status_code == 404


# ----------------------------------------
# PATCH: Update programs
# ----------------------------------------


def test_patch_updates_only_supplied_fields(staff_client, db):
    program = add_program(db, "Original Name")

    response = staff_client.patch(
        f"/admin/programs/{program.id}",
        json={"description": "Updated description"},
    )

    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Original Name"
    assert response.json()["description"] == "Updated description"
    assert response.json()["contact_email"] == "internal@example.com"


def test_rename_to_existing_name_returns_409(staff_client, db):
    program = add_program(db, "Program A")
    add_program(db, "Program B")

    response = staff_client.patch(
        f"/admin/programs/{program.id}",
        json={"name": "Program B"},
    )

    assert response.status_code == 409


def test_patch_nonnullable_field_to_null_returns_422(staff_client, db):
    program = add_program(db, "Program A")

    response = staff_client.patch(
        f"/admin/programs/{program.id}",
        json={"is_active": None},
    )

    assert response.status_code == 422


def test_patch_nonexistent_program_returns_404(staff_client):
    response = staff_client.patch(
        f"/admin/programs/{uuid.uuid4()}",
        json={"is_active": False},
    )

    assert response.status_code == 404


# ----------------------------------------
# Public API
# ----------------------------------------


def test_public_list_hides_inactive_programs_and_contact_email(client, db):
    active = add_program(db, "Active Program")

    add_program(
        db,
        "Inactive Program",
        is_active=False,
    )

    response = client.get("/programs")

    assert response.status_code == 200, response.text

    programs = response.json()

    assert [item["id"] for item in programs] == [str(active.id)]

    assert all("contact_email" not in item for item in programs)


def test_public_filters_by_role_and_region(client, db):
    add_program(
        db,
        "Athlete Middle",
        audiences=[InquiryRole.ATHLETE],
        regions=[Region.MIDDLE],
    )

    add_program(
        db,
        "Athlete East",
        audiences=[InquiryRole.ATHLETE],
        regions=[Region.EAST],
    )

    add_program(
        db,
        "Volunteer Middle",
        audiences=[InquiryRole.VOLUNTEER],
        regions=[Region.MIDDLE],
    )

    response = client.get(
        "/programs",
        params={
            "role": "athlete",
            "region": "middle",
        },
    )

    assert response.status_code == 200, response.text

    assert [item["name"] for item in response.json()] == ["Athlete Middle"]


def test_invalid_public_region_returns_422(client):
    response = client.get(
        "/programs",
        params={"region": "north"},
    )

    assert response.status_code == 422


# ----------------------------------------
# Deactivation
# ----------------------------------------


def test_deactivation_preserves_program_for_admin(staff_client, db):
    program = add_program(db, "Deactivate Me")

    patch = staff_client.patch(
        f"/admin/programs/{program.id}",
        json={"is_active": False},
    )

    assert patch.status_code == 200, patch.text
    assert patch.json()["is_active"] is False

    public_response = staff_client.get("/programs")

    assert public_response.status_code == 200

    assert all(item["id"] != str(program.id) for item in public_response.json())

    admin_response = staff_client.get(f"/admin/programs/{program.id}")

    assert admin_response.status_code == 200
    assert admin_response.json()["is_active"] is False


# ----------------------------------------
# Admin filtering
# ----------------------------------------


def test_admin_filters_by_activity_role_region_and_search(staff_client, db):
    add_program(
        db,
        "Middle Athlete",
        audiences=[InquiryRole.ATHLETE],
        regions=[Region.MIDDLE],
    )

    add_program(
        db,
        "East Athlete",
        audiences=[InquiryRole.ATHLETE],
        regions=[Region.EAST],
    )

    add_program(
        db,
        "Middle Volunteer",
        audiences=[InquiryRole.VOLUNTEER],
        regions=[Region.MIDDLE],
        is_active=False,
    )

    response = staff_client.get(
        "/admin/programs",
        params={
            "is_active": True,
            "role": "athlete",
            "region": "middle",
            "q": "athlete",
        },
    )

    assert response.status_code == 200, response.text

    body = response.json()

    assert body["total"] == 1
    assert [item["name"] for item in body["items"]] == ["Middle Athlete"]

    inactive = staff_client.get(
        "/admin/programs",
        params={"is_active": False},
    )

    assert inactive.status_code == 200

    assert [item["name"] for item in inactive.json()["items"]] == ["Middle Volunteer"]


# ----------------------------------------
# Pagination
# ----------------------------------------


def test_admin_list_paginates(staff_client, db):
    for index in range(3):
        add_program(db, f"Program {index}")

    response = staff_client.get(
        "/admin/programs",
        params={
            "page": 2,
            "page_size": 2,
        },
    )

    assert response.status_code == 200, response.text

    body = response.json()

    assert body["total"] == 3
    assert body["page"] == 2
    assert body["page_size"] == 2
    assert len(body["items"]) == 1


def test_admin_list_rejects_invalid_page_size(staff_client):
    response = staff_client.get(
        "/admin/programs",
        params={"page_size": 101},
    )

    assert response.status_code == 422


# ----------------------------------------
# Authentication
# ----------------------------------------


def test_admin_endpoints_require_auth(client, db):
    program = add_program(db, "Private Program")

    assert client.get("/admin/programs").status_code == 401

    assert client.get(f"/admin/programs/{program.id}").status_code == 401

    assert (
        client.post(
            "/admin/programs",
            json=VALID_PROGRAM,
        ).status_code
        == 401
    )

    assert (
        client.patch(
            f"/admin/programs/{program.id}",
            json={},
        ).status_code
        == 401
    )


# ----------------------------------------
# No DELETE endpoint
# ----------------------------------------


def test_programs_cannot_be_deleted(staff_client, db):
    program = add_program(db, "Keep This Program")

    response = staff_client.delete(f"/admin/programs/{program.id}")

    assert response.status_code == 405

    assert db.get(Program, program.id) is not None
