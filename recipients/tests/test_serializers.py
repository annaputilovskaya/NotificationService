"""Тесты сериализатора получателя."""

import pytest

from recipients.models import Recipient
from recipients.serializers import RecipientSerializer


@pytest.mark.django_db
def test_email_must_be_unique():
    Recipient.objects.create(email="dup@example.com")

    serializer = RecipientSerializer(data={"email": "dup@example.com"})

    assert not serializer.is_valid()
    assert "email" in serializer.errors
