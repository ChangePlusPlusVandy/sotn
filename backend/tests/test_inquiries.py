from app.models.inquiry import Inquiry, InquiryStatus

VALID = {
    "role": "athlete",
    "contact_name": "Test Person",
    "contact_email": "test@example.com",
    "zip_code": "37203",
    "answers": {"sport_interest": "tennis"},
}


def test_create_inquiry_returns_reference_only(client, db):
    res = client.post("/inquiries", json=VALID)

    assert res.status_code == 201
    body = res.json()
    assert set(body) == {"id", "status"}
    assert body["status"] == "new"

    inquiry = db.get(Inquiry, body["id"])
    assert inquiry.contact_email == "test@example.com"
    assert inquiry.status == InquiryStatus.NEW
    assert inquiry.answers == {"sport_interest": "tennis"}


def test_create_inquiry_requires_contact_method(client):
    res = client.post("/inquiries", json={**VALID, "contact_email": None})
    assert res.status_code == 422


def test_create_inquiry_rejects_unknown_role(client):
    res = client.post("/inquiries", json={**VALID, "role": "astronaut"})
    assert res.status_code == 422


def test_create_inquiry_rejects_bad_zip(client):
    res = client.post("/inquiries", json={**VALID, "zip_code": "abc"})
    assert res.status_code == 422


def add_inquiry(db, **overrides) -> Inquiry:
    fields = {
        "role": "athlete",
        "contact_name": "Test Person",
        "contact_email": "test@example.com",
        "zip_code": "37203",
        **overrides,
    }
    inquiry = Inquiry(**fields)
    db.add(inquiry)
    db.flush()
    return inquiry


def test_admin_routes_require_auth(client, db):
    inquiry = add_inquiry(db)

    assert client.get("/admin/inquiries").status_code == 401
    assert client.get(f"/admin/inquiries/{inquiry.id}").status_code == 401
    assert client.patch(f"/admin/inquiries/{inquiry.id}", json={}).status_code == 401


def test_list_inquiries_filters_and_searches(staff_client, db):
    add_inquiry(db, contact_name="Ada Athlete")
    add_inquiry(db, contact_name="Val Volunteer", role="volunteer")
    add_inquiry(db, contact_name="Ada Donor", role="donor", status="closed")

    res = staff_client.get("/admin/inquiries", params={"role": "volunteer"})
    assert [i["contact_name"] for i in res.json()["items"]] == ["Val Volunteer"]

    res = staff_client.get("/admin/inquiries", params={"status": "closed"})
    assert [i["contact_name"] for i in res.json()["items"]] == ["Ada Donor"]

    res = staff_client.get("/admin/inquiries", params={"q": "ada"})
    assert res.json()["total"] == 2


def test_list_inquiries_paginates(staff_client, db):
    for n in range(3):
        add_inquiry(db, contact_name=f"Person {n}")

    body = staff_client.get(
        "/admin/inquiries", params={"page": 2, "page_size": 2}
    ).json()

    assert body["total"] == 3
    assert body["page"] == 2
    assert len(body["items"]) == 1


def test_get_inquiry_returns_full_record(staff_client, db):
    inquiry = add_inquiry(db, answers={"sport_interest": "tennis"})

    res = staff_client.get(f"/admin/inquiries/{inquiry.id}")

    assert res.status_code == 200
    assert res.json()["contact_email"] == "test@example.com"
    assert res.json()["answers"] == {"sport_interest": "tennis"}


def test_get_inquiry_404(staff_client):
    res = staff_client.get("/admin/inquiries/00000000-0000-0000-0000-000000000000")
    assert res.status_code == 404


def test_update_inquiry_changes_only_sent_fields(staff_client, db):
    inquiry = add_inquiry(db, contact_phone="615-555-0100")

    res = staff_client.patch(
        f"/admin/inquiries/{inquiry.id}", json={"status": "contacted"}
    )

    assert res.status_code == 200
    assert res.json()["status"] == "contacted"
    assert res.json()["contact_phone"] == "615-555-0100"


def test_update_inquiry_rejects_null_required_field(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.patch(f"/admin/inquiries/{inquiry.id}", json={"status": None})

    assert res.status_code == 422


def test_update_inquiry_must_keep_a_contact_method(staff_client, db):
    inquiry = add_inquiry(db)

    res = staff_client.patch(
        f"/admin/inquiries/{inquiry.id}", json={"contact_email": None}
    )

    assert res.status_code == 422
