"""Тесты проверки доступности email."""

import socket
from unittest.mock import MagicMock, patch

import pytest

from notifications.utils import check_email_availability


@patch("notifications.utils.dns.resolver.resolve")
@patch("notifications.utils.smtplib.SMTP")
def test_valid_email_returns_none(mock_smtp_cls, mock_resolve):
    mock_resolve.return_value = [MagicMock(exchange=MagicMock())]
    mock_resolve.return_value[0].exchange.to_text.return_value = "mx.example.com"
    server = mock_smtp_cls.return_value
    server.helo.return_value = (250, b"ok")
    server.rcpt.return_value = (250, b"ok")

    result = check_email_availability("user@example.com")

    assert result is None


@patch("notifications.utils.dns.resolver.resolve")
def test_invalid_email_raises(mock_resolve):
    mock_resolve.side_effect = Exception("no dns")

    # noqa: B017 — контракт функции (plan-frozen) — слепой Exception
    with pytest.raises(Exception):  # noqa: B017
        check_email_availability("user@example.com")


@patch("notifications.utils.dns.resolver.resolve")
@patch("notifications.utils.smtplib.SMTP")
def test_helo_rejection_raises(mock_smtp_cls, mock_resolve):
    mock_resolve.return_value = [MagicMock(exchange=MagicMock())]
    mock_resolve.return_value[0].exchange.to_text.return_value = "mx.example.com"
    server = mock_smtp_cls.return_value
    server.helo.return_value = (550, b"rejected")

    # noqa: B017 — контракт функции (plan-frozen) — слепой Exception
    with pytest.raises(Exception):  # noqa: B017
        check_email_availability("user@example.com")


@patch("notifications.utils.dns.resolver.resolve")
def test_does_not_mutate_global_socket_timeout(mock_resolve):
    mock_resolve.side_effect = Exception("no dns")
    default_before = socket.getdefaulttimeout()

    # noqa: B017 — контракт функции (plan-frozen) — слепой Exception
    with pytest.raises(Exception):  # noqa: B017
        check_email_availability("user@example.com", timeout=1)

    assert socket.getdefaulttimeout() == default_before
