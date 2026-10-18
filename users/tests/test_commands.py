"""Тесты команды csu."""

import pytest
from django.core.management import call_command

from users.models import User


@pytest.mark.django_db
def test_skips_when_env_missing(monkeypatch):
    monkeypatch.delenv("DJANGO_SUPERUSER_EMAIL", raising=False)
    monkeypatch.delenv("DJANGO_SUPERUSER_PASSWORD", raising=False)

    call_command("csu")

    assert not User.objects.filter(is_superuser=True).exists()


@pytest.mark.django_db
def test_creates_superuser_from_env(monkeypatch):
    monkeypatch.setenv("DJANGO_SUPERUSER_EMAIL", "boss@example.com")
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", "Str0ng-pass-1")

    call_command("csu")

    user = User.objects.get(email="boss@example.com")
    assert user.is_superuser and user.is_staff
    assert user.check_password("Str0ng-pass-1")
