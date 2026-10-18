"""Smoke-тесты CRUD получателей."""

import pytest


def test_requires_auth(api_client):
    assert api_client.get("/recipients/").status_code == 401


@pytest.mark.django_db
def test_crud_flow(auth_client):
    created = auth_client.post(
        "/recipients/", {"email": "crud@example.com"}, format="json"
    )
    assert created.status_code == 201
    pk = created.json()["id"]

    assert auth_client.get(f"/recipients/{pk}/").status_code == 200

    updated = auth_client.patch(
        f"/recipients/{pk}/", {"first_name": "John"}, format="json"
    )
    assert updated.status_code == 200
    assert updated.json()["first_name"] == "John"

    assert auth_client.delete(f"/recipients/{pk}/").status_code == 204
