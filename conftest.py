"""Общие фикстуры pytest."""

import pytest
from rest_framework.test import APIClient

from recipients.models import Recipient
from users.models import User


@pytest.fixture
def api_client() -> APIClient:
    """Неаутентифицированный APIClient."""
    return APIClient()


@pytest.fixture
def user(db) -> User:
    """Обычный пользователь-владелец уведомлений."""
    return User.objects.create_user(
        email="user@example.com", password="Str0ng-pass-1"
    )


@pytest.fixture
def other_user(db) -> User:
    """Второй пользователь (для проверки изоляции данных)."""
    return User.objects.create_user(
        email="other@example.com", password="Str0ng-pass-1"
    )


@pytest.fixture
def auth_client(api_client: APIClient, user: User) -> APIClient:
    """APIClient, аутентифицированный как user."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def recipient(db) -> Recipient:
    """Получатель с email."""
    return Recipient.objects.create(email="recipient@example.com")
