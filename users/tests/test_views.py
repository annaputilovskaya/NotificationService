"""Smoke-тесты аутентификации."""

import pytest


@pytest.mark.django_db
def test_register_login_refresh(api_client):
    register = api_client.post(
        "/users/register/",
        {"email": "smoke@example.com", "password": "Str0ng-pass-1"},
        format="json",
    )
    assert register.status_code == 201

    login = api_client.post(
        "/users/login/",
        {"email": "smoke@example.com", "password": "Str0ng-pass-1"},
        format="json",
    )
    assert login.status_code == 200
    tokens = login.json()
    assert "access" in tokens and "refresh" in tokens

    refresh = api_client.post(
        "/users/token-refresh/", {"refresh": tokens["refresh"]}, format="json"
    )
    assert refresh.status_code == 200
    assert "access" in refresh.json()
