"""Тесты стратегий отправки (внешние сервисы замоканы)."""

from unittest.mock import patch

import pytest

from notifications.strategies import (
    EmailNotification,
    SMSNotification,
    TelegramNotification,
    get_strategies_map,
)
from recipients.models import Recipient


@pytest.fixture
def recipients(db):
    return [
        Recipient.objects.create(
            email="a@example.com", tg_chat_id="111", phone="+79000000001"
        ),
        Recipient.objects.create(
            email="b@example.com", tg_chat_id="222", phone="+79000000002"
        ),
    ]


class TestEmailNotification:
    @patch("notifications.strategies.check_email_availability")
    @patch("notifications.strategies.EmailMessage")
    def test_success_returns_empty_list(self, mock_message, mock_check, recipients):
        mock_message.return_value.send.return_value = 1

        result = EmailNotification().send("s", "m", recipients)

        assert result == []
        assert mock_check.call_count == len(recipients)

    @patch("notifications.strategies.check_email_availability")
    @patch("notifications.strategies.EmailMessage")
    def test_send_returning_zero_counts_as_failure(
        self, mock_message, mock_check, recipients
    ):
        mock_message.return_value.send.return_value = 0

        result = EmailNotification().send("s", "m", recipients)

        assert result == [r.pk for r in recipients]

    @patch(
        "notifications.strategies.check_email_availability",
        side_effect=Exception("bad"),
    )
    def test_exception_counts_as_failure(self, mock_check, recipients):
        result = EmailNotification().send("s", "m", recipients)

        assert result == [r.pk for r in recipients]


class TestTelegramNotification:
    @patch("notifications.strategies.requests.post")
    def test_success(self, mock_post, recipients):
        mock_post.return_value.json.return_value = {"ok": True}

        result = TelegramNotification().send("s", "m", recipients)

        assert result == []

    @patch("notifications.strategies.requests.post")
    def test_api_ok_false_is_failure(self, mock_post, recipients):
        mock_post.return_value.json.return_value = {"ok": False, "description": "e"}

        result = TelegramNotification().send("s", "m", recipients)

        assert result == [r.pk for r in recipients]

    def test_missing_chat_id_is_failure(self, db):
        recipient = Recipient.objects.create(email="nochat@example.com")

        result = TelegramNotification().send("s", "m", [recipient])

        assert result == [recipient.pk]


class TestSMSNotification:
    @patch("notifications.strategies.requests.post")
    def test_success(self, mock_post, recipients):
        mock_post.return_value.json.return_value = {"status": "OK"}

        result = SMSNotification().send("s", "m", recipients)

        assert result == []

    @patch("notifications.strategies.requests.post")
    def test_failure(self, mock_post, recipients):
        mock_post.return_value.json.return_value = {
            "status": "ERROR",
            "sms": {"status_text": "bad"},
        }

        result = SMSNotification().send("s", "m", recipients)

        assert result == [r.pk for r in recipients]

    def test_missing_phone_is_failure(self, db):
        recipient = Recipient.objects.create(email="nophone@example.com")

        result = SMSNotification().send("s", "m", [recipient])

        assert result == [recipient.pk]


def test_strategies_map_has_three_channels():
    strategies = get_strategies_map()
    assert set(strategies) == {"email", "telegram", "sms"}
