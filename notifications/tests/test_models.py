"""Тесты модели Notification."""

import pytest

from notifications.models import Notification


@pytest.mark.django_db
def test_str_without_topic():
    notification = Notification.objects.create(owner=None)
    assert str(notification) == f"Notification #{notification.pk}"


@pytest.mark.django_db
def test_str_with_topic(user):
    notification = Notification.objects.create(topic="Hello", owner=user)
    assert str(notification) == "Hello"
