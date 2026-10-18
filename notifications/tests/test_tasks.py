"""Тесты задачи send_notification: failover и retry."""

from unittest.mock import MagicMock, patch

import pytest
from celery.exceptions import MaxRetriesExceededError, Retry

from notifications.models import Notification
from notifications.tasks import send_notification


@pytest.fixture
def notification(user):
    return Notification.objects.create(topic="t", text="x", owner=user)


def _strategies(email, telegram, sms):
    return {"email": email, "telegram": telegram, "sms": sms}


@patch("notifications.tasks.get_strategies_map")
def test_stops_after_first_success(mock_map, notification, recipient):
    email, telegram, sms = MagicMock(), MagicMock(), MagicMock()
    email.send.return_value = []
    mock_map.return_value = _strategies(email, telegram, sms)
    notification.recipients.add(recipient)

    send_notification(notification.pk, [recipient.pk])

    notification.refresh_from_db()
    assert notification.status == "COMPLETED"
    email.send.assert_called_once()
    telegram.send.assert_not_called()
    sms.send.assert_not_called()


@patch("notifications.tasks.get_strategies_map")
def test_failover_to_next_strategy(mock_map, notification, recipient):
    email, telegram, sms = MagicMock(), MagicMock(), MagicMock()
    email.send.return_value = [recipient.pk]
    telegram.send.return_value = []
    mock_map.return_value = _strategies(email, telegram, sms)
    notification.recipients.add(recipient)

    send_notification(notification.pk, [recipient.pk])

    notification.refresh_from_db()
    assert notification.status == "COMPLETED"
    telegram.send.assert_called_once()
    sms.send.assert_not_called()


@patch("notifications.tasks.get_strategies_map")
def test_retry_only_for_failed_recipients(mock_map, notification, recipient, db):
    from recipients.models import Recipient

    second = Recipient.objects.create(email="second@example.com")
    email, telegram, sms = MagicMock(), MagicMock(), MagicMock()
    email.send.return_value = [second.pk]
    telegram.send.return_value = []
    mock_map.return_value = _strategies(email, telegram, sms)
    notification.recipients.add(recipient, second)

    send_notification(notification.pk, [recipient.pk, second.pk])

    notified_ids = set(
        telegram.send.call_args.kwargs["recipient_list"].values_list("id", flat=True)
    )
    assert notified_ids == {second.pk}


@patch("notifications.tasks.get_strategies_map")
def test_all_failed_raises_retry(mock_map, notification, recipient):
    email, telegram, sms = MagicMock(), MagicMock(), MagicMock()
    email.send.return_value = [recipient.pk]
    telegram.send.return_value = [recipient.pk]
    sms.send.return_value = [recipient.pk]
    mock_map.return_value = _strategies(email, telegram, sms)
    notification.recipients.add(recipient)

    with pytest.raises(Retry):
        send_notification.apply(args=(notification.pk, [recipient.pk]), throw=True)

    notification.refresh_from_db()
    assert notification.status == "IN_PROGRESS"


@patch("notifications.tasks.get_strategies_map")
def test_exhausted_retries_are_reraised(mock_map, notification, recipient, caplog):
    email, telegram, sms = MagicMock(), MagicMock(), MagicMock()
    email.send.return_value = [recipient.pk]
    telegram.send.return_value = [recipient.pk]
    sms.send.return_value = [recipient.pk]
    mock_map.return_value = _strategies(email, telegram, sms)
    notification.recipients.add(recipient)

    with patch.object(
        send_notification, "retry", side_effect=MaxRetriesExceededError()
    ):
        with pytest.raises(MaxRetriesExceededError):
            send_notification(notification.pk, [recipient.pk])

    assert any(
        record.levelname == "ERROR" and "max retries exceeded" in record.message
        for record in caplog.records
    )


def test_missing_notification_is_logged_not_raised(db):
    send_notification(999999, [1])  # не должно поднимать исключение


@patch("notifications.tasks.Notification.objects.get")
def test_transient_db_error_triggers_retry(mock_get, db, caplog):
    from django.db import OperationalError

    mock_get.side_effect = OperationalError("connection lost")

    with pytest.raises(Retry):
        send_notification(999999, [1])

    assert any(
        record.levelname == "ERROR" and "database error" in record.message
        for record in caplog.records
    )
