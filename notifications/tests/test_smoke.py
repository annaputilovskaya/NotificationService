"""Smoke-тесты доступности сервисных страниц."""

import pytest


@pytest.mark.django_db
def test_swagger_reachable(api_client):
    assert api_client.get("/swagger/").status_code == 200
