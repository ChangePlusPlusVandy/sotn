"""Tests for the Location API."""


def test_locations_is_public(client):
    res = client.get("/locations")
    assert res.status_code == 200


def test_locations_lists_regions_and_counties(client):
    body = client.get("/locations").json()

    assert body["regions"] == ["east", "middle", "west"]
    assert len(body["counties"]) == 95
    assert "Knox" in body["counties"]
