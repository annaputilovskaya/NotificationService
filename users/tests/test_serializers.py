"""Тесты сериализаторов пользователя."""

import pytest

from users.serializers import UserDetailSerializer, UserSerializer


@pytest.mark.django_db
def test_create_user_hashes_password():
    serializer = UserSerializer(
        data={"email": "new@example.com", "password": "Str0ng-pass-1"}
    )
    assert serializer.is_valid(), serializer.errors

    user = serializer.save()

    assert user.password != "Str0ng-pass-1"
    assert user.check_password("Str0ng-pass-1")


@pytest.mark.django_db
def test_create_user_rejects_weak_password():
    serializer = UserSerializer(data={"email": "weak@example.com", "password": "123"})
    assert not serializer.is_valid()
    assert "password" in serializer.errors


def test_detail_serializer_excludes_password(user):
    data = UserDetailSerializer(user).data
    assert "password" not in data
