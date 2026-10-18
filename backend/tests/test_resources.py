from app.models.resource import Resource

VALID = {
    "title": "Training for Life overview",
    "description": "What the program is and who it is for",
    "kind": "video",
    "url": "https://example.com/training-for-life",
    "audiences": ["athlete", "volunteer"],
}

MISSING_ID = "00000000-0000-0000-0000-000000000000"


def add_resource(db, **overrides) -> Resource:
    fields = {
        "title": "Test Resource",
        "kind": "link",
        "url": "https://example.com",
        "audiences": ["athlete"],
        "is_published": True,
        **overrides,
    }
    resource = Resource(**fields)
    db.add(resource)
    db.flush()
    return resource


# Public routes


def test_public_list_shows_only_published(client, db):
    add_resource(db, title="Live")
    add_resource(db, title="Draft", is_published=False)

    res = client.get("/resources")

    assert res.status_code == 200
    assert [r["title"] for r in res.json()["items"]] == ["Live"]


def test_public_list_filters_by_role(client, db):
    add_resource(db, title="For athletes", audiences=["athlete"])
    add_resource(db, title="For both", audiences=["athlete", "volunteer"])
    add_resource(db, title="For donors", audiences=["donor"])

    res = client.get("/resources", params={"role": "volunteer"})

    assert [r["title"] for r in res.json()["items"]] == ["For both"]


def test_public_list_hides_unpublished_even_with_role(client, db):
    add_resource(db, title="Draft", audiences=["volunteer"], is_published=False)

    res = client.get("/resources", params={"role": "volunteer"})

    assert res.json()["total"] == 0


def test_public_list_rejects_unknown_role(client):
    res = client.get("/resources", params={"role": "astronaut"})
    assert res.status_code == 422


def test_public_cannot_write(client, db):
    resource = add_resource(db)

    assert client.post("/resources", json=VALID).status_code == 405
    assert client.delete(f"/resources/{resource.id}").status_code in (404, 405)


# Auth


def test_admin_routes_require_auth(client, db):
    resource = add_resource(db)
    path = f"/admin/resources/{resource.id}"

    assert client.get("/admin/resources").status_code == 401
    assert client.post("/admin/resources", json=VALID).status_code == 401
    assert client.get(path).status_code == 401
    assert client.patch(path, json={}).status_code == 401
    assert client.delete(path).status_code == 401
    assert db.get(Resource, resource.id) is not None


# Create


def test_create_resource(staff_client, db):
    res = staff_client.post("/admin/resources", json=VALID)

    assert res.status_code == 201
    body = res.json()
    assert body["title"] == VALID["title"]
    assert body["audiences"] == ["athlete", "volunteer"]
    assert body["is_published"] is False

    resource = db.get(Resource, body["id"])
    assert resource.kind == "video"
    assert resource.url == VALID["url"]


def test_create_resource_rejects_unknown_kind(staff_client):
    res = staff_client.post("/admin/resources", json={**VALID, "kind": "podcast"})
    assert res.status_code == 422


def test_create_resource_rejects_unknown_audience(staff_client):
    res = staff_client.post(
        "/admin/resources", json={**VALID, "audiences": ["astronaut"]}
    )
    assert res.status_code == 422


def test_create_resource_requires_title_and_url(staff_client):
    assert (
        staff_client.post("/admin/resources", json={**VALID, "title": ""}).status_code
        == 422
    )
    no_url = {k: v for k, v in VALID.items() if k != "url"}
    assert staff_client.post("/admin/resources", json=no_url).status_code == 422


def test_create_resource_rejects_long_title(staff_client):
    res = staff_client.post("/admin/resources", json={**VALID, "title": "x" * 201})
    assert res.status_code == 422


# Admin list


def test_admin_list_filters_and_searches(staff_client, db):
    add_resource(db, title="Coach guide", kind="pdf")
    add_resource(db, title="Intro video", kind="video", is_published=False)
    add_resource(db, title="Partner link", description="Guide for partners")

    res = staff_client.get("/admin/resources")
    assert res.json()["total"] == 3

    res = staff_client.get("/admin/resources", params={"kind": "pdf"})
    assert [r["title"] for r in res.json()["items"]] == ["Coach guide"]

    res = staff_client.get("/admin/resources", params={"is_published": False})
    assert [r["title"] for r in res.json()["items"]] == ["Intro video"]

    res = staff_client.get("/admin/resources", params={"q": "GUIDE"})
    assert res.json()["total"] == 2


def test_admin_list_paginates(staff_client, db):
    for n in range(3):
        add_resource(db, title=f"Resource {n}")

    body = staff_client.get(
        "/admin/resources", params={"page": 2, "page_size": 2}
    ).json()

    assert body["total"] == 3
    assert body["page"] == 2
    assert len(body["items"]) == 1


# Get


def test_get_resource(staff_client, db):
    resource = add_resource(db, is_published=False)

    res = staff_client.get(f"/admin/resources/{resource.id}")

    assert res.status_code == 200
    assert res.json()["id"] == str(resource.id)
    assert res.json()["is_published"] is False


def test_get_resource_404(staff_client):
    res = staff_client.get(f"/admin/resources/{MISSING_ID}")
    assert res.status_code == 404


# Update


def test_update_resource_changes_only_sent_fields(staff_client, db):
    resource = add_resource(db, title="Old title", is_published=False)

    res = staff_client.patch(
        f"/admin/resources/{resource.id}", json={"is_published": True}
    )

    assert res.status_code == 200
    assert res.json()["is_published"] is True
    assert res.json()["title"] == "Old title"


def test_update_resource_audiences(staff_client, db):
    resource = add_resource(db, audiences=["athlete"])

    res = staff_client.patch(
        f"/admin/resources/{resource.id}", json={"audiences": ["partner", "donor"]}
    )

    assert res.json()["audiences"] == ["partner", "donor"]


def test_update_resource_can_clear_description(staff_client, db):
    resource = add_resource(db, description="Old")

    res = staff_client.patch(
        f"/admin/resources/{resource.id}", json={"description": None}
    )

    assert res.status_code == 200
    assert res.json()["description"] is None


def test_update_resource_rejects_null_required_field(staff_client, db):
    resource = add_resource(db)

    res = staff_client.patch(f"/admin/resources/{resource.id}", json={"title": None})

    assert res.status_code == 422


def test_update_resource_404(staff_client):
    res = staff_client.patch(f"/admin/resources/{MISSING_ID}", json={"title": "x"})
    assert res.status_code == 404


# Delete


def test_delete_resource(staff_client, db):
    resource = add_resource(db)
    resource_id = resource.id

    res = staff_client.delete(f"/admin/resources/{resource_id}")

    assert res.status_code == 204
    assert res.content == b""
    db.expire_all()
    assert db.get(Resource, resource_id) is None


def test_delete_resource_404(staff_client):
    res = staff_client.delete(f"/admin/resources/{MISSING_ID}")
    assert res.status_code == 404
