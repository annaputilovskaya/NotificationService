"""Проверки env-настроек."""

import pytest
from django.conf import settings


def test_pagination_configured():
    assert settings.REST_FRAMEWORK["PAGE_SIZE"] == 20
    assert (
        settings.REST_FRAMEWORK["DEFAULT_PAGINATION_CLASS"]
        == "rest_framework.pagination.PageNumberPagination"
    )


def test_cors_middleware_enabled():
    assert "corsheaders.middleware.CorsMiddleware" in settings.MIDDLEWARE


def test_sms_test_default_is_false():
    assert settings.SMS_TEST is False


@pytest.mark.django_db
def test_swagger_title(api_client):
    response = api_client.get("/swagger.json/")
    assert response.status_code == 200
    assert "Notification Service API" in response.content.decode()
